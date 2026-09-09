# Glossary

Documentation only.

## R-numbers (rulings, newest wins)

- R1 V1 propagated slope conditioning (1e-12 primary, 10× slope bound, band [-2.3,-1.7]).
- R2 preserve/restore signed evidence; explicit commits; preserve dirty work.
- R3 ODR closure deferred to Phase 5 / V12.
- R4 conditional twin seed (change only if pre-fix dictionaries identical); negative control required.
- R5 frozen coupling mapping; conventions/window authority supersedes v0.6.0's incorrect printed P-A row.
- R6 supervised session scope.
- R13 repair `tools/function_inventory.py` scope without forking; byte-identical legacy output; emit `docs/SU2QC_FUNCTION_INVENTORY.md`.
- R14 write `docs/SU2QC_LOGIC_AND_TESTS.md` by hand in house format.
- R15 write `docs/SU2QC_CONTRACTS.md`; the five mandatory entries recorded exactly as currently true (with the user-approved meson correction).
- R16 documentation must not change status.
- R17 refresh Graphify with `su2qc` in scope; fix the two recorded warnings.
- R18 query bundle contents/budget/layout (`zip_results/SU2ZX_QUERY_<commit>_<UTC>.zip`).
- R19 bundle self-test (five checks on the extracted archive).

## V-rows (C0)

- V1 — regression: Trotter scaling artifact byte-identical to HEAD + slopes.
- V10 — twin variance: distinct count dictionaries + bootstrap SE.
- V11 — estimator: synthetic channels, closure, matched subtraction, yield.

## C-gates (campaign)

- C0 — legacy suite + jmax=1 counts + V1/V10/V11. PARTIAL.
- C1 — frozen thresholds/hashes + claim table. Unamended.
- C2 — route agreement / observable time series / counts. NOT STARTED.

## D-decisions (documented scope decisions)

- D4 (G3 fallback): drop the failing/absent S8/C7 encodings; record as FAIL criteria, excluded from PASS logic.

## Status vocabulary

`MEASURED` (recorded measurement), `PROVEN` (derived), `PROPOSED` (proposed, not
implemented), `NOT IMPLEMENTED`, `UNENFORCED` (no supplied test constrains the
behaviour), `DEFERRED`, `BLOCKED`. `EMULATED` labels noisy-simulator numbers.
Documentation must never upgrade a status.

## Campaign status triple

C0 PARTIAL · C1 unamended · C2 NOT STARTED.