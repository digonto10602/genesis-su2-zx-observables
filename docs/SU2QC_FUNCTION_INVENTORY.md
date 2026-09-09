# Python function and test inventory

Generated from the shipped source AST. Calls are syntactic expressions,
not a resolved runtime call graph. Full code is included at each linked path.
Test assertions describe checks; execution outcomes are in the JUnit/log files.

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/__init__.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/__init__.py)

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/__init__.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/__init__.py)

Circuit constructors for the L12 encoding.

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/export_l12.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/export_l12.py)

Write circuits/resources_logical.md and export L12 circuits (QPY + QASM3).

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py)

Exact gauge-invariant block unitaries and Strang circuits for L12 (G3).

Method (structure, not generic 12-qubit synthesis):
  * Each Hamiltonian group T in {D, h0..h3, B} is an 82x82 matrix from the
    verified route-1 Hamiltonian (term split checked exact by the dynamics
    lane).  Lifted to the 4096-dim code space it is E T E^dag: zero on every
    unphysical code, so exp(-i theta E T E^dag) is the identity on the
    complement -> gauge invariance by construction, zero leakage.
  * D is diagonal: a 12-qubit Diagonal gate (phases on the 82 codes, 1 else).
  * Each h_l and B act non-trivially on a SUPPORT of s < 12 qubits (found
    numerically as the qubits whose bits ever change or on which the matrix
    element depends); the lifted operator factorizes as U_s (x) I on the rest
    when all elements depend only on the support bits.  For links whose
    Jordan-Wigner string crosses other vertices, the sign depends on the
    parity (a XOR b) of those vertices; the support then includes those
    (a,b) pairs.  U_s = expm(-i theta M_s) on 2^s dims (s <= 10), built as a
    UnitaryGate.  Exactness is verified by tests to 1e-12.
  * Strang step: D/2 . [h0,h2]/2 . [h1,h3]/2 . B . [h1,h3]/2 . [h0,h2]/2 . D/2
    (l0=(v0,v1), l2=(v3,v2) disjoint; l1=(v1,v2), l3=(v0,v3) disjoint).

Verification helpers avoid dense 4096x4096 operators: the circuit is applied
to statevectors on the 82 codes with Aer/Statevector, and compared with the
exact 82-dim propagator.

### `params(g2=None, m=None)` — line 46

Direct call expressions: `json.loads`, `p.exists`, `p.read_text`, `vals.update`

### `terms(g2, m)` — line 60

(basis, {group: 82x82 ndarray}) from the dynamics-lane exact split.

Direct call expressions: `_term_split`, `float`, `lru_cache`

### `code_index()` — line 69

Direct call expressions: `enumerate`, `lru_cache`, `physical_codes`

### `basis_to_code(basis)` — line 74

Direct call expressions: `encode`, `np.array`

### `_support(M, codes_of_basis)` — line 80

Minimal-ish qubit set S such that M[i,j] (including zeros) is a
function of the support bits of codes i and j only.  Greedy: start with
the bits that flip on any nonzero element, then add the single bit that
removes the most conflicts until none remain.

Direct call expressions: `S.add`, `abs`, `complex`, `enumerate`, `len`, `n_conflicts`, `np.abs`, `np.argwhere`, `np.array`, `range`, `set`, `sorted`, `sum`

### `local_matrix(M, codes_of_basis, S)` — line 126

2^|S| x 2^|S| Hermitian matrix acting on support S (sorted).

Direct call expressions: `L.conj`, `enumerate`, `len`, `np.abs`, `np.argwhere`, `np.max`, `np.zeros`, `sum`

### `supports(g2, m)` — line 139

Direct call expressions: `_support`, `basis_to_code`, `lru_cache`, `terms`

### `unitary(group, theta, g2, m)` — line 148

12-qubit circuit for exp(-i theta E T_group E^dag).

Direct call expressions: `Diagonal`, `QuantumCircuit`, `UnitaryGate`, `basis_to_code`, `expm`, `local_matrix`, `lru_cache`, `np.diag`, `np.exp`, `np.ones`, `np.real`, `qc.append`, `range`, `supports`, `terms`

### `strang_step(dt, g2, m)` — line 165

Direct call expressions: `QuantumCircuit`, `float`, `qc.compose`, `unitary`

### `prep_stretched(qc=None)` — line 175

Direct call expressions: `QuantumCircuit`, `encode`, `qc.x`, `range`

### `full_circuit(r, dt=None, g2=None, m=None, merge_D=True)` — line 184

Direct call expressions: `float`, `params`, `prep_stretched`, `qc.compose`, `range`, `strang_step`, `unitary`

### `exact_strang_matrix(dt, g2, m)` — line 209

Exact matrix of ONE Strang step in the circuit's group ordering:
D/2 . h0/2 . h2/2 . h1/2 . h3/2 . B . h3/2 . h1/2 . h2/2 . h0/2 . D/2
(h0,h2 commute; h1,h3 commute).

Direct call expressions: `expm`, `reversed`, `terms`

### `circuit_state(qc)` — line 225

Statevector (4096) of a circuit from |0...0>.

Direct call expressions: `Statevector`

### `to_basis(vec4096, basis)` — line 230

Direct call expressions: `basis_to_code`

### `leakage_prob(vec4096)` — line 235

Direct call expressions: `code_index`, `float`, `np.abs`, `np.ones`, `np.sum`

### `resources(circ)` — line 244

Direct call expressions: `int`, `sum`, `t.depth`, `transpile`

### `n_conflicts(S)` — line 92

Direct call expressions: `abs`, `complex`, `enumerate`, `np.array`, `range`, `sorted`, `sum`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py)

Structured synthesis of the L12 block unitaries.

The implementation deliberately keeps the code-space structure visible: the
small connected components of each local matrix are synthesized independently
and the diagonal term is a degree-three phase polynomial.

### `_local_patterns(codes, support)` — line 26

Direct call expressions: `enumerate`, `sum`

### `_gray_map(x, y, target, n)` — line 30

CNOT sequence making x,y differ only on target (self-inverse).

Direct call expressions: `range`

### `_mapped_pattern(p, cnots, target)` — line 35

Direct call expressions: none

### `_minimal_controls(x, y, target, cnots, physical)` — line 42

Smallest control set (exhaustive over subsets, |support| <= 8) such
that no OTHER physical local pattern matches the selected pattern on
the controls after the Gray-code CNOT conjugation.

Direct call expressions: `_mapped_pattern`, `all`, `any`, `combinations`, `len`, `max`, `max(physical).bit_length`, `range`, `sorted`

### `_mc_single_qubit(u, k)` — line 59

Multi-controlled single-qubit unitary as a controlled UGate (ZYZ
angles + phase), which qiskit synthesizes far more cheaply than a
controlled generic UnitaryGate.

Direct call expressions: `OneQubitEulerDecomposer`, `OneQubitEulerDecomposer('U').angles_and_phase`, `QuantumCircuit`, `UGate`, `abs`, `g.control`, `np.asarray`, `sub.append`, `sub.to_gate`, `sub.to_gate().control`

### `_two_level(qc, support, x, y, mat, physical)` — line 78

Apply a 2x2 unitary on local patterns x,y using a Gray path.

Direct call expressions: `ValueError`, `_gray_map`, `_mc_single_qubit`, `_minimal_controls`, `abs`, `len`, `np.arctan2`, `np.asarray`, `qc.append`, `qc.cx`, `qc.mcrx`, `qc.rx`, `qc.x`, `range`, `reversed`

### `_givens_decomposition(v)` — line 125

Return (diagonal, factors) with v=factors[0]...D.

Direct call expressions: `ArithmeticError`, `abs`, `factors.append`, `np.abs`, `np.array`, `np.conj`, `np.diag`, `np.eye`, `np.hypot`, `np.ix_`, `np.max`

### `_phase_on_pattern(qc, support, pattern, phase, physical)` — line 145

Direct call expressions: `PhaseGate`, `PhaseGate(phase).control`, `abs`, `all`, `any`, `controls.remove`, `len`, `list`, `qc.append`, `qc.x`, `range`, `reversed`

### `_component_patterns(L)` — line 171

Direct call expressions: `comp.add`, `int`, `len`, `np.abs`, `np.flatnonzero`, `out.append`, `range`, `set`, `sorted`, `stack.append`, `stack.pop`, `todo.pop`, `todo.remove`

### `_synth_local(group, theta, g2, m)` — line 187

Direct call expressions: `QuantumCircuit`, `ValueError`, `_component_patterns`, `_givens_decomposition`, `_local_patterns`, `_phase_on_pattern`, `_two_level`, `enumerate`, `expm`, `float`, `g.conj`, `len`, `np.angle`, `np.ix_`, `physical_codes`, `reversed`, `sl.basis_to_code`, `sl.local_matrix`, `sl.supports`, `sl.terms`

### `_bit_polynomial(g2, m)` — line 213

Direct call expressions: `float`, `p.get`, `range`, `sorted`, `tuple`

### `_diagonal(qc, theta, g2, m)` — line 226

Direct call expressions: `_bit_polynomial`, `_bit_polynomial(g2, m).items`, `abs`, `len`, `qc.cx`, `qc.rz`, `range`, `reversed`, `tuple`, `zpoly.get`, `zpoly.items`, `zpoly.pop`

