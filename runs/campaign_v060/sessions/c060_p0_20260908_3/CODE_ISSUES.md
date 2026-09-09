# Code issues and proposed solutions

Status: diagnostic findings, not a repair acceptance or physics sign-off.
The production package and existing campaign tests are unchanged. The new, executed diagnostic scripts live in this session directory. Fable planning/escalation remains blocked, so the changes below are proposals unless explicitly marked IMPLEMENTED.

## 1. The old V10 test can overwrite historical evidence — confirmed by source

Where: runs/campaign_v060/tests/gate_C0/test_twin_variance.py:27-29.
Problem: every execution writes into c060_p0_20260908_2, regardless of the current session. An assertion at r=0 also stops collection before r=1.
Proposed repair: require an explicit session output directory; collect both points before evaluating the combined acceptance; save partial failures with a status and command record. Never default to an earlier session.
Required verification: run from two working directories, force a failure at r=0, and verify historical files remain byte-identical and both requested points have either results or explicit failure records.
IMPLEMENTED containment: diagnose_unchanged.py runs the existing test only in an isolated copy under .work/. It cannot write the real historical result. The source manifest is rechecked before packaging. This is containment, not a repair to the campaign test.

## 2. The V10 test checks the wrong path and weak conditions — confirmed by source

Where: test_twin_variance.py:10-35.
Problem: compact=True bypasses AerSimulator.from_backend; any positive uncertainty is accepted; the negative control repeats one Python object rather than running five jobs; seeds, uncertainty ratios and zero-variance cases are not saved.
Proposed repair: run the structured, routed production circuits; save actual runtime seeds, counts and per-observable uncertainty ratios; apply R8 unchanged to every nonzero pooled variance; execute a real equal-seed control. Do not find new seeds until a statistical test passes.
IMPLEMENTED diagnosis: diagnose_seeds.py runs both raw backend paths and the pre-fix production repeats. diagnose_control.py runs five actual equal-seed production calls at r=0 and checks rejection by the distinctness condition. These are not post-fix R8 results.

## 3. run_counts uses adjacent seeds and changes caller-owned options

Where: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py:54-63.
Measured: the raw production shift test matched every overlapping shot; separated seeds produced distinct dictionaries. The equal-seed control also measured the simulator option changing from 101 to 500 after run_counts.
Proposed repair, CONDITIONAL on mandatory approval: the R7 SeedSequence.spawn derivation inside run_counts, 31-bit effective seeds recorded in a sidecar, and removal of set_options. Keep run_counts' existing signature and legacy observables unchanged.
Required verification: full pre/post/control runs at both r values; exact-seed reproducibility; simulator options unchanged; effective-seed record matches calls; variance ratios judged once against R8. A raw direct 500/501 Aer shift test should remain true after a wrapper-only fix; see PHYSICS_ISSUES.md.
NOT IMPLEMENTED in production: no mandatory Fable plan/escalation is available.

## 4. V11 tests are incomplete and the invalid-key requirement is ambiguous

Where: test_estimator.py:7-36; twin.py:105-143.
Problem: three labels instead of the required coverage, one genuinely negative entry rather than two, no independent decoded-label oracle for all four channels, inequality instead of the two-configuration equality, and yield tested through a caller-selected key set instead of postselect.
Proposed repair: four independent-oracle tests with literal expected values, signed channel totals, matched subtraction and a physical/unphysical counts mix. Keep ODR explicitly deferred to V12.
Measured: exhaustive inspection of all 82 physical codes found exactly two codes for occupation (1,1,0,2), 2058 and 3793, and zero singleton closure failures. A rejected code with weight 0.25 leaves the current closure residual at zero because both sides exclude it. Changing that meaning needs a ruling, not a fabricated failing example.

## 5. V1 reads old evidence instead of deriving current results

Where: test_v1_regression.py:14-27.
Problem: it checks that a committed JSON still equals HEAD and reads a prior session's conditioning bound. This does not demonstrate that current code regenerated the numbers. An empty conditioning list also bypasses all slope checks.
Proposed repair: compute the three fitted slopes and conditioning bounds from this session's freshly generated G3 arrays and a pinned reference commit; require exactly the three expected observables; compare primary arrays and slope bands; write the current-session JSON. Keep the reference root explicit for Git operations.
IMPLEMENTED diagnosis: fresh legacy tests and G1-G3 execute in the sandbox, with command/exit records and exports in this session. Existing V1 gate code is NOT repaired or re-signed.

## 6. Empty-count handling is inconsistent

Where: twin.py:152-155 versus postselect at :66-69.
Measured: physical_yield({}, set()) raises ZeroDivisionError; postselect({}) returns ({}, 0.0).
Proposed repair: define one empty-input contract, prefer the actual postselect path required by R9, and test it. Do not silently delete a public helper without checking callers. Production change deferred with the rest of BUILD.

## Diagnostic harness repair actually made and exercised

Attempt 1 gave the compact simulator a 133-wire physical circuit and raised CircuitTooWideForTarget (maximum 29). Preserved under attempt1/. Attempt 2 uses the existing compact-test construction on its logical wires, while keeping the production path routed. Both backend shift probes completed after this correction. The compact results are secondary and never substituted for production evidence.

## Review cautions

The raw Opus report is included for transparency, not treated as an authoritative list of confirmed bugs. Read REVIEW_CHECKS.md: several suggested defects were unsupported, contradicted by finite enumeration, or already resolved by the governing prompt. No Hamiltonian, Gauss-law, channel-definition or Trotter change was made from reviewer prose alone.
