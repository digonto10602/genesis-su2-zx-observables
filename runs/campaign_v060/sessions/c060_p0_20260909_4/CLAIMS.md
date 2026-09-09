# Claims

One row per substantive claim, its status, and its evidence path. Statuses:
`MEASURED / PROVEN / PROPOSED / UNVERIFIED / VOID`. Documentation only; no status
is upgraded by this table.

| Claim | Status | Evidence |
|---|---|---|
| v0.5.0 twin σ is a valid independent-repeat uncertainty | **VOID** | `evidence/seed-diagnosis.json` (1023 of 1024 shots overlap after one-shot shift, both paths), `equal-seed-control.json` |
| `run_counts` repeats are independent draws | **VOID** (violated on measured backend/path) | `evidence/seed-diagnosis.json`, `evidence/equal-seed-control.json` |
| `sim.set_options` mutates caller-owned state | **MEASURED** | `evidence/equal-seed-control.json` (101 → 500) |
| Meson channel admits only `N=4` (Σq=0) states | **PROVEN** (structural) + finite 82-code oracle | `src/runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py` (lines 51, 53, 57); `evidence/oracle-diagnostics.json` (`non_N4_meson_codes: []`) |
| Survival selector is rank-1 | **VOID** | `evidence/oracle-diagnostics.json` (two codewords 2058 and 3793, one occupation pattern) |
| Closure identity holds on the present basis | **MEASURED** (82-code finite oracle) | `evidence/oracle-diagnostics.json` (`singleton_closure_failures: []`) |
| `channel_closure_residual` detects invalid codes (R9) | **VOID / UNSATISFIABLE AS WRITTEN** | `evidence/oracle-diagnostics.json` (`invalid_input` residual 0.0) |
| `physical_yield` empty input is defined | **VOID** | `evidence/oracle-diagnostics.json` (`empty_physical_yield` ZeroDivisionError) |
| A production seed repair exists | **PROPOSED** (NOT IMPLEMENTED) | `docs/SU2QC_CONTRACTS.md` |
| Legacy suite (45) passes on current snapshot | **MEASURED** (historical) | `evidence/DIAGNOSTIC_RESULTS.json` |
| C0 has passed | **VOID** | C0 is PARTIAL (`INDEX.md`, `evidence/CAMPAIGN_STATE.json`) |
| No hardware job has ever been submitted | **MEASURED** | `evidence/PREREGISTRATION.md`, repo conventions |
| Bundle self-test passes all five R19 checks | **MEASURED** (this build) | `SELFTEST.json`, `MANIFEST.json` |

Every "instantiated in this bundle" path resolves inside the archive (verified by
`SELFTEST.json` check 1).