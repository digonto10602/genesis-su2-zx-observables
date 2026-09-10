# SU2ZX · GI-Cost Campaign · v0.6.4 — close C0, amend C1, then drive C2 to C5 on a fixed cycle

**Hermes prompt v0.6.4 · path: `SU2ZX/prompts/gi_cost_campaign_v.0.6.4.md`**
**Amends v0.6.3 (which amends v0.6.2, v0.6.1, v0.6.0). All remain in force; this file adds rulings R20–R26. Where files disagree, the newest wins. Nothing here loosens a threshold except the one reduction the campaign authority made explicitly and which R21 records as a reduction.**

---

## 0. Where the campaign actually stands

Session `c060_p0_20260909_5` repaired the twin seed derivation and re-gated C0. The
result, measured rather than asserted:

- The defect is confirmed on the production path. At 12 qubits and 1,024 shots, seeds
  500 and 501 give 0 same-index matches and 1,023 shift matches; seeds spawned from a
  numpy `SeedSequence` give 1. Consecutive seeds were one shot stream offset by a
  single draw, so no v0.5.0 twin sigma was ever an independent-repeat uncertainty.
- `run_counts` now spawns seeds, passes them only through `sim.run`, and no longer
  mutates the caller's simulator. `physical_yield` returns 0.0 on empty input.
  `channel_closure_residual` gained an undecodable-weight term that is identically
  zero on properly post-selected input and finally lets the residual see a corrupted
  one; that closed the R9 row two sessions had recorded as unsatisfiable.
- **C0 is PARTIAL.** V1, V11 (four R9 rows) and the j_max = 1 counts pass; eight test
  cases, zero failures. V10 passes at r = 0 on the full 4,000 shots with five distinct
  dictionaries of five, against four of five before the repair. V10 at r = 1 was not
  met on cost: the circuit is 821,320 operations at depth 506,888 on the 133-qubit
  target and costs a measured 15.6 s per shot, so R8's 1,024 shots across five repeats
  needs roughly 22 hours on this machine against the ten minutes the ruling budgeted.
- C1 remains **unamended**. C2 is **not started**; its counting rows are prepared but
  not gated. C3 to C8 are untouched.
- No hardware job has ever been submitted. `HARDWARE_MODE` is disabled and no IBM
  credentials are configured.

---

## 1. Rulings

**R20 · The cycle is fixed, and every step writes something down.** Each gate is worked
in this order, and the order does not vary:

1. **Plan (Fable 5.1, medium).** The plan is written into a new `prompts/` file before
   any code is touched, not only into a reply.
2. **Build (Sonnet 5 high, or Opus 5 medium for the subtler pieces).** Code and tests.
3. **Watch (Sonnet 5).** While generation runs, Sonnet watches it and reports the
   measurements as measurements.
4. **Report (Opus 5 high).** Results, artifacts and reports are written into their
   corresponding folders.
5. **Read and hand on (Fable 5.1, medium).** Fable reads the reports, zips the
   evidence, and writes the plan for fixes and next steps into the *next* `prompts/`
   file.
6. Repeat until every gate is closed or explicitly blocked.

A build agent may not run a long verification while an authoritative gate run is in
flight. Two noisy-twin simulations on one twelve-core machine roughly halve each
other's speed, which cost this campaign three aborted runs in one evening.

**R21 · The r = 1 shot count is reduced, deliberately, and recorded as a reduction.**
The campaign authority lowered r = 1 from R8's 1,024 shots to 128 on 2026-09-09, on the
cost evidence above. This is the one number this file changes. It is recorded as a
reduction in the C0 ledger row, in the test that carries it, and in the C1 amendment;
it is never described as R8 having been met. The measured consequence is stated with
it: the r = 1 post-selection yield is 2.5%, so 128 shots leaves about 3.2 kept shots
per repeat, and a bootstrap sigma over five repeats of three kept shots is not a
meaningful uncertainty. Therefore:

- V10 splits into two sub-rows. **Distinctness** is judged at both r. **The factor-two
  multinomial variance band is judged at r = 0 only**, and at r = 1 it is recorded as
  *not evaluable at this shot count*, with the kept-count evidence, never as a pass.
- If a future session can afford more shots, the r = 1 variance sub-row is reopened.
  Until then C0 closes as **pass with a named, evidenced reduction**, or stays partial
  if the distinctness sub-row fails.

**R22 · C1 amendment, executed not deferred.** Apply the prepared amendment: inline the
three SHA-256 values; resolve the conventions-hash ambiguity by recording both hashes
under the labelled keys `conventions_md` and `conventions_py` in the preregistration and
the state file; add the prespecified defect classes including "twin seed derivation
changes → rerun V10, new C0 row"; add the one-line reasons to R1, R3 and R4; add R21's
shot reduction as an amendment entry naming the cost evidence; re-hash; write
`gates.C1 = pass (amended <utc>)` carrying the old and new preregistration hashes.

