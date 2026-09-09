# Gate map — gate → row → test file → evidence file → status

Documentation only. Status unchanged by this document.

## Campaign gates

| Gate | Row | Test file | Evidence file | Status |
|---|---|---|---|---|
| C0 | V1 regression (byte-identical Trotter artifact + slopes) | `tests/gate_C0/test_v1_regression.py` | `evidence/trotter_scaling.json`, session logs | PARTIAL (gate overall) |
| C0 | V10 twin variance (distinct dictionaries, bootstrap SE) | `tests/gate_C0/test_twin_variance.py` | `evidence/twin_variance.json`, `evidence/seed-diagnosis.json`, `evidence/equal-seed-control.json` | failing — seed overlap |
| C0 | V11 estimator (synthetic channels, closure, subtraction, yield) | `tests/gate_C0/test_estimator.py` | session logs | PARTIAL |
| C0 | jmax=1 kernel dim 152 + projector orthonormality | `tests/gate_C0/test_jmax1_counts.py` | session logs | documented |
| C1 | frozen thresholds/hashes, claim table | (state files) | `evidence/GATE_THRESHOLDS.yaml`, `evidence/PREREGISTRATION.md`, `evidence/CAMPAIGN_STATE.json` | unamended |
| C2 | route agreement / observable time series / counts | (not built) | — | NOT STARTED |

## Section-8 gates

| Gate | Criterion summary | Script |
|---|---|---|
| G1 | (conventions/labels) | `gates/gate_G1.py` |
| G2 | (dynamics/limits) | `gates/gate_G2.py` |
| G3 | L12 suite, block unitaries, Strang, Trotter leakage | `gates/gate_G3.py` |

## Campaign status triple

C0 PARTIAL · C1 unamended · C2 NOT STARTED. No gate PASS is asserted by this map;
prior-session artifacts are cited as historical evidence, not as this session's own
gate results.