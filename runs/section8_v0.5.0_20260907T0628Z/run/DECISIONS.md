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