### `synth_unitary(group, theta, g2, m)` — line 249

Synthesize one exact L12 block using only one-qubit and controlled gates.

Direct call expressions: `QuantumCircuit`, `ValueError`, `_diagonal`, `_synth_local`, `float`, `lru_cache`, `qc.compose`

### `synth_strang_step(dt, g2, m)` — line 262

Direct call expressions: `QuantumCircuit`, `qc.compose`, `synth_unitary`

### `synth_full_circuit(r, dt=None, g2=None, m=None, merge_D=True)` — line 271

Direct call expressions: `qc.compose`, `range`, `sl.params`, `sl.prep_stretched`, `synth_strang_step`, `synth_unitary`

### `_resources(circ)` — line 290

Direct call expressions: `sum`, `t.depth`, `transpile`

### `write_resources(path='circuits/resources_synth.md')` — line 296

Direct call expressions: `'\n'.join`, `Path`, `Path(path).write_text`, `_resources`, `range`, `rows.append`, `sl.params`, `synth_full_circuit`, `synth_strang_step`, `synth_unitary`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/__init__.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/__init__.py)

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py)

Phase 4: route logical L12 circuits to a Heron-class target and verify.

route(circ, backend, opt=3, seed=7) -> (isa_circ, layout_info)
routed_equivalence(logical, isa) -> 1 - |<psi_routed|psi_logical>| including
      the final layout permutation (statevector on the 12 logical qubits).
routed_resources(isa) -> dict(n_2q, depth_2q, depth)
pyzx_tp(circ) -> circuit after the monograph's topology-preserving PyZX pass
      (reused from the repo's src/su2zx/compiler_study.py if importable).

### `fake_heron()` — line 30

Direct call expressions: `FakeTorino`

### `route(circ, backend=None, opt=3, seed=7, initial_layout=None)` — line 35

Direct call expressions: `fake_heron`, `int`, `isa.layout.final_index_layout`, `list`, `range`, `transpile`

### `routed_resources(isa)` — line 50

Direct call expressions: `int`, `isa.depth`, `sum`

### `routed_equivalence(logical, isa)` — line 58

1 - |<routed|logical>| with the routed state pulled back through
final_index_layout to the logical qubit order (statevector, no measure).

Direct call expressions: `QuantumCircuit`, `Statevector`, `abs`, `enumerate`, `float`, `int`, `isa.find_bit`, `isa.layout.final_index_layout`, `len`, `np.transpose`, `np.transpose(psi_r, rest + perm_axes).reshape`, `np.vdot`, `psi_r.reshape`, `range`, `set`, `small.append`, `sorted`

### `pyzx_pass(circ, strategy='basic')` — line 88

The monograph's PyZX pipeline (repo src/su2zx/core.py) with its dense
12-qubit Operator equivalence check replaced by a statevector check on
the 82 physical codes (done by the caller via routed_equivalence-style
comparison). strategy: 'basic' (topology-preserving), 'full_reduce'.

Direct call expressions: `ValueError`, `cand.to_qasm`, `g.copy`, `qasm2.dumps`, `qasm2.loads`, `zx.Circuit.from_qasm`, `zx.extract.extract_circuit`, `zx.extract.extract_circuit(g.copy(), up_to_perm=False, quiet=True).to_basic_gates`, `zx.optimize.basic_optimization`, `zx.simplify.full_reduce`, `zxc.copy`, `zxc.to_graph`

### `state_equivalence(a, b)` — line 113

1 - |<a|b>| for two same-width circuits from |0>.

Direct call expressions: `Statevector`, `abs`, `float`, `np.vdot`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py)

Phase 4 production: compile, route, PyZX comparison, twin run, decision inputs.

Writes compile/resources_routed.{md,json}, compile/layout.json,
compile/twin_check.json, analysis/tables/twin_timeseries.csv.

### `n2(c)` — line 29

Direct call expressions: `sum`

### `d2(c)` — line 33

Direct call expressions: `c.depth`, `int`

### `_zx(strategy)` — line 48

Direct call expressions: `rt.pyzx_pass`, `transpile`

### `f(c)` — line 49

Direct call expressions: `rt.pyzx_pass`, `transpile`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py)

FROZEN conventions for the SU(2) single-plaquette patch with dynamical matter.

Frozen at G0 of run section8_v0.5.0_20260907T0628Z. DO NOT EDIT.
Both Hamiltonian routes, all encodings, circuits, and analysis import from here
and ONLY from here. Any objection goes to physics/conventions_objection_*.md.

Model (Section 5.1 of the v0.5.0 prompt):
  Lattice units a = 1. One square plaquette, open boundaries.
  H = (g^2/2) sum_l E_l^2
    + m sum_v (-1)^{x_v+y_v} psi\dagger_v psi_v
    + (1/2) sum_l ( eta_l psi\dagger_{s(l)} U_l psi_{t(l)} + h.c. )
    - (1/(2 g^2)) Tr( U_box + U_box\dagger )
  U_box = U_l1 U_l2 U_l3\dagger U_l4\dagger   (counter-clockwise v1->v2->v3->v4->v1)
  E^2 = j(j+1) per link. Truncation j in {0, 1/2} (hardcore gluon); j_max = 1
  is built too for the truncation-error statement.

### `parity(v: int)` — line 23

(-1)^{x+y} for vertex index v in 0..3.  v1,v3 even (+1); v2,v4 odd (-1).

Direct call expressions: none

### `eta(l: int)` — line 37

Staggered phase of link l: eta_x = 1, eta_y = (-1)^x  (x of the source).

Direct call expressions: none

### `charge(v: int, n: int)` — line 55

Local charge relative to the staggered vacuum: q_v = n_v - n_vac(v).

Direct call expressions: none

### `casimir(j: float)` — line 67

SU(2) quadratic Casimir j(j+1).

Direct call expressions: none

### `coupling_electric(g2: float)` — line 77

Coefficient of sum_l E_l^2.

Direct call expressions: none

### `coupling_magnetic(g2: float)` — line 81

Coefficient of -Tr(U_box + U_box^dag) (i.e. H_B = -c * Tr(...)).

Direct call expressions: none

### `tree_level_resonance(g2: float)` — line 89

Direct call expressions: none

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/__init__.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/__init__.py)

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/engine.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/engine.py)

Exact-dynamics engine for the 82-state (jmax=0.5) / 152-state (jmax=1) SU(2) plaquette.

evolve(H, psi0, times) -> array of states (dense expm on 82-dim; use scipy.linalg.expm
of -iH dt step matrix, cumulative).
self_check(g2, m, jmax, t_max) -> dict with expm_krylov_dev, energy_drift, N_drift.

### `evolve(H, psi0, times)` — line 15

Evolve psi0 under sparse H at times t (array).

Returns array of shape (len(times), dim) with state vectors at each time.
Uses dense expm of -i*H*dt per step (cumulative), since the Hilbert space
is small (82 or 152 dims).

Direct call expressions: `H.toarray`, `V.conj`, `eigh`, `np.asarray`, `np.asarray(psi0, dtype=complex).flatten`, `np.exp`, `np.linalg.norm`, `np.outer`

### `self_check(g2: float, m: float, jmax: float, t_max: float)` — line 35

Verify expm vs Krylov conservation.

Returns dict with:
  expm_krylov_dev: max ||psi_dense(t) - psi_krylov(t)||_inf over ~21 times on [0, t_max]
  energy_drift: max |<H>(t) - <H>(0)|
  N_drift: max |<N>(t) - <N>(0)|
Targets: <=1e-9, <=1e-10, <=1e-10.

Direct call expressions: `H.toarray`, `H.tocsc`, `abs`, `basis.index`, `build_hamiltonian`, `enumerate`, `expm`, `expm_multiply`, `float`, `np.abs`, `np.conj`, `np.linspace`, `np.max`, `np.real`, `np.sum`, `np.zeros`, `range`, `set`, `sum`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/run_g2.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/run_g2.py)

Run the full G2 production sequence and print a summary (OPS lane).

Operating point: g2 = 4.0, m = 3 g2/16 = 0.75 (tree-level resonance).
Rationale (physics/DISCREPANCIES.md): the W_bar-argmax estimator is
dominated by the BB-bar channel at small m and does not localize the
tree-level resonance; the breaking-time estimator argmin t_b does, at g2 >= 4
where the electric scale dominates hopping and the resonance is sharp.

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py)

Mass scan / resonance finder, truncation comparison, Trotter-window selector.

Rewritten by the OPS lane after the delegated builder timed out (partial file);
classification bugs fixed: P_surv is the EXACT charge pattern (+1,-1,0,0), not
a sorted-|q| match.

### `_idx(basis, label)` — line 26

Direct call expressions: `KeyError`, `enumerate`

### `_classify(basis)` — line 33

Per-state channel masks: surv, meson, BBbar, other (within N=4).

Direct call expressions: `abs`, `all`, `any`, `enumerate`, `len`, `np.zeros`, `range`, `sum`, `tuple`

### `_diagnostics(basis)` — line 53

Direct call expressions: `cv.casimir`, `np.array`, `range`

### `channel_probs(basis, states)` — line 59

Direct call expressions: `_classify`, `np.abs`

### `mass_scan(g2_values=(1.0, 2.0, 4.0, 8.0), n_m=25, t_window=(0.0, 40.0), jmax=0.5)` — line 67

