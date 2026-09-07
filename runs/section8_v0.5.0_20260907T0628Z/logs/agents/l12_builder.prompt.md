# L12 encoding + gauge-invariant block-unitary Strang circuits (G3 primary)

You are a builder inside RUN (CWD). Interpreter: ../../.mamba/envs/su2zx/bin/python
(numpy/scipy/qiskit 2.5/qiskit-aer/pytest). Read first: src/su2qc/conventions.py
(frozen), src/su2qc/ham/route_spinnet.py (the verified Hamiltonian; import it,
never modify it), physics/window.json if it exists (else default g2=1, m=0.1875,
dt=0.4, r_max=3).

You own EXCLUSIVELY: src/su2qc/encodings/__init__.py, src/su2qc/encodings/l12.py,
src/su2qc/circuits/__init__.py, src/su2qc/circuits/strang_l12.py,
tests/test_l12.py. Nothing else.

## L12 encoding (12 qubits, 3 per vertex)

Per vertex v: qubits (3v, 3v+1, 3v+2) = (a_v, b_v, c_v) where a_v is the vertex's
copy of its FIRST incident link's bit, b_v the SECOND (vertex v's incident links
in the fixed order used by the Hamiltonian basis: v0:(l3,l0), v1:(l0,l1),
v2:(l1,l2), v3:(l2,l3) - i.e. _VLINKS in route_spinnet), link bit = 1 iff
j = 1/2. c_v is the matter bit: links agree (a=b) -> c=0 vacuum, c=1 baryon;
links disagree -> c=0 doublet, c=1 LEAKAGE. Each link's value is stored TWICE
(once at each endpoint); the two copies must agree.

encode(label) -> 12-bit int (basis label ((j1..j4),(n1..n4),0) -> computational
state); decode(bits) -> label or None if unphysical; physical_codes() -> sorted
list of the 82 valid codes; leakage flags (all diagonal): per-vertex
(a XOR b) AND c; per-link consistency: copies of link l at its two endpoints
must agree (4 flags). is_physical(bits) = all flags clear. Qubit order in
bitstrings follows the repo rule q11...q0 (Qiskit convention); document the
mapping and test it with a known state (stretched string label
((0,.5,.5,.5),(1,1,0,2),0): links l0=0,l1=1,l2=1,l3=1 -> per vertex v0:(l3,l0)=(1,0)
disagree c=doublet=0 etc. - compute and assert the exact 12-bit integer in a test).

## Gauge-invariant block unitaries (the heart of G3)

Build, as qiskit QuantumCircuit(12) with NO measurement, for each Hamiltonian
group T in {D, h0, h1, h2, h3, B} and angle theta: U_T(theta) with
P_phys U_T(theta) P_phys = e^{-i theta T_enc} exactly and U_T never maps
physical -> unphysical. T_enc = the 4096x4096 matrix that acts as route_spinnet's
term T on encoded physical states and as identity... NO - as anything unitary
on the orthogonal complement, PROVIDED it never mixes the subspaces.

