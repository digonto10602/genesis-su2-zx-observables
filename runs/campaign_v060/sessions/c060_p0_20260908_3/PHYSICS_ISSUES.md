# Physics and statistical issues requiring a ruling

This is an operational issues report, NOT a final physics sign-off. No Hamiltonian, Gauss-law convention, observable definition or acceptance threshold was changed. Exact measurements are in seed-diagnosis.json, oracle-diagnostics.json and variance_pre_fix.csv. All noisy results are EMULATED, never hardware.

## P1. Adjacent-seed shot overlap: measured, but repair not accepted

On the production AerSimulator.from_backend path, at r=0 with 1,024 shots, memories from seed 500 shifted by one position equal memories from seed 501 over all 1,023 overlapping entries. The compact secondary path also returns true. Repeating the same seed reproduces the same counts; five seeds separated by 1,000,000 produce five distinct dictionaries.

These measurements directly demonstrate the overlap symptom anticipated by R7 for these circuits and backend settings. They are not a universal proof of Aer's implementation for every simulation method, circuit, noise model or version.

Proposed solution: derive effective per-repeat seeds inside run_counts using the prescribed SeedSequence.spawn construction, record the seeds and pass them only as run-time options. Keep the prescribed pre/post/control evidence and variance thresholds. No seed repair was implemented because mandatory Fable planning/escalation is unavailable.

Trust consequence: do not interpret the old adjacent-seed bootstrap uncertainties as independent-repeat error bars. No new hardware or scientific endpoint claim can be based on them. The exact historical diagnosis wording and scope of an erratum still require the mandated review/sign-off; the original results have not been overwritten.

## P2. The requested post-fix raw shift test cannot change under a wrapper-only fix

R7 directly calls sim.run with seeds 500 and 501, but proposes changing run_counts. Those direct calls never execute run_counts. A corrected wrapper therefore cannot make that raw test false.

Proposed clarification: retain the raw 500/501 test as the mechanism demonstration; separately require no shifted equality for the actual effective seeds emitted by the repaired wrapper. Record both truth values and distinguish them explicitly. Do not replace the raw test with a differently seeded test while calling it the same test. This is a specification clarification awaiting approval, not a passed row.

## P3. Invalid-weight closure is not defined by the current requirement

The current helper skips any code rejected by l12.decode on both sides. A rejected code with nonzero weight therefore contributes nothing and cannot create a nonzero residual. The read-only probe confirms a zero residual with invalid code 1 carrying weight 0.25.

Proposed clarification: keep physical-sector closure as its own identity and expose invalid weight separately, or explicitly define a strict rejection contract. R9 currently asks for a nonzero closure residual; an exception or separate invalid-weight measure does not satisfy that wording without a ruling. Do not silently redefine physical channels or make both expected and measured sides share the same classifier just to pass.

## P4. The two-configuration identity has concrete finite-basis evidence

All 82 current physical codes were enumerated. Exactly codes 2058 and 3793 have occupations (1,1,0,2). No singleton physical-code closure failure was found. These are code-level diagnostics, not a replacement for the independent Gauss-law derivation/docstring and signed multi-codeword oracle tests required by R9.

The Opus review's proposed N-not-4 meson counterexample is absent from this finite basis; see REVIEW_CHECKS.md. Do not change channel definitions to fix a nonexistent counterexample.

## P5. A statistical acceptance miss must remain visible

With five repeats, the SE estimate itself fluctuates. R8 applies its factor-two band to every observable with nonzero pooled variance at both r values. The final diagnostic CSV reports pre-fix ratios and structural-zero cases without turning an old-code ratio into post-fix acceptance.

If an approved post-fix run later falls outside the band, preserve it as a failed/discrepant row. Do not select a different seed, omit the observable or widen the threshold. Further changes to statistical acceptance require the mandated physics decision.

## Blocking boundary

Fable weekly usage was reported at 51% during preflight; capacity under the configured 50% ceiling for planning and final sign-off was not established. Opus code review and these read-only diagnostics do not substitute for Fable. C0 stays partial, C1 is not amended, C2 stays blocked.
