# v0.4.0 consecutive-seed grep (R12), 2026-09-09

R12 requires a grep of the archived, published v0.4.0 package for the same
consecutive-seed pattern that voids the v0.5.0 twin sigmas, with the result
reported and no repair applied.

**Finding: the pattern is not present.** The archived package calls an Aer
simulator in one place only, `src/su2zx/scaling_study.py:76`, as
`simulator.run(saved, shots=1, seed_simulator=11)`. It is a single shot at a
fixed seed inside a matrix-product-state timing study, not a set of repeats
seeded by increment, so no sequence of adjacent seeds is ever sampled and no
uncertainty is derived from repeats seeded that way.

The other archived Aer users are `src/su2zx/tn_study.py`, `tools/report_v040.py`
and `tools/provenance.py`; none of them passes `seed_simulator` at all. The one
repetition loop, `src/su2zx/core.py:195`, is a ZX-rewrite repetition count and
performs no sampling.

No change was made to the archived package, which stays as published. Nothing
here amends the v0.4.0 errata.
