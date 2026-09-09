"""Independent R7 measurements on unchanged sandbox code; no seed repair."""
from pathlib import Path
import collections
import hashlib
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
SESSION = Path(__file__).resolve().parent
SANDBOX = ROOT / '.work/c062_diagnostics/SU2ZX'
LEGACY = SANDBOX / 'runs/section8_v0.5.0_20260907T0628Z'
sys.path.insert(0, str(LEGACY / 'src'))
import numpy as np
from qiskit import transpile, qpy
from su2qc.twin import twin
from su2qc.compile import route
from su2qc.circuits import synth_l12
from su2qc.circuits.strang_l12 import full_circuit
from su2qc.encodings import l12

result = {'status': 'running', 'source': 'EMULATED', 'code': 'unchanged HEAD sandbox copy',
          'paths': {}, 'prefixed_production': {}, 'not_run': ['post-fix tests; BUILD blocked', 'R8 post-fix acceptance'],
          'raw_direct_seeds': [500, 501], 'shots_shift': 1024}


def save():
    (SESSION / 'seed-diagnosis.json').write_text(json.dumps(result, indent=2) + '\n')


def moments(counts, bootstrap_seed):
    mean, two, y = twin.bootstrap(counts, n_boot=1000, seed=bootstrap_seed)
    pooled = collections.Counter()
    kept_n = []
    for c in counts:
        kept, _ = twin.postselect(c)
        pooled.update(kept)
        kept_n.append(sum(kept.values()))
    total = sum(pooled.values())
    values = {bits: twin.observables({bits: 1}) for bits in pooled}
    rows = {}
    for key in mean:
        mu = sum(n * values[bits][key] for bits, n in pooled.items()) / total
        # Centered sum avoids cancellation spuriously making structural zero nonzero.
        var = sum(n * (values[bits][key] - mu)**2 for bits, n in pooled.items()) / total
        unique = set(v[key] for v in values.values())
        if len(unique) == 1:
            var = 0.0
        expected = 0.894 * np.sqrt(var / (5 * np.mean(kept_n)))
        rows[key] = {'mean': mean[key], 'two_sigma': two[key], 'pooled_variance': var,
                     'expected_bootstrap_se': float(expected),
                     'ratio': float(two[key] / (2 * expected)) if expected else None,
                     'structural_zero_in_pooled_sample': var == 0.0}
    return {'distinct': len({tuple(sorted(c.items())) for c in counts}),
            'key_counts': [len(c) for c in counts], 'counts': counts,
            'kept_per_repeat': kept_n, 'yield_mean': y, 'observables': rows}


backend = route.fake_heron()
layout = json.loads((LEGACY / 'compile/layout.json').read_text())['initial_physical']
# Exact run_g4 production route (structured synthesis, FakeTorino, level 3, seed 7).
isa0, _ = route.route(synth_l12.synth_full_circuit(0), backend, opt=3, seed=7, initial_layout=layout)
meas0 = twin.add_measurements(isa0)
result['r0_resources'] = route.routed_resources(isa0)
with (SESSION / 'diagnostic-r0-isa.qpy').open('wb') as f:
    qpy.dump(meas0, f)
for name, compact in [('production', False), ('compact', True)]:
    sim = twin.twin_backend(seed=101, backend=backend, compact=compact)
    # The compact simulator cannot accept 133 physical wires. Use the existing
    # compact-test construction, not a remapped physical noise model.
    if compact:
        compact_isa = transpile(full_circuit(0), sim, optimization_level=0,
                                seed_transpiler=101)
        measured = twin.add_measurements(compact_isa)
    else:
        measured = meas0
    t = transpile(measured, sim, optimization_level=0, seed_transpiler=500)
    raw = []
    for seed in (500, 501, 500):
        start = time.monotonic()
        res = sim.run(t, shots=1024, seed_simulator=seed, memory=True).result()
        assert res.success
        raw.append({'seed': seed, 'memory': res.get_memory(), 'counts': dict(res.get_counts()),
                    'metadata': res.results[0].metadata, 'seconds': time.monotonic()-start})
    a,b,c = raw
    result['paths'][name] = {'raw': raw, 'shift_equal': a['memory'][1:] == b['memory'][:-1],
        'equal_seed_counts_equal': a['counts'] == c['counts'],
        'equal_multisets': collections.Counter(a['memory']) == collections.Counter(b['memory']),
        'same_index_matches': sum(x == y for x,y in zip(a['memory'], b['memory'])),
        'shift_matches': sum(x == y for x,y in zip(a['memory'][1:], b['memory'][:-1]))}
    save()
    separated = [500 + k * 1000000 for k in range(5)]
    counts = [dict(sim.run(t, shots=1024, seed_simulator=seed).result().get_counts()) for seed in separated]
    result['paths'][name]['well_separated'] = {'seeds': separated, **moments(counts, 77)}
    save()
    print(name, 'raw shift', result['paths'][name]['shift_equal'], 'separated distinct', result['paths'][name]['well_separated']['distinct'], flush=True)

sim = twin.twin_backend(seed=101, backend=backend)
for r, shots in ((0,4000), (1,1024)):
    if r:
        isa, _ = route.route(synth_l12.synth_full_circuit(r), backend, opt=3, seed=7, initial_layout=layout)
        meas = twin.add_measurements(isa)
    else:
        meas = meas0
    start = time.monotonic()
    print('pre-fix production r', r, 'starting', flush=True)
    counts = twin.run_counts([meas] * 5, shots, 500 + 10*r, sim)
    result['prefixed_production'][str(r)] = {'shots': shots, 'seeds': [500+10*r+k for k in range(5)],
                                          'seconds': time.monotonic()-start, **moments(counts, r)}
    save()
    print('pre-fix production r',r,'distinct',result['prefixed_production'][str(r)]['distinct'],flush=True)
# Diagnostic of impossible invalid-key residual requirement, without changing code.
physical = l12.physical_codes()
invalid = next(k for k in range(4096) if l12.decode(k) is None)
q = {physical[0]: 1.0, invalid: 0.25}
result['invalid_key_closure'] = {'invalid_code': invalid, 'decode_rejected': l12.decode(invalid) is None,
                              'residual_with_invalid_weight': twin.channel_closure_residual(q),
                              'residual_without_invalid_weight': twin.channel_closure_residual({physical[0]:1.0}),
                              'note': 'Both helper sides ignore invalid codes; no physics repair applied.'}
result['status'] = 'independent pre-fix measurements complete; not R8 acceptance or C0 sign-off'
save()
