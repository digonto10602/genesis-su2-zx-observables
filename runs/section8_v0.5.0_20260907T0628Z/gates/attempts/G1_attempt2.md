# G1 attempt 2 (T+1:35 - T+2:40)

Route 2 rebuilt: codex skeleton (physical basis via vertex-local Gauss singlets —
verified dims 82/152, sectors, electric clusters) + orchestrator completion of the
full redundant-space terms (E, mass, JW hoppings, plaquette trace) and projection.
U conjugation convention selected numerically: (conjL=True, conjR=False) gives
max |[G^a_v, H_term]| = 0.0 exactly for all 7 term groups. H_phys dim 82, herm 0.

Route comparison FAILED: sorted-spectra max rel dev 0.12–1.32 across 6 coupling
points (target 1e-12); time-series dev 1.02 (target 1e-10). Diagnostics: diagonals
agree (4e-16); route 1 hopping elements uniformly 1/(2 sqrt 2) and magnetic
uniformly 1/16 g2^-1 vs route 2 structured values — route 1 omits dressed-vertex
recoupling factors.

Escalation triggered per §4.2 → solutions/0.5.0.md (first escalation of the run).
