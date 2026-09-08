# Structured synthesis of the L12 block unitaries (G4 prerequisite)

You are a builder in RUN (CWD). Interpreter: ../../.mamba/envs/su2zx/bin/python
(qiskit 2.5, aer, numpy, scipy, pytest). You own ONLY
src/su2qc/circuits/synth_l12.py and tests/test_synth_l12.py. Do not modify
strang_l12.py, the encodings, or anything else. Read src/su2qc/circuits/strang_l12.py
first: it provides terms(g2,m) -> (basis, {group: 82x82}), supports(g2,m) ->
{group: sorted qubit list}, local_matrix(M, codes, S) -> 2^|S| Hermitian
matrix on the support, and the verified generic-synthesis unitary(group,theta,
g2,m). Parameters: sl.params() (g2=4, m=0.75, dt=0.8333, r_max=3).

## Structure you must exploit (measured)
- Each hopping group h_l on 6 qubits: local Hermitian matrix of dim 64 with 16
  nonzeros forming 4 independent 2-level blocks and 2 independent 3-level
  blocks (real entries: ±0.3536, ±0.5, ±0.7071). The rest of the 64-dim space
  is untouched (zero rows).
- The plaquette group B on 8 qubits (the 8 link-copy bits): dim 256, 16
  nonzeros = 8 independent 2-level blocks (real entries ±0.0625, ±0.125,
  ±0.25 at g2=4); each block pairs a code with the code where ALL 8 link bits
  are flipped (the "generalized flip" of the run prompt §5.5).
- D is diagonal on the 82 physical codes (phases), 1 elsewhere is NOT required:
  any phase on unphysical codes is allowed (they are never populated), so you
  may choose the cheapest diagonal that is correct on the 82 codes.

## Deliver: synth_l12.py with
  synth_unitary(group, theta, g2, m) -> QuantumCircuit(12), exact to 1e-10 on
  the physical subspace, NEVER mapping physical -> unphysical codes, using
  ONLY these structural methods (no UnitaryGate larger than 2 qubits, no
  generic isometry synthesis):
  1. Two-level blocks {|x>,|y>} with real symmetric coupling c (and possibly
     equal diagonals a — check; if the two diagonals differ, include the
     relative phase): exp(-i theta [[a, c],[c, a]]) restricted to the pair.
     Implement with a Gray-code path: conjugate by CNOT/X so that |x> and |y>
     differ in exactly one target qubit and the remaining support bits are a
     fixed control pattern; then apply a multi-controlled RX(2*theta*c)
     (qiskit MCRX / mcrx or RXGate().control(k, ctrl_state=...)) on the target
     with controls on the other support bits; uncompute the conjugation. Use
     the minimal control set: controls are only needed to distinguish this
     pair from the OTHER codes in the support space that are reachable
     (physical codes with the same off-support bits) — compute the minimal
     control set numerically (drop a control if no physical code in the
     support space collides after dropping). This is the "minimal control set
     found numerically" of the prompt.
  2. Three-level blocks: decompose the 3x3 Hermitian block exactly:
     exp(-i theta M3) via an eigendecomposition into a sequence of at most
     3 two-level (Givens) rotations plus diagonal phases on the 3 states
     (standard two-level decomposition of a 3x3 unitary), each two-level
     step implemented as in (1) with a possibly complex rotation (use
     controlled U(θ,φ,λ) on the target). Or: implement the 3x3 block via a
     small chain: exp(-iθM3) exactly equals a 3x3 unitary V; write V = product
     of two-level unitaries by Givens elimination (V is 3x3, this is 3 Givens
     rotations + 3 phases) — exact, not Trotterized.
  3. Diagonal D: exp(-i theta D) with D diagonal on the 82 codes. Realize as a
     phase polynomial: fit the 82 phases with a sum over Z-monomials on the
     12 qubits using only monomials of weight <= 3 restricted to each vertex's
     3 qubits plus link-pair terms if needed — D = electric (a function of the
     8 link bits, separable: sum over links of (g2/2)(3/4)*bit, taking ONE copy
     per link) + mass (function of each vertex's (a,b,c): n_v = 2c if a==b,
     1 if a!=b, i.e. n_v = c*(1 - (a xor b))*2 + (a xor b) — a weight-3
     polynomial per vertex). So D is exactly a sum of local RZ and RZZ/RZZZ
     terms: implement with RZ + CNOT ladders (RZZ = CX RZ CX; RZZZ = ladder).
     Exact by construction.
  Also: synth_strang_step(dt, g2, m) and synth_full_circuit(r, dt=None,
  g2=None, m=None, merge_D=True) mirroring strang_l12's ordering
  (D/2, h0/2, h2/2, h1/2, h3/2, B, h3/2, h1/2, h2/2, h0/2, D/2; prep = X on
  the stretched code = sl.prep_stretched()).

## Tests (tests/test_synth_l12.py, all @pytest.mark.unit; runtime < 3 min)
For each group and theta in {0.13, 0.61}: build synth circuit; for each of
the 82 physical codes prepare it (X gates), run Statevector, compare the 82
amplitudes with expm(-i theta T_group)[:, j] to 1e-10, and assert the norm on
unphysical codes <= 1e-12. Same for synth_strang_step vs sl.exact_strang_matrix
(1e-10). Then resources: transpile(circ, basis_gates=['cz','rz','sx','x','id'],
optimization_level=3, seed_transpiler=7); count 2q gates and 2q depth per
group, per step, per full circuit r=1..3; write circuits/resources_synth.md
(same table format as circuits/resources_logical.md) and print the numbers.
Target: as low as you can — the run budget is ~250 CZ per Strang step; report
honestly whatever you get; do NOT stop early if you are above budget, just
report.

Acceptance: `../../.mamba/envs/su2zx/bin/python -m pytest tests/test_synth_l12.py -q`
green. Print JSON: {files, worst_dev, worst_leak, cz_per_group, cz_per_step,
cz_full_r3, depth2q_step}. Time box 75 min.
