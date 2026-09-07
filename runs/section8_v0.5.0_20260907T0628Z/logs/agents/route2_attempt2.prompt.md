# Route 2 builder — attempt 2 (Codex)

Implement, from scratch, `src/su2qc/ham/route_gausskernel.py` and `tests/test_route_gausskernel.py`
inside the run directory (you are started in the run directory; treat it as CWD root).
A broken partial file may exist at src/su2qc/ham/route_gausskernel.py — delete and rewrite it.

You own ONLY those two files. Do NOT read, import, or modify `src/su2qc/ham/route_spinnet.py`
or `tests/test_route_spinnet.py` (independence requirement). You MUST read
`src/su2qc/conventions.py` first — it is frozen (geometry, staggered phases eta=(+1,-1,+1,+1),
plaquette orientation U_box = U_0 U_1 U_2^dag U_3^dag, parities (+1,-1,+1,-1), n_vac=(0,2,0,2),
JW mode order (v,c) v-major, couplings). Import constants from it.

Python interpreter: ../../.mamba/envs/su2zx/bin/python (numpy, scipy, pytest available; NO sympy).

## Physics: redundant Kogut–Susskind formulation + Gauss-law kernel projection

System: SU(2) lattice gauge theory on one square plaquette (4 vertices, 4 links, open
boundaries), two-color staggered fermions (one color doublet per vertex, 8 JW modes),
link truncation jmax in {0.5, 1.0}.

H = (g2/2) sum_l E_l^2 + m sum_v parity_v n_v
  + (1/2) sum_l eta_l ( psi^dag_{s(l)} U_l psi_{t(l)} + h.c. )
  - (1/(2 g2)) ReTr( U_0 U_1 U_2^dag U_3^dag )    [i.e. -(1/(2g2)) Tr(U_box + U_box^dag) with Tr real: Tr(U)+Tr(U^dag) = 2 ReTr(U_box)... implement as -(1/(2g2)) (Tr U_box + Tr U_box^dag)]

Link Hilbert space (truncated rigid rotor): states |j, mL, mR>, j = 0..jmax in half-steps,
mL, mR in -j..j. Dim 5 at jmax=1/2, 14 at jmax=1.

Link operators:
- E^2 diagonal: j(j+1).
- Left generators E^a_L act on mL as spin-j angular momentum matrices (a = x,y,z);
  right generators E^a_R act on mR. Convention: choose signs such that Gauss law below
  closes; standard choice: [E^a_L, U] = -(sigma^a/2) U (left mult), [E^a_R, U] = U (sigma^a/2).
  Concretely with U as defined below, E^a_L acting on the mL index with matrices T^a_(j)
  and E^a_R acting on mR with matrices T^a_(j) works with an appropriate relative sign —
  VERIFY NUMERICALLY and fix signs until the commutator identities hold; then Gauss law is
  G^a_v = sum_{l: s(l)=v} E^a_{L,l} + sum_{l: t(l)=v} E^a_{R,l} + Q^a_v with
  Q^a_v = sum_{ab} psi^dag_{v,alpha} (sigma^a/2)_{alpha beta} psi_{v,beta}.
