# C2 preparation evidence, 2026-09-09

Gate C2 is not judged by this session and no C2 verdict is issued here. What
follows is the classical enumeration evidence that the C2 rows will need, so
that the gate can later be decided on measured numbers rather than on prose.

Three independent methods were written for every count: an integer
Clebsch-Gordan singlet multiplicity at each vertex, a Gauss-law kernel nullity,
and a Haar projection. The two route implementations of the campaign were then
run against the same targets where they apply.

| Row | Target | Measured | Agreement |
|---|---|---|---|
| V3, j_max = 1 plaquette | 152, sectors 3 / 36 / 74 / 36 / 3 | 152, same sectors | three independent methods and both routes agree |
| V5, static bridge, small | 112, sectors 2 / 27 / 54 / 27 / 2 | 112, same sectors | three independent methods agree |
| V5, static bridge, large | 2,417, sectors 4 / 119 / 597 / 977 / 597 / 119 / 4 | 2,417, same sectors | three independent methods agree |
| V7, 2x3 ladder | 1,727 | 1,727, sectors 4 / 95 / 426 / 677 / 426 / 95 / 4 | three independent methods agree |

The 2x3 ladder is six vertices, seven links and two plaquettes, at j_max = 1/2
and with no static charges. Its sector histogram is reported here because the
campaign fixes only the total; nothing was tuned to reach it, and a disagreement
would have been recorded rather than adjusted.

## An ambiguity the enumeration settled

The campaign describes the static charges as sitting at the two far corners of
the ladder, which is not a unique placement. Rather than pick the reading that
fits, the lane enumerated all fifteen ways of placing two static charges and
reported every count. Only the two diagonally opposite corner pairs give 2,417;
far corners in the same row give 2,418, the same column gives 2,442, and
adjacent placements give between 2,706 and 3,041. So far corners means
diagonally opposite, and the data says so independently of the prose. The
single-plaquette case behaves identically: both diagonal pairs give 112 and all
four adjacent pairs give 113.

## A caveat the eventual gate must carry

Neither frozen route implements a two-by-three geometry; both are hard-coded to
the single plaquette. The 1,727 count therefore cannot yet be evidenced by route
code, only by the three independent methods. As a proxy, all three methods were
run against both routes on the single plaquette at j_max = 1/2 and all give 82,
matching the frozen expected dimension. Route agreement at 2x3 needs the route
extension that V2 and V7 call for, and that work has not been done.

The projector orthonormality deviation measured on the j_max = 1 route is
8.88e-16 against a threshold of 1e-12.

What C2 still needs and this session did not produce: V2, which requires the
four-coefficient Hamiltonian signature at both coupling points and the v0.5.0
route-agreement test rerun against it; V4, the truncation table at the frozen
time points; and V6, the bridge dynamics scan, which the campaign records as
never blocking. Those rows are untouched and remain not started.