Scan m in [0, g2/2] for each g2. Two resonance estimators are recorded:
argmax of W_bar (prompt criterion 2) and argmin of t_b (breaking time);
see physics/DISCREPANCIES.md for why they differ at strong coupling.

Direct call expressions: `','.join`, `_idx`, `build_hamiltonian`, `channel_probs`, `evolve`, `fh.write`, `float`, `int`, `json.dump`, `len`, `list`, `np.argmax`, `np.argmin`, `np.linspace`, `np.trapezoid`, `np.where`, `np.zeros`, `open`, `os.makedirs`, `os.path.join`, `rows.append`, `str`, `tbs.append`, `wbar.append`

### `timeseries_at(g2, m, jmax=0.5, times=None, tag='exact_timeseries')` — line 113

Direct call expressions: `','.join`, `H.toarray`, `_diagnostics`, `_figures`, `_idx`, `build_hamiltonian`, `channel_probs`, `enumerate`, `evolve`, `fh.write`, `np.abs`, `np.einsum`, `np.linspace`, `np.real`, `np.zeros`, `open`, `os.makedirs`, `os.path.join`, `states.conj`

### `_figures(times, ps, pm, pb, po, e2, nv, tag)` — line 144

Direct call expressions: `ax.legend`, `ax.plot`, `ax.set_title`, `ax.set_xlabel`, `ax.set_ylabel`, `e2.sum`, `fig.savefig`, `fig.tight_layout`, `matplotlib.use`, `os.makedirs`, `os.path.join`, `plt.close`, `plt.subplots`, `range`

### `truncation(g2, m)` — line 177

Max channel-probability shift jmax=1 vs jmax=1/2 over t in [0,12].

Direct call expressions: `_idx`, `build_hamiltonian`, `channel_probs`, `evolve`, `fh.write`, `float`, `json.dump`, `np.abs`, `np.linspace`, `np.max`, `np.stack`, `np.zeros`, `open`, `os.path.join`

### `_term_split(g2, m, jmax=0.5)` — line 208

Split H into D (diagonal), h_l (per-link hopping), B (magnetic).

Direct call expressions: `H.toarray`, `Hn.toarray`, `abs`, `build_hamiltonian`, `build_hamiltonian_no_magnetic`, `enumerate`, `hs.append`, `len`, `np.abs`, `np.diag`, `np.max`, `np.zeros_like`, `range`, `set`, `sum`

### `strang_step_matrix(D, hs, B, dt)` — line 236

One Strang step in the CIRCUIT layer ordering (prompt §5.5):
D/2 · [h0,h2]/2 · [h1,h3]/2 · B · [h1,h3]/2 · [h0,h2]/2 · D/2.

Direct call expressions: `expm`, `reversed`

### `strang_error(g2, m, dt, r, jmax=0.5)` — line 250

Observable error of r Strang steps vs exact at t = r dt.

Direct call expressions: `_classify`, `_diagnostics`, `_idx`, `_term_split`, `abs`, `expm`, `float`, `max`, `np.abs`, `np.max`, `np.zeros`, `psi0.copy`, `range`, `strang_step_matrix`

### `select_window(g2=1.0, m=None, jmax=0.5)` — line 269

Choose (g2, m, dt, r_max) per prompt Phase-2 criterion 5.

Direct call expressions: `_idx`, `build_hamiltonian`, `channel_probs`, `evolve`, `float`, `json.dump`, `json.load`, `np.array`, `np.zeros`, `open`, `os.path.join`, `str`, `strang_error`

### `verify_window(w)` — line 306

Recompute the window criteria (gate G2 calls this).

Direct call expressions: `_idx`, `build_hamiltonian`, `channel_probs`, `evolve`, `float`, `np.array`, `np.zeros`, `strang_error`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/__init__.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/__init__.py)

Encodings used by the compact SU(2) circuit experiments.

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py)

The 12-qubit, three-bits-per-vertex L12 encoding.

Qubit ``3*v,3*v+1,3*v+2`` is respectively (first link, second link,
matter).  Integers use q0 as the least significant bit; displayed Qiskit
strings consequently read q11 ... q0.

### `_bit(code, q)` — line 15

Direct call expressions: `int`

### `_maps()` — line 19

Direct call expressions: `enumerate`, `enumerate_basis`, `int`, `lru_cache`, `round`

### `encode(label)` — line 33

Encode a canonical route-spinnet basis label as a 12-bit integer.

Direct call expressions: `ValueError`, `_maps`, `_maps().items`

### `decode(bits)` — line 40

Decode an integer (or a q11...q0 bit string) or return ``None``.

Direct call expressions: `_maps`, `_maps().get`, `any`, `int`, `isinstance`, `len`

### `physical_codes()` — line 50

Direct call expressions: `_maps`, `sorted`

### `leakage_flags(bits)` — line 53

Return vertex leakage and four endpoint-consistency flags.

Direct call expressions: `_bit`, `bool`, `enumerate`, `int`, `isinstance`, `link.append`, `range`, `tuple`

### `is_physical(bits)` — line 67

Direct call expressions: `any`, `leakage_flags`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/__init__.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/__init__.py)

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/compare.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/compare.py)

Verifier-owned comparison of the two independent Hamiltonian routes (G1).

Basis-independent checks:
  * sorted spectra at >= 5 coupling points (incl. m = 0),
  * observable time series from the stretched string on t in [0, 10].
Owned by the VERIFY lane; neither route builder edits this file.

### `_get_routes()` — line 34

Direct call expressions: none

### `_norm_label(label)` — line 40

Direct call expressions: `float`, `int`, `tuple`

### `spectra_comparison(jmax=0.5, points=COUPLING_POINTS)` — line 45

Max relative deviation of sorted spectra between routes per point.

Direct call expressions: `_get_routes`, `eigh`, `float`, `max`, `np.abs`, `np.max`, `np.sort`, `out1[0].toarray`, `out2[0].toarray`, `r1.build_hamiltonian`, `r2.build_hamiltonian`, `rows.append`

### `_observables(route_mod, H, basis, psi0_index, times)` — line 63

Time series of P_surv, n_v, E2_l from basis state psi0_index.

Direct call expressions: `(p @ e2).tolist`, `(p @ nmat).tolist`, `cv.casimir`, `cv.charge`, `enumerate`, `expm`, `float`, `int`, `np.abs`, `np.all`, `np.array`, `np.zeros`, `range`, `series.append`

### `time_series_comparison(g2=1.0, m=0.1875, jmax=0.5, times=TIMES)` — line 88

Max abs deviation of stretched-string observables between routes.

Direct call expressions: `_get_routes`, `_norm_label`, `_observables`, `abs`, `enumerate`, `float`, `len`, `max`, `np.abs`, `np.array`, `np.max`, `out1[0].toarray`, `out2[0].toarray`, `r1.build_hamiltonian`, `r2.build_hamiltonian`, `zip`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py)

Verifier-owned limit tests for gate G1.

* pure_electric_check: g2 -> infinity degeneracy pattern 16,16,18,16,16.
* frozen_matter_check: m -> infinity 2x2 block equals the monograph's
  one-plaquette H~1 after a documented normalization reconciliation.
* magnetic_off_check: B = 0 spectrum equals an independently constructed
  4-site periodic 1+1D SU(2) chain (built in limits_1d.py by a separate
  builder; falls back to a cross-route B-off comparison if absent, and
  reports which was used).

### `pure_electric_check(g2_big=1000000.0)` — line 28

Spectrum at g2 -> inf, m = 0: electric levels with k-degeneracies.

Direct call expressions: `H.toarray`, `bool`, `eigh`, `float`, `int`, `np.abs`, `np.max`, `np.rint`, `np.rint(evals / unit).astype`, `np.sort`, `np.sum`, `r1.build_hamiltonian`, `range`

### `frozen_matter_check(tol=1e-09)` — line 46

m -> inf: the 2-state block (links all-0 / all-1/2, matter at vacuum)
equals the monograph's one-plaquette H~1 after reconciliation.

Monograph (repo core.py, n=1): H~1 = 1.5 I - 1.5 Z - 2x X, x = 2/g^4,
H~ = 2H/g^2  =>  H1 = (g2/2)(1.5 I - 1.5 Z) - (2/g2) X  acting on
(|0000>, |hhhh>) with Z|0000> = +|0000>.
Patch H on the same 2 states: diag(0, 4*(g2/2)*(3/4)) = diag(0, 1.5 g2)
from the electric term, mass term = m*const (equal on both, shift),
magnetic term couples them with element -(1/(2g2)) * w where w is the
plaquette vertex-factor product; expected |w| = 2 (Tr over the two color
paths), giving off-diagonal -1/g2... The reconciliation (documented in
physics/conventions_reconciliation.md) fixes the mapping:
  H_patch|_2x2 = a I + b (H1_monograph) with b = 1 expected up to the
  magnetic normalization ratio r = offdiag_patch / (-2/g2).
This check extracts the effective 2x2 block at large m numerically via
2nd-order perturbation (large-m suppresses matter excitations) by exact
projection: keep the two basis states, project H (matter untouched by B,
hopping leaves the block at O(1/m)).

Direct call expressions: `H.toarray`, `abs`, `bool`, `enumerate`, `float`, `int`, `len`, `max`, `np.abs`, `np.array`, `np.diag`, `np.eye`, `np.imag`, `np.ix_`, `np.max`, `np.real`, `r1.build_hamiltonian`, `tuple`

