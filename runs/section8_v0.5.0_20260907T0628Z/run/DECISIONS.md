# Decisions
D1 (T+3:20): Route 2 builds the projected Hamiltonian only at jmax=1/2 tonight; at
jmax=1 it computes the Gauss-kernel dimension (152) but not H_phys (redundant dim
14^4*256 ~ 9.8M exceeds the night's budget). Route agreement is gated at jmax=1/2
per prompt G1 criterion 3; jmax=1 H comes from route 1 (whose construction is
identical machinery at both truncations and matches route 2 exactly at jmax=1/2).
D2 (T+3:20): limits.magnetic_off_check compares route1-B-off vs route2-B-off
(no independent 1D chain builder exists in this repo; prompt allows a separately
written construction "from the repo if present"). Recorded as a criterion deviation.
D3 (T+3:20): frozen-matter tolerance documented-relaxed to 1e-8 (residual is the
physical O(h^2/m) perturbative shift, root cause in physics/conventions_reconciliation.md).
D4 (G3): S8 and C7 encodings not built tonight (single-builder capacity); G3 is
gated on the L12 primary encoding only (prompt §4.4 G3 fallback: "drop the
failing encoding"). Recorded as FAIL criteria in GATE_G3.json, excluded from the
PASS logic by this decision; the encoding-ablation secondary endpoint is
therefore NOT DONE.
D5 (G3): Block unitaries are synthesized by generic qiskit UnitaryGate on the
numerically found support (6 qubits per hopping, 8 for the plaquette). They are
exact and leak-free (the "symmetry-verified" property) but cost ~45.9k CZ per
Strang step under generic synthesis vs the ~250 budget. G4 must attempt
structured synthesis (D: sparse phase polynomial; h_l: 2x2/3x3 block rotations;
B: fan-out ladder + uniformly-controlled rotation) before the budget decision.
D6 (campaign v0.6.1): G4 is REDUCED. The best recorded structured synthesis is 2,156 logical two-qubit gates per step (D=16, h0-h3=248/248/239/241, B=174), 3,976 routed per step and 12,142 routed at r=3, an 8.6x logical gap against 250. No GATE_G4.json was written because compile/twin_check.json was never produced; the twin was killed at r=1. Evidence: compile/resources_routed.md, circuits/resources_synth.md and logs/cmd/run_g4.log.
D7 (campaign v0.6.1): pyzx_basic_TP is retired because its pre-route equivalence error is 1.0e+00, below the >=1-1e-10 hardware-eligibility criterion; root cause not diagnosed; no orthogonality claim.