Recommended constructive method (simple, exact, and passes the criteria; do not
over-engineer): for each group T, build the 82x82 matrix T_phys from
route_spinnet (D = diagonal electric+mass of H; h_l = the hopping-only terms of
link l: reconstruct by masking build_hamiltonian_no_magnetic elements whose
labels differ in (j_l, n_s, n_t) exactly; B = H - H_no_magnetic). Lift to 4096:
M = E T_phys E^dag where E is the 4096x82 encoding isometry (columns =
computational basis vectors of the 82 codes). U = expm(-i theta M) acts as the
identity on the complement (M annihilates it) - gauge invariance by
construction, unitary, exact. Then convert to a circuit via
qiskit.quantum_info.Operator + qiskit.transpile-free UnitaryGate... CAREFUL:
a 12-qubit UnitaryGate is a 4096x4096 dense synthesis - too deep. Instead
exploit locality: D is diagonal -> implement as phase gates on the 82 codes
via a diagonal 4096-vector (qiskit Diagonal on 12 qubits is fine, it
synthesizes to CZ/RZ ladders); h_l acts ONLY on the 6 qubits of its two
endpoint vertices (3+3) tensor identity on the rest -> build the 64x64 unitary
on those qubits (lift the vertex-local action: h_l's matrix elements depend
only on the two vertices' states AND the shared link bits, all within those 6
qubits; the JW inter-site sign for non-adjacent sites (l1: v1-v2 adjacent in
order, l3 v4->v3 adjacent, l0 v0->v1 adjacent, l2 v3->v2 NO - l2 connects
v3(idx3)? check LINKS: l2: (3,2) v4->v3 adjacent in site order? sites 3,2
adjacent yes; all four links connect order-adjacent or... l1=(1,2) adjacent,
l3=(0,3): sites 0 and 3 - the JW string crosses sites 1,2: the sign
(-1)^(n_1+n_2) depends on OTHER vertices' matter bits -> for l3 you must
include the parity of n_1+n_2. n_v parity in L12: doublet (c=0, links
disagree) has n odd... n parity = 1 iff links disagree (n=1) i.e. parity bit =
a_v XOR b_v of those vertices. So h_3's unitary needs controls on (a XOR b) of
v1 and v2: implement U_h3 as an 8-qubit operator (6 + the 2 parity... a,b of
v1 and v2 = 4 extra qubits -> 10 qubits) OR simpler: conjugate by CNOTs
computing p_1 = a_1 XOR b_1 into an ancilla-free trick: compute parity into
one of the qubits temporarily. SIMPLEST ROBUST OPTION (allowed): build h_l's
lifted 4096 matrix M_l = E h_l_phys E^dag, then note it factorizes as
(64x64 on 6 qubits) tensor identity XOR sign-controlled; verify numerically:
reshape M_l and test whether it is supported on the 6 endpoint qubits alone;
for the two links where the JW string bites (identify them numerically),
build the 256x256 operator on 8 qubits (6 + the two parity-relevant qubit
pairs reduced: use a_w XOR b_w computed by a CNOT a_w->b_w making b_w the
parity bit, control on it, then uncompute). Then synthesize each small block
unitary with qiskit's UnitaryGate on <= 8 qubits (fine for G3; depth
optimization happens in G4 compile).\n\nStrang step circuit:
strang_step(theta_dict or dt) applying e^{-iD dt/2} h0 h2 (parallel pair? l0
and l2 share no vertex: l0=(0,1), l2=(3,2) - disjoint! l1=(1,2), l3=(0,3)
disjoint) [h0,h2 at dt/2] [h1,h3 at dt/2] e^{-iB dt} [h1,h3 dt/2] [h0,h2 dt/2]
e^{-iD dt/2}. full_circuit(r, dt) = prep(stretched string: X gates to the
code) + r Strang steps (merge adjacent D half-steps). Export helpers:
resources(circ) -> dict(n_2q, depth_2q) counting 2-qubit gates after
qiskit.transpile(circ, basis_gates=['cz','rz','sx','x','id'],
optimization_level=1).

## Tests (tests/test_l12.py, @pytest.mark.unit) - THE G3 CRITERIA

tolerances: unitary equivalence 1e-12, leakage 1e-12 (prompt says 1e-12 for
P_phys (U - e^{-i theta T}) P_phys and P_unphys U P_phys):
1. encode/decode roundtrip on all 82 labels; physical_codes() has 82 distinct
   entries; leakage flags clear exactly on the 82 codes and fire on all others
   (scan all 4096).
2. For each T in {D,h0,h1,h2,h3,B}, theta in {0.13, 0.61}: build U_circ via
   qiskit Operator(circ).data; check norm(P_phys (U_circ - expm(-i theta
   M_T)) P_phys) <= 1e-12 and norm(P_unphys U_circ P_phys) <= 1e-12 (P_phys =
   sum over 82 codes).
3. Full Strang step (dt from window.json or 0.4) vs exact product of expm's on
   the encoded space from the stretched-string code: state fidelity deviation
   <= 1e-10.
4. Noiseless leakage: simulate full_circuit(r_max, dt) with AerSimulator
   statevector; sum of probabilities on non-physical codes <= 1e-14; and
   sampling 10000 shots yields zero flagged strings.
5. Trotter scaling: error of P_surv and sum E2 vs exact evolution at t fixed
   (t = r_max*dt) for r in {1,2,4,8,16}: fitted log-log slope in [-2.3,-1.7].
   (Use the ENCODED circuit for r in {1,2,4} and the matrix Strang product for
   {8,16} if circuit simulation is slow; document which.)
6. Write circuits/resources_logical.md: table of 2q count and 2q depth per
   group, per Strang step, per full circuit (r=1..3); export full_circuit(r)
   for r=0..3 as QPY to circuits/l12_r{r}.qpy and OpenQASM3 to
   circuits/l12_r{r}.qasm.

Acceptance: cd RUN && ../../.mamba/envs/su2zx/bin/python -m pytest
tests/test_l12.py -q green; the resources file and 8 exported circuit files
exist. Print a JSON summary {files, unitary_worst_dev, leakage_stat_probs,
strang_dev, trotter_slopes, resources_per_step}. Time box: 90 min. Runtime of
the test suite must stay < 10 min (cache expensive objects at module scope).
