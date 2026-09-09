# Session summary — c060_p0_20260908_3

PARTIAL / BLOCKED: independent diagnostics reproduced the adjacent-seed overlap and the old C0 failures; no production repair or physics sign-off was accepted. The r=1 production diagnostic timed out at 2,400 seconds without returning its five-repeat batch.

## What actually ran

- Fresh unchanged-code legacy regression: 45/45 passed.
- Fresh deterministic G1, G2 and G3 scripts: exit 0; G3 retains the recorded D4 exclusion of S8/C7. These reruns have no new Claude physics sign-off.
- Unchanged C0 suite: 6 tests, 2 failures, 0 errors. V10 observed 3 distinct dictionaries instead of 5 on its compact path. V1 rejected regenerated JSON because it compares bytes to HEAD.
- Independent raw r=0 shift diagnostic: production TRUE and compact TRUE for all 1,023 overlapping shot outcomes at direct seeds 500/501, 1,024 shots. Same-seed counts reproduced exactly. Well-separated seeds 500,1000500,2000500,3000500,4000500 gave 5 distinct dictionaries on each path.
- Pre-fix production r=0: 5 repeats × 4,000 shots, seeds 500…504, 4 distinct dictionaries. P_surv bootstrap SE = 0.0001217156 versus predicted 0.0017204333, ratio 0.0707471 (well below R8's 0.5 lower bound). Full per-observable table: variance_pre_fix.csv. This is pre-fix evidence, not R8 post-fix acceptance.
- Real r=0 equal-seed control: five production calls, seed 500 each, one dictionary; distinctness condition rejected it. Shared simulator seed option changed from 101 to 500.
- r=1 pre-fix production at 1,024 shots: INCOMPLETE after timeout. No count/variance result is claimed. No post-fix runs or r=1 negative control were performed.
- Finite basis probe: 82 physical codes; occupations (1,1,0,2) occur only at 2058/3793; no physical singleton closure failures. Rejected code 1 with weight 0.25 leaves closure residual zero. Empty physical_yield raises ZeroDivisionError; postselect({}) returns ({},0).
- Fresh G3 slope probe: all three primary error arrays satisfy 1e-12 and all three fitted slopes satisfy their freshly computed 10× bounds and G3 bands. This does not repair the V1 gate test or establish final repaired-snapshot V1.

## Implemented versus proposed

Implemented and exercised: isolated diagnostic sandbox, executable baseline/seed/control/oracle probes, compact-harness repair after a preserved failed attempt, result aggregation, CSV/plots and Graphify AST refresh. Verified all 200 original legacy/campaign-test files are unchanged.

Proposed but NOT implemented: production SeedSequence repair, new independent-oracle V11 tests, fresh-evidence V1 wrapper and C1 hash amendment. Mandatory Fable planning/escalation remains blocked under the configured budget policy. Opus code review completed; its unsupported findings are qualified in REVIEW_CHECKS.md. No review prose was used as sole justification for physics changes.

## Clear problem/solution reports

PHYSICS_ISSUES.md — seed-overlap evidence and unresolved acceptance/closure decisions.
CODE_ISSUES.md — exact defects, minimal proposed fixes and required tests.
EXECUTION_ISSUES.md — budget interpretation, timeout, historical evidence protection, hashes and resume order.
REVIEW_CHECKS.md — raw-review claims checked against actual code/data.
DIAGNOSTIC_RESULTS.json and process-results.json — machine-readable results and process exits.

C0 remains PARTIAL; C1 unchanged/not amended; C2 NOT STARTED. None of the prior sign-off blockers is claimed closed by a signed final snapshot. No thresholds changed, no commits/pushes, no hardware job submitted. Original campaign state/ledger and all historical numeric outputs are preserved. Preflight-only reports are retained as PREFLIGHT_SUMMARY.md and PREFLIGHT_PHYSICS_STATUS.md.

Next action: Obtain mandatory Fable planning/escalation, resolve the raw-versus-effective-seed shift and invalid-key/hash contracts, obtain the prescribed mechanism ruling, then implement and re-gate on a fresh snapshot. Repeat r=1 with per-repeat checkpointing and an explicitly recorded execution budget; never substitute compact data for it.

Final archive: zip_results/SU2ZX_v062_c060_p0_20260908_3_diagnostics.zip. Start with START_HERE.txt. Archive checksum receipt is separate from scientific gate acceptance.
