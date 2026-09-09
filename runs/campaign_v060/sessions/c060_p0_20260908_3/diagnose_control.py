"""Run the equal-runtime-seed negative control on unchanged production code."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
SESSION = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.work/c062_diagnostics/SU2ZX/runs/section8_v0.5.0_20260907T0628Z/src'))
from qiskit import qpy
from su2qc.twin import twin

with (SESSION / 'diagnostic-r0-isa.qpy').open('rb') as f:
    measured = qpy.load(f)[0]
sim = twin.twin_backend(seed=101)
before = sim.options.seed_simulator
# Five real production calls, each with runtime seed=500, not five aliases of one dict.
counts = [twin.run_counts([measured], 4000, 500, sim)[0] for _ in range(5)]
distinct = len({tuple(sorted(c.items())) for c in counts})
try:
    assert distinct == 5, f'five distinct required; observed {distinct}'
    rejected = False
except AssertionError:
    rejected = True
result = {'source':'EMULATED','r':0,'shots':4000,'runtime_seeds':[500]*5,
          'counts':counts,'distinct':distinct,'distinctness_check_rejected':rejected,
          'simulator_seed_option_before':before,'simulator_seed_option_after':sim.options.seed_simulator,
          'scope':'independent pre-fix r0 control; not the post-fix R8 r0/r1 controls'}
(SESSION/'equal-seed-control.json').write_text(json.dumps(result,indent=2)+'\n')
assert distinct == 1 and rejected
print('Five real equal-seed calls: distinct=',distinct,'rejected=',rejected)
print('Shared simulator option before/after:',before,sim.options.seed_simulator)
