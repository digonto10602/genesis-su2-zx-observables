# Session summary — c060_p0_20260909_5

Gate C0: **PARTIAL**. C1: unamended. C2: not started, preparation evidence only.
No hardware job has ever been submitted. Every noisy number here is EMULATED.

## What this session was authorised to do

The user lifted the budget deferral that had blocked the production physics
repair, the C0 re-gate and the C1 amendment in the two prior sessions, and asked
for the campaign to be driven to its end gate.

## The defect, confirmed before anything was changed

On the production path, `AerSimulator.from_backend(FakeTorino)`, at 12 qubits and
1,024 shots, seeds 500 and 501 give 0 same-index matches and 1,023 shift matches:
consecutive seeds are one shot stream offset by a single draw. Seeds spawned from
a numpy SeedSequence give 1 shift match. Evidence: `seed-mechanism.json`.

## The repair

`run_counts` now derives per-repeat seeds from
`numpy.random.SeedSequence(seed).spawn(n)`, reduced to 31-bit ints, passed only
through `sim.run(..., seed_simulator=...)`. The `sim.set_options` mutation of
caller-owned state is gone: the caller's seed survives at 101 where it was
previously overwritten to 500. The signature is unchanged, so `run_g4.py` needs
no edit, and the seeds used are exposed through `LAST_SEEDS` / `run_counts_meta`.

`physical_yield` returns 0.0 on empty input, matching `postselect`, per ruling.

`channel_closure_residual` gains one term on its right-hand side: the weight of
keys that fail to decode. It is identically zero on any properly post-selected
input, so no gated number moves, and it makes the residual equal minus the
injected weight on a corrupted input. This closed the R9 row that two prior
sessions recorded as unsatisfiable. Ruling: `ruling-R9-closure-residual.md`.

## Gate rows

| Row | Verdict | Evidence |
|---|---|---|
| V1 restored evidence and conditioned slopes | pass | `slope-conditioning.json` |
| V10 twin variance | **partial** | `twin-row-calibrated.json` |
| V11 estimator, four R9 rows | pass | `gate_C0.xml` |
| V11 ODR closure | deferred to Phase 5 | preregistration |
| Tier 2, j_max = 1 counts | pass | `gate_C0.xml` |
| Repository cleanliness | evaluated after the gate commit | `git-status-final.txt` |

Eight test cases ran, eight passed, no failures, no skips, 122.3 s.

## V10, stated exactly

At r = 0, on R8's own 4,000 shots, the repaired code gives **5 distinct
dictionaries of 5** with a mean kept count of 2,553.4, against **4 of 5** for the
pre-fix code. The repair does what it was meant to do.

At r = 1 the row is **not met, on cost**. The circuit transpiles to 821,320
operations at depth 506,888 on the 133-qubit target and costs a measured **27.5
seconds per shot**, so R8's 1,024 shots across 5 repeats needs about **39 hours**
on this machine against the roughly 10 minutes the ruling budgets for it. Three
attempts were aborted, at 88, 44 and 28 minutes. A token run at 8 shots produced
5 distinct raw dictionaries but a mean kept count of 0.2 shots, which is
statistically empty and is not offered as evidence.

**R8's shot count was not amended to fit the hardware.** Loosening a threshold so
a row can be declared a pass is the move this campaign forbids, so the row is
recorded as unmet and C0 stays partial. What the campaign now has, which it did
not have this morning, is the measured cost that makes the choice concrete:
lower r = 1's shot count deliberately, move it to the cheaper simulator path, or
budget real compute for it.

## Also recorded

- `DISCREPANCIES.md` and `DECISIONS.md` in the v0.5.0 run carry D-E: the v0.5.0
  twin sigmas are void, and no v0.5.0 twin number was ever gated.
- The archived v0.4.0 package was grepped for the same seed pattern and does not
  carry it; it calls an Aer simulator once, at a fixed seed, for a single shot.
- C2 preparation, not a gate verdict: V3 gives 152 with sectors 3/36/74/36/3,
  V5 gives 112 and 2,417 with their stated sectors, V7 gives 1,727, each by three
  independent methods. The "far corners" placement ambiguity was settled by
  enumerating all fifteen placements: only diagonal pairs give 2,417. Neither
  frozen route implements a 2x3 geometry, so V7 cannot yet be evidenced by route
  code.

## Next action

Decide the r = 1 shot count deliberately at C1, then rerun V10's r = 1 row and
close C0. C2 rows V2, V4 and V6 remain untouched.
