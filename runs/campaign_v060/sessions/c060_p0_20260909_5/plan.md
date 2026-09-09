# Plan of record — c060_p0_20260909_5

Authorised by the user on 2026-09-09 to carry the campaign through the gates,
which lifts the budget deferral that blocked the production physics repair, the
C0 re-gate and the C1 amendment in the two prior sessions. Fable 5.1 plans and
signs off, Opus 5 builds and reviews, tests run mechanically.

## Rulings issued this session

- **Seed derivation (R7).** Confirmed on the production path before any edit:
  at 12 qubits and 1,024 shots, seeds 500 and 501 give 0 same-index matches and
  1,023 shift matches, so consecutive seeds are one shot stream offset by one
  draw. Seeds spawned from a numpy SeedSequence give 1 shift match. `run_counts`
  moves to spawned seeds passed only through `sim.run`, the caller-state
  mutation goes away, and the seeds used are exposed for the ledger.
- **`physical_yield` on empty input.** Returns 0.0, matching `postselect`. The
  two functions may not disagree on the same degenerate input.
- **R9 violating-input row.** Both sides of `channel_closure_residual` skip keys
  that fail to decode, so an unphysical key contributes nothing to the residual.
  The test states the required behaviour rather than being weakened; if the row
  cannot pass against the current implementation it is marked with its reason
  and comes back to me for a repair ruling, and no other row is softened.
- **Closure identity.** Unchanged. It holds on the present basis by exhaustive
  enumeration of the 82 physical codes, is basis-dependent rather than
  structural, and no channel definition is touched.

## Lanes

- A: `run_counts` repair and the V10 test per R8.
- B: the V11 estimator test per R9, independent in-test oracle.
- C: the V1 regression test per R10, evidence written to this session.
- Mechanical: the gate command, the production twin runs, the manifest.
- Review: Opus on the manifest's files, then Fable sign-off on the same snapshot.

## Order

1. Lanes A, B, C in parallel on disjoint files.
2. Review of the repair and the three tests.
3. Gate C0 with the recorded command and a junit XML into this session.
4. Ledger, state, evidence manifest, review, sign-off, commit.
5. C1 amendment per R12: three hashes inline, the conventions-hash ambiguity
   resolved under labelled keys, defect classes including twin seed derivation,
   re-hash, commit.
6. C2 rows V2 to V7 as far as they go, with anything unreached recorded as not
   started rather than implied.

## Standing constraints

No hardware submission. No git push. No threshold, band, Hamiltonian, Gauss-law
convention or observable definition is changed. Historical evidence in the
v0.5.0 run directory is read, never overwritten; the D-E discrepancy and D6
decision appends are the only writes there and they add records rather than
replacing them.
