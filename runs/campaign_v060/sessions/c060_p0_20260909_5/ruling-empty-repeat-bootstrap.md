# Ruling — an empty repeat must not enter the bootstrap, 2026-09-10

## What was found

The report lane, reading the 128-shot V10 evidence, found that at r = 1 one of the
five repeats kept zero shots. `twin.observables` on an empty kept dictionary returns
every channel probability as 0.0 and `dC` at its floor of -2.25, and
`twin.bootstrap` then resamples those five per-repeat vectors as though the empty one
were a measurement. It is not a measurement. It is a sentinel.

This is a real defect, separate from the seed defect repaired earlier in the session,
and it explains the `P_BBbar` ratio of 2.603 at r = 1 directly: one hard zero among
five points inflates the spread. At a 2.03% yield with 128 shots, drawing an empty
repeat was close to inevitable.

## Ruling

An empty repeat carries no information and may not be treated as a sample.

1. `bootstrap` must count repeats with zero kept shots, exclude them from the
   resample, and return that count alongside the result so the caller can see it.
2. A V10 row computed from fewer than the full five non-empty repeats is **not** a
   pass. It is recorded with the number of usable repeats, and the row is unmet if
   that number is below what the acceptance requires.
3. The zero-kept case must never be silently represented by `dC = -2.25`, which is a
   physically meaningful value at the bottom of the Casimir range and is
   indistinguishable, downstream, from a real measurement.

## Consequence for the present evidence

The r = 1 variance number in `twin_variance.json` is contaminated by this defect and
is withdrawn as evidence for anything. The r = 1 row stands as not evaluable, now for
two compounding reasons: 2.6 kept shots per repeat, and one repeat with none at all.

The r = 0 row is **not** affected: all five repeats there kept about 2,553 shots. The
`dC` shortfall at r = 0 remains an open finding with its own candidate explanations,
and this ruling does not close it.

## Implementation

Handed to the next build cycle, not applied here, because it changes a function that
the gate under discussion depends on. The equivalent per-repeat diagnostic the report
recommends — persisting the per-repeat observable vectors and per-repeat `Var_s` that
the code already computes and then discards — is the cheapest way to make both this
defect and the `dC` finding visible in future runs, and goes in the same change.