### `magnetic_off_check(tol=1e-10)` — line 102

B = 0 spectrum vs an independent periodic 1D 4-site SU(2) chain.

Direct call expressions: `H.toarray`, `H2.toarray`, `eigh`, `float`, `hasattr`, `limits_1d.chain_spectrum`, `max`, `np.abs`, `np.max`, `np.sort`, `r1.build_hamiltonian_no_magnetic`, `r2.build_hamiltonian_no_magnetic`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py)

Route 2: redundant Kogut-Susskind space followed by Gauss-law projection.

Construction:
  * Each link is a truncated rigid rotor |j, mL, mR> (dim 5 at jmax=1/2).
  * Matter: 8 Jordan-Wigner fermionic modes in the frozen order (v-major).
  * The physical basis is built from vertex-local Gauss singlets (codex-built,
    verified: dims 82/152, sector dims 2,20,38,20,2, electric clusters).
  * H is built on the FULL redundant space (electric, mass, 4 hoppings with JW
    strings, plaquette trace) and projected: H_phys = P^dag H_red P.
  * The U matrix-element convention (which color index is conjugated) is
    selected NUMERICALLY as the unique variant that makes [G^a_v, H_hop] = 0;
    the choice is recorded in U_CONVENTION after first build.

Limitation (recorded in run/DECISIONS.md): at jmax=1 only the kernel dimension
(152) is computed by this route; the projected H_1 matrix is route-1-only
(redundant dim 14^4*256 ~ 9.8M exceeds the night's memory/time budget).
Route agreement is gated at jmax=1/2 per the run prompt (G1 criterion 3).

### `_spins(jmax)` — line 33

Direct call expressions: `int`, `range`, `tuple`

### `_link_states(jmax)` — line 37

Direct call expressions: `_spins`, `np.arange`

### `_spin(j)` — line 43

Direct call expressions: `enumerate`, `len`, `np.arange`, `np.diag`, `np.diag(m).astype`, `np.sqrt`, `np.zeros`, `p.T.conj`

### `_cg(j, m, a, jp)` — line 52

CG(j,m;1/2,a|jp,m+a), a = +-1/2, closed forms.

Direct call expressions: `abs`, `np.sqrt`

### `_local_fermions()` — line 64

Direct call expressions: `aa.append`, `aa[a].conj`, `np.array`, `np.diag`, `np.zeros`, `out.append`, `range`, `sum`

### `_local_singlet(ja, jb, n, signs)` — line 84

Direct call expressions: `_local_fermions`, `_spin`, `b.bit_count`, `eigh`, `gs.append`, `int`, `len`, `np.eye`, `np.ix_`, `np.kron`, `np.where`, `np.zeros`, `range`, `sum`, `x.reshape`

### `_physical_basis(jmax)` — line 104

Direct call expressions: `_link_states`, `_local_singlet`, `_spins`, `abs`, `any`, `col.conj`, `col.multiply`, `col.multiply(col.conj()).sum`, `cols.append`, `csr_matrix`, `entries.get`, `entries.values`, `enumerate`, `float`, `hstack`, `int`, `itertools.product`, `labels.append`, `len`, `li.append`, `np.arange`, `np.argwhere`, `np.fromiter`, `np.prod`, `np.sqrt`, `np.zeros`, `range`, `states.index`, `tuple`

### `_basis(jmax)` — line 158

Direct call expressions: `_physical_basis`, `float`

### `kernel_dimension(jmax)` — line 165

Direct call expressions: `_basis`, `len`

### `_link_JLR(jmax)` — line 175

(JL[a], JR[a]) dl x dl sparse, a = x,y,z.

Direct call expressions: `_link_states`, `_spin`, `_spins`, `abs`, `csr_matrix`, `enumerate`, `len`, `np.arange`, `np.zeros`, `range`

### `_link_U(jmax, conjL, conjR)` — line 196

U[(alpha,beta)] dl x dl sparse; conjX conjugates that color index.

Direct call expressions: `_cg`, `_link_states`, `_spins`, `abs`, `csr_matrix`, `enumerate`, `len`, `max`, `np.sqrt`, `np.zeros`, `round`

### `_fermion_ops()` — line 229

Global JW annihilation ops a_k on the 256-dim space, k = 2v + c.

Direct call expressions: `bin`, `bin(fb & (1 << k) - 1).count`, `cols.append`, `csr_matrix`, `data.append`, `ops.append`, `range`, `rows.append`

### `_embed_link(op, l, dl, dm)` — line 245

kron: identity on links < l, op on link l, identity after, identity fermions.

Direct call expressions: `identity`, `kron`

### `_embed_links_fermi(link_ops, fermi_op, dl, dm)` — line 255

link_ops: dict l -> op (missing = identity); fermi_op on 256.

Direct call expressions: `identity`, `kron`, `link_ops.get`, `range`

### `_gauss_ops(jmax)` — line 269

G[a][v] on the full redundant space.

Direct call expressions: `_embed_link`, `_embed_links_fermi`, `_fermion_ops`, `_link_JLR`, `_link_states`, `abs`, `csr_matrix`, `ends.append`, `enumerate`, `f[2 * v + c1].conj`, `f[2 * v + c1].conj().T.tocsr`, `len`, `range`

### `_c_of_alpha(al)` — line 300

Direct call expressions: none

### `_build_terms(jmax, conjL, conjR)` — line 304

All Hamiltonian term groups on the full redundant space (coefficient-free
where possible): returns dict with electric, mass, hop_l (l=0..3, WITHOUT
the 1/2 eta prefactor), trU (the plaquette trace, not Hermitized).

Direct call expressions: `U.items`, `_c_of_alpha`, `_embed_link`, `_embed_links_fermi`, `_fermion_ops`, `_link_U`, `_link_states`, `casimir`, `diags`, `enumerate`, `fpart.tocsr`, `h.conj`, `h.conj().T.tocsr`, `hops.append`, `identity`, `len`, `mass_f.tocsr`, `range`, `sum`, `v.conj`, `v.conj().T.tocsr`, `x.conj`, `x.conj().T.tocsr`

### `_select_convention(jmax=0.5)` — line 353

Pick (conjL, conjR) as the variant with vanishing [G, hop] and [G, trU].

Direct call expressions: `_build_terms`, `_gauss_ops`, `float`, `max`, `np.abs`, `np.max`, `range`

### `_terms(jmax)` — line 383

Direct call expressions: `_select_convention`, `float`

### `gauss_commutator_norms(jmax)` — line 390

Max over v, a of max-abs entry of [G^a_v, H_term], per term group.

Direct call expressions: `_gauss_ops`, `_terms`, `float`, `max`, `named.items`, `np.abs`, `np.max`, `range`, `terms['trU'].conj`, `terms['trU'].conj().T.tocsr`

### `_h_red(g2, m, jmax, magnetic=True)` — line 412

Direct call expressions: `_terms`, `coupling_electric`, `coupling_magnetic`, `range`, `t['trU'].conj`, `t['trU'].conj().T.tocsr`

### `build_hamiltonian(g2, m, jmax)` — line 422

Direct call expressions: `((H + H.conj().T) / 2).tocsr`, `(P.conj().T @ _h_red(g2, m, jmax) @ P).tocsr`, `H.conj`, `NotImplementedError`, `P.conj`, `_basis`, `_h_red`, `float`

### `build_hamiltonian_no_magnetic(g2, m, jmax)` — line 434

Direct call expressions: `((H + H.conj().T) / 2).tocsr`, `(P.conj().T @ _h_red(g2, m, jmax, magnetic=False) @ P).tocsr`, `H.conj`, `NotImplementedError`, `P.conj`, `_basis`, `_h_red`, `float`

### `get_state(label, basis_labels)` — line 444

Direct call expressions: `basis_labels.index`

### `_obs(labels)` — line 450

Direct call expressions: `abs`, `all`, `any`, `casimir`, `diags`, `int`, `len`, `range`, `sum`, `tuple`

### `E2_link(l, basis_labels)` — line 466

Direct call expressions: `_obs`

### `n_op(v, basis_labels)` — line 470

Direct call expressions: `_obs`

### `N_total(basis_labels)` — line 474

Direct call expressions: `_obs`

### `P_surv(basis_labels)` — line 478

Direct call expressions: `_obs`

### `P_meson(basis_labels)` — line 482

Direct call expressions: `_obs`

### `P_BBbar(basis_labels)` — line 486

Direct call expressions: `_obs`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py)

Route 1: analytic spin-network / dressed-site Hamiltonian for SU(2) single plaquette
with dynamical two-color staggered fermions.

Basis: ((j1,j2,j3,j4), (n1,n2,n3,n4), tag) where:
  j_l in {0, 1/2} (jmax=0.5) or {0, 1/2, 1} (jmax=1) as floats
  n_v in {0,1,2} with gauge-invariant constraints per vertex
  tag = 0 (always for 2-valent vertices)

Gauge invariance at each 2-valent vertex with incident link spins (j_a, j_b) and matter n_v:
  - if j_a == j_b:     n_v in {0, 2}  (vacuum or baryon)
  - if |j_a - j_b| == 1/2: n_v = 1  (doublet)
  - if |j_a - j_b| == 1:     NOT allowed (projected out, only jmax=1)

