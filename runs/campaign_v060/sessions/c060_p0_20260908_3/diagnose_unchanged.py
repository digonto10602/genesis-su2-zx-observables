"""Read-only-on-source diagnostic bench; not a repaired C0 gate."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
SESSION = Path(__file__).resolve().parent
SANDBOX = ROOT / '.work/c062_diagnostics/SU2ZX'
LEGACY = Path('runs/section8_v0.5.0_20260907T0628Z')
PY = ROOT / '.mamba/envs/su2zx/bin/python'


def save(name, data):
    (SESSION / name).write_text(json.dumps(data, indent=2) + '\n')


def setup():
    assert ROOT.name == 'SU2ZX'
    assert not SANDBOX.exists(), 'Use a fresh sandbox; do not overwrite evidence'
    SANDBOX.mkdir(parents=True)
    for rel in (LEGACY, Path('runs/campaign_v060/tests')):
        shutil.copytree(ROOT / rel, SANDBOX / rel,
                        ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache'))
    old = Path('runs/campaign_v060/sessions/c060_p0_20260907/slope-conditioning.json')
    (SANDBOX / old).parent.mkdir(parents=True)
    shutil.copy2(ROOT / old, SANDBOX / old)
    (SANDBOX / 'runs/campaign_v060/sessions/c060_p0_20260908_2').mkdir(parents=True)
    (SANDBOX / '.mamba').symlink_to(ROOT / '.mamba', target_is_directory=True)
    for sub in ('tmp', 'cache', 'mpl'):
        (SANDBOX / sub).mkdir()
    save('diagnostic-source-manifest.json', {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for base in (ROOT / LEGACY, ROOT / 'runs/campaign_v060/tests')
        for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts
    })
    print('Fresh sandbox:', SANDBOX, flush=True)


def run_tests():
    env = dict(os.environ, PYTHONPATH=str(SANDBOX / LEGACY / 'src'),
               TMPDIR=str(SANDBOX / 'tmp'), XDG_CACHE_HOME=str(SANDBOX / 'cache'),
               MPLCONFIGDIR=str(SANDBOX / 'mpl'), OPENBLAS_NUM_THREADS='1',
               OMP_NUM_THREADS='2', PYTHONDONTWRITEBYTECODE='1')
    commands = [('baseline-regression', [str(PY), '-m', 'pytest',
        *['tests/' + n for n in ('test_route_spinnet.py', 'test_route_gausskernel.py',
                                'test_dynamics.py', 'test_l12.py')],
        '-q', '-p', 'no:cacheprovider', '--junitxml=' + str(SESSION / 'diagnostic-regression.xml')], SANDBOX / LEGACY)]
    commands += [(f'baseline-G{i}', [str(PY), f'gates/gate_G{i}.py'], SANDBOX / LEGACY) for i in (1, 2, 3)]
    # This runs unchanged tests, including their known hardcoded write, ONLY in the sandbox.
    commands += [('baseline-C0', [str(PY), '-m', 'pytest', 'runs/campaign_v060/tests/gate_C0',
        '-q', '-p', 'no:cacheprovider', '--junitxml=' + str(SESSION / 'diagnostic-C0.xml')], SANDBOX)]
    records = []
    for name, cmd, cwd in commands:
        t = time.monotonic()
        with (SESSION / (name + '.log')).open('w') as log:
            try:
                rc = subprocess.run(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT,
                                    timeout=900).returncode
            except subprocess.TimeoutExpired:
                rc = 124
        records.append({'name': name, 'command': cmd, 'cwd': str(cwd), 'exit_code': rc,
                        'seconds': time.monotonic()-t, 'log': name + '.log'})
        save('diagnostic-execution.json', records)
        print(name, 'exit', rc, flush=True)
        if rc and name != 'baseline-C0':
            print('Regression failed; dependent gate diagnostics stopped.', flush=True)
            break
    completed = {row['name'] for row in records if row['exit_code'] == 0}
    generated = [f'gates/GATE_G{i}.json' for i in (1, 2, 3)
                 if f'baseline-G{i}' in completed]
    if 'baseline-G3' in completed:
        generated.append('circuits/trotter_scaling.json')
    for rel in generated:
        p = SANDBOX / LEGACY / rel
        if p.exists():
            shutil.copy2(p, SESSION / ('diagnostic-' + p.name))
    print('Unchanged baseline finished; these are not signed campaign gates.', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'setup':
        setup()
    elif sys.argv[1] == 'baseline':
        run_tests()
