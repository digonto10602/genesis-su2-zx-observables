# Review brief for the C0 evidence (R11 step 4)

The reviewer is bounded to the files listed in `evidence-manifest.json` and must
not read or judge anything outside them. The review is adversarial: its job is
to find a row that cannot carry its own weight, not to confirm the gate.

## What to attack, in order

1. **The seed repair.** Does `run_counts` derive seeds in a way that is
   reproducible from the base seed alone, and does it leave the caller's
   simulator untouched? Is there any remaining path by which two repeats share a
   shot stream? The mechanism claim rests on `seed-mechanism.json`; check that
   the numbers there support the claim actually made, and no wider one.
2. **The V10 acceptance.** R8 wants the factor-two multinomial band on every
   observable with nonzero variance, structurally empty observables listed and
   never counted as evidence of determinism, and a negative control that is a
   real run. Confirm the test does each, and that the recorded ratios come from
   measured data rather than from a formula evaluated on itself.
3. **The V11 rows.** The expected side of every assertion must come from an
   oracle written inside the test. Any call to the module under test on an
   expected side is a finding. Check that the violating-input row now measures
   what it claims and that the ruling on the undecodable-weight term did not
   change the residual on physical input.
4. **The V1 row.** Its rerun reproduced the committed arrays exactly, so the
   slope assertion is zero against a zero bound. Say plainly whether that is
   acceptable evidence or whether the row should be recorded with the bound
   unexercised. Do not let it pass as though headroom had been demonstrated.
5. **Cross-session leakage.** No row may cite an earlier session's artifact as
   its own evidence, and no test may write into an earlier session's directory.
6. **Status integrity.** Nothing in the ledger, the state file or the evidence
   may upgrade a status, assert a gate that did not run, or describe emulated
   data as hardware data. No hardware job has ever been submitted.

## Required output

A verdict per row, blocking or advisory, each naming the file and line that
supports it. If a row cannot be judged from the manifest alone, say so rather
than inferring. Finish the review; a review that stops early is rerun with a
narrower file list, never recorded as done.