Hamiltonian: H = H_elec + H_mass + H_hop + H_mag

eta = (+1, -1, +1, +1) per link l1..l4.
Staggered vacuum: n_vac = (0,2,0,2).  Vertices v1..v4 at (0,0),(1,0),(1,1),(0,1).
Links: l1:v1->v2, l2:v2->v3, l3:v4->v3, l4:v1->v4.
Plaquette: U_box = U_l1 U_l2 U_l3^dag U_l4^dag (counter-clockwise v1->v2->v3->v4->v1).

### `_cg_half(j: float, m: float, s: int, jp: float, mp: float)` — line 49

Closed-form CG(j,m;1/2,s/2|jp,mp), with no symbolic dependency.

Direct call expressions: `abs`, `max`, `np.sqrt`

### `_mvalues(j: float)` — line 61

Direct call expressions: `int`, `range`, `round`, `tuple`

### `_vertex_state(ja: float, jb: float, n: int)` — line 65

Unit-norm invariant vertex state as an array (da, db, 4).

All three indices are state-type (each transforms with +J); the tensor is
the unique singlet of V_ja x V_jb x V_matter(n):
  n=0/2 (needs ja==jb): metric tensor (-1)^(ja-ma) delta_{ma,-mb}/sqrt(2ja+1)
    with fermion Fock f=0 (n=0) or f=3 (n=2);
  n=1 (needs |ja-jb|=1/2): T[ma,mb,c] = (-1)^(ja+ma) *
    CG(jb, mb; 1/2, s_c | ja, -ma), s_c=+1 for c=0, -1 for c=1;
    Fock f = 1 (c=0 occupied) or 2 (c=1 occupied); unit-normalized.
Fock basis: f = n_c0 + 2 n_c1.

Direct call expressions: `_cg_half`, `_mvalues`, `abs`, `enumerate`, `int`, `len`, `np.sqrt`, `np.sum`, `np.zeros`, `round`

### `_sigma_plus(c: int)` — line 102

Direct call expressions: `np.zeros`, `range`

### `_sigma_minus(c: int)` — line 110

Direct call expressions: `_sigma_plus`

### `_zc(c: int)` — line 114

Direct call expressions: `np.diag`, `range`

### `_end_insertion(j: float, jp: float, c: int, end: str, dagger: bool=False)` — line 121

Matrix (2jp+1)x(2j+1) taking the link-end m index from j to jp.

