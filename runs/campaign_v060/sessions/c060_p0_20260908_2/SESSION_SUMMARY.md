# Session summary — c060_p0_20260908_2

C0 remains PARTIAL. The fresh final sandbox regression passed 45/45; G1 passed 17/17, G2 passed 20/20, and G3 passed its L12 core with S8/C7 omitted under D4. C1 passed: preregistration, claim table, frozen thresholds, R1/R3/R4/R5/R6 rulings, and hashes are present. C2 did not start.

Validation: V1 R1 passed substantively after restoring signed HEAD artifacts; primary values are preserved and the fitted slopes satisfy the propagated-bound rule and G3 band. The independent j_max=1 generating-function test passed, including route sector splits 3,36,74,36,3 and projector orthonormality. V11 focused tests passed after adding signed quasi-weight and closed-form assertions, but Fable correctly refused to sign V11 as PASS because the final evidence packet lacks a separate independent classifier/closed-form audit and the ODR row is deferred to Phase 5. V10 failed: the compact calibration-derived twin produced only 3 distinct dictionaries at r=0 where 5 are required; the r=1 branch did not execute. The seed path needs a production-path fix and a fresh pre-fix/negative-control run.

Rulings applied: R1 through R6. R2 preserved the four divergent v0.5.0 artifacts and restored signed versions; explicit Phase-4, reference, and dry-run records were committed. R4's compact diagnostic was not accepted as production-path evidence. No threshold was loosened. No QPU job has ever been submitted; hardware mode remains disabled.

Commits: 4276d72 campaign: commit phase-4 artifacts from v0.5.0; 6a49f68 campaign: commit phase-4 artifacts from v0.5.0 (remaining explicit paths); c7172eb repo: status report, graphify refresh, campaign references (2026-09-07); b993ca6 ops: hermes run records 2026-09-07. Current C0/C1 campaign changes remain to be committed at the gate after V10 repair.

Evidence: this session's `final-regression.xml`, `final-G1.log`, `final-G2.log`, `final-G3.log`, `gate_C0.xml`, `gate_C0.log`, `twin_variance.json`, `predictions_C0.md`, `signoff_C0.md`, `review_C0_retry.md`, `tier2_ledger.md`, and `evidence-manifest.json` (the latter is superseded by the final snapshot manifest created after this summary).

Next action verbatim: Resolve the V10 seed-plumbing failure, rerun the full C0 command with a fresh evidence manifest and review/sign-off; do not start C2.
