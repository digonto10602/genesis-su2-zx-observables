"""Finite read-only checks of review hypotheses; not physics sign-off."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
SESSION = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.work/c062_diagnostics/SU2ZX/runs/section8_v0.5.0_20260907T0628Z/src'))
from su2qc.encodings import l12
from su2qc.twin import twin
from su2qc import conventions

codes = l12.physical_codes()
non_half_meson = []
closure_bad = []
survival = []
for code in codes:
    js, ns, _ = l12.decode(code)
    q = tuple(ns[i] - conventions.N_VAC[i] for i in range(4))
    if all(abs(x) == 1 for x in q) and sum(ns) != 4:
        non_half_meson.append(code)
    if ns == (1,1,0,2):
        survival.append({'code':code,'links':js,'occupations':ns})
    residual = twin.channel_closure_residual({code:1.0})
    if abs(residual) > 1e-10:
        closure_bad.append({'code':code,'residual':residual})
invalid = next(i for i in range(4096) if l12.decode(i) is None)
try:
    empty = {'returned': twin.physical_yield({}, set())}
except Exception as e:
    empty = {'exception':type(e).__name__,'message':str(e)}
result = {'physical_code_count':len(codes),'vacuum_occupations':conventions.N_VAC,
          'non_N4_meson_codes':non_half_meson,'singleton_closure_failures':closure_bad,
          'survival_occupation_codes':survival,
          'invalid_input':{'code':invalid,'decode_is_none':l12.decode(invalid) is None,
                           'residual':twin.channel_closure_residual({codes[0]:1.,invalid:0.25})},
          'empty_physical_yield':empty,'empty_postselect':twin.postselect({}),
          'interpretation':'Finite code inspection only; no channel-definition amendment or gate sign-off.'}
(SESSION/'oracle-diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