**R23 · C2 is opened with the counting rows already in hand.** The enumeration evidence
exists and reproduces every campaign target by three independent methods: V3 gives 152
with sectors (3, 36, 74, 36, 3); V5 gives 112 with (2, 27, 54, 27, 2) and 2,417 with
(4, 119, 597, 977, 597, 119, 4); V7 gives 1,727 with (4, 95, 426, 677, 426, 95, 4). The
"far corners" ambiguity was settled by enumerating all fifteen placements: only
diagonally opposite pairs give 2,417. What C2 still needs, and what this cycle builds:

- **V2.** The four-coefficient Hamiltonian signature `H(coeffs=(cE,cM,cH,cB), jmax,
  geometry, static_charges)` with the `H(gE, mu, jmax)` wrapper reproducing v0.5.0 at
  gE = 2, at both coupling points P-A and P-S, and the v0.5.0 G1 route-agreement test
  rerun against the new signature at 1e-12 route agreement and 1e-10 observable time
  series.
- **V4.** The truncation table, j_max = 1 against j_max = 1/2, at the frozen time
  points, every primary observable.
- **V6.** The bridge dynamics K-scan on the static-charge cases. Recorded pass,
  near-pass or fail; **never blocking**, per D-C7.
- **V7 route agreement.** Neither frozen route implements a 2x3 geometry. Either extend
  a route to that geometry or record V7's route-agreement clause as unmet with the
  reason; the count itself already stands by three methods.

**R24 · C3 and C4 follow, in that order.** C3 needs at least one accepted Krylov circuit
per (point, hardware time point) with the V8 row, K(t) curves at both points on the
82-state system, the rejected list and the layout table. Thresholds: infidelity ≤ 1e-3,
observable error ≤ 1e-3, unused-codeword weight ≤ 1e-5, leakage ≤ 1e-12. C4 needs V9,
the E1 resource frontier and E5 extensibility drafts with the NOISELESS accuracy columns
filled, a synthesis sprint closed inside four hours with its number, and the decision
row naming the GI hardware circuit's routed CZ and depth.

**R25 · C5 is the last gate reachable without hardware, and it must say so.** C5 needs
V12 with E2 passing on EMULATED data at two or more time points per arm, the E3 sign
pattern reported per arm, δ_dev frozen, the preregistration hash, and the QPU estimate
inside the cap with its approval file. Every number in it stays labelled EMULATED.
Producing C5 does not authorise submission.

**R26 · C6, C7 and C8 are blocked, and the block is a fact about credentials, not a
judgement.** C6 requires HARDWARE rows from a real device. `HARDWARE_MODE` is disabled
and no IBM credentials are configured, and this campaign does not submit hardware jobs
without an explicit human instruction. C7 and C8 consume C6's data. They are recorded as
**BLOCKED: awaiting credentials and a human decision to submit**, never as not-yet-run.
No emulated result may be presented in a C6, C7 or C8 row.

---

## 2. Order of work

1. Finish the V10 rerun at 128 shots; record both sub-rows per R21; close or re-mark C0.
2. Apply R22, commit `campaign: C1 amended`.
3. C2: build V2, then V4, then V6, wire the prepared counting evidence into the gate
   rows, resolve or record the V7 route-agreement clause. Gate C2.
4. C3, then C4, each on the full cycle of R20.
5. C5 on EMULATED data, with R25's labelling.
6. Write C6, C7 and C8 as blocked per R26, with the exact missing precondition.

## 3. Acceptance

| Gate | Pass requires | Evidence |
|---|---|---|
| C0 | V1, V11, Tier 2 pass; V10 distinctness at both r; variance band at r = 0; r = 1 variance recorded not evaluable with kept counts; git status empty after the gate commit | session ledger rows |
| C1 | three hashes inline; conventions ambiguity resolved under labelled keys; defect classes including twin seed derivation and the R21 reduction; old and new hashes in the row | `PREREGISTRATION.md`, state |
| C2 | V2 both points; V3, V5, V7 counts; V4 table; V6 recorded; V7 route clause resolved or recorded unmet | gate rows plus `c2_prep/` |
| C3 | V8 per accepted circuit; K(t) both points; rejected list; layout table | C3 session |
| C4 | V9; E1 and E5 drafts; sprint closed with its number; decision row | C4 session |
| C5 | V12 on EMULATED at ≥ 2 time points per arm; δ_dev frozen; hash; QPU estimate in cap | C5 session |
| C6–C8 | BLOCKED, precondition named | this file |

## 4. Stop conditions

- A threshold cannot be met → record the row unmet with the measured number. Never
  amend a threshold to fit the hardware; R21's reduction was made by the campaign
  authority, in writing, with cost evidence, and is the only one.
- A gate run exceeding its budget → stop it, keep the partial log under a name that
  says what it was, and record the measured cost.
- Any temptation to present EMULATED data in a hardware row → stop; that is the one
  falsification this campaign cannot survive.
- No hardware submission and no git push without an explicit instruction.