L end (source vertex): entry[m',m] = sign_c * CG(j,m;1/2,-s_c|jp,m')
R end (target vertex): entry[m',m] = CG(j,m;1/2,+s_c|jp,m')
with s_c = +1 for c=0, -1 for c=1; sign_c = +1 for c=0, -1 for c=1.
The sqrt((2j+1)/(2j'+1)) Wigner prefactor is NOT included here; it is
applied once per link in the amplitude assembly.
dagger=True returns the conjugate-transposed insertion of the reverse
transition (for U^dagger links).

Direct call expressions: `_cg_half`, `_end_insertion`, `_mvalues`, `enumerate`, `len`, `np.zeros`

### `_vertex_overlap2(ja, jb, n_old, ja2, jb2, n_new, ins_a=None, ins_b=None, fop=None)` — line 153

<T'(ja2,jb2,n_new)| (ins_a x ins_b x fop) |T(ja,jb,n_old)>.

Direct call expressions: `_mvalues`, `_vertex_state`, `float`, `len`, `np.einsum`, `np.eye`

### `_fermion_sign(source: int, target: int, n: tuple[int, int, int, int])` — line 165

Parity of the middle sites for psi^dag_source ... psi_target (v-ordered).

Direct call expressions: `range`, `sum`

### `_check_vertex_gauge_invariant(n_vals: tuple[int, int, int, int], j_tuple: tuple[float, float, float, float])` — line 173

Check whether a full matter assignment satisfies all 4 vertex gauge-invariants.

For vertex v with incident link spins (j_a, j_b):
  - j_a == j_b     => n_v in {0, 2}
  - |j_a - j_b| == 1/2 => n_v = 1
  - |j_a - j_b| == 1   => forbidden (projected out)

Direct call expressions: `abs`

### `enumerate_basis(jmax: float)` — line 234

Return list of basis labels ((j1,j2,j3,j4), (n1,n2,n3,n4), 0) for the given jmax.

The basis is constructed by iterating all allowed link spins and then, for each,
all matter assignments that satisfy the 4 vertex constraints.

Direct call expressions: `ValueError`, `_check_vertex_gauge_invariant`, `abs`, `basis.append`

### `_electric_diag(j_tuple: tuple[float, float, float, float], g2: float)` — line 317

Electric term: (g2/2) * sum_l j_l(j_l+1).  Diagonal in the basis.

Direct call expressions: `cv.casimir`, `sum`

### `_mass_diag(n_tuple: tuple[int, int, int, int], m: float)` — line 322

Mass term: m * sum_v parity_v n_v.  Diagonal in the basis.

Direct call expressions: `range`, `sum`

### `_hopping_matrix_element(j_from: tuple[float, float, float, float], n_from: tuple[int, int, int, int], link_idx: int, j_to: tuple[float, float, float, float], n_to: tuple[int, int, int, int])` — line 329

Matrix element <to| (1/2) eta_l psi^dag_s U_l psi_t |from> for one link.

Only the forward direction (n_s + 1, n_t - 1) is computed; the caller adds
the h.c. partner into the transposed entry.

Direct call expressions: `_end_insertion`, `_fermion_sign`, `_site_annihilate`, `_site_create`, `_vertex_overlap_at`, `abs`, `complex`, `np.sqrt`, `range`

### `_site_create(c: int, side: str)` — line 370

Site creation op for color c with the JW Z-string on the given side.

Direct call expressions: `_sigma_plus`, `_zc`, `range`

### `_site_annihilate(c: int, side: str)` — line 379

Direct call expressions: `_site_create`

### `_vertex_overlap_at(v, j_from, n_from, j_to, n_to, ins_by_link, fop=None)` — line 383

Direct call expressions: `_vertex_overlap2`, `ins_by_link.get`

### `_magnetic_matrix_element(j_from, n, j_to)` — line 390

<to| Tr(U_l1 U_l2 U_l3^dag U_l4^dag) |from> by four local contractions.

Color loop: sum_{abcd} U0^{ab} U1^{bc} (U2^dag)^{cd} (U3^dag)^{da}; per
vertex the two incident link-end insertions carry the loop colors:
  v1: l4(L,a,dag), l1(L,a) | v2: l1(R,b), l2(L,b)
  v3: l2(R,c), l3(R,c,dag) | v4: l3(L,d,dag), l4(R,d,dag)
Wigner prefactor per link: sqrt((2j+1)/(2j'+1)) for plain links,
sqrt((2j'+1)/(2j+1)) for daggered links.

Direct call expressions: `_end_insertion`, `_vertex_overlap_at`, `abs`, `complex`, `np.sqrt`, `range`, `spec.items`

### `build_hamiltonian(g2: float, m: float, jmax: float)` — line 433

Build the full route-1 Hamiltonian for the single plaquette.

Returns (H_sparse, basis) where basis is the list of labels in the same order
as the matrix rows/cols.

Physics:
  H = H_elec + H_mass + H_hop + H_mag
  H_elec = (g2/2) sum_l j_l(j_l+1)                     (diagonal)
  H_mass = m sum_v parity_v n_v                          (diagonal, parity=+ - + -)
  H_hop  = (1/2) sum_l ( eta_l psi^dag_{s(l)} U_l psi_{t(l)} + h.c. )  (off-diagonal)
  H_mag  = -(1/(2g2)) Tr(U_box + U_box^dag)            (off-diagonal)

Direct call expressions: `H.tocsr`, `_electric_diag`, `_hopping_matrix_element`, `_magnetic_matrix_element`, `_mass_diag`, `complex`, `enumerate`, `enumerate_basis`, `len`, `lil_matrix`, `list`, `np.conjugate`, `range`, `tuple`

### `build_hamiltonian_no_magnetic(g2: float, m: float, jmax: float)` — line 531

Build the Hamiltonian without the magnetic term (electric + mass + hopping only).

Same basis ordering as build_hamiltonian, useful for limit checks.

Direct call expressions: `H.tocsr`, `_electric_diag`, `_hopping_matrix_element`, `_mass_diag`, `complex`, `enumerate`, `enumerate_basis`, `len`, `lil_matrix`, `list`, `np.array`, `np.conjugate`, `range`, `tuple`

### `number_op(v: int)` — line 582

Return the number operator n_v for vertex v (diagonal in the basis).

The returned function takes (dim, basis) and returns a CSR matrix.

Direct call expressions: `H.tocsr`, `enumerate`, `float`, `lil_matrix`

### `total_number()` — line 595

Return the total fermion number sum_v n_v (diagonal in the basis).

Direct call expressions: `H.tocsr`, `enumerate`, `float`, `lil_matrix`, `sum`

### `casimir_link(l: int)` — line 605

Return the electric casimir operator j_l(j_l+1) for link l (diagonal in the basis).

Direct call expressions: `H.tocsr`, `cv.casimir`, `enumerate`, `lil_matrix`

### `_charge_projector(charge_tuple: tuple[int, int, int, int], basis: list, dim: int)` — line 617

Projector onto states with given local charges q_v = n_v - n_vac(v).

Args:
    charge_tuple: (q_v1, q_v2, q_v3, q_v4) where q_v = n_v - n_vac(v)
    basis: list of basis labels
    dim: dimension of the basis

Direct call expressions: `H.tocsr`, `enumerate`, `int`, `lil_matrix`, `range`, `tuple`

### `P_stretched(g2: float, m: float, jmax: float)` — line 634

Projector onto states with q = (+1, -1, 0, 0).

Direct call expressions: `_charge_projector`, `enumerate_basis`, `len`

### `P_short(g2: float, m: float, jmax: float)` — line 641

Projector onto states with q = (+1, -1, 0, 0) — the short sector.

Direct call expressions: `_charge_projector`, `enumerate_basis`, `len`

### `P_surv(g2: float, m: float, jmax: float)` — line 648

Projector onto states with q = (+1, -1, 0, 0) (surviving stretched string).

Direct call expressions: `_charge_projector`, `enumerate_basis`, `len`

### `P_meson(g2: float, m: float, jmax: float)` — line 655

Projector onto states with |q_v| = 1 for all v.

Direct call expressions: `H.tocsr`, `abs`, `all`, `enumerate`, `enumerate_basis`, `int`, `len`, `lil_matrix`, `range`, `tuple`

### `P_BBbar(g2: float, m: float, jmax: float)` — line 667

Projector onto any state with |q_v| = 2 for some v (takes precedence).

Direct call expressions: `H.tocsr`, `abs`, `any`, `enumerate`, `enumerate_basis`, `int`, `len`, `lil_matrix`, `range`, `tuple`

### `charge(v: int, n: int)` — line 680

Local charge relative to the staggered vacuum: q_v = n_v - n_vac(v).

Direct call expressions: none

### `validate_dimensions(jmax: float=0.5)` — line 687

Validate that the basis dimension and sector counts match expectations.

Direct call expressions: `enumerate_basis`, `expected_sectors.get`, `len`, `range`, `sector_dims.get`, `sum`

### `validate_hermiticity(H: csr_matrix, atol: float=1e-13)` — line 717

Check that H is Hermitian within tolerance.

Direct call expressions: `H.toarray`, `H_arr.T.conj`, `float`, `np.abs`, `np.max`

### `validate_commutator(H: csr_matrix, N_op: csr_matrix, atol: float=1e-13)` — line 727

Check [H, N] = 0 within tolerance.

Direct call expressions: `H.toarray`, `N_op.toarray`, `float`, `np.abs`, `np.max`

### `pure_electric_check(g2_big: float=1000000.0)` — line 739

Spectrum at g2 -> inf, m = 0: electric levels with k-degeneracies.

From limits.py pure_electric_check.

Direct call expressions: `H.toarray`, `bh`, `bool`, `eigh`, `float`, `int`, `np.abs`, `np.max`, `np.rint`, `np.rint(evals / unit).astype`, `np.sort`, `np.sum`, `range`

### `_no(dim_: int, basis_: list)` — line 587

Direct call expressions: `H.tocsr`, `enumerate`, `float`, `lil_matrix`

### `_no(dim_: int, basis_: list)` — line 597

Direct call expressions: `H.tocsr`, `enumerate`, `float`, `lil_matrix`, `sum`

### `_no(dim_: int, basis_: list)` — line 607

Direct call expressions: `H.tocsr`, `cv.casimir`, `enumerate`, `lil_matrix`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py)

Minimal replication manifest helper for the campaign.

Phase 8 will extend this module to rebuild all tables and figures. Phase 0 only
provides deterministic file hashing and committed-vs-rerun comparison.

### `sha256_file(path: str | Path)` — line 13

Direct call expressions: `Path`, `Path(path).read_bytes`, `hashlib.sha256`, `hashlib.sha256(Path(path).read_bytes()).hexdigest`

### `manifest(paths: list[str | Path])` — line 17

Direct call expressions: `Path`, `sha256_file`, `sorted`, `str`

### `compare_manifests(expected: dict[str, str], actual: dict[str, str])` — line 21

Direct call expressions: `actual.get`, `expected.get`, `len`, `set`, `sorted`

### `write_manifest(paths: list[str | Path], output: str | Path)` — line 27

Direct call expressions: `Path`, `Path(output).write_text`, `json.dumps`, `manifest`

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/__init__.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/__init__.py)

## [runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py](../runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py)

Noise-model twin: FakeTorino (or a real backend's properties) via
AerSimulator.from_backend, with leakage post-selection and observables.

  twin_backend(seed)              -> AerSimulator noise twin
  run_counts(isa_circs, shots, seed, backend) -> list of counts dicts (physical
        bit order already mapped back to LOGICAL q11..q0 strings via the
        circuit's final layout, so l12.decode applies directly)
  postselect(counts)              -> (kept_counts, yield_fraction)
  observables(kept_counts)        -> dict of P_surv, P_meson, P_BBbar, P_other,
        E2_l (4), n_v (4), from decoded labels (all Z-basis, diagonal)
  bootstrap(counts_list, fn, n_boot, seed) -> mean, 2sigma per observable

### `twin_backend(seed=1234, backend=None, compact=False)` — line 28

Direct call expressions: `AerSimulator`, `AerSimulator.from_backend`, `FakeTorino`, `NoiseModel.from_backend`

### `add_measurements(isa)` — line 40

Measure the 12 logical qubits (at their final physical positions) into
classical bits c[i] = logical i, so the count strings read q11..q0.

Direct call expressions: `ClassicalRegister`, `isa.copy`, `isa.layout.final_index_layout`, `len`, `list`, `qc.add_register`, `qc.measure`, `range`

### `run_counts(isa_meas_list, shots, seed, sim)` — line 54

Direct call expressions: `dict`, `enumerate`, `hasattr`, `out.append`, `res.get_counts`, `sim.run`, `sim.run(t, shots=shots, seed_simulator=seed + k).result`, `sim.set_options`, `transpile`

### `postselect(counts)` — line 66

Direct call expressions: `counts.items`, `counts.values`, `kept.values`, `l12.is_physical`, `sum`

### `observables(kept)` — line 72

Direct call expressions: `abs`, `all`, `any`, `cv.casimir`, `e2.sum`, `float`, `kept.items`, `kept.values`, `l12.decode`, `np.array`, `np.zeros`, `range`, `sum`, `tuple`

### `channel_weights(kept)` — line 105

Return signed-weight channel totals without renormalizing the input.

Direct call expressions: `abs`, `all`, `any`, `kept.items`, `l12.decode`, `range`, `sum`, `tuple`

### `channel_closure_residual(kept)` — line 130

Check the corrected V11 closure identity on signed quasi-weights.

Direct call expressions: `abs`, `any`, `channel_weights`, `float`, `kept.items`, `l12.decode`, `range`, `sum`, `tuple`

### `matched_subtraction(observed, control)` — line 146

Compute O(t)-O(0) over the union of observable keys.

Direct call expressions: `control.get`, `float`, `observed.get`, `set`

### `physical_yield(counts, physical_keys)` — line 152

Return the fraction of counts in the supplied physical-key set.

Direct call expressions: `counts.items`, `counts.values`, `float`, `sum`

### `bootstrap(counts_list, n_boot=400, seed=0)` — line 158

Bootstrap over repeats (each element of counts_list is one repeat).
Returns (mean dict, two_sigma dict, yield mean).

Direct call expressions: `A.mean`, `A[rng.integers(0, n, n)].mean`, `boots.std`, `dict`, `float`, `len`, `list`, `mean.tolist`, `np.array`, `np.mean`, `np.random.default_rng`, `observables`, `per.append`, `per[0].keys`, `postselect`, `range`, `rng.integers`, `two_sigma.tolist`, `ys.append`, `zip`

## [runs/section8_v0.5.0_20260907T0628Z/tests/conftest.py](../runs/section8_v0.5.0_20260907T0628Z/tests/conftest.py)

## [runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py](../runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py)

Unit tests for the exact-dynamics lane (gate G2 support).

### `test_self_check()` — line 15

Direct call expressions: `engine.self_check`

Decorator: `pytest.mark.unit`

```python
assert r['expm_krylov_dev'] <= 1e-09
assert r['energy_drift'] <= 1e-10
assert r['N_drift'] <= 1e-10
```

### `test_evolve_matches_expm()` — line 23

Direct call expressions: `H.toarray`, `build_hamiltonian`, `engine.evolve`, `expm`, `np.abs`, `np.array`, `np.max`, `np.zeros`, `scan._idx`

Decorator: `pytest.mark.unit`

```python
assert np.max(np.abs(s[-1] - ref)) <= 1e-12
```

### `test_term_split_is_exact()` — line 34

Direct call expressions: `h.conj`, `np.abs`, `np.diag`, `np.max`, `scan._term_split`, `sum`

Decorator: `pytest.mark.unit`

```python
assert np.max(np.abs(D + sum(hs) + B - Hd)) <= 1e-13
assert np.max(np.abs(h - h.conj().T)) <= 1e-13
assert np.max(np.abs(np.diag(h))) == 0.0
```

### `test_channel_masks_partition_N4_sector()` — line 44

Direct call expressions: `build_hamiltonian`, `int`, `mes.sum`, `n4.sum`, `np.all`, `np.array`, `scan._classify`, `sum`, `surv.sum`

Decorator: `pytest.mark.unit`

```python
assert int(n4.sum()) == 38
assert np.all((surv + mes + bb + oth)[n4] == 1)
assert int(surv.sum()) == 2 and int(mes.sum()) == 2
```

### `test_artifacts_and_window()` — line 54

Direct call expressions: `json.load`, `open`, `os.path.exists`, `os.path.join`, `scan.verify_window`, `w.get`

Decorator: `pytest.mark.unit`

```python
assert res['n_mass_points'] >= 21 and res['n_g2_values'] >= 2
assert os.path.exists(os.path.join(RUN, 'analysis', 'tables', 'exact_mass_scan.csv'))
assert w['r_max'] in (2, 3)
assert v['strang_err'] <= 0.05
assert v['psurv_drop'] >= 0.3 or w.get('shortfall_flagged')
assert v['pair_weight'] >= 0.05 or w.get('shortfall_flagged')
```

## [runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py](../runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py)

G3 tests: L12 encoding, exact block unitaries, Strang circuits, leakage.

### `test_encoding_roundtrip_and_flags()` — line 18

Direct call expressions: `format`, `l12.decode`, `l12.encode`, `l12.is_physical`, `l12.physical_codes`, `len`, `range`, `set`, `sum`

Decorator: `pytest.mark.unit`

```python
assert len(codes) == 82 and len(set(codes)) == 82
assert n_phys == 82
assert code == 3793
assert l12.decode(format(code, '012b')) == sl.STRETCHED
assert l12.encode(l12.decode(c)) == c
assert l12.is_physical(c)
```

### `_apply_on_codes(qc, basis)` — line 32

Matrix of the circuit restricted to physical codes (82x82) and the
leakage block (unphys x phys), via 82 statevector runs.

Direct call expressions: `QuantumCircuit`, `Statevector`, `enumerate`, `float`, `l12.physical_codes`, `max`, `np.linalg.norm`, `np.ones`, `np.zeros`, `prep.compose`, `prep.x`, `range`, `sl.basis_to_code`

### `test_block_unitary_exact_and_leak_free(group, theta)` — line 58

Direct call expressions: `_apply_on_codes`, `expm`, `np.linalg.norm`, `pytest.mark.parametrize`, `sl.terms`, `sl.unitary`

Decorator: `pytest.mark.unit`

Decorator: `pytest.mark.parametrize('group', sl.GROUPS)`

Decorator: `pytest.mark.parametrize('theta', [0.13, 0.61])`

```python
assert np.linalg.norm(Uphys - Uex) <= 1e-12
assert leak <= 1e-12
```

### `test_full_strang_step_matches_exact_product()` — line 68

Direct call expressions: `Statevector`, `_apply_on_codes`, `np.abs`, `np.linalg.norm`, `np.max`, `sl.exact_strang_matrix`, `sl.full_circuit`, `sl.strang_step`, `sl.terms`

Decorator: `pytest.mark.unit`

```python
assert np.linalg.norm(Uphys - Uex) <= 1e-10
assert leak <= 1e-12
assert np.max(np.abs(a - b)) <= 1e-12
```

### `test_noiseless_leakage_zero()` — line 83

Direct call expressions: `AerSimulator`, `Statevector`, `counts.items`, `l12.is_physical`, `meas.measure_all`, `qc.copy`, `sim.run`, `sim.run(t, shots=10000).result`, `sim.run(t, shots=10000).result().get_counts`, `sl.full_circuit`, `sl.leakage_prob`, `sum`, `transpile`

Decorator: `pytest.mark.unit`

```python
assert sl.leakage_prob(v) <= 1e-14
assert flagged == 0
```

### `test_trotter_scaling()` — line 100

Second-order scaling: error vs r at fixed t = RMAX*DT, r in 1..16.

Direct call expressions: `_classify`, `_diagnostics`, `abs`, `basis.index`, `errs_e.append`, `errs_psi.append`, `errs_s.append`, `expm`, `fit`, `float`, `json.dump`, `np.abs`, `np.linalg.norm`, `np.log`, `np.max`, `np.polyfit`, `np.zeros`, `open`, `os.path.join`, `psi0.copy`, `range`, `sl.exact_strang_matrix`, `sl.terms`, `slopes.items`

Decorator: `pytest.mark.unit`

```python
assert -2.3 <= s <= -1.7, (k, s, errs_s, errs_e, errs_psi)
```

### `test_window_strang_error()` — line 136

Direct call expressions: `strang_error`

Decorator: `pytest.mark.unit`

```python
assert strang_error(G2, M, DT, RMAX) <= 0.05
```

## [runs/section8_v0.5.0_20260907T0628Z/tests/test_route_gausskernel.py](../runs/section8_v0.5.0_20260907T0628Z/tests/test_route_gausskernel.py)

### `test_kernel_dimensions_and_number_sectors()` — line 12

Direct call expressions: `(P.conj().T @ P).toarray`, `(P1.conj().T @ P1).toarray`, `P.conj`, `P1.conj`, `_basis`, `build_hamiltonian`, `kernel_dimension`, `len`, `np.abs`, `np.eye`, `np.max`, `print`, `range`, `sum`

```python
assert len(labels) == 82
assert counts == {0: 2, 1: 0, 2: 20, 3: 0, 4: 38, 5: 0, 6: 20, 7: 0, 8: 2}
assert np.max(np.abs((P.conj().T @ P).toarray() - np.eye(82))) < 1e-12
assert kernel_dimension(1.0) == 152
assert len(labels1) == 152
assert np.max(np.abs((P1.conj().T @ P1).toarray() - np.eye(152))) < 1e-12
```

### `test_hermiticity_and_gauss_diagnostics()` — line 29

Direct call expressions: `H.getH`, `build_hamiltonian`, `gauss_commutator_norms`, `max`, `norms.values`, `np.abs`, `np.max`, `print`

```python
assert err <= 1e-13
assert max(norms.values()) <= 1e-12
```

### `test_pure_electric_clusters_and_stretched_label()` — line 39

Direct call expressions: `H.diagonal`, `build_hamiltonian`, `get_state`, `list`, `np.array_equal`, `np.round`, `np.unique`, `print`, `sum`, `zip`

```python
assert np.array_equal(mult, [16, 16, 18, 16, 16])
assert sum((x == stretched for x in labels)) == 1
assert get_state(stretched, labels) >= 0
```

## [runs/section8_v0.5.0_20260907T0628Z/tests/test_route_spinnet.py](../runs/section8_v0.5.0_20260907T0628Z/tests/test_route_spinnet.py)

Unit tests for route 1 (analytic spin-network/dressed-site) Hamiltonian.

Tests the SU(2) single-plaquette Hamiltonian with dynamical two-color staggered
fermions.  All numbers validated against the expected values from the conventions
and limit-check files.

### `test_basis_dimension(self, jmax, expected_dim)` — line 28

Direct call expressions: `enumerate_basis`, `len`, `pytest.mark.parametrize`

Decorator: `pytest.mark.parametrize('jmax,expected_dim', [(0.5, 82), (1.0, 152)])`

```python
assert dim == expected_dim, f'jmax={jmax}: dim={dim} != {expected_dim}'
```

### `test_sector_decomposition(self, jmax)` — line 33

Sector dims at jmax=0.5: N=0,2,4,6,8 -> 2,20,38,20,2 (only even N).

Direct call expressions: `enumerate_basis`, `pytest.mark.parametrize`, `sum`

Decorator: `pytest.mark.parametrize('jmax', [0.5])`

```python
assert sector_dims[N] == expected[N], f'jmax={jmax}: N={N} got {sector_dims[N]} expected {expected[N]}'
```

### `test_H_hermitian(self, g2, m, jmax)` — line 59

Direct call expressions: `H.toarray`, `H_arr.T.conj`, `build_hamiltonian`, `np.abs`, `np.max`, `pytest.mark.parametrize`

Decorator: `pytest.mark.parametrize('g2, m, jmax', [(1.0, 0.0, 0.5), (1.0, 0.1875, 0.5), (0.5, 0.2, 0.5), (2.0, 0.375, 0.5)])`

```python
assert diff <= 1e-13, f'H not Hermitian at (g2={g2}, m={m}, jmax={jmax}): max_diff={diff}'
```

### `test_H_commutes_with_N(self, g2, m, jmax)` — line 75

Direct call expressions: `H.toarray`, `build_hamiltonian`, `enumerate`, `float`, `len`, `np.abs`, `np.max`, `np.zeros`, `pytest.mark.parametrize`, `sum`

Decorator: `pytest.mark.parametrize('g2, m, jmax', [(1.0, 0.0, 0.5), (1.0, 0.1875, 0.5), (0.5, 0.2, 0.5)])`

```python
assert max_comm <= 1e-13, f'[H,N] != 0 at (g2={g2}, m={m}, jmax={jmax}): max_comm={max_comm}'
```

### `test_electric_degeneracies(self)` — line 94

At g2 -> inf, m=0: degeneracies 16,16,18,16,16 by k=#(j=1/2 links).

Direct call expressions: `H.toarray`, `build_hamiltonian`, `int`, `np.abs`, `np.linalg.eigvalsh`, `np.max`, `np.rint`, `np.rint(evals / unit).astype`, `np.sort`, `np.sum`, `range`

```python
assert got == expected, f'Electric degeneracies got {got} expected {expected}'
assert rel <= 1e-08, f'Relative dev {rel} > 1e-8'
```

### `test_no_magnetic_shape(self, g2, m, jmax)` — line 118

Direct call expressions: `build_hamiltonian_no_magnetic`, `pytest.mark.parametrize`

Decorator: `pytest.mark.parametrize('g2, m, jmax', [(1.0, 0.0, 0.5), (1.0, 0.1875, 0.5), (0.5, 0.2, 0.5)])`

```python
assert H_no_mag.shape == (expected_dim, expected_dim)
```

### `test_no_mag_hermitian(self, g2, m, jmax)` — line 126

Direct call expressions: `H_arr.T.conj`, `H_no_mag.toarray`, `build_hamiltonian_no_magnetic`, `np.abs`, `np.max`, `pytest.mark.parametrize`

Decorator: `pytest.mark.parametrize('g2, m, jmax', [(1.0, 0.0, 0.5)])`

```python
assert diff <= 1e-13
```

### `test_no_mag_commuting_N(self, g2, m, jmax)` — line 135

Direct call expressions: `H_no_mag.toarray`, `build_hamiltonian_no_magnetic`, `enumerate`, `float`, `len`, `np.abs`, `np.max`, `np.zeros`, `pytest.mark.parametrize`, `sum`

Decorator: `pytest.mark.parametrize('g2, m, jmax', [(1.0, 0.0, 0.5)])`

```python
assert max_comm <= 1e-13
```

### `test_basis_dimensions_match(self)` — line 150

Basis dimensions match expected values.

Direct call expressions: `validate_dimensions`

```python
assert r05['dim_match'], f"jmax=0.5 dim={r05['dim']} != 82"
assert r10['dim_match'], f"jmax=1.0 dim={r10['dim']} != 152"
```

### `test_sector_dims(self)` — line 157

Sector decomposition at jmax=0.5 matches expectations.

Direct call expressions: `validate_dimensions`

```python
assert r['sector_N0_match'], f"N=0 sector wrong: {r['sector_dims'][0]}"
assert r['sector_N2_match'], f"N=2 sector wrong: {r['sector_dims'][2]}"
assert r['sector_N4_match'], f"N=4 sector wrong: {r['sector_dims'][4]}"
assert r['sector_N6_match'], f"N=6 sector wrong: {r['sector_dims'][6]}"
assert r['sector_N8_match'], f"N=8 sector wrong: {r['sector_dims'][8]}"
```

### `test_pure_electric_check(self)` — line 166

Pure electric degeneracy check from limits.py.

Direct call expressions: `pure_electric_check`

```python
assert pe['ok'], f'Pure electric check failed: {pe}'
```

### `test_hermiticity_via_validator(self)` — line 171

Hermiticity check via validator.

Direct call expressions: `build_hamiltonian`, `validate_hermiticity`

```python
assert hcheck['hermitian'], f"H not Hermitian: max_diff={hcheck['max_diff']}"
```

## [runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py](../runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py)

G4 structural-synthesis verification for L12.

### `_apply(qc, codes)` — line 16

Direct call expressions: `QuantumCircuit`, `Statevector`, `enumerate`, `float`, `len`, `max`, `np.linalg.norm`, `np.ones`, `np.zeros`, `prep.compose`, `prep.x`, `range`

### `test_synth_block(group, theta)` — line 36

Direct call expressions: `_apply`, `expm`, `np.abs`, `np.max`, `pytest.mark.parametrize`, `sl.basis_to_code`, `sl.terms`, `sy.synth_unitary`

Decorator: `pytest.mark.unit`

Decorator: `pytest.mark.parametrize('group', sl.GROUPS)`

Decorator: `pytest.mark.parametrize('theta', (0.13, 0.61))`

```python
assert np.max(np.abs(got - expm(-1j * theta * terms[group]))) <= 1e-10
assert leak <= 1e-12
```

### `test_synth_strang()` — line 45

Direct call expressions: `_apply`, `np.abs`, `np.max`, `sl.basis_to_code`, `sl.exact_strang_matrix`, `sl.params`, `sl.terms`, `sy.synth_strang_step`

Decorator: `pytest.mark.unit`

```python
assert np.max(np.abs(got - sl.exact_strang_matrix(sl.params()['dt'], 4.0, 0.75))) <= 1e-10
assert leak <= 1e-12
```

### `test_resources_and_json(capsys)` — line 54

Direct call expressions: `Path`, `Path('circuits/resources_synth.md').exists`, `all`, `dict`, `int`, `json.dumps`, `print`, `sy.write_resources`

Decorator: `pytest.mark.unit`

```python
assert Path('circuits/resources_synth.md').exists()
assert all((v['n_2q'] >= 0 for _, v in rows))
```

## [runs/section8_v0.5.0_20260907T0628Z/gates/gate_G0.py](../runs/section8_v0.5.0_20260907T0628Z/gates/gate_G0.py)

Gate G0: bootstrap complete.

### `check(name, ok, target, value)` — line 7

Direct call expressions: `bool`, `crit.append`

## [runs/section8_v0.5.0_20260907T0628Z/gates/gate_G1.py](../runs/section8_v0.5.0_20260907T0628Z/gates/gate_G1.py)

Gate G1: 82-state Hamiltonian by two independent routes + limit tests.

Deterministic; recomputes every criterion from the route modules directly.

### `check(name, target, value, ok)` — line 20

Direct call expressions: `bool`, `crit.append`, `print`

### `main()` — line 25

Direct call expressions: `H.toarray`, `Hd.conj`, `Ns.count`, `all`, `check`, `compare.spectra_comparison`, `compare.time_series_comparison`, `datetime.datetime.utcnow`, `datetime.datetime.utcnow().isoformat`, `float`, `g.values`, `int`, `json.dump`, `limits.frozen_matter_check`, `limits.magnetic_off_check`, `limits.pure_electric_check`, `max`, `mod.build_hamiltonian`, `np.abs`, `np.array`, `np.diag`, `np.max`, `open`, `os.environ.get`, `os.path.exists`, `os.path.join`, `print`, `r2.gauss_commutator_norms`, `r2.kernel_dimension`, `set`, `sorted`, `str`, `sum`

## [runs/section8_v0.5.0_20260907T0628Z/gates/gate_G2.py](../runs/section8_v0.5.0_20260907T0628Z/gates/gate_G2.py)

Gate G2: exact dynamics, resonance scan, window selection.

Reads artifacts produced by the dynamics builders and re-verifies the
critical numbers directly (expm vs Krylov, conservation, window criteria).

### `check(name, target, value, ok)` — line 20

Direct call expressions: `bool`, `crit.append`, `print`

### `main()` — line 25

Direct call expressions: `all`, `check`, `datetime.datetime.utcnow`, `datetime.datetime.utcnow().isoformat`, `engine.self_check`, `int`, `json.dump`, `json.load`, `open`, `os.environ.get`, `os.path.exists`, `os.path.join`, `print`, `scan.verify_window`, `summary.get`, `trj.get`, `w.get`

## [runs/section8_v0.5.0_20260907T0628Z/gates/gate_G3.py](../runs/section8_v0.5.0_20260907T0628Z/gates/gate_G3.py)

Gate G3: encodings, exact block unitaries, Strang circuits, Trotter, leakage.

Runs the G3 test suite (the criteria are the tests) and re-derives the headline
numbers for the JSON. Scope note: L12 only tonight (S8/C7 not built);
recorded as a partial criterion, not hidden.

### `check(name, target, value, ok)` — line 21

Direct call expressions: `bool`, `crit.append`, `print`

### `main()` — line 26

Direct call expressions: `QuantumCircuit`, `Statevector`, `all`, `c['name'].startswith`, `check`, `datetime.datetime.utcnow`, `datetime.datetime.utcnow().isoformat`, `expm`, `float`, `int`, `json.dump`, `json.load`, `l12.physical_codes`, `len`, `max`, `np.abs`, `np.max`, `open`, `os.environ.get`, `os.path.exists`, `os.path.getsize`, `os.path.join`, `prep.compose`, `prep.x`, `print`, `r.stdout.strip`, `r.stdout.strip().splitlines`, `range`, `sl.basis_to_code`, `sl.full_circuit`, `sl.leakage_prob`, `sl.params`, `sl.terms`, `sl.unitary`, `subprocess.run`

## [runs/section8_v0.5.0_20260907T0628Z/gates/gate_G4.py](../runs/section8_v0.5.0_20260907T0628Z/gates/gate_G4.py)

Gate G4: compile after routing, noisy twin, Plan-B decision.

Reads compile/resources_routed.json + compile/twin_check.json produced by
src/su2qc/compile/run_g4.py and re-verifies routed equivalence for the
chosen pipeline on the r_max circuit.

### `check(name, target, value, ok)` — line 18

Direct call expressions: `bool`, `crit.append`, `print`

### `main()` — line 23

Direct call expressions: `all`, `any`, `check`, `datetime.datetime.utcnow`, `datetime.datetime.utcnow().isoformat`, `int`, `json.dump`, `json.load`, `open`, `open(os.path.join(RUN, 'run', 'DECISIONS.md')).read`, `os.environ.get`, `os.path.exists`, `os.path.join`, `print`, `rr.get`