- Link matrix elements (the j=1/2 Wigner-D insertion):
  <j', mL', mR' | U^{alpha beta} | j, mL, mR> =
     sqrt((2j+1)/(2j'+1)) * CG(j, mL; 1/2, alpha | j', mL') * CG(j, mR; 1/2, beta | j', mR')
  for j' = j ± 1/2 within truncation (alpha, beta = ±1/2 label the color-fundamental indices).
  Hand-code CG closed forms (no sympy):
    CG(j,m;1/2,+1/2|j+1/2,m+1/2)= sqrt((j+m+1)/(2j+1))
    CG(j,m;1/2,-1/2|j+1/2,m-1/2)= sqrt((j-m+1)/(2j+1))
    CG(j,m;1/2,+1/2|j-1/2,m+1/2)= -sqrt((j-m)/(2j+1))
    CG(j,m;1/2,-1/2|j-1/2,m-1/2)= sqrt((j+m)/(2j+1))
  With this U, check numerically the required commutation with E_L/E_R and FIX THE SIGN
  CONVENTION so that ||[G^a_v, H_hop_l]|| = 0. Also needed: U^dag entries (conjugate transpose).
  IMPORTANT SUBTLETY: this truncated U is not exactly unitary (truncation), that is fine;
  gauge covariance [G, hop] = 0 must still hold exactly because CG factors carry the reps.

Matter: 8 fermionic modes with JW strings in the frozen order modes 0..7 =
(v0c0, v0c1, v1c0, v1c1, ..., v3c1). psi_{v,c} = (prod_{k < mode(v,c)} Z_k) sigma^-_{mode}.

Gauss law / physical space: at each vertex the total SU(2) generator
G^a_v (links incident as source use E_L, as target use E_R, plus matter charge Q^a_v).
Physical subspace = states annihilated by all G^a_v (equivalently the zero eigenspace of
sum_a (G^a_v)^2 per vertex). Kernel dims must be 82 (jmax=0.5) and 152 (jmax=1.0).

Efficient kernel construction (REQUIRED, do not diagonalize the full redundant space at
jmax=1): total redundant dim at jmax=1/2 is 5^4 * 2^8 = 160000 (sparse fine), at jmax=1 it
is 14^4 * 256 ≈ 9.8M — you must block: fix the link j-configuration sector (j1..j4) (16
sectors at jmax=1/2, 81 at jmax=1) and the fermion occupation numbers; within a sector,
each vertex couples only (mL/mR of its two incident links) x (its 4-dim matter Fock space);
build the vertex-local singlet (G^2_v = 0) subspace per vertex and tensor the 4 vertices.
Label each resulting kernel vector ((j1,j2,j3,j4),(n1,n2,n3,n4),0) — n_v = local fermion
number, a good quantum number of the kernel construction. Assert orthonormality and that
each allowed (j-sector, n-pattern) yields exactly the predicted multiplicity (2-valent
intertwiners are unique: 1 state per allowed combo; allowed = at each vertex j_a=j_b with
n in {0,2} or |j_a-j_b|=1/2 with n=1).

## Required API (module-level)

- build_hamiltonian(g2, m, jmax) -> (H_phys sparse csr (hermitian), basis_labels list, P)
  where P is the (dim_redundant x dim_phys) sparse isometry, basis_labels[i] as above.
- build_hamiltonian_no_magnetic(g2, m, jmax) -> same but without the plaquette term.
- gauss_commutator_norms(jmax) -> dict {"electric":x,"mass":x,"hop_0":x,...,"hop_3":x,
  "magnetic":x} of max over v,a of max-abs entry of the sparse commutator [G^a_v, H_term]
  on the redundant space. All must be <= 1e-12.
- get_state(label, basis_labels) -> index helper (or expose labels so the stretched string
  ((0.0,0.5,0.5,0.5),(1,1,0,2),0) can be located).
- Observables in the projected basis: E2_link(l), n_op(v), N_total, and channel projectors
  P_surv (q=(+1,-1,0,0)), P_meson (all |q_v|=1), P_BBbar (any |q_v|=2), q_v = n_v - n_vac(v)
  — all diagonal, computable from basis_labels alone; return sparse matrices; signature
  (basis_labels) or (g2,m,jmax)-independent as you prefer, but document.

## Tests (tests/test_route_gausskernel.py, @pytest.mark.unit)

Must check and PRINT: kernel dims 82 and 152; sector dims N=0,2,4,6,8 -> 2,20,38,20,2, no
odd N; hermiticity <= 1e-13; gauss_commutator_norms all <= 1e-12 (jmax=0.5 at least);
pure-electric degeneracies at g2=1e6, m=0: eigenvalue clusters at (g2/2)(3/4)k with
multiplicities 16,16,18,16,16; stretched-string label present exactly once.
Keep full test runtime < 3 min (jmax=1 build < ~90 s).

Acceptance: `../../.mamba/envs/su2zx/bin/python -m pytest tests/test_route_gausskernel.py -q`
all green, run from the run directory.

When done print a JSON summary: files, key numbers, convention sign choices you made, open questions.
