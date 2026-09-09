Write a source-derived first draft of SU2QC_CONTRACTS, only for the listed public functions. This is the documentation-only Opus PHYSICS-as-documentation lane of an accepted Fable plan. No tools, no code edits, no imports/execution of su2qc. Output Markdown only, no enclosing fence, at most 8500 words. Never invent tests or claim a test enforces more than its assertions. No campaign physics sign-off.

Use one heading per function exactly: ### su2qc.module.function
Then Signature, Source (repository path:line-range), Inputs, Outputs, Invariants, Side effects, Empty/degenerate and errors, Enforcement. State concrete behaviour, including implicit assumptions and absent validation. For each invariant, name the test file and test function/line that enforces it, or write UNENFORCED. Missing input validation is NOT a validated precondition. Preserve return types/shapes/sign conventions, encoding bit order, channel/estimator semantics and mutable/cached return behaviour. Distinguish direct checks from indirect integration coverage. Document main/run helpers' file writes and CLI operations accurately; no generic filler. Every substantive contract cites a source line/range. Source includes exact line numbers below. Imported external-library primitives are not package-authored API entries; local imported su2qc callables are documented at their definitions. No public classes exist in the AST scan. Include all functions listed, no new functions.

Status: C0 PARTIAL; C1 unamended; C2 NOT STARTED (stored state may say BLOCKED); no production repair; all noisy simulator results EMULATED; every v0.5.0 twin sigma is void as independent-repeat uncertainty. Existing test outputs are historical, not new gate passes. Unenforced invariants are UNENFORCED. Proposed repairs are PROPOSED, NOT IMPLEMENTED. No thresholds changed.

Mandatory R15 correction approved by user and Fable plan: n in {0,1,2}, N_VAC=(0,2,0,2) makes all |q|=1 force n=(1,1,1,1), N=4 and sum q=0. The prompt's claimed non-N4 meson hazard and its jmax=1 recurrence are false under these conventions; explicitly supersede that paragraph. Preserve channels as implemented. State closure equation exactly from source and distinguish the structural argument for the occupation domain from the measured finite 82-code oracle. Invalid code with nonzero weight is skipped by both sides, so residual cannot detect it; R9 demand is UNSATISFIABLE AS WRITTEN, awaiting ruling.

For run_counts: fixed transpiler seed, re-transpile every circuit, per-circuit simulator seed seed+k, mutates sim.set_options and persists. Independence VIOLATED in measured backend/path, cite historical seed-diagnosis.json and equal-seed-control.json (do not extrapolate to every random generator/backend). Explicit 1023 overlapping entries out of 1024 shots matched after a one-shot shift on both production and compact paths, and caller seed101->500 in equal-seed control. Proposed repair NOT IMPLEMENTED, campaign physics acceptance DEFERRED; do not describe current quota as exhausted. bootstrap samples counts_list elements, so returned 2*s is not valid independent-repeat uncertainty for these correlated elements; ordinary bootstrap adequacy also needs representative replicates and sufficient sample size, not independence alone. physical_yield empty raises ZeroDivisionError vs postselect empty returns ({},0.0), UNENFORCED. Survival projector actually combines two physical codewords for one occupation pattern; do not call it rank1. Physical yield denominator includes all reported shots and can be zero. Negative/unnormalized weights and float/int key assumptions are caller preconditions, not validated guarantees.

Do not use a review's prose as authority; the numbered code below and measured JSON summaries are the authority. Historical JSONs are located at runs/campaign_v060/sessions/c060_p0_20260908_3/. Cite full paths when using them. Do not quote the incorrect original R15 meson paragraph as true. Markdown source references may be inline path:line text, with paths preserved for bundle mapping.

# Required entries
[
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "params",
    "signature": "params(g2=None, m=None)",
    "line": 46,
    "end_line": 56,
    "docstring": null,
    "returns": [
      "vals"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "terms",
    "signature": "terms(g2, m)",
    "line": 60,
    "end_line": 65,
    "docstring": "(basis, {group: 82x82 ndarray}) from the dynamics-lane exact split.",
    "returns": [
      "(basis, {'D': D, 'h0': hs[0], 'h1': hs[1], 'h2': hs[2], 'h3': hs[3], 'B': B, 'H': Hd})"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "code_index",
    "signature": "code_index()",
    "line": 69,
    "end_line": 71,
    "docstring": null,
    "returns": [
      "(codes, {c: i for i, c in enumerate(codes)})"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "basis_to_code",
    "signature": "basis_to_code(basis)",
    "line": 74,
    "end_line": 75,
    "docstring": null,
    "returns": [
      "np.array([encode(lab) for lab in basis])"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "local_matrix",
    "signature": "local_matrix(M, codes_of_basis, S)",
    "line": 126,
    "end_line": 135,
    "docstring": "2^|S| x 2^|S| Hermitian matrix acting on support S (sorted).",
    "returns": [
      "L"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "supports",
    "signature": "supports(g2, m)",
    "line": 139,
    "end_line": 142,
    "docstring": null,
    "returns": [
      "{g: _support(T[g], cb) for g in ('h0', 'h1', 'h2', 'h3', 'B')}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "unitary",
    "signature": "unitary(group, theta, g2, m)",
    "line": 148,
    "end_line": 162,
    "docstring": "12-qubit circuit for exp(-i theta E T_group E^dag).",
    "returns": [
      "qc",
      "qc"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "strang_step",
    "signature": "strang_step(dt, g2, m)",
    "line": 165,
    "end_line": 172,
    "docstring": null,
    "returns": [
      "qc"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "prep_stretched",
    "signature": "prep_stretched(qc=None)",
    "line": 175,
    "end_line": 181,
    "docstring": null,
    "returns": [
      "qc"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "full_circuit",
    "signature": "full_circuit(r, dt=None, g2=None, m=None, merge_D=True)",
    "line": 184,
    "end_line": 204,
    "docstring": null,
    "returns": [
      "qc",
      "qc",
      "qc"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "exact_strang_matrix",
    "signature": "exact_strang_matrix(dt, g2, m)",
    "line": 209,
    "end_line": 222,
    "docstring": "Exact matrix of ONE Strang step in the circuit's group ordering:\nD/2 . h0/2 . h2/2 . h1/2 . h3/2 . B . h3/2 . h1/2 . h2/2 . h0/2 . D/2\n(h0,h2 commute; h1,h3 commute).",
    "returns": [
      "U"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "circuit_state",
    "signature": "circuit_state(qc)",
    "line": 225,
    "end_line": 227,
    "docstring": "Statevector (4096) of a circuit from |0...0>.",
    "returns": [
      "Statevector(qc).data"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "to_basis",
    "signature": "to_basis(vec4096, basis)",
    "line": 230,
    "end_line": 232,
    "docstring": null,
    "returns": [
      "vec4096[cb]"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "leakage_prob",
    "signature": "leakage_prob(vec4096)",
    "line": 235,
    "end_line": 239,
    "docstring": null,
    "returns": [
      "float(np.sum(np.abs(vec4096[mask]) ** 2))"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py",
    "module": "circuits/strang_l12.py",
    "name": "resources",
    "signature": "resources(circ)",
    "line": 244,
    "end_line": 250,
    "docstring": null,
    "returns": [
      "{'n_2q': int(n2), 'depth_2q': int(t.depth(lambda x: x.operation.num_qubits == 2)), 'depth': int(t.depth())}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py",
    "module": "circuits/synth_l12.py",
    "name": "synth_unitary",
    "signature": "synth_unitary(group, theta, g2, m)",
    "line": 249,
    "end_line": 259,
    "docstring": "Synthesize one exact L12 block using only one-qubit and controlled gates.",
    "returns": [
      "qc"
    ],
    "raises": [
      "ValueError(group)"
    ]
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py",
    "module": "circuits/synth_l12.py",
    "name": "synth_strang_step",
    "signature": "synth_strang_step(dt, g2, m)",
    "line": 262,
    "end_line": 268,
    "docstring": null,
    "returns": [
      "qc"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py",
    "module": "circuits/synth_l12.py",
    "name": "synth_full_circuit",
    "signature": "synth_full_circuit(r, dt=None, g2=None, m=None, merge_D=True)",
    "line": 271,
    "end_line": 287,
    "docstring": null,
    "returns": [
      "qc",
      "qc",
      "qc"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py",
    "module": "circuits/synth_l12.py",
    "name": "write_resources",
    "signature": "write_resources(path='circuits/resources_synth.md')",
    "line": 296,
    "end_line": 307,
    "docstring": null,
    "returns": [
      "rows"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py",
    "module": "compile/route.py",
    "name": "fake_heron",
    "signature": "fake_heron()",
    "line": 30,
    "end_line": 32,
    "docstring": null,
    "returns": [
      "FakeTorino()"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py",
    "module": "compile/route.py",
    "name": "route",
    "signature": "route(circ, backend=None, opt=3, seed=7, initial_layout=None)",
    "line": 35,
    "end_line": 47,
    "docstring": null,
    "returns": [
      "(isa, {'initial_physical': [int(x) for x in init], 'final_index_layout': [int(x) for x in isa.layout.final_index_layout()] if lay else list(range(12))})"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py",
    "module": "compile/route.py",
    "name": "routed_resources",
    "signature": "routed_resources(isa)",
    "line": 50,
    "end_line": 55,
    "docstring": null,
    "returns": [
      "{'n_2q': int(n2), 'depth_2q': int(isa.depth(lambda x: x.operation.num_qubits == 2)), 'depth': int(isa.depth())}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py",
    "module": "compile/route.py",
    "name": "routed_equivalence",
    "signature": "routed_equivalence(logical, isa)",
    "line": 58,
    "end_line": 85,
    "docstring": "1 - |<routed|logical>| with the routed state pulled back through\nfinal_index_layout to the logical qubit order (statevector, no measure).",
    "returns": [
      "float(1.0 - abs(np.vdot(vec, psi_l)))"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py",
    "module": "compile/route.py",
    "name": "pyzx_pass",
    "signature": "pyzx_pass(circ, strategy='basic')",
    "line": 88,
    "end_line": 110,
    "docstring": "The monograph's PyZX pipeline (repo src/su2zx/core.py) with its dense\n12-qubit Operator equivalence check replaced by a statevector check on\nthe 82 physical codes (done by the caller via routed_equivalence-style\ncomparison). strategy: 'basic' (topology-preserving), 'full_reduce'.",
    "returns": [
      "qasm2.loads(cand.to_qasm())"
    ],
    "raises": [
      "ValueError(strategy)"
    ]
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py",
    "module": "compile/route.py",
    "name": "state_equivalence",
    "signature": "state_equivalence(a, b)",
    "line": 113,
    "end_line": 116,
    "docstring": "1 - |<a|b>| for two same-width circuits from |0>.",
    "returns": [
      "float(1.0 - abs(np.vdot(va, vb)))"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py",
    "module": "compile/run_g4.py",
    "name": "n2",
    "signature": "n2(c)",
    "line": 29,
    "end_line": 30,
    "docstring": null,
    "returns": [
      "sum((1 for i in c.data if i.operation.num_qubits == 2 and i.operation.name != 'barrier'))"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py",
    "module": "compile/run_g4.py",
    "name": "d2",
    "signature": "d2(c)",
    "line": 33,
    "end_line": 34,
    "docstring": null,
    "returns": [
      "int(c.depth(lambda x: x.operation.num_qubits == 2))"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/engine.py",
    "module": "dynamics/engine.py",
    "name": "evolve",
    "signature": "evolve(H, psi0, times)",
    "line": 15,
    "end_line": 32,
    "docstring": "Evolve psi0 under sparse H at times t (array).\n\nReturns array of shape (len(times), dim) with state vectors at each time.\nUses dense expm of -i*H*dt per step (cumulative), since the Hilbert space\nis small (82 or 152 dims).",
    "returns": [
      "phases * c0[None, :] @ V.T"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/engine.py",
    "module": "dynamics/engine.py",
    "name": "self_check",
    "signature": "self_check(g2: float, m: float, jmax: float, t_max: float)",
    "line": 35,
    "end_line": 130,
    "docstring": "Verify expm vs Krylov conservation.\n\nReturns dict with:\n  expm_krylov_dev: max ||psi_dense(t) - psi_krylov(t)||_inf over ~21 times on [0, t_max]\n  energy_drift: max |<H>(t) - <H>(0)|\n  N_drift: max |<N>(t) - <N>(0)|\nTargets: <=1e-9, <=1e-10, <=1e-10.",
    "returns": [
      "{'expm_krylov_dev': expm_krylov_dev, 'energy_drift': energy_drift, 'N_drift': N_drift}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py",
    "module": "dynamics/scan.py",
    "name": "channel_probs",
    "signature": "channel_probs(basis, states)",
    "line": 59,
    "end_line": 62,
    "docstring": null,
    "returns": [
      "(p @ surv, p @ meson, p @ bbbar, p @ other)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py",
    "module": "dynamics/scan.py",
    "name": "mass_scan",
    "signature": "mass_scan(g2_values=(1.0, 2.0, 4.0, 8.0), n_m=25, t_window=(0.0, 40.0), jmax=0.5)",
    "line": 67,
    "end_line": 108,
    "docstring": "Scan m in [0, g2/2] for each g2. Two resonance estimators are recorded:\nargmax of W_bar (prompt criterion 2) and argmin of t_b (breaking time);\nsee physics/DISCREPANCIES.md for why they differ at strong coupling.",
    "returns": [
      "out"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py",
    "module": "dynamics/scan.py",
    "name": "timeseries_at",
    "signature": "timeseries_at(g2, m, jmax=0.5, times=None, tag='exact_timeseries')",
    "line": 113,
    "end_line": 141,
    "docstring": null,
    "returns": [
      "{'t': times, 'P_surv': ps, 'P_meson': pm, 'P_BBbar': pb, 'P_other': po, 'E2': e2, 'n': nv, 'energy': en, 'P_stretched': p_st, 'P_short': p_sh}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py",
    "module": "dynamics/scan.py",
    "name": "truncation",
    "signature": "truncation(g2, m)",
    "line": 177,
    "end_line": 203,
    "docstring": "Max channel-probability shift jmax=1 vs jmax=1/2 over t in [0,12].",
    "returns": [
      "res"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py",
    "module": "dynamics/scan.py",
    "name": "strang_step_matrix",
    "signature": "strang_step_matrix(D, hs, B, dt)",
    "line": 236,
    "end_line": 247,
    "docstring": "One Strang step in the CIRCUIT layer ordering (prompt \u00a75.5):\nD/2 \u00b7 [h0,h2]/2 \u00b7 [h1,h3]/2 \u00b7 B \u00b7 [h1,h3]/2 \u00b7 [h0,h2]/2 \u00b7 D/2.",
    "returns": [
      "U"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py",
    "module": "dynamics/scan.py",
    "name": "strang_error",
    "signature": "strang_error(g2, m, dt, r, jmax=0.5)",
    "line": 250,
    "end_line": 266,
    "docstring": "Observable error of r Strang steps vs exact at t = r dt.",
    "returns": [
      "max(devs)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py",
    "module": "dynamics/scan.py",
    "name": "select_window",
    "signature": "select_window(g2=1.0, m=None, jmax=0.5)",
    "line": 269,
    "end_line": 303,
    "docstring": "Choose (g2, m, dt, r_max) per prompt Phase-2 criterion 5.",
    "returns": [
      "best",
      "cand"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py",
    "module": "dynamics/scan.py",
    "name": "verify_window",
    "signature": "verify_window(w)",
    "line": 306,
    "end_line": 316,
    "docstring": "Recompute the window criteria (gate G2 calls this).",
    "returns": [
      "{'psurv_drop': float(ps[0] - ps[1]), 'pair_weight': float(pm[1] + pb[1]), 'strang_err': float(strang_error(g2, m, dt, r))}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py",
    "module": "encodings/l12.py",
    "name": "encode",
    "signature": "encode(label)",
    "line": 33,
    "end_line": 38,
    "docstring": "Encode a canonical route-spinnet basis label as a 12-bit integer.",
    "returns": [
      "code"
    ],
    "raises": [
      "ValueError(f'not a physical L12 label: {label!r}')"
    ]
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py",
    "module": "encodings/l12.py",
    "name": "decode",
    "signature": "decode(bits)",
    "line": 40,
    "end_line": 48,
    "docstring": "Decode an integer (or a q11...q0 bit string) or return ``None``.",
    "returns": [
      "_maps().get(bits)",
      "None",
      "None"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py",
    "module": "encodings/l12.py",
    "name": "physical_codes",
    "signature": "physical_codes()",
    "line": 50,
    "end_line": 51,
    "docstring": null,
    "returns": [
      "sorted(_maps())"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py",
    "module": "encodings/l12.py",
    "name": "leakage_flags",
    "signature": "leakage_flags(bits)",
    "line": 53,
    "end_line": 65,
    "docstring": "Return vertex leakage and four endpoint-consistency flags.",
    "returns": [
      "{'vertex': vertex, 'link': tuple(link)}",
      "{'vertex': (True,) * 4, 'link': (True,) * 4}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py",
    "module": "encodings/l12.py",
    "name": "is_physical",
    "signature": "is_physical(bits)",
    "line": 67,
    "end_line": 69,
    "docstring": null,
    "returns": [
      "not any(f['vertex']) and (not any(f['link']))"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "twin_backend",
    "signature": "twin_backend(seed=1234, backend=None, compact=False)",
    "line": 28,
    "end_line": 37,
    "docstring": null,
    "returns": [
      "AerSimulator.from_backend(backend, seed_simulator=seed)",
      "AerSimulator(noise_model=noise)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "add_measurements",
    "signature": "add_measurements(isa)",
    "line": 40,
    "end_line": 51,
    "docstring": "Measure the 12 logical qubits (at their final physical positions) into\nclassical bits c[i] = logical i, so the count strings read q11..q0.",
    "returns": [
      "qc"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "run_counts",
    "signature": "run_counts(isa_meas_list, shots, seed, sim)",
    "line": 54,
    "end_line": 63,
    "docstring": null,
    "returns": [
      "out"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "postselect",
    "signature": "postselect(counts)",
    "line": 66,
    "end_line": 69,
    "docstring": null,
    "returns": [
      "(kept, sum(kept.values()) / tot if tot else 0.0)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "observables",
    "signature": "observables(kept)",
    "line": 72,
    "end_line": 102,
    "docstring": null,
    "returns": [
      "acc"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "channel_weights",
    "signature": "channel_weights(kept)",
    "line": 105,
    "end_line": 127,
    "docstring": "Return signed-weight channel totals without renormalizing the input.",
    "returns": [
      "out"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "channel_closure_residual",
    "signature": "channel_closure_residual(kept)",
    "line": 130,
    "end_line": 143,
    "docstring": "Check the corrected V11 closure identity on signed quasi-weights.",
    "returns": [
      "float(lhs - rhs)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "matched_subtraction",
    "signature": "matched_subtraction(observed, control)",
    "line": 146,
    "end_line": 149,
    "docstring": "Compute O(t)-O(0) over the union of observable keys.",
    "returns": [
      "{key: float(observed.get(key, 0.0) - control.get(key, 0.0)) for key in set(observed) | set(control)}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "physical_yield",
    "signature": "physical_yield(counts, physical_keys)",
    "line": 152,
    "end_line": 155,
    "docstring": "Return the fraction of counts in the supplied physical-key set.",
    "returns": [
      "float(sum((value for key, value in counts.items() if key in physical_keys)) / total)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py",
    "module": "twin/twin.py",
    "name": "bootstrap",
    "signature": "bootstrap(counts_list, n_boot=400, seed=0)",
    "line": 158,
    "end_line": 175,
    "docstring": "Bootstrap over repeats (each element of counts_list is one repeat).\nReturns (mean dict, two_sigma dict, yield mean).",
    "returns": [
      "(dict(zip(keys, mean.tolist())), dict(zip(keys, two_sigma.tolist())), float(np.mean(ys)))"
    ],
    "raises": []
  }
]
# Measured evidence summaries
{
  "seed-diagnosis.json": {
    "status": "partial: diagnostic process exited 124 at 2400-second cap during r1; no completed r1 counts",
    "source": "EMULATED",
    "code": "unchanged HEAD sandbox copy",
    "paths": {
      "production": {
        "raw": {
          "omitted_from_drafting_input": true,
          "items": 3,
          "reason": "full data retained in cited evidence file"
        },
        "shift_equal": true,
        "equal_seed_counts_equal": true,
        "equal_multisets": false,
        "same_index_matches": 424,
        "shift_matches": 1023,
        "well_separated": {
          "seeds": [
            500,
            1000500,
            2000500,
            3000500,
            4000500
          ],
          "distinct": 5,
          "key_counts": [
            42,
            41,
            46,
            46,
            47
          ],
          "counts": {
            "omitted_from_drafting_input": true,
            "items": 5,
            "reason": "full data retained in cited evidence file"
          },
          "kept_per_repeat": [
            687,
            735,
            721,
            723,
            703
          ],
          "yield_mean": 0.6970703125,
          "observables": {
            "P_surv": {
              "mean": 0.9506074044281579,
              "two_sigma": 0.006399823350801536,
              "pooled_variance": 0.046881708645656016,
              "expected_bootstrap_se": 0.0032401563015165,
              "ratio": 0.9875794182839587,
              "structural_zero_in_pooled_sample": false
            },
            "P_meson": {
              "mean": 0.0,
              "two_sigma": 0.0,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "P_BBbar": {
              "mean": 0.04939259557184224,
              "two_sigma": 0.006399823350801544,
              "pooled_variance": 0.04688170864565601,
              "expected_bootstrap_se": 0.0032401563015165,
              "ratio": 0.9875794182839599,
              "structural_zero_in_pooled_sample": false
            },
            "P_other": {
              "mean": 0.0,
              "two_sigma": 0.0,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "P_stretched": {
              "mean": 0.9506074044281579,
              "two_sigma": 0.006399823350801536,
              "pooled_variance": 0.046881708645656016,
              "expected_bootstrap_se": 0.0032401563015165,
              "ratio": 0.9875794182839587,
              "structural_zero_in_pooled_sample": false
            },
            "P_short": {
              "mean": 0.0,
              "two_sigma": 0.0,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "E2_l1": {
              "mean": 0.0002040816326530612,
              "two_sigma": 0.0003711373161273446,
              "pooled_variance": 0.00015756301284032572,
              "expected_bootstrap_se": 0.00018784142884398922,
              "ratio": 0.987900588308426,
              "structural_zero_in_pooled_sample": false
            },
            "E2_l2": {
              "mean": 0.7468662410475975,
              "two_sigma": 0.0007686920585991352,
              "pooled_variance": 0.0023541715847863686,
              "expected_bootstrap_se": 0.0007260780394309435,
              "ratio": 0.5293453436503809,
              "structural_zero_in_pooled_sample": false
            },
            "E2_l3": {
              "mean": 0.75,
              "two_sigma": 1.7208107345559408e-17,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "E2_l4": {
              "mean": 0.75,
              "two_sigma": 1.7208107345559408e-17,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "n_v1": {
              "mean": 1.0002721088435373,
              "two_sigma": 0.0004948497548364009,
              "pooled_variance": 0.0002801120228272457,
              "expected_bootstrap_se": 0.00025045523845865225,
              "ratio": 0.9879005883083092,
              "structural_zero_in_pooled_sample": false
            },
            "n_v2": {
              "mean": 0.9955495458865926,
              "two_sigma": 0.0013568909863214153,
              "pooled_variance": 0.00446295074935069,
              "expected_bootstrap_se": 0.0009997128902925606,
              "ratio": 0.6786403373894321,
              "structural_zero_in_pooled_sample": false
            },
            "n_v3": {
              "mean": 0.02497124440101751,
              "two_sigma": 0.0026795795890847563,
              "pooled_variance": 0.04504920448735065,
              "expected_bootstrap_se": 0.0031761997553467884,
              "ratio": 0.42182164150317913,
              "structural_zero_in_pooled_sample": false
            },
            "n_v4": {
              "mean": 1.9292473305019109,
              "two_sigma": 0.010066739367375805,
              "pooled_variance": 0.13623053533505614,
              "expected_bootstrap_se": 0.005523336166101811,
              "ratio": 0.9112915695008817,
              "structural_zero_in_pooled_sample": false
            },
            "dC": {
              "mean": -0.0029296773197494907,
              "two_sigma": 0.0006493166643274928,
              "pooled_variance": 0.002513059398743625,
              "expected_bootstrap_se": 0.0007501802420225069,
              "ratio": 0.4327737708586652,
              "structural_zero_in_pooled_sample": false
            }
          }
        }
      },
      "compact": {
        "raw": {
          "omitted_from_drafting_input": true,
          "items": 3,
          "reason": "full data retained in cited evidence file"
        },
        "shift_equal": true,
        "equal_seed_counts_equal": true,
        "equal_multisets": false,
        "same_index_matches": 414,
        "shift_matches": 1023,
        "well_separated": {
          "seeds": [
            500,
            1000500,
            2000500,
            3000500,
            4000500
          ],
          "distinct": 5,
          "key_counts": [
            47,
            51,
            42,
            47,
            51
          ],
          "counts": {
            "omitted_from_drafting_input": true,
            "items": 5,
            "reason": "full data retained in cited evidence file"
          },
          "kept_per_repeat": [
            648,
            672,
            654,
            657,
            617
          ],
          "yield_mean": 0.634375,
          "observables": {
            "P_surv": {
              "mean": 0.9726165937352744,
              "two_sigma": 0.005565189577934388,
              "pooled_variance": 0.026650636845106653,
              "expected_bootstrap_se": 0.0025608450675182223,
              "ratio": 1.0865924004000267,
              "structural_zero_in_pooled_sample": false
            },
            "P_meson": {
              "mean": 0.0,
              "two_sigma": 0.0,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "P_BBbar": {
              "mean": 0.02738340626472554,
              "two_sigma": 0.005565189577934429,
              "pooled_variance": 0.026650636845106653,
              "expected_bootstrap_se": 0.0025608450675182223,
              "ratio": 1.086592400400035,
              "structural_zero_in_pooled_sample": false
            },
            "P_other": {
              "mean": 0.0,
              "two_sigma": 0.0,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "P_stretched": {
              "mean": 0.9726165937352744,
              "two_sigma": 0.005565189577934388,
              "pooled_variance": 0.026650636845106653,
              "expected_bootstrap_se": 0.0025608450675182223,
              "ratio": 1.0865924004000267,
              "structural_zero_in_pooled_sample": false
            },
            "P_short": {
              "mean": 0.0,
              "two_sigma": 0.0,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "E2_l1": {
              "mean": 0.0004525720838794233,
              "two_sigma": 0.0005027971332070429,
              "pooled_variance": 0.00034615371490451116,
              "expected_bootstrap_se": 0.0002918528958810956,
              "ratio": 0.8613879462958772,
              "structural_zero_in_pooled_sample": false
            },
            "E2_l2": {
              "mean": 0.7495484752120026,
              "two_sigma": 0.00048624461030312237,
              "pooled_variance": 0.00034615371490451116,
              "expected_bootstrap_se": 0.0002918528958810956,
              "ratio": 0.8330302991086721,
              "structural_zero_in_pooled_sample": false
            },
            "E2_l3": {
              "mean": 0.75,
              "two_sigma": 0.0,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "E2_l4": {
              "mean": 0.75,
              "two_sigma": 0.0,
              "pooled_variance": 0.0,
              "expected_bootstrap_se": 0.0,
              "ratio": null,
              "structural_zero_in_pooled_sample": true
            },
            "n_v1": {
              "mean": 0.9993965705548273,
              "two_sigma": 0.0006703961776093973,
              "pooled_variance": 0.0006153843820524643,
              "expected_bootstrap_se": 0.0003891371945081275,
              "ratio": 0.861387946295886,
              "structural_zero_in_pooled_sample": false
            },
            "n_v2": {
              "mean": 0.9987945375041642,
              "two_sigma": 0.000998648121585581,
              "pooled_variance": 0.001230010434613798,
              "expected_bootstrap_se": 0.0005501535331268949,
              "ratio": 0.9076085687476982,
              "structural_zero_in_pooled_sample": false
            },
            "n_v3": {
              "mean": 0.035777170570061356,
              "two_sigma": 0.007015529141144296,
              "pooled_variance": 0.06953729767769176,
              "expected_bootstrap_se": 0.004136551285972433,
              "ratio": 0.8479925251905905,
              "structural_zero_in_pooled_sample": false
            },
            "n_v4": {
              "mean": 1.9828192499816186,
              "two_sigma": 0.006187143022028115,
              "pooled_variance": 0.03418549346016647,
              "expected_bootstrap_se": 0.0029003501705485474,
              "ratio": 1.0666200041731395,
              "structural_zero_in_pooled_sample": false
            },
            "dC": {
              "mean": 1.0472958820173517e-06,
              "two_sigma": 0.0006461403807420064,
              "pooled_variance": 0.0006927339901477833,
              "expected_bootstrap_se": 0.00041286945812807883,
              "ratio": 0.7824996109806251,
              "structural_zero_in_pooled_sample": false
            }
          }
        }
      }
    },
    "prefixed_production": {
      "0": {
        "shots": 4000,
        "seeds": [
          500,
          501,
          502,
          503,
          504
        ],
        "seconds": 32.26912897300099,
        "distinct": 4,
        "key_counts": [
          79,
          79,
          79,
          79,
          79
        ],
        "counts": {
          "omitted_from_drafting_input": true,
          "items": 5,
          "reason": "full data retained in cited evidence file"
        },
        "kept_per_repeat": [
          2760,
          2761,
          2761,
          2761,
          2761
        ],
        "yield_mean": 0.6901999999999999,
        "observables": {
          "P_surv": {
            "mean": 0.9459576712911201,
            "two_sigma": 0.00024343125628671956,
            "pooled_variance": 0.05112173567755423,
            "expected_bootstrap_se": 0.0017204332950417004,
            "ratio": 0.07074707778217557,
            "structural_zero_in_pooled_sample": false
          },
          "P_meson": {
            "mean": 0.0,
            "two_sigma": 0.0,
            "pooled_variance": 0.0,
            "expected_bootstrap_se": 0.0,
            "ratio": null,
            "structural_zero_in_pooled_sample": true
          },
          "P_BBbar": {
            "mean": 0.05404232870887991,
            "two_sigma": 0.0002434312562867099,
            "pooled_variance": 0.05112173567755423,
            "expected_bootstrap_se": 0.0017204332950417004,
            "ratio": 0.07074707778217276,
            "structural_zero_in_pooled_sample": false
          },
          "P_other": {
            "mean": 0.0,
            "two_sigma": 0.0,
            "pooled_variance": 0.0,
            "expected_bootstrap_se": 0.0,
            "ratio": null,
            "structural_zero_in_pooled_sample": true
          },
          "P_stretched": {
            "mean": 0.9459576712911201,
            "two_sigma": 0.00024343125628671956,
            "pooled_variance": 0.05112173567755423,
            "expected_bootstrap_se": 0.0017204332950417004,
            "ratio": 0.07074707778217557,
            "structural_zero_in_pooled_sample": false
          },
          "P_short": {
            "mean": 0.0,
            "two_sigma": 0.0,
            "pooled_variance": 0.0,
            "expected_bootstrap_se": 0.0,
            "ratio": null,
            "structural_zero_in_pooled_sample": true
          },
          "E2_l1": {
            "mean": 0.000271660393997134,
            "two_sigma": 3.5698232666012094e-08,
            "pooled_variance": 0.0002036714918533686,
            "expected_bootstrap_se": 0.00010859258357589412,
            "ratio": 0.00016436772885628515,
            "structural_zero_in_pooled_sample": false
          },
          "E2_l2": {
            "mean": 0.7470117356660314,
            "two_sigma": 3.9268055932000525e-07,
            "pooled_variance": 0.0022322684800646143,
            "expected_bootstrap_se": 0.0003595077499763049,
            "ratio": 0.0005461364314759372,
            "structural_zero_in_pooled_sample": false
          },
          "E2_l3": {
            "mean": 0.75,
            "two_sigma": 2.1075541217829818e-17,
            "pooled_variance": 0.0,
            "expected_bootstrap_se": 0.0,
            "ratio": null,
            "structural_zero_in_pooled_sample": true
          },
          "E2_l4": {
            "mean": 0.75,
            "two_sigma": 2.1075541217829818e-17,
            "pooled_variance": 0.0,
            "expected_bootstrap_se": 0.0,
            "ratio": null,
            "structural_zero_in_pooled_sample": true
          },
          "n_v1": {
            "mean": 0.9996377861413371,
            "two_sigma": 4.7597643564595385e-08,
            "pooled_variance": 0.0003620826521837664,
            "expected_bootstrap_se": 0.00014479011143452548,
            "ratio": 0.00016436772889051607,
            "structural_zero_in_pooled_sample": false
          },
          "n_v2": {
            "mean": 0.9956534336960459,
            "two_sigma": 5.711717227248832e-07,
            "pooled_variance": 0.004327673574850658,
            "expected_bootstrap_se": 0.0005005670876603063,
            "ratio": 0.0005705246477496045,
            "structural_zero_in_pooled_sample": false
          },
          "n_v3": {
            "mean": 0.028180269698544425,
            "two_sigma": 0.0003156283495770336,
            "pooled_variance": 0.05158199707105336,
            "expected_bootstrap_se": 0.0017281606803844717,
            "ratio": 0.0913191560135526,
            "structural_zero_in_pooled_sample": false
          },
          "n_v4": {
            "mean": 1.9240799647260758,
            "two_sigma": 0.000261928471025897,
            "pooled_variance": 0.14607619644346512,
            "expected_bootstrap_se": 0.0029082033443886012,
            "ratio": 0.045032695449458475,
            "structural_zero_in_pooled_sample": false
          },
          "dC": {
            "mean": -0.002716603939971307,
            "two_sigma": 3.569823266049704e-07,
            "pooled_variance": 0.002437563557982471,
            "expected_bootstrap_se": 0.00037567562510631487,
            "ratio": 0.0004751204267031507,
            "structural_zero_in_pooled_sample": false
          }
        }
      }
    },
    "not_run": [
      "post-fix tests; BUILD blocked",
      "R8 post-fix acceptance"
    ],
    "raw_direct_seeds": [
      500,
      501
    ],
    "shots_shift": 1024,
    "r0_resources": {
      "n_2q": 0,
      "depth_2q": 0,
      "depth": 1
    }
  },
  "equal-seed-control.json": {
    "source": "EMULATED",
    "r": 0,
    "shots": 4000,
    "runtime_seeds": [
      500,
      500,
      500,
      500,
      500
    ],
    "counts": {
      "omitted_from_drafting_input": true,
      "items": 5,
      "reason": "full data retained in cited evidence file"
    },
    "distinct": 1,
    "distinctness_check_rejected": true,
    "simulator_seed_option_before": 101,
    "simulator_seed_option_after": 500,
    "scope": "independent pre-fix r0 control; not the post-fix R8 r0/r1 controls"
  },
  "oracle-diagnostics.json": {
    "physical_code_count": 82,
    "vacuum_occupations": [
      0,
      2,
      0,
      2
    ],
    "non_N4_meson_codes": [],
    "singleton_closure_failures": [],
    "survival_occupation_codes": [
      {
        "code": 2058,
        "links": [
          0.5,
          0.0,
          0.0,
          0.0
        ],
        "occupations": [
          1,
          1,
          0,
          2
        ]
      },
      {
        "code": 3793,
        "links": [
          0.0,
          0.5,
          0.5,
          0.5
        ],
        "occupations": [
          1,
          1,
          0,
          2
        ]
      }
    ],
    "invalid_input": {
      "code": 1,
      "decode_is_none": true,
      "residual": 0.0
    },
    "empty_physical_yield": {
      "exception": "ZeroDivisionError",
      "message": "division by zero"
    },
    "empty_postselect": [
      {},
      0.0
    ],
    "interpretation": "Finite code inspection only; no channel-definition amendment or gate sign-off."
  }
}

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py
1|"""Exact gauge-invariant block unitaries and Strang circuits for L12 (G3).
2|
3|Method (structure, not generic 12-qubit synthesis):
4|  * Each Hamiltonian group T in {D, h0..h3, B} is an 82x82 matrix from the
5|    verified route-1 Hamiltonian (term split checked exact by the dynamics
6|    lane).  Lifted to the 4096-dim code space it is E T E^dag: zero on every
7|    unphysical code, so exp(-i theta E T E^dag) is the identity on the
8|    complement -> gauge invariance by construction, zero leakage.
9|  * D is diagonal: a 12-qubit Diagonal gate (phases on the 82 codes, 1 else).
10|  * Each h_l and B act non-trivially on a SUPPORT of s < 12 qubits (found
11|    numerically as the qubits whose bits ever change or on which the matrix
12|    element depends); the lifted operator factorizes as U_s (x) I on the rest
13|    when all elements depend only on the support bits.  For links whose
14|    Jordan-Wigner string crosses other vertices, the sign depends on the
15|    parity (a XOR b) of those vertices; the support then includes those
16|    (a,b) pairs.  U_s = expm(-i theta M_s) on 2^s dims (s <= 10), built as a
17|    UnitaryGate.  Exactness is verified by tests to 1e-12.
18|  * Strang step: D/2 . [h0,h2]/2 . [h1,h3]/2 . B . [h1,h3]/2 . [h0,h2]/2 . D/2
19|    (l0=(v0,v1), l2=(v3,v2) disjoint; l1=(v1,v2), l3=(v0,v3) disjoint).
20|
21|Verification helpers avoid dense 4096x4096 operators: the circuit is applied
22|to statevectors on the 82 codes with Aer/Statevector, and compared with the
23|exact 82-dim propagator.
24|"""
25|from __future__ import annotations
26|
27|import json
28|from functools import lru_cache
29|from pathlib import Path
30|
31|import numpy as np
32|from qiskit import QuantumCircuit, transpile
33|from qiskit.circuit.library import Diagonal, UnitaryGate
34|from qiskit.quantum_info import Statevector
35|from scipy.linalg import expm
36|
37|from su2qc.encodings.l12 import encode, physical_codes
38|
39|N = 4096
40|NQ = 12
41|GROUPS = ("D", "h0", "h1", "h2", "h3", "B")
42|RUN = Path(__file__).resolve().parents[3]
43|STRETCHED = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)
44|
45|
46|def params(g2=None, m=None):
47|    vals = {"g2": 4.0, "m": 0.75, "dt": 0.8333333333333334, "r_max": 3}
48|    p = RUN / "physics" / "window.json"
49|    if p.exists():
50|        w = json.loads(p.read_text())
51|        vals.update({k: w[k] for k in ("g2", "m", "dt", "r_max") if k in w})
52|    if g2 is not None:
53|        vals["g2"] = g2
54|    if m is not None:
55|        vals["m"] = m
56|    return vals
57|
58|
59|@lru_cache(maxsize=8)
60|def terms(g2, m):
61|    """(basis, {group: 82x82 ndarray}) from the dynamics-lane exact split."""
62|    from su2qc.dynamics.scan import _term_split
63|    Hd, D, hs, B, basis = _term_split(float(g2), float(m))
64|    return basis, {"D": D, "h0": hs[0], "h1": hs[1], "h2": hs[2],
65|                   "h3": hs[3], "B": B, "H": Hd}
66|
67|
68|@lru_cache(maxsize=1)
69|def code_index():
70|    codes = physical_codes()
71|    return codes, {c: i for i, c in enumerate(codes)}
72|
73|
74|def basis_to_code(basis):
75|    return np.array([encode(lab) for lab in basis])
76|
77|
78|# ------------------------------------------------------------ support search
79|
80|def _support(M, codes_of_basis):
81|    """Minimal-ish qubit set S such that M[i,j] (including zeros) is a
82|    function of the support bits of codes i and j only.  Greedy: start with
83|    the bits that flip on any nonzero element, then add the single bit that
84|    removes the most conflicts until none remain."""
85|    nz = np.argwhere(np.abs(M) > 1e-14)
86|    S = set()
87|    for i, j in nz:
88|        S |= {q for q in range(NQ)
89|              if (codes_of_basis[i] >> q) & 1 != (codes_of_basis[j] >> q) & 1}
90|    n = len(codes_of_basis)
91|
92|    def n_conflicts(S):
93|        Sl = sorted(S)
94|        rest = [q for q in range(NQ) if q not in S]
95|        pat = np.array([sum(((c >> q) & 1) << k for k, q in enumerate(Sl))
96|                        for c in codes_of_basis])
97|        off = np.array([sum(((c >> q) & 1) << k for k, q in enumerate(rest))
98|                        for c in codes_of_basis])
99|        seen = {}
100|        bad = 0
101|        for i in range(n):
102|            for j in range(n):
103|                if off[i] != off[j]:
104|                    continue  # U_S (x) I gives 0 here, and so does M
105|                key = (pat[i], pat[j])
106|                v = complex(M[i, j])
107|                if key in seen:
108|                    if abs(seen[key] - v) > 1e-12:
109|                        bad += 1
110|                else:
111|                    seen[key] = v
112|        return bad
113|
114|    while n_conflicts(S) > 0:
115|        best = None
116|        for q in range(NQ):
117|            if q in S:
118|                continue
119|            c = n_conflicts(S | {q})
120|            if best is None or c < best[0]:
121|                best = (c, q)
122|        S.add(best[1])
123|    return sorted(S)
124|
125|
126|def local_matrix(M, codes_of_basis, S):
127|    """2^|S| x 2^|S| Hermitian matrix acting on support S (sorted)."""
128|    d = 1 << len(S)
129|    L = np.zeros((d, d), complex)
130|    for i, j in np.argwhere(np.abs(M) > 1e-14):
131|        x = sum(((codes_of_basis[i] >> q) & 1) << k for k, q in enumerate(S))
132|        y = sum(((codes_of_basis[j] >> q) & 1) << k for k, q in enumerate(S))
133|        L[x, y] = M[i, j]
134|    assert np.max(np.abs(L - L.conj().T)) < 1e-13
135|    return L
136|
137|
138|@lru_cache(maxsize=8)
139|def supports(g2, m):
140|    basis, T = terms(g2, m)
141|    cb = basis_to_code(basis)
142|    return {g: _support(T[g], cb) for g in ("h0", "h1", "h2", "h3", "B")}
143|
144|
145|# ------------------------------------------------------------ circuits
146|
147|@lru_cache(maxsize=64)
148|def unitary(group, theta, g2, m):
149|    """12-qubit circuit for exp(-i theta E T_group E^dag)."""
150|    basis, T = terms(g2, m)
151|    cb = basis_to_code(basis)
152|    qc = QuantumCircuit(NQ, name=f"U_{group}")
153|    if group == "D":
154|        diag = np.ones(N, complex)
155|        diag[cb] = np.exp(-1j * theta * np.real(np.diag(T["D"])))
156|        qc.append(Diagonal(diag), range(NQ))
157|        return qc
158|    S = supports(g2, m)[group]
159|    L = local_matrix(T[group], cb, S)
160|    U = expm(-1j * theta * L)
161|    qc.append(UnitaryGate(U, label=f"U_{group}"), S)
162|    return qc
163|
164|
165|def strang_step(dt, g2, m):
166|    qc = QuantumCircuit(NQ)
167|    seq = (("D", dt / 2), ("h0", dt / 2), ("h2", dt / 2), ("h1", dt / 2),
168|           ("h3", dt / 2), ("B", dt), ("h3", dt / 2), ("h1", dt / 2),
169|           ("h2", dt / 2), ("h0", dt / 2), ("D", dt / 2))
170|    for g, th in seq:
171|        qc.compose(unitary(g, float(th), g2, m), inplace=True)
172|    return qc
173|
174|
175|def prep_stretched(qc=None):
176|    qc = qc or QuantumCircuit(NQ)
177|    code = encode(STRETCHED)
178|    for q in range(NQ):
179|        if (code >> q) & 1:
180|            qc.x(q)
181|    return qc
182|
183|
184|def full_circuit(r, dt=None, g2=None, m=None, merge_D=True):
185|    p = params(g2, m)
186|    dt = p["dt"] if dt is None else dt
187|    qc = prep_stretched()
188|    if r == 0:
189|        return qc
190|    if not merge_D:
191|        for _ in range(r):
192|            qc.compose(strang_step(dt, p["g2"], p["m"]), inplace=True)
193|        return qc
194|    # merged adjacent D half-steps: D/2 [core] D [core] ... D/2
195|    core = (("h0", dt / 2), ("h2", dt / 2), ("h1", dt / 2), ("h3", dt / 2),
196|            ("B", dt), ("h3", dt / 2), ("h1", dt / 2), ("h2", dt / 2),
197|            ("h0", dt / 2))
198|    qc.compose(unitary("D", dt / 2, p["g2"], p["m"]), inplace=True)
199|    for k in range(r):
200|        for g, th in core:
201|            qc.compose(unitary(g, float(th), p["g2"], p["m"]), inplace=True)
202|        qc.compose(unitary("D", dt / 2 if k == r - 1 else dt, p["g2"], p["m"]),
203|                   inplace=True)
204|    return qc
205|
206|
207|# ------------------------------------------------------------ exact references
208|
209|def exact_strang_matrix(dt, g2, m):
210|    """Exact matrix of ONE Strang step in the circuit's group ordering:
211|    D/2 . h0/2 . h2/2 . h1/2 . h3/2 . B . h3/2 . h1/2 . h2/2 . h0/2 . D/2
212|    (h0,h2 commute; h1,h3 commute)."""
213|    _, T = terms(g2, m)
214|    order = ["h0", "h2", "h1", "h3"]
215|    U = expm(-1j * T["D"] * dt / 2)
216|    for g in order:
217|        U = expm(-1j * T[g] * dt / 2) @ U
218|    U = expm(-1j * T["B"] * dt) @ U
219|    for g in reversed(order):
220|        U = expm(-1j * T[g] * dt / 2) @ U
221|    U = expm(-1j * T["D"] * dt / 2) @ U
222|    return U
223|
224|
225|def circuit_state(qc):
226|    """Statevector (4096) of a circuit from |0...0>."""
227|    return Statevector(qc).data
228|
229|
230|def to_basis(vec4096, basis):
231|    cb = basis_to_code(basis)
232|    return vec4096[cb]
233|
234|
235|def leakage_prob(vec4096):
236|    codes, _ = code_index()
237|    mask = np.ones(N, bool)
238|    mask[codes] = False
239|    return float(np.sum(np.abs(vec4096[mask]) ** 2))
240|
241|
242|# ------------------------------------------------------------ resources
243|
244|def resources(circ):
245|    t = transpile(circ, basis_gates=["cz", "rz", "sx", "x", "id"],
246|                  optimization_level=1, seed_transpiler=7)
247|    n2 = sum(1 for inst in t.data if inst.operation.num_qubits == 2)
248|    return {"n_2q": int(n2),
249|            "depth_2q": int(t.depth(lambda x: x.operation.num_qubits == 2)),
250|            "depth": int(t.depth())}

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py
1|"""Structured synthesis of the L12 block unitaries.
2|
3|The implementation deliberately keeps the code-space structure visible: the
4|small connected components of each local matrix are synthesized independently
5|and the diagonal term is a degree-three phase polynomial.
6|"""
7|from __future__ import annotations
8|
9|from functools import lru_cache
10|import json
11|from pathlib import Path
12|
13|import numpy as np
14|from qiskit import QuantumCircuit, transpile
15|from qiskit.circuit.library import PhaseGate, UnitaryGate
16|from scipy.linalg import expm
17|
18|from su2qc.circuits import strang_l12 as sl
19|from su2qc.encodings.l12 import encode, physical_codes
20|
21|NQ = 12
22|GROUPS = sl.GROUPS
23|_LINK_REP = (1, 4, 7, 10)  # one copy of links 0,1,2,3
24|
25|
26|def _local_patterns(codes, support):
27|    return {sum(((c >> q) & 1) << k for k, q in enumerate(support)) for c in codes}
28|
29|
30|def _gray_map(x, y, target, n):
31|    """CNOT sequence making x,y differ only on target (self-inverse)."""
32|    return [(target, q) for q in range(n) if q != target and ((x >> q) & 1) != ((y >> q) & 1)]
33|
34|
35|def _mapped_pattern(p, cnots, target):
36|    for c, t in cnots:
37|        if (p >> c) & 1:
38|            p ^= 1 << t
39|    return p
40|
41|
42|def _minimal_controls(x, y, target, cnots, physical):
43|    """Smallest control set (exhaustive over subsets, |support| <= 8) such
44|    that no OTHER physical local pattern matches the selected pattern on
45|    the controls after the Gray-code CNOT conjugation."""
46|    from itertools import combinations
47|    mx = _mapped_pattern(x, cnots, target)
48|    n = max(max(physical).bit_length(), target + 1)
49|    fixed = {q: (mx >> q) & 1 for q in range(n) if q != target}
50|    others = [_mapped_pattern(z, cnots, target) for z in physical if z not in (x, y)]
51|    cand = sorted(fixed)
52|    for k in range(len(cand) + 1):
53|        for sub in combinations(cand, k):
54|            if not any(all(((mz >> q) & 1) == fixed[q] for q in sub) for mz in others):
55|                return sorted(sub), fixed
56|    return cand, fixed
57|
58|
59|def _mc_single_qubit(u, k):
60|    """Multi-controlled single-qubit unitary as a controlled UGate (ZYZ
61|    angles + phase), which qiskit synthesizes far more cheaply than a
62|    controlled generic UnitaryGate."""
63|    from qiskit.circuit.library import UGate
64|    from qiskit.synthesis.one_qubit import OneQubitEulerDecomposer
65|    theta, phi, lam, phase = OneQubitEulerDecomposer("U").angles_and_phase(np.asarray(u, complex))
66|    g = UGate(theta, phi, lam)
67|    if abs(phase) > 1e-14:
68|        # global phase of the target block becomes a controlled phase
69|        from qiskit.circuit.library import PhaseGate
70|        from qiskit import QuantumCircuit
71|        sub = QuantumCircuit(1, name="u_ph")
72|        sub.append(g, [0])
73|        sub.global_phase = phase
74|        return sub.to_gate().control(k) if k else sub.to_gate()
75|    return g.control(k) if k else g
76|
77|
78|def _two_level(qc, support, x, y, mat, physical):
79|    """Apply a 2x2 unitary on local patterns x,y using a Gray path."""
80|    n = len(support)
81|    differing = [q for q in range(n) if ((x >> q) & 1) != ((y >> q) & 1)]
82|    if not differing:
83|        raise ValueError("two-level states must differ")
84|    # choose the target (and Gray path) giving the fewest controls
85|    best = None
86|    for tgt in differing:
87|        cn = _gray_map(x, y, tgt, n)
88|        ctr, fx = _minimal_controls(x, y, tgt, cn, physical)
89|        score = (len(ctr), len(cn))
90|        if best is None or score < best[0]:
91|            best = (score, tgt, cn, ctr, fx)
92|    _, target, cnots, controls, fixed = best
93|    for c, t in cnots:
94|        qc.cx(support[c], support[t])
95|    # Transform the pair's matrix into computational target order.
96|    if ((x >> target) & 1) == 0:
97|        u = np.asarray(mat, complex)
98|    else:
99|        u = np.asarray([[mat[1, 1], mat[1, 0]], [mat[0, 1], mat[0, 0]]], complex)
100|    for q in controls:
101|        if not fixed[q]:
102|            qc.x(support[q])
103|    cq = [support[q] for q in controls]
104|    tq = support[target]
105|    # Zero-diagonal real couplings give exp(-i a X) = RX(2a): use the
106|    # specialised multi-controlled RX synthesis (much cheaper than a
107|    # generic controlled unitary).
108|    if (abs(u[0, 0] - u[1, 1]) < 1e-13 and abs(u[0, 1] - u[1, 0]) < 1e-13
109|            and abs(u[0, 0].imag) < 1e-13 and abs(u[0, 1].real) < 1e-13):
110|        ang = 2.0 * np.arctan2(-u[0, 1].imag, u[0, 0].real)
111|        if controls:
112|            qc.mcrx(ang, cq, tq)
113|        else:
114|            qc.rx(ang, tq)
115|    else:
116|        gate = _mc_single_qubit(u, len(controls))
117|        qc.append(gate, cq + [tq])
118|    for q in reversed(controls):
119|        if not fixed[q]:
120|            qc.x(support[q])
121|    for c, t in reversed(cnots):
122|        qc.cx(support[c], support[t])
123|
124|
125|def _givens_decomposition(v):
126|    """Return (diagonal, factors) with v=factors[0]...D."""
127|    a = np.array(v, complex)
128|    factors = []
129|    for i, j, col in ((0, 1, 0), (0, 2, 0), (1, 2, 1)):
130|        aa, bb = a[i, col], a[j, col]
131|        r = np.hypot(abs(aa), abs(bb))
132|        if r < 1e-14:
133|            continue
134|        g = np.eye(3, dtype=complex)
135|        g[np.ix_([i, j], [i, j])] = [[np.conj(aa) / r, np.conj(bb) / r],
136|                                      [-bb / r, aa / r]]
137|        a = g @ a
138|        factors.append((i, j, g[np.ix_([i, j], [i, j])]))
139|    # Numerical phases are retained; tiny off-diagonals are roundoff.
140|    if np.max(np.abs(a - np.diag(np.diag(a)))) > 2e-10:
141|        raise ArithmeticError("Givens elimination failed")
142|    return np.diag(a), factors
143|
144|
145|def _phase_on_pattern(qc, support, pattern, phase, physical):
146|    if abs(phase) < 1e-15:
147|        return
148|    # Use the last support bit as target and retain only controls necessary to
149|    # distinguish this physical local pattern.
150|    target = len(support) - 1
151|    controls = [q for q in range(len(support)) if q != target]
152|    for q in list(controls):
153|        trial = [z for z in controls if z != q]
154|        if not any(z != pattern and all(((z >> k) & 1) == ((pattern >> k) & 1) for k in trial + [target]) for z in physical):
155|            controls.remove(q)
156|    # X target turns the desired target value into 1; PhaseGate then phases it.
157|    if not ((pattern >> target) & 1):
158|        qc.x(support[target])
159|    fixed = {q: (pattern >> q) & 1 for q in controls}
160|    for q in controls:
161|        if not fixed[q]:
162|            qc.x(support[q])
163|    qc.append(PhaseGate(phase).control(len(controls)), [support[q] for q in controls] + [support[target]])
164|    for q in reversed(controls):
165|        if not fixed[q]:
166|            qc.x(support[q])
167|    if not ((pattern >> target) & 1):
168|        qc.x(support[target])
169|
170|
171|def _component_patterns(L):
172|    n = len(L)
173|    todo = set(range(n))
174|    out = []
175|    while todo:
176|        root = todo.pop(); comp = {root}; stack = [root]
177|        while stack:
178|            i = stack.pop()
179|            for j in np.flatnonzero(np.abs(L[i]) > 1e-13):
180|                j = int(j)
181|                if j in todo:
182|                    todo.remove(j); comp.add(j); stack.append(j)
183|        out.append(sorted(comp))
184|    return out
185|
186|
187|def _synth_local(group, theta, g2, m):
188|    basis, terms = sl.terms(float(g2), float(m))
189|    cb = sl.basis_to_code(basis)
190|    support = sl.supports(float(g2), float(m))[group]
191|    L = sl.local_matrix(terms[group], cb, support)
192|    physical = _local_patterns(physical_codes(), support)
193|    qc = QuantumCircuit(NQ, name=f"synth_{group}")
194|    for comp in _component_patterns(L):
195|        if len(comp) not in (2, 3):
196|            if len(comp) == 1:
197|                continue
198|            raise ValueError(f"unexpected component size {len(comp)}")
199|        if len(comp) == 2:
200|            _two_level(qc, support, comp[0], comp[1], expm(-1j * theta * L[np.ix_(comp, comp)]), physical)
201|            continue
202|        v = expm(-1j * theta * L[np.ix_(comp, comp)])
203|        diag, factors = _givens_decomposition(v)
204|        for k, p in enumerate(comp):
205|            _phase_on_pattern(qc, support, p, np.angle(diag[k]), physical)
206|        # v = E1^dag E2^dag E3^dag D; append in reverse elimination order.
207|        for i, j, g in reversed(factors):
208|            mat = g.conj().T
209|            _two_level(qc, support, comp[i], comp[j], mat, physical)
210|    return qc
211|
212|
213|def _bit_polynomial(g2, m):
214|    p = {(): 0.0}
215|    for q in _LINK_REP:
216|        p[(q,)] = p.get((q,), 0.0) + 3.0 * float(g2) / 8.0
217|    parity = (1, -1, 1, -1)
218|    for v in range(4):
219|        a, b, c = 3*v, 3*v+1, 3*v+2
220|        for key, val in [((c,), 2.0), ((a,), 1.0), ((b,), 1.0),
221|                         ((a,b), -2.0), ((a,c), -2.0), ((b,c), -2.0), ((a,b,c), 4.0)]:
222|            p[tuple(sorted(key))] = p.get(tuple(sorted(key)), 0.0) + float(m) * parity[v] * val
223|    return p
224|
225|
226|def _diagonal(qc, theta, g2, m):
227|    # Convert bit monomials to Z monomials: bit=(1-Z)/2.
228|    zpoly = {}
229|    for bits, coeff in _bit_polynomial(g2, m).items():
230|        k = len(bits)
231|        for mask in range(1 << k):
232|            zs = tuple(bits[i] for i in range(k) if (mask >> i) & 1)
233|            zpoly[zs] = zpoly.get(zs, 0.0) + coeff * (2.0 ** -k) * (-1.0) ** len(zs)
234|    qc.global_phase += -theta * zpoly.pop((), 0.0)
235|    for qs, coeff in zpoly.items():
236|        if abs(coeff) < 1e-14:
237|            continue
238|        if len(qs) == 1:
239|            qc.rz(2.0 * theta * coeff, qs[0])
240|        else:
241|            for q in qs[:-1]:
242|                qc.cx(q, qs[-1])
243|            qc.rz(2.0 * theta * coeff, qs[-1])
244|            for q in reversed(qs[:-1]):
245|                qc.cx(q, qs[-1])
246|
247|
248|@lru_cache(maxsize=64)
249|def synth_unitary(group, theta, g2, m):
250|    """Synthesize one exact L12 block using only one-qubit and controlled gates."""
251|    theta, g2, m = float(theta), float(g2), float(m)
252|    if group not in GROUPS:
253|        raise ValueError(group)
254|    qc = QuantumCircuit(NQ, name=f"synth_{group}")
255|    if group == "D":
256|        _diagonal(qc, theta, g2, m)
257|    else:
258|        qc.compose(_synth_local(group, theta, g2, m), inplace=True)
259|    return qc
260|
261|
262|def synth_strang_step(dt, g2, m):
263|    qc = QuantumCircuit(NQ)
264|    seq = (("D", dt/2), ("h0", dt/2), ("h2", dt/2), ("h1", dt/2), ("h3", dt/2),
265|           ("B", dt), ("h3", dt/2), ("h1", dt/2), ("h2", dt/2), ("h0", dt/2), ("D", dt/2))
266|    for group, theta in seq:
267|        qc.compose(synth_unitary(group, theta, g2, m), inplace=True)
268|    return qc
269|
270|
271|def synth_full_circuit(r, dt=None, g2=None, m=None, merge_D=True):
272|    p = sl.params(g2, m); dt = p["dt"] if dt is None else dt
273|    qc = sl.prep_stretched()
274|    if r == 0:
275|        return qc
276|    if not merge_D:
277|        for _ in range(r):
278|            qc.compose(synth_strang_step(dt, p["g2"], p["m"]), inplace=True)
279|        return qc
280|    core = (("h0", dt/2), ("h2", dt/2), ("h1", dt/2), ("h3", dt/2), ("B", dt),
281|            ("h3", dt/2), ("h1", dt/2), ("h2", dt/2), ("h0", dt/2))
282|    qc.compose(synth_unitary("D", dt/2, p["g2"], p["m"]), inplace=True)
283|    for k in range(r):
284|        for group, theta in core:
285|            qc.compose(synth_unitary(group, theta, p["g2"], p["m"]), inplace=True)
286|        qc.compose(synth_unitary("D", dt/2 if k == r-1 else dt, p["g2"], p["m"]), inplace=True)
287|    return qc
288|
289|
290|def _resources(circ):
291|    t = transpile(circ, basis_gates=["cz", "rz", "sx", "x", "id"], optimization_level=3, seed_transpiler=7)
292|    return {"n_2q": sum(x.operation.num_qubits == 2 for x in t.data),
293|            "depth_2q": t.depth(lambda x: x.operation.num_qubits == 2), "depth": t.depth()}
294|
295|
296|def write_resources(path="circuits/resources_synth.md"):
297|    p = sl.params(); rows = []
298|    for g in GROUPS:
299|        rows.append((f"group {g} (theta={p['dt']/2:.4f})", _resources(synth_unitary(g, p['dt']/2, p['g2'], p['m']))))
300|    rows.append(("one Strang step", _resources(synth_strang_step(p['dt'], p['g2'], p['m']))))
301|    for r in range(4):
302|        rows.append((f"full circuit r={r} (prep + steps, merged D)", _resources(synth_full_circuit(r))))
303|    out = ["# Synthesized resources, L12 encoding", "", f"Window: g2={p['g2']}, m={p['m']}, dt={p['dt']:.4f}.", "",
304|           "| circuit | 2q count | 2q depth | total depth |", "|---|---:|---:|---:|"]
305|    out += [f"| {name} | {r['n_2q']} | {r['depth_2q']} | {r['depth']} |" for name, r in rows]
306|    Path(path).write_text("\n".join(out) + "\n")
307|    return rows

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py
1|"""Phase 4: route logical L12 circuits to a Heron-class target and verify.
2|
3|  route(circ, backend, opt=3, seed=7) -> (isa_circ, layout_info)
4|  routed_equivalence(logical, isa) -> 1 - |<psi_routed|psi_logical>| including
5|        the final layout permutation (statevector on the 12 logical qubits).
6|  routed_resources(isa) -> dict(n_2q, depth_2q, depth)
7|  pyzx_tp(circ) -> circuit after the monograph's topology-preserving PyZX pass
8|        (reused from the repo's src/su2zx/compiler_study.py if importable).
9|"""
10|from __future__ import annotations
11|
12|import json
13|import os
14|import sys
15|
16|import numpy as np
17|from qiskit import QuantumCircuit, transpile
18|from qiskit.quantum_info import Statevector
19|from qiskit.transpiler import CouplingMap
20|
21|RUN = os.path.dirname(os.path.dirname(os.path.dirname(
22|    os.path.dirname(os.path.abspath(__file__)))))
23|REPO = os.path.dirname(os.path.dirname(RUN))
24|if os.path.join(REPO, "src") not in sys.path:
25|    sys.path.insert(0, os.path.join(REPO, "src"))
26|
27|NATIVE = ["cz", "rz", "sx", "x", "id"]
28|
29|
30|def fake_heron():
31|    from qiskit_ibm_runtime.fake_provider import FakeTorino
32|    return FakeTorino()
33|
34|
35|def route(circ, backend=None, opt=3, seed=7, initial_layout=None):
36|    backend = backend or fake_heron()
37|    isa = transpile(circ, backend=backend, optimization_level=opt,
38|                    seed_transpiler=seed, initial_layout=initial_layout)
39|    lay = isa.layout
40|    init = [lay.initial_layout[q] for q in circ.qubits] if lay else list(range(12))
41|    final = None
42|    if lay is not None and lay.final_layout is not None:
43|        fl = lay.final_layout
44|        final = [fl[q] for q in isa.qubits]
45|    return isa, {"initial_physical": [int(x) for x in init],
46|                 "final_index_layout": [int(x) for x in isa.layout.final_index_layout()]
47|                 if lay else list(range(12))}
48|
49|
50|def routed_resources(isa):
51|    n2 = sum(1 for inst in isa.data if inst.operation.num_qubits == 2
52|             and inst.operation.name != "barrier")
53|    return {"n_2q": int(n2),
54|            "depth_2q": int(isa.depth(lambda x: x.operation.num_qubits == 2)),
55|            "depth": int(isa.depth())}
56|
57|
58|def routed_equivalence(logical, isa):
59|    """1 - |<routed|logical>| with the routed state pulled back through
60|    final_index_layout to the logical qubit order (statevector, no measure)."""
61|    from qiskit.quantum_info import Operator
62|    psi_l = Statevector(logical).data
63|    # reduce ISA circuit to only its active physical qubits
64|    fil = isa.layout.final_index_layout()
65|    active = sorted({isa.find_bit(q).index for inst in isa.data for q in inst.qubits}
66|                    | set(int(x) for x in fil))
67|    idx = {p: k for k, p in enumerate(active)}
68|    small = QuantumCircuit(len(active))
69|    for inst in isa.data:
70|        if inst.operation.name in ("barrier", "measure", "delay"):
71|            continue
72|        small.append(inst.operation, [idx[isa.find_bit(q).index] for q in inst.qubits])
73|    psi_r = Statevector(small).data
74|    # logical qubit i sits at physical fil[i]
75|    order = [idx[fil[i]] for i in range(logical.num_qubits)]  # small-qubit per logical
76|    # permute psi_r so that qubit k of result = logical k
77|    n = len(active)
78|    psi_r = psi_r.reshape([2] * n)  # axis 0 = qubit n-1 (qiskit little endian)
79|    # axes: qiskit bit q corresponds to axis n-1-q
80|    perm_axes = [n - 1 - order[i] for i in range(logical.num_qubits)][::-1]
81|    rest = [a for a in range(n) if a not in perm_axes]
82|    psi_r = np.transpose(psi_r, rest + perm_axes).reshape(-1, 2 ** logical.num_qubits)
83|    # idle ancilla qubits are |0>: take the row where rest-axes are all zero
84|    vec = psi_r[0]
85|    return float(1.0 - abs(np.vdot(vec, psi_l)))
86|
87|
88|def pyzx_pass(circ, strategy="basic"):
89|    """The monograph's PyZX pipeline (repo src/su2zx/core.py) with its dense
90|    12-qubit Operator equivalence check replaced by a statevector check on
91|    the 82 physical codes (done by the caller via routed_equivalence-style
92|    comparison). strategy: 'basic' (topology-preserving), 'full_reduce'."""
93|    from qiskit import qasm2
94|    import pyzx as zx
95|    denominator = zx.settings.float_to_fraction_max_denominator
96|    try:
97|        zx.settings.float_to_fraction_max_denominator = 2 ** 40
98|        zxc = zx.Circuit.from_qasm(qasm2.dumps(circ))
99|    finally:
100|        zx.settings.float_to_fraction_max_denominator = denominator
101|    if strategy == "basic":
102|        cand = zx.optimize.basic_optimization(zxc.copy(), do_swaps=False, quiet=True)
103|    elif strategy == "full_reduce":
104|        g = zxc.to_graph()
105|        zx.simplify.full_reduce(g, quiet=True)
106|        cand = zx.extract.extract_circuit(g.copy(), up_to_perm=False,
107|                                          quiet=True).to_basic_gates()
108|    else:
109|        raise ValueError(strategy)
110|    return qasm2.loads(cand.to_qasm())
111|
112|
113|def state_equivalence(a, b):
114|    """1 - |<a|b>| for two same-width circuits from |0>."""
115|    va, vb = Statevector(a).data, Statevector(b).data
116|    return float(1.0 - abs(np.vdot(va, vb)))
117|
118|
119|if __name__ == "__main__":
120|    sys.path.insert(0, os.path.join(RUN, "src"))
121|    from su2qc.circuits import strang_l12 as sl
122|    b = fake_heron()
123|    qc = sl.full_circuit(1)
124|    isa, lay = route(qc, b)
125|    print(routed_resources(isa), lay)
126|    print("equiv", routed_equivalence(qc, isa))

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py
1|"""Phase 4 production: compile, route, PyZX comparison, twin run, decision inputs.
2|
3|Writes compile/resources_routed.{md,json}, compile/layout.json,
4|compile/twin_check.json, analysis/tables/twin_timeseries.csv.
5|"""
6|import json
7|import os
8|import sys
9|import time
10|
11|import numpy as np
12|
13|sys.path.insert(0, "src")
14|from qiskit import transpile  # noqa: E402
15|from su2qc.circuits import strang_l12 as sl  # noqa: E402
16|from su2qc.circuits import synth_l12 as sy  # noqa: E402
17|from su2qc.compile import route as rt  # noqa: E402
18|from su2qc.dynamics import scan  # noqa: E402
19|from su2qc.twin import twin  # noqa: E402
20|
21|P = sl.params()
22|G2, M, DT, RMAX = P["g2"], P["m"], P["dt"], P["r_max"]
23|os.makedirs("compile", exist_ok=True)
24|t0 = time.time()
25|backend = rt.fake_heron()
26|NATIVE = ["cz", "rz", "sx", "x", "id"]
27|
28|
29|def n2(c):
30|    return sum(1 for i in c.data if i.operation.num_qubits == 2 and i.operation.name != "barrier")
31|
32|
33|def d2(c):
34|    return int(c.depth(lambda x: x.operation.num_qubits == 2))
35|
36|
37|# ---------------------------------------------------------------- pipelines
38|rows = []
39|isa_by_r = {}
40|layout = None
41|logical = {r: sy.synth_full_circuit(r) for r in range(RMAX + 1)}
42|step_logical = sy.synth_strang_step(DT, G2, M)
43|
44|pipelines = {}
45|# Qiskit L3 (native synthesis + routing, seeded)
46|pipelines["qiskit_L3"] = lambda c: c
47|# PyZX passes are applied to the native-basis logical circuit before routing
48|def _zx(strategy):
49|    def f(c):
50|        flat = transpile(c, basis_gates=["cx", "rz", "sx", "x", "h", "s", "t", "tdg", "sdg"],
51|                         optimization_level=1, seed_transpiler=7)
52|        return rt.pyzx_pass(flat, strategy)
53|    return f
54|pipelines["pyzx_basic_TP"] = _zx("basic")
55|pipelines["pyzx_full_reduce"] = _zx("full_reduce")
56|
57|results = {}
58|for name, pre in pipelines.items():
59|    try:
60|        pre_step = pre(step_logical)
61|        eq_step = rt.state_equivalence(sl.prep_stretched().compose(step_logical),
62|                                       sl.prep_stretched().compose(pre_step)) \
63|            if name != "qiskit_L3" else 0.0
64|        isa_step, lay = rt.route(pre_step, backend, opt=3, seed=7)
65|        per_step = {"n_2q": n2(isa_step), "depth_2q": d2(isa_step)}
66|        full = {}
67|        for r in range(RMAX + 1):
68|            pre_full = pre(logical[r]) if r else logical[r]
69|            isa, layr = rt.route(pre_full, backend, opt=3, seed=7,
70|                                 initial_layout=lay["initial_physical"])
71|            full[r] = {"n_2q": n2(isa), "depth_2q": d2(isa),
72|                       "layout": layr}
73|            if name == "qiskit_L3":
74|                isa_by_r[r] = isa
75|        eq_full = rt.routed_equivalence(logical[RMAX], isa) if name == "qiskit_L3" else None
76|        results[name] = {"pre_route_equiv_step": eq_step, "per_step": per_step,
77|                         "full": {str(r): {k: v for k, v in full[r].items() if k != "layout"}
78|                                  for r in full},
79|                         "routed_equiv_rmax": eq_full}
80|        if name == "qiskit_L3":
81|            layout = full[RMAX]["layout"]
82|        print(name, "step", per_step, "full r=%d" % RMAX, full[RMAX]["n_2q"], full[RMAX]["depth_2q"],
83|              "eq", eq_step, eq_full, f"{time.time()-t0:.0f}s", flush=True)
84|    except Exception as e:  # noqa: BLE001
85|        results[name] = {"error": repr(e)}
86|        print(name, "FAILED", repr(e), flush=True)
87|
88|# routed equivalence of the chosen ISA circuits for every r (qiskit_L3)
89|eqs = {str(r): rt.routed_equivalence(logical[r], isa_by_r[r]) for r in range(RMAX + 1)}
90|print("routed equivalence per r:", eqs, flush=True)
91|
92|best_name = "qiskit_L3"
93|best = results[best_name]
94|chosen = {"encoding": "L12", "pipeline": best_name,
95|          "per_step_2q": best["per_step"]["n_2q"],
96|          "full_rmax_2q": best["full"][str(RMAX)]["n_2q"],
97|          "depth_2q_full_rmax": best["full"][str(RMAX)]["depth_2q"]}
98|json.dump({"chosen": chosen, "pipelines": results, "equivalence_rmax": eqs[str(RMAX)],
99|           "equivalence_per_r": eqs, "backend": backend.name,
100|           "notes": "structured synthesis (Gray-path multi-controlled RX on minimal "
101|                    "control sets, exact 3x3 Givens blocks, phase-polynomial D)"},
102|          open("compile/resources_routed.json", "w"), indent=1)
103|json.dump({"backend": backend.name, "initial_physical": layout["initial_physical"],
104|           "final_index_layout": layout["final_index_layout"], "seed_transpiler": 7,
105|           "optimization_level": 3}, open("compile/layout.json", "w"), indent=1)
106|
107|with open("compile/resources_routed.md", "w") as fh:
108|    fh.write("# Routed resources (FakeTorino, CZ-native), L12 structured synthesis\n\n")
109|    fh.write(f"Window g2={G2}, m={M}, dt={DT:.4f}, r_max={RMAX}. seed_transpiler=7, opt level 3.\n\n")
110|    fh.write("| pipeline | step CZ | step 2q-depth | full r=3 CZ | full r=3 2q-depth | pre-route equiv | routed equiv (r=3) |\n|---|---:|---:|---:|---:|---|---|\n")
111|    for nme, res in results.items():
112|        if "error" in res:
113|            fh.write(f"| {nme} | ERROR: {res['error']} |\n"); continue
114|        fh.write(f"| {nme} | {res['per_step']['n_2q']} | {res['per_step']['depth_2q']} | "
115|                 f"{res['full'][str(RMAX)]['n_2q']} | {res['full'][str(RMAX)]['depth_2q']} | "
116|                 f"{res['pre_route_equiv_step']:.1e} | {res['routed_equiv_rmax'] if res['routed_equiv_rmax'] is not None else 'n/a'} |\n")
117|    fh.write("\nBudget (prompt): ~250 CZ/step, ~1000 CZ/circuit, 2q depth < ~200 (+10% slack).\n")
118|    fh.write("Per-r routed CZ (qiskit_L3): " + ", ".join(
119|        f"r={r}: {results['qiskit_L3']['full'][str(r)]['n_2q']}" for r in range(RMAX + 1)) + "\n")
120|
121|# ---------------------------------------------------------------- twin run
122|sim = twin.twin_backend(seed=101)
123|times = [r * DT for r in range(RMAX + 1)]
124|exact = scan.timeseries_at(G2, M, 0.5, np.array(times), tag="exact_at_window")
125|REPEATS, SHOTS = 5, 4000
126|rows_tw = []
127|n_within = 0
128|yields = {}
129|for r in range(RMAX + 1):
130|    meas = twin.add_measurements(isa_by_r[r])
131|    counts = twin.run_counts([meas] * REPEATS, SHOTS, 500 + 10 * r, sim)
132|    mean, two_sig, y = twin.bootstrap(counts, n_boot=300, seed=r)
133|    yields[r] = y
134|    ok_all = True
135|    for key, exv in (("P_surv", exact["P_surv"][r]), ("n_v3", exact["n"][r][2]),
136|                     ("E2_l1", exact["E2"][r][0])):
137|        within = abs(mean[key] - exv) <= max(two_sig[key], 1e-12)
138|        ok_all &= within
139|        rows_tw.append((r, times[r], key, exv, mean[key], two_sig[key], int(within), y))
140|    n_within += int(ok_all)
141|    print(f"twin r={r} t={times[r]:.3f} yield={y:.3f} P_surv twin={mean['P_surv']:.3f}±{two_sig['P_surv']:.3f} exact={exact['P_surv'][r]:.3f} within={ok_all}", flush=True)
142|
143|os.makedirs("analysis/tables", exist_ok=True)
144|with open("analysis/tables/twin_timeseries.csv", "w") as fh:
145|    fh.write("r,t,observable,exact,twin_mean,twin_2sigma,within,yield\n")
146|    for row in rows_tw:
147|        fh.write(",".join(str(x) for x in row) + "\n")
148|json.dump({"yield_deepest": yields[RMAX], "yields": yields,
149|           "n_points_within_2sigma": n_within, "repeats": REPEATS, "shots": SHOTS,
150|           "mode": "twin", "backend": backend.name, "arm": "A0 (raw + post-selection)"},
151|          open("compile/twin_check.json", "w"), indent=1)
152|print("done", f"{time.time()-t0:.0f}s")

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/engine.py
1|"""Exact-dynamics engine for the 82-state (jmax=0.5) / 152-state (jmax=1) SU(2) plaquette.
2|
3|evolve(H, psi0, times) -> array of states (dense expm on 82-dim; use scipy.linalg.expm
4|of -iH dt step matrix, cumulative).
5|self_check(g2, m, jmax, t_max) -> dict with expm_krylov_dev, energy_drift, N_drift.
6|"""
7|
8|import numpy as np
9|from scipy.sparse.linalg import expm_multiply
10|from scipy.linalg import expm
11|from su2qc.ham.route_spinnet import build_hamiltonian
12|import su2qc.conventions as cv
13|
14|
15|def evolve(H, psi0, times):
16|    """Evolve psi0 under sparse H at times t (array).
17|
18|    Returns array of shape (len(times), dim) with state vectors at each time.
19|    Uses dense expm of -i*H*dt per step (cumulative), since the Hilbert space
20|    is small (82 or 152 dims).
21|    """
22|    psi0 = np.asarray(psi0, dtype=complex).flatten()
23|    psi0 = psi0 / np.linalg.norm(psi0)  # normalize
24|
25|    # Exact evolution via one eigendecomposition (H Hermitian, tiny):
26|    # psi(t) = V exp(-i E t) V^dag psi0.  Exact for arbitrary time grids.
27|    from scipy.linalg import eigh
28|    E, V = eigh(H.toarray())
29|    c0 = V.conj().T @ psi0
30|    times = np.asarray(times, dtype=float)
31|    phases = np.exp(-1j * np.outer(times, E))          # (T, dim)
32|    return (phases * c0[None, :]) @ V.T
33|
34|
35|def self_check(g2: float, m: float, jmax: float, t_max: float) -> dict:
36|    """Verify expm vs Krylov conservation.
37|
38|    Returns dict with:
39|      expm_krylov_dev: max ||psi_dense(t) - psi_krylov(t)||_inf over ~21 times on [0, t_max]
40|      energy_drift: max |<H>(t) - <H>(0)|
41|      N_drift: max |<N>(t) - <N>(0)|
42|    Targets: <=1e-9, <=1e-10, <=1e-10.
43|    """
44|    H, basis = build_hamiltonian(g2, m, jmax)
45|    dim = H.shape[0]
46|
47|    # Diagonal energy: electric + mass
48|    # Electric: (g2/2) * sum_l j_l(j_l+1)
49|    # Mass: m * sum_v parity_v n_v; parity = (+1, -1, +1, -1)
50|    parity = cv.PARITY  # (+1, -1, +1, -1)
51|
52|    # Build per-state diagonal energy and fermion number
53|    H_diag = np.zeros(dim)
54|    N_diag = np.zeros(dim)
55|
56|    for i, (j_tuple, n_tuple, _) in enumerate(basis):
57|        # Electric term
58|        el = 0.0
59|        for j in j_tuple:
60|            el += j * (j + 1.0)
61|        H_diag[i] = (g2 / 2.0) * el
62|
63|        # Mass term + fermion number
64|        mass = m * sum(parity[v] * n_tuple[v] for v in range(4))
65|        H_diag[i] += mass
66|        N_diag[i] = float(sum(n_tuple))
67|
68|    # Initial state: stretched string |((0.0,0.5,0.5,0.5),(1,1,0,2),0)>
69|    stretched_label = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)
70|    if stretched_label in set(basis):
71|        psi0_idx = basis.index(stretched_label)
72|    else:
73|        psi0_idx = 0
74|
75|    psi0 = np.zeros(dim, dtype=complex)
76|    psi0[psi0_idx] = 1.0
77|
78|    # Sample ~21 times
79|    n_times = 21
80|    times = np.linspace(0, t_max, n_times)
81|
82|    # Dense evolution using expm per step
83|    psi_dense = np.zeros((n_times, dim), dtype=complex)
84|    psi_dense[0] = psi0
85|
86|    for k in range(1, n_times):
87|        dt = times[k] - times[k - 1]
88|        if abs(dt) < 1e-15:
89|            psi_dense[k] = psi_dense[k - 1]
90|            continue
91|        U = expm(-1j * H.toarray() * dt)
92|        psi_dense[k] = U @ psi_dense[k - 1]
93|
94|    # Krylov evolution (sparse expm_multiply)
95|    # expm_multiply(A, B, start, stop) computes expm(A * t) @ B for t in [start, stop]
96|    psi_krylov = np.zeros((n_times, dim), dtype=complex)
97|    psi_krylov[0] = psi0
98|
99|    for k in range(1, n_times):
100|        A = -1j * H.tocsc() * float(times[k])
101|        psi_krylov[k] = expm_multiply(A, psi0)
102|
103|    # Compute inf-norm deviation
104|    dev = np.max(np.abs(psi_dense - psi_krylov), axis=1)
105|    expm_krylov_dev = float(np.max(dev))
106|
107|    # Compute energy <H>(t) = psi^dagger H psi
108|    H_arr = H.toarray()
109|    energies = np.zeros(n_times)
110|    for k in range(n_times):
111|        psi = psi_dense[k]
112|        exp_val = np.real(np.conj(psi) @ (H_arr @ psi))
113|        energies[k] = exp_val
114|
115|    energy_drift = float(np.max(np.abs(energies - energies[0])))
116|
117|    # Fermion number expectation
118|    N_expect = np.zeros(n_times)
119|    for k in range(n_times):
120|        psi = psi_dense[k]
121|        N_exp = np.sum(np.abs(psi) ** 2 * N_diag)
122|        N_expect[k] = float(N_exp)
123|
124|    N_drift = float(np.max(np.abs(N_expect - N_expect[0])))
125|
126|    return {
127|        "expm_krylov_dev": expm_krylov_dev,
128|        "energy_drift": energy_drift,
129|        "N_drift": N_drift,
130|    }

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py
1|"""Mass scan / resonance finder, truncation comparison, Trotter-window selector.
2|
3|Rewritten by the OPS lane after the delegated builder timed out (partial file);
4|classification bugs fixed: P_surv is the EXACT charge pattern (+1,-1,0,0), not
5|a sorted-|q| match.
6|"""
7|
8|import json
9|import os
10|
11|import numpy as np
12|from scipy.linalg import expm
13|
14|import su2qc.conventions as cv
15|from su2qc.dynamics.engine import evolve
16|from su2qc.ham.route_spinnet import (build_hamiltonian,
17|                                     build_hamiltonian_no_magnetic)
18|
19|RUN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
20|    os.path.dirname(os.path.abspath(__file__)))))
21|
22|STRETCHED = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)
23|SHORT = ((0.5, 0.0, 0.0, 0.0), (1, 1, 0, 2), 0)
24|
25|
26|def _idx(basis, label):
27|    for i, lab in enumerate(basis):
28|        if lab == label:
29|            return i
30|    raise KeyError(label)
31|
32|
33|def _classify(basis):
34|    """Per-state channel masks: surv, meson, BBbar, other (within N=4)."""
35|    dim = len(basis)
36|    surv = np.zeros(dim)
37|    meson = np.zeros(dim)
38|    bbbar = np.zeros(dim)
39|    other = np.zeros(dim)
40|    for i, (jt, nt, _) in enumerate(basis):
41|        q = tuple(nt[v] - cv.N_VAC[v] for v in range(4))
42|        if any(abs(x) == 2 for x in q):
43|            bbbar[i] = 1
44|        elif q == (1, -1, 0, 0):
45|            surv[i] = 1
46|        elif all(abs(x) == 1 for x in q):
47|            meson[i] = 1
48|        elif sum(nt) == 4:
49|            other[i] = 1
50|    return surv, meson, bbbar, other
51|
52|
53|def _diagnostics(basis):
54|    e2 = np.array([[cv.casimir(lab[0][l]) for l in range(4)] for lab in basis])
55|    nv = np.array([[lab[1][v] for v in range(4)] for lab in basis])
56|    return e2, nv
57|
58|
59|def channel_probs(basis, states):
60|    surv, meson, bbbar, other = _classify(basis)
61|    p = np.abs(states) ** 2
62|    return p @ surv, p @ meson, p @ bbbar, p @ other
63|
64|
65|# ---------------------------------------------------------------- mass scan
66|
67|def mass_scan(g2_values=(1.0, 2.0, 4.0, 8.0), n_m=25, t_window=(0.0, 40.0),
68|              jmax=0.5):
69|    """Scan m in [0, g2/2] for each g2. Two resonance estimators are recorded:
70|    argmax of W_bar (prompt criterion 2) and argmin of t_b (breaking time);
71|    see physics/DISCREPANCIES.md for why they differ at strong coupling."""
72|    tables = os.path.join(RUN_DIR, "analysis", "tables")
73|    physics = os.path.join(RUN_DIR, "physics")
74|    os.makedirs(tables, exist_ok=True)
75|    rows = []
76|    mstar = {}
77|    mstar_tb = {}
78|    t_eval = np.linspace(t_window[0], t_window[1], 401)
79|    for g2 in g2_values:
80|        m_vals = np.linspace(0.0, 0.5 * g2, n_m)
81|        wbar = []
82|        tbs = []
83|        for m in m_vals:
84|            H, basis = build_hamiltonian(g2, m, jmax)[:2]
85|            psi0 = np.zeros(H.shape[0], complex)
86|            psi0[_idx(basis, STRETCHED)] = 1.0
87|            states = evolve(H, psi0, t_eval)
88|            ps, pm, pb, po = channel_probs(basis, states)
89|            drop = np.where(ps <= 0.5)[0]
90|            t_b = t_eval[drop[0]] if len(drop) else t_eval[np.argmin(ps)]
91|            W = np.trapezoid(pm + pb, t_eval) / (t_eval[-1] - t_eval[0])
92|            wbar.append(W)
93|            tbs.append(t_b)
94|            rows.append((g2, m, t_b, W,
95|                         np.trapezoid(pm, t_eval) / (t_eval[-1] - t_eval[0]),
96|                         np.trapezoid(pb, t_eval) / (t_eval[-1] - t_eval[0])))
97|        mstar[str(g2)] = float(m_vals[int(np.argmax(wbar))] / g2)
98|        mstar_tb[str(g2)] = float(m_vals[int(np.argmin(tbs))] / g2)
99|    with open(os.path.join(tables, "exact_mass_scan.csv"), "w") as fh:
100|        fh.write("g2,m,t_b,W_bar,P_meson_avg,P_BBbar_avg\n")
101|        for r in rows:
102|            fh.write(",".join(f"{x:.10g}" for x in r) + "\n")
103|    out = {"mstar_over_g2": mstar, "mstar_over_g2_tb": mstar_tb,
104|           "n_mass_points": n_m, "n_g2_values": len(g2_values),
105|           "t_window": list(t_window), "tree_level": 3.0 / 16.0}
106|    with open(os.path.join(physics, "resonance.json"), "w") as fh:
107|        json.dump(out, fh, indent=1)
108|    return out
109|
110|
111|# ------------------------------------------------------------- time series
112|
113|def timeseries_at(g2, m, jmax=0.5, times=None, tag="exact_timeseries"):
114|    if times is None:
115|        times = np.linspace(0.0, 12.0, 121)
116|    H, basis = build_hamiltonian(g2, m, jmax)[:2]
117|    psi0 = np.zeros(H.shape[0], complex)
118|    psi0[_idx(basis, STRETCHED)] = 1.0
119|    states = evolve(H, psi0, times)
120|    ps, pm, pb, po = channel_probs(basis, states)
121|    e2m, nvm = _diagnostics(basis)
122|    p = np.abs(states) ** 2
123|    e2 = p @ e2m
124|    nv = p @ nvm
125|    i_st, i_sh = _idx(basis, STRETCHED), _idx(basis, SHORT)
126|    p_st, p_sh = p[:, i_st], p[:, i_sh]
127|    Hd = H.toarray()
128|    en = np.real(np.einsum("ti,ij,tj->t", states.conj(), Hd, states))
129|    tables = os.path.join(RUN_DIR, "analysis", "tables")
130|    os.makedirs(tables, exist_ok=True)
131|    with open(os.path.join(tables, f"{tag}.csv"), "w") as fh:
132|        fh.write("t,P_stretched,P_short,P_surv,P_meson,P_BBbar,P_other,"
133|                 "E2_l1,E2_l2,E2_l3,E2_l4,n_v1,n_v2,n_v3,n_v4,energy\n")
134|        for k, t in enumerate(times):
135|            vals = [t, p_st[k], p_sh[k], ps[k], pm[k], pb[k], po[k],
136|                    *e2[k], *nv[k], en[k]]
137|            fh.write(",".join(f"{x:.10g}" for x in vals) + "\n")
138|    _figures(times, ps, pm, pb, po, e2, nv, tag)
139|    return {"t": times, "P_surv": ps, "P_meson": pm, "P_BBbar": pb,
140|            "P_other": po, "E2": e2, "n": nv, "energy": en,
141|            "P_stretched": p_st, "P_short": p_sh}
142|
143|
144|def _figures(times, ps, pm, pb, po, e2, nv, tag):
145|    import matplotlib
146|    matplotlib.use("Agg")
147|    import matplotlib.pyplot as plt
148|    figs = os.path.join(RUN_DIR, "analysis", "figures")
149|    os.makedirs(figs, exist_ok=True)
150|    fig, ax = plt.subplots(figsize=(7, 4.2))
151|    for y, lab in ((ps, "P_surv"), (pm, "P_meson"), (pb, "P_BBbar"),
152|                   (po, "P_other")):
153|        ax.plot(times, y, label=lab)
154|    ax.set_xlabel("t [a]"); ax.set_ylabel("probability"); ax.legend()
155|    ax.set_title("String-breaking channels (exact)")
156|    fig.tight_layout(); fig.savefig(os.path.join(figs, "exact_channels.png"), dpi=140)
157|    plt.close(fig)
158|    fig, ax = plt.subplots(figsize=(7, 4.2))
159|    ax.plot(times, e2.sum(axis=1) - 9.0 / 4.0, "k-", label="ΔC = ΣE² − 9/4")
160|    for l in range(4):
161|        ax.plot(times, e2[:, l], "--", alpha=0.6, label=f"E²_l{l+1}")
162|    ax.set_xlabel("t [a]"); ax.legend(fontsize=8)
163|    ax.set_title("Casimir reduction (exact)")
164|    fig.tight_layout(); fig.savefig(os.path.join(figs, "exact_casimir.png"), dpi=140)
165|    plt.close(fig)
166|    fig, ax = plt.subplots(figsize=(7, 4.2))
167|    for v in range(4):
168|        ax.plot(times, nv[:, v], label=f"n_v{v+1}")
169|    ax.set_xlabel("t [a]"); ax.set_ylabel("⟨n_v⟩"); ax.legend()
170|    ax.set_title("Site-resolved density (exact)")
171|    fig.tight_layout(); fig.savefig(os.path.join(figs, "exact_density.png"), dpi=140)
172|    plt.close(fig)
173|
174|
175|# ------------------------------------------------------------- truncation
176|
177|def truncation(g2, m):
178|    """Max channel-probability shift jmax=1 vs jmax=1/2 over t in [0,12]."""
179|    times = np.linspace(0.0, 12.0, 121)
180|    out = {}
181|    for jmax in (0.5, 1.0):
182|        H, basis = build_hamiltonian(g2, m, jmax)[:2]
183|        psi0 = np.zeros(H.shape[0], complex)
184|        psi0[_idx(basis, STRETCHED)] = 1.0
185|        states = evolve(H, psi0, times)
186|        ps, pm, pb, po = channel_probs(basis, states)
187|        out[jmax] = np.stack([ps, pm, pb, po])
188|    d = float(np.max(np.abs(out[0.5] - out[1.0])))
189|    res = {"max_abs_dprob": d, "g2": g2, "m": m}
190|    with open(os.path.join(RUN_DIR, "physics", "truncation_error.json"), "w") as fh:
191|        json.dump(res, fh, indent=1)
192|    with open(os.path.join(RUN_DIR, "physics", "truncation_error.md"), "w") as fh:
193|        fh.write("# Truncation error (jmax=1 vs jmax=1/2)\n\n"
194|                 f"At (g2, m) = ({g2}, {m}), stretched-string evolution on "
195|                 f"t ∈ [0, 12]:\n\n"
196|                 f"max |Δp| over channels and times = {d:.4g}\n\n")
197|        if d > 0.1:
198|            fh.write("**FLAG: exceeds 0.1 — hardcore-gluon truncation is a "
199|                     "leading systematic in this window.**\n")
200|        else:
201|            fh.write("Below the 0.1 threshold: hardcore-gluon truncation is "
202|                     "subleading in the chosen window.\n")
203|    return res
204|
205|
206|# ------------------------------------------------- Strang error and window
207|
208|def _term_split(g2, m, jmax=0.5):
209|    """Split H into D (diagonal), h_l (per-link hopping), B (magnetic)."""
210|    H, basis = build_hamiltonian(g2, m, jmax)[:2]
211|    Hn = build_hamiltonian_no_magnetic(g2, m, jmax)[0]
212|    Hd = H.toarray()
213|    Hnd = Hn.toarray()
214|    D = np.diag(np.diag(Hnd))
215|    B = Hd - Hnd
216|    hop = Hnd - D
217|    hs = []
218|    for l in range(4):
219|        hl = np.zeros_like(hop)
220|        s, t = cv.LINKS[l][0], cv.LINKS[l][1]
221|        for i, (ji, ni, _) in enumerate(basis):
222|            for j in range(len(basis)):
223|                if abs(hop[i, j]) < 1e-14:
224|                    continue
225|                jj, nj = basis[j][0], basis[j][1]
226|                dj = [abs(ji[k] - jj[k]) > 1e-12 for k in range(4)]
227|                dn = [ni[k] != nj[k] for k in range(4)]
228|                if dj == [k == l for k in range(4)] and \
229|                        set(k for k in range(4) if dn[k]) == {s, t}:
230|                    hl[i, j] = hop[i, j]
231|        hs.append(hl)
232|    assert np.max(np.abs(D + sum(hs) + B - Hd)) <= 1e-13, "term split failed"
233|    return Hd, D, hs, B, basis
234|
235|
236|def strang_step_matrix(D, hs, B, dt):
237|    """One Strang step in the CIRCUIT layer ordering (prompt §5.5):
238|    D/2 · [h0,h2]/2 · [h1,h3]/2 · B · [h1,h3]/2 · [h0,h2]/2 · D/2."""
239|    order = [hs[0], hs[2], hs[1], hs[3]]
240|    U = expm(-1j * D * dt / 2.0)
241|    for h in order:
242|        U = expm(-1j * h * dt / 2.0) @ U
243|    U = expm(-1j * B * dt) @ U
244|    for h in reversed(order):
245|        U = expm(-1j * h * dt / 2.0) @ U
246|    U = expm(-1j * D * dt / 2.0) @ U
247|    return U
248|
249|
250|def strang_error(g2, m, dt, r, jmax=0.5):
251|    """Observable error of r Strang steps vs exact at t = r dt."""
252|    Hd, D, hs, B, basis = _term_split(g2, m, jmax)
253|    psi0 = np.zeros(Hd.shape[0], complex)
254|    psi0[_idx(basis, STRETCHED)] = 1.0
255|    Us = strang_step_matrix(D, hs, B, dt)
256|    psi_s = psi0.copy()
257|    for _ in range(r):
258|        psi_s = Us @ psi_s
259|    psi_e = expm(-1j * Hd * (r * dt)) @ psi0
260|    e2m, nvm = _diagnostics(basis)
261|    surv = _classify(basis)[0]
262|    pe, ps_ = np.abs(psi_e) ** 2, np.abs(psi_s) ** 2
263|    devs = [abs(pe @ surv - ps_ @ surv),
264|            float(np.max(np.abs(pe @ nvm - ps_ @ nvm))),
265|            float(np.max(np.abs(pe @ e2m - ps_ @ e2m)))]
266|    return max(devs)
267|
268|
269|def select_window(g2=1.0, m=None, jmax=0.5):
270|    """Choose (g2, m, dt, r_max) per prompt Phase-2 criterion 5."""
271|    physics = os.path.join(RUN_DIR, "physics")
272|    if m is None:
273|        res = json.load(open(os.path.join(physics, "resonance.json")))
274|        m = res["mstar_over_g2"][str(g2)] * g2
275|    H, basis = build_hamiltonian(g2, m, jmax)[:2]
276|    psi0 = np.zeros(H.shape[0], complex)
277|    psi0[_idx(basis, STRETCHED)] = 1.0
278|    best = None
279|    for r_max in (3, 2):
280|        for t_tot in (3.0, 2.5, 3.5, 4.0, 2.0, 5.0, 6.0, 1.5):
281|            dt = t_tot / r_max
282|            times = np.array([0.0, t_tot])
283|            states = evolve(H, psi0, times)
284|            ps, pm, pb, po = channel_probs(basis, states)
285|            drop = ps[0] - ps[1]
286|            pair = pm[1] + pb[1]
287|            serr = strang_error(g2, m, dt, r_max, jmax)
288|            cand = {"g2": g2, "m": m, "dt": dt, "r_max": r_max,
289|                    "expected": {"psurv_drop": float(drop),
290|                                 "pair_weight": float(pair),
291|                                 "strang_err": float(serr)},
292|                    "shortfall_flagged": False}
293|            if serr <= 0.05:
294|                if drop >= 0.3 and pair >= 0.05:
295|                    with open(os.path.join(physics, "window.json"), "w") as fh:
296|                        json.dump(cand, fh, indent=1)
297|                    return cand
298|                if best is None or (drop > best["expected"]["psurv_drop"]):
299|                    best = cand
300|    best["shortfall_flagged"] = True
301|    with open(os.path.join(physics, "window.json"), "w") as fh:
302|        json.dump(best, fh, indent=1)
303|    return best
304|
305|
306|def verify_window(w):
307|    """Recompute the window criteria (gate G2 calls this)."""
308|    g2, m, dt, r = w["g2"], w["m"], w["dt"], w["r_max"]
309|    H, basis = build_hamiltonian(g2, m, 0.5)[:2]
310|    psi0 = np.zeros(H.shape[0], complex)
311|    psi0[_idx(basis, STRETCHED)] = 1.0
312|    states = evolve(H, psi0, np.array([0.0, r * dt]))
313|    ps, pm, pb, po = channel_probs(basis, states)
314|    return {"psurv_drop": float(ps[0] - ps[1]),
315|            "pair_weight": float(pm[1] + pb[1]),
316|            "strang_err": float(strang_error(g2, m, dt, r))}

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py
1|"""The 12-qubit, three-bits-per-vertex L12 encoding.
2|
3|Qubit ``3*v,3*v+1,3*v+2`` is respectively (first link, second link,
4|matter).  Integers use q0 as the least significant bit; displayed Qiskit
5|strings consequently read q11 ... q0.
6|"""
7|from __future__ import annotations
8|
9|from functools import lru_cache
10|from numbers import Integral
11|from su2qc.ham.route_spinnet import enumerate_basis, _VLINKS
12|
13|N_QUBITS = 12
14|
15|def _bit(code, q):
16|    return (int(code) >> q) & 1
17|
18|@lru_cache(maxsize=1)
19|def _maps():
20|    out = {}
21|    for label in enumerate_basis(.5):
22|        js, ns, tag = label
23|        bits = 0
24|        for v, (la, lb) in enumerate(_VLINKS):
25|            a, b = int(round(2*js[la])), int(round(2*js[lb]))
26|            # In this truncation the link bit is 0/1 == j 0/1/2.
27|            bits |= a << (3*v)
28|            bits |= b << (3*v+1)
29|            bits |= (1 if ns[v] == 2 else 0) << (3*v+2)
30|        out[bits] = label
31|    return out
32|
33|def encode(label) -> int:
34|    """Encode a canonical route-spinnet basis label as a 12-bit integer."""
35|    for code, candidate in _maps().items():
36|        if candidate == label:
37|            return code
38|    raise ValueError(f"not a physical L12 label: {label!r}")
39|
40|def decode(bits):
41|    """Decode an integer (or a q11...q0 bit string) or return ``None``."""
42|    if isinstance(bits, str):
43|        if len(bits) != 12 or any(c not in "01" for c in bits):
44|            return None
45|        bits = int(bits, 2)
46|    if not isinstance(bits, Integral) or not 0 <= bits < 4096:
47|        return None
48|    return _maps().get(bits)
49|
50|def physical_codes() -> list[int]:
51|    return sorted(_maps())
52|
53|def leakage_flags(bits):
54|    """Return vertex leakage and four endpoint-consistency flags."""
55|    if isinstance(bits, str):
56|        try: bits = int(bits, 2)
57|        except ValueError: return {"vertex": (True,)*4, "link": (True,)*4}
58|    vertex = tuple(bool(_bit(bits, 3*v) ^ _bit(bits, 3*v+1)) and bool(_bit(bits, 3*v+2))
59|                   for v in range(4))
60|    # Compare the two endpoint copies, using the fixed vertex incidence order.
61|    link = []
62|    for l in range(4):
63|        copies = [(3*v + k) for v, pair in enumerate(_VLINKS) for k, ll in enumerate(pair) if ll == l]
64|        link.append(bool(_bit(bits, copies[0]) ^ _bit(bits, copies[1])))
65|    return {"vertex": vertex, "link": tuple(link)}
66|
67|def is_physical(bits) -> bool:
68|    f = leakage_flags(bits)
69|    return not any(f["vertex"]) and not any(f["link"])

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py
1|"""Noise-model twin: FakeTorino (or a real backend's properties) via
2|AerSimulator.from_backend, with leakage post-selection and observables.
3|
4|  twin_backend(seed)              -> AerSimulator noise twin
5|  run_counts(isa_circs, shots, seed, backend) -> list of counts dicts (physical
6|        bit order already mapped back to LOGICAL q11..q0 strings via the
7|        circuit's final layout, so l12.decode applies directly)
8|  postselect(counts)              -> (kept_counts, yield_fraction)
9|  observables(kept_counts)        -> dict of P_surv, P_meson, P_BBbar, P_other,
10|        E2_l (4), n_v (4), from decoded labels (all Z-basis, diagonal)
11|  bootstrap(counts_list, fn, n_boot, seed) -> mean, 2sigma per observable
12|"""
13|from __future__ import annotations
14|
15|import os
16|import sys
17|
18|import numpy as np
19|
20|RUN = os.path.dirname(os.path.dirname(os.path.dirname(
21|    os.path.dirname(os.path.abspath(__file__)))))
22|sys.path.insert(0, os.path.join(RUN, "src"))
23|
24|from su2qc import conventions as cv  # noqa: E402
25|from su2qc.encodings import l12  # noqa: E402
26|
27|
28|def twin_backend(seed=1234, backend=None, compact=False):
29|    from qiskit_aer import AerSimulator
30|    if backend is None:
31|        from qiskit_ibm_runtime.fake_provider import FakeTorino
32|        backend = FakeTorino()
33|    if compact:
34|        from qiskit_aer.noise import NoiseModel
35|        noise = NoiseModel.from_backend(backend)
36|        return AerSimulator(noise_model=noise)
37|    return AerSimulator.from_backend(backend, seed_simulator=seed)
38|
39|
40|def add_measurements(isa):
41|    """Measure the 12 logical qubits (at their final physical positions) into
42|    classical bits c[i] = logical i, so the count strings read q11..q0."""
43|    from qiskit import ClassicalRegister
44|    fil = (isa.layout.final_index_layout() if isa.layout is not None
45|           else list(range(len(isa.qubits))))
46|    qc = isa.copy()
47|    cr = ClassicalRegister(12, "c")
48|    qc.add_register(cr)
49|    for i in range(12):
50|        qc.measure(qc.qubits[fil[i]], cr[i])
51|    return qc
52|
53|
54|def run_counts(isa_meas_list, shots, seed, sim):
55|    from qiskit import transpile
56|    out = []
57|    for k, qc in enumerate(isa_meas_list):
58|        t = transpile(qc, sim, optimization_level=0, seed_transpiler=seed)
59|        if hasattr(sim, "set_options"):
60|            sim.set_options(seed_simulator=seed + k)
61|        res = sim.run(t, shots=shots, seed_simulator=seed + k).result()
62|        out.append(dict(res.get_counts()))
63|    return out
64|
65|
66|def postselect(counts):
67|    kept = {s: n for s, n in counts.items() if l12.is_physical(s)}
68|    tot = sum(counts.values())
69|    return kept, (sum(kept.values()) / tot if tot else 0.0)
70|
71|
72|def observables(kept):
73|    tot = sum(kept.values())
74|    acc = {"P_surv": 0.0, "P_meson": 0.0, "P_BBbar": 0.0, "P_other": 0.0,
75|           "P_stretched": 0.0, "P_short": 0.0}
76|    e2 = np.zeros(4)
77|    nv = np.zeros(4)
78|    for s, n in kept.items():
79|        lab = l12.decode(s)
80|        w = n / tot
81|        js, ns, _ = lab
82|        q = tuple(ns[v] - cv.N_VAC[v] for v in range(4))
83|        if any(abs(x) == 2 for x in q):
84|            acc["P_BBbar"] += w
85|        elif q == (1, -1, 0, 0):
86|            acc["P_surv"] += w
87|            if tuple(js) == (0.0, 0.5, 0.5, 0.5):
88|                acc["P_stretched"] += w
89|            elif tuple(js) == (0.5, 0.0, 0.0, 0.0):
90|                acc["P_short"] += w
91|        elif all(abs(x) == 1 for x in q):
92|            acc["P_meson"] += w
93|        elif sum(ns) == 4:
94|            acc["P_other"] += w
95|        e2 += w * np.array([cv.casimir(j) for j in js])
96|        nv += w * np.array(ns, float)
97|    for l in range(4):
98|        acc[f"E2_l{l+1}"] = float(e2[l])
99|    for v in range(4):
100|        acc[f"n_v{v+1}"] = float(nv[v])
101|    acc["dC"] = float(e2.sum() - 2.25)
102|    return acc
103|
104|
105|def channel_weights(kept):
106|    """Return signed-weight channel totals without renormalizing the input."""
107|    out = {"P_surv": 0.0, "P_meson": 0.0, "P_BBbar": 0.0,
108|           "P_other": 0.0, "P_stretched": 0.0, "P_short": 0.0}
109|    for bits, weight in kept.items():
110|        lab = l12.decode(bits)
111|        if lab is None:
112|            continue
113|        js, ns, _ = lab
114|        q = tuple(ns[v] - cv.N_VAC[v] for v in range(4))
115|        if any(abs(x) == 2 for x in q):
116|            out["P_BBbar"] += weight
117|        elif q == (1, -1, 0, 0):
118|            out["P_surv"] += weight
119|            if tuple(js) == (0.0, 0.5, 0.5, 0.5):
120|                out["P_stretched"] += weight
121|            elif tuple(js) == (0.5, 0.0, 0.0, 0.0):
122|                out["P_short"] += weight
123|        elif all(abs(x) == 1 for x in q):
124|            out["P_meson"] += weight
125|        elif sum(ns) == 4:
126|            out["P_other"] += weight
127|    return out
128|
129|
130|def channel_closure_residual(kept):
131|    """Check the corrected V11 closure identity on signed quasi-weights."""
132|    channels = channel_weights(kept)
133|    lhs = sum(channels[k] for k in ("P_surv", "P_meson", "P_BBbar", "P_other"))
134|    rhs = 0.0
135|    for bits, weight in kept.items():
136|        lab = l12.decode(bits)
137|        if lab is None:
138|            continue
139|        _, ns, _ = lab
140|        q = tuple(ns[v] - cv.N_VAC[v] for v in range(4))
141|        if sum(ns) == 4 or any(abs(x) == 2 for x in q):
142|            rhs += weight
143|    return float(lhs - rhs)
144|
145|
146|def matched_subtraction(observed, control):
147|    """Compute O(t)-O(0) over the union of observable keys."""
148|    return {key: float(observed.get(key, 0.0) - control.get(key, 0.0))
149|            for key in set(observed) | set(control)}
150|
151|
152|def physical_yield(counts, physical_keys):
153|    """Return the fraction of counts in the supplied physical-key set."""
154|    total = sum(counts.values())
155|    return float(sum(value for key, value in counts.items() if key in physical_keys) / total)
156|
157|
158|def bootstrap(counts_list, n_boot=400, seed=0):
159|    """Bootstrap over repeats (each element of counts_list is one repeat).
160|    Returns (mean dict, two_sigma dict, yield mean)."""
161|    rng = np.random.default_rng(seed)
162|    per = []
163|    ys = []
164|    for c in counts_list:
165|        k, y = postselect(c)
166|        per.append(observables(k))
167|        ys.append(y)
168|    keys = list(per[0].keys())
169|    A = np.array([[p[k] for k in keys] for p in per])
170|    n = len(per)
171|    boots = np.array([A[rng.integers(0, n, n)].mean(axis=0) for _ in range(n_boot)])
172|    mean = A.mean(axis=0)
173|    two_sigma = 2.0 * boots.std(axis=0, ddof=1)
174|    return (dict(zip(keys, mean.tolist())), dict(zip(keys, two_sigma.tolist())),
175|            float(np.mean(ys)))

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/tests/conftest.py
1|import sys
2|from pathlib import Path
3|
4|# Ensure RUN/src is on sys.path so `import su2qc...` works for all tests.
5|SRC = Path(__file__).resolve().parents[1] / "src"
6|if str(SRC) not in sys.path:
7|    sys.path.insert(0, str(SRC))

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py
1|"""Unit tests for the exact-dynamics lane (gate G2 support)."""
2|import json
3|import os
4|
5|import numpy as np
6|import pytest
7|
8|from su2qc.dynamics import engine, scan
9|from su2qc.ham.route_spinnet import build_hamiltonian
10|
11|RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
12|
13|
14|@pytest.mark.unit
15|def test_self_check():
16|    r = engine.self_check(4.0, 0.75, 0.5, 10.0)
17|    assert r["expm_krylov_dev"] <= 1e-9
18|    assert r["energy_drift"] <= 1e-10
19|    assert r["N_drift"] <= 1e-10
20|
21|
22|@pytest.mark.unit
23|def test_evolve_matches_expm():
24|    from scipy.linalg import expm
25|    H, b = build_hamiltonian(1.0, 0.2, 0.5)[:2]
26|    psi0 = np.zeros(82, complex)
27|    psi0[scan._idx(b, scan.STRETCHED)] = 1.0
28|    s = engine.evolve(H, psi0, np.array([0.0, 7.3]))
29|    ref = expm(-1j * H.toarray() * 7.3) @ psi0
30|    assert np.max(np.abs(s[-1] - ref)) <= 1e-12
31|
32|
33|@pytest.mark.unit
34|def test_term_split_is_exact():
35|    Hd, D, hs, B, basis = scan._term_split(4.0, 0.75)
36|    assert np.max(np.abs(D + sum(hs) + B - Hd)) <= 1e-13
37|    # each hopping block is Hermitian and off-diagonal
38|    for h in hs:
39|        assert np.max(np.abs(h - h.conj().T)) <= 1e-13
40|        assert np.max(np.abs(np.diag(h))) == 0.0
41|
42|
43|@pytest.mark.unit
44|def test_channel_masks_partition_N4_sector():
45|    _, b = build_hamiltonian(1.0, 0.1, 0.5)[:2]
46|    surv, mes, bb, oth = scan._classify(b)
47|    n4 = np.array([sum(l[1]) == 4 for l in b])
48|    assert int(n4.sum()) == 38
49|    assert np.all((surv + mes + bb + oth)[n4] == 1)
50|    assert int(surv.sum()) == 2 and int(mes.sum()) == 2
51|
52|
53|@pytest.mark.unit
54|def test_artifacts_and_window():
55|    res = json.load(open(os.path.join(RUN, "physics", "resonance.json")))
56|    assert res["n_mass_points"] >= 21 and res["n_g2_values"] >= 2
57|    assert os.path.exists(os.path.join(RUN, "analysis", "tables",
58|                                       "exact_mass_scan.csv"))
59|    w = json.load(open(os.path.join(RUN, "physics", "window.json")))
60|    assert w["r_max"] in (2, 3)
61|    v = scan.verify_window(w)
62|    assert v["strang_err"] <= 0.05
63|    assert v["psurv_drop"] >= 0.3 or w.get("shortfall_flagged")
64|    assert v["pair_weight"] >= 0.05 or w.get("shortfall_flagged")

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py
1|"""G3 tests: L12 encoding, exact block unitaries, Strang circuits, leakage."""
2|import json
3|import os
4|
5|import numpy as np
6|import pytest
7|from scipy.linalg import expm
8|
9|from su2qc.circuits import strang_l12 as sl
10|from su2qc.encodings import l12
11|
12|RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
13|P = sl.params()
14|G2, M, DT, RMAX = P["g2"], P["m"], P["dt"], P["r_max"]
15|
16|
17|@pytest.mark.unit
18|def test_encoding_roundtrip_and_flags():
19|    codes = l12.physical_codes()
20|    assert len(codes) == 82 and len(set(codes)) == 82
21|    for c in codes:
22|        assert l12.encode(l12.decode(c)) == c
23|        assert l12.is_physical(c)
24|    n_phys = sum(l12.is_physical(b) for b in range(4096))
25|    assert n_phys == 82
26|    # known state: stretched string
27|    code = l12.encode(sl.STRETCHED)
28|    assert code == 3793
29|    assert l12.decode(format(code, "012b")) == sl.STRETCHED
30|
31|
32|def _apply_on_codes(qc, basis):
33|    """Matrix of the circuit restricted to physical codes (82x82) and the
34|    leakage block (unphys x phys), via 82 statevector runs."""
35|    from qiskit import QuantumCircuit
36|    from qiskit.quantum_info import Statevector
37|    cb = sl.basis_to_code(basis)
38|    codes = l12.physical_codes()
39|    mask = np.ones(4096, bool)
40|    mask[codes] = False
41|    Uphys = np.zeros((82, 82), complex)
42|    leak = 0.0
43|    for j, c in enumerate(cb):
44|        prep = QuantumCircuit(12)
45|        for q in range(12):
46|            if (c >> q) & 1:
47|                prep.x(q)
48|        prep.compose(qc, inplace=True)
49|        v = Statevector(prep).data
50|        Uphys[:, j] = v[cb]
51|        leak = max(leak, float(np.linalg.norm(v[mask])))
52|    return Uphys, leak
53|
54|
55|@pytest.mark.unit
56|@pytest.mark.parametrize("group", sl.GROUPS)
57|@pytest.mark.parametrize("theta", [0.13, 0.61])
58|def test_block_unitary_exact_and_leak_free(group, theta):
59|    basis, T = sl.terms(G2, M)
60|    qc = sl.unitary(group, theta, G2, M)
61|    Uphys, leak = _apply_on_codes(qc, basis)
62|    Uex = expm(-1j * theta * T[group])
63|    assert np.linalg.norm(Uphys - Uex) <= 1e-12
64|    assert leak <= 1e-12
65|
66|
67|@pytest.mark.unit
68|def test_full_strang_step_matches_exact_product():
69|    basis, T = sl.terms(G2, M)
70|    qc = sl.strang_step(DT, G2, M)
71|    Uphys, leak = _apply_on_codes(qc, basis)
72|    Uex = sl.exact_strang_matrix(DT, G2, M)
73|    assert np.linalg.norm(Uphys - Uex) <= 1e-10
74|    assert leak <= 1e-12
75|    # merged-D full circuit == unmerged
76|    from qiskit.quantum_info import Statevector
77|    a = Statevector(sl.full_circuit(2, merge_D=True)).data
78|    b = Statevector(sl.full_circuit(2, merge_D=False)).data
79|    assert np.max(np.abs(a - b)) <= 1e-12
80|
81|
82|@pytest.mark.unit
83|def test_noiseless_leakage_zero():
84|    from qiskit.quantum_info import Statevector
85|    from qiskit_aer import AerSimulator
86|    from qiskit import transpile
87|    qc = sl.full_circuit(RMAX)
88|    v = Statevector(qc).data
89|    assert sl.leakage_prob(v) <= 1e-14
90|    meas = qc.copy()
91|    meas.measure_all()
92|    sim = AerSimulator(seed_simulator=11)
93|    t = transpile(meas, sim, optimization_level=0)
94|    counts = sim.run(t, shots=10000).result().get_counts()
95|    flagged = sum(n for s, n in counts.items() if not l12.is_physical(s))
96|    assert flagged == 0
97|
98|
99|@pytest.mark.unit
100|def test_trotter_scaling():
101|    """Second-order scaling: error vs r at fixed t = RMAX*DT, r in 1..16."""
102|    from su2qc.dynamics.scan import _classify, _diagnostics
103|    basis, T = sl.terms(G2, M)
104|    t_tot = RMAX * DT
105|    i0 = basis.index(sl.STRETCHED)
106|    psi0 = np.zeros(82, complex)
107|    psi0[i0] = 1.0
108|    surv = _classify(basis)[0]
109|    e2m, _ = _diagnostics(basis)
110|    ex = expm(-1j * T["H"] * t_tot) @ psi0
111|    pe = np.abs(ex) ** 2
112|    rs = [8, 16, 32, 64, 128]
113|    errs_s, errs_e, errs_psi = [], [], []
114|    for r in rs:
115|        U = sl.exact_strang_matrix(t_tot / r, G2, M)   # matrix form, exact
116|        psi = psi0.copy()
117|        for _ in range(r):
118|            psi = U @ psi
119|        p = np.abs(psi) ** 2
120|        errs_s.append(abs(p @ surv - pe @ surv))
121|        errs_e.append(np.max(np.abs(p @ e2m - pe @ e2m)))
122|        errs_psi.append(float(np.linalg.norm(psi - ex)))
123|    fit = lambda e: float(np.polyfit(np.log(rs), np.log(e), 1)[0])
124|    slopes = {"Psurv": fit(errs_s), "E2": fit(errs_e), "state": fit(errs_psi)}
125|    json.dump({"r": rs, "t": t_tot, "err_Psurv": errs_s, "err_E2": errs_e,
126|               "err_state": errs_psi,
127|               "slope_Psurv": slopes["Psurv"], "slope_E2": slopes["E2"],
128|               "slope_state": slopes["state"]},
129|              open(os.path.join(RUN, "circuits", "trotter_scaling.json"), "w"),
130|              indent=1)
131|    for k, s in slopes.items():
132|        assert -2.3 <= s <= -1.7, (k, s, errs_s, errs_e, errs_psi)
133|
134|
135|@pytest.mark.unit
136|def test_window_strang_error():
137|    from su2qc.dynamics.scan import strang_error
138|    assert strang_error(G2, M, DT, RMAX) <= 0.05

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/tests/test_route_gausskernel.py
1|import numpy as np
2|import pytest
3|
4|from src.su2qc.ham.route_gausskernel import (
5|    _basis, build_hamiltonian, gauss_commutator_norms, get_state, kernel_dimension,
6|)
7|
8|
9|pytestmark = pytest.mark.unit
10|
11|
12|def test_kernel_dimensions_and_number_sectors():
13|    H, labels, P = build_hamiltonian(1.0, 0.0, 0.5)
14|    counts = {n: sum(sum(x[1]) == n for x in labels) for n in range(9)}
15|    print("kernel dims:", len(labels))
16|    print("N sectors:", counts)
17|    assert len(labels) == 82
18|    assert counts == {0: 2, 1: 0, 2: 20, 3: 0, 4: 38, 5: 0, 6: 20, 7: 0, 8: 2}
19|    assert np.max(np.abs((P.conj().T @ P).toarray() - np.eye(82))) < 1e-12
20|
21|    # Legacy D1 validates the jmax=1 kernel, not its unimplemented Hamiltonian.
22|    assert kernel_dimension(1.0) == 152
23|    labels1, P1 = _basis(1.0)
24|    print("jmax=1 kernel dim:", len(labels1))
25|    assert len(labels1) == 152
26|    assert np.max(np.abs((P1.conj().T @ P1).toarray() - np.eye(152))) < 1e-12
27|
28|
29|def test_hermiticity_and_gauss_diagnostics():
30|    H, labels, _ = build_hamiltonian(0.73, 0.19, 0.5)
31|    err = np.max(np.abs((H - H.getH()).data)) if (H - H.getH()).nnz else 0.0
32|    print("hermiticity:", err)
33|    assert err <= 1e-13
34|    norms = gauss_commutator_norms(0.5)
35|    print("Gauss commutator norms:", norms)
36|    assert max(norms.values()) <= 1e-12
37|
38|
39|def test_pure_electric_clusters_and_stretched_label():
40|    H, labels, _ = build_hamiltonian(1e6, 0.0, 0.5)
41|    vals, mult = np.unique(np.round(H.diagonal().real, 7), return_counts=True)
42|    print("electric clusters:", list(zip(vals, mult)))
43|    assert np.array_equal(mult, [16, 16, 18, 16, 16])
44|    stretched = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)
45|    assert sum(x == stretched for x in labels) == 1
46|    assert get_state(stretched, labels) >= 0

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/tests/test_route_spinnet.py
1|"""Unit tests for route 1 (analytic spin-network/dressed-site) Hamiltonian.
2|
3|Tests the SU(2) single-plaquette Hamiltonian with dynamical two-color staggered
4|fermions.  All numbers validated against the expected values from the conventions
5|and limit-check files.
6|"""
7|
8|from __future__ import annotations
9|
10|import numpy as np
11|import pytest
12|
13|from su2qc.ham.route_spinnet import (
14|    build_hamiltonian,
15|    build_hamiltonian_no_magnetic,
16|    enumerate_basis,
17|    pure_electric_check,
18|    validate_dimensions,
19|    validate_hermiticity,
20|)
21|
22|
23|@pytest.mark.unit
24|class TestBasisDimensions:
25|    """Test basis size and sector decomposition."""
26|
27|    @pytest.mark.parametrize("jmax,expected_dim", [(0.5, 82), (1.0, 152)])
28|    def test_basis_dimension(self, jmax, expected_dim):
29|        dim = len(enumerate_basis(jmax))
30|        assert dim == expected_dim, f"jmax={jmax}: dim={dim} != {expected_dim}"
31|
32|    @pytest.mark.parametrize("jmax", [0.5])
33|    def test_sector_decomposition(self, jmax):
34|        """Sector dims at jmax=0.5: N=0,2,4,6,8 -> 2,20,38,20,2 (only even N)."""
35|        basis = enumerate_basis(jmax)
36|        sector_dims = {0: 0, 2: 0, 4: 0, 6: 0, 8: 0}
37|        for _, n_tuple, _ in basis:
38|            N = sum(n_tuple)
39|            if N in sector_dims:
40|                sector_dims[N] += 1
41|
42|        expected = {0: 2, 2: 20, 4: 38, 6: 20, 8: 2}
43|        for N in expected:
44|            assert sector_dims[N] == expected[N], (
45|                f"jmax={jmax}: N={N} got {sector_dims[N]} expected {expected[N]}"
46|            )
47|
48|
49|@pytest.mark.unit
50|class TestHermiticity:
51|    """Test that H is Hermitian."""
52|
53|    @pytest.mark.parametrize("g2, m, jmax", [
54|        (1.0, 0.0, 0.5),
55|        (1.0, 0.1875, 0.5),
56|        (0.5, 0.2, 0.5),
57|        (2.0, 0.375, 0.5),
58|    ])
59|    def test_H_hermitian(self, g2, m, jmax):
60|        H, _ = build_hamiltonian(g2, m, jmax)
61|        H_arr = H.toarray()
62|        diff = np.max(np.abs(H_arr - H_arr.T.conj()))
63|        assert diff <= 1e-13, f"H not Hermitian at (g2={g2}, m={m}, jmax={jmax}): max_diff={diff}"
64|
65|
66|@pytest.mark.unit
67|class TestCommutator:
68|    """Test [H, N] = 0 (fermion number conservation)."""
69|
70|    @pytest.mark.parametrize("g2, m, jmax", [
71|        (1.0, 0.0, 0.5),
72|        (1.0, 0.1875, 0.5),
73|        (0.5, 0.2, 0.5),
74|    ])
75|    def test_H_commutes_with_N(self, g2, m, jmax):
76|        H, basis = build_hamiltonian(g2, m, jmax)
77|        dim = len(basis)
78|
79|        # Build total number operator
80|        N_full = np.zeros((dim, dim))
81|        for i, (_, n_tuple, _) in enumerate(basis):
82|            N_full[i, i] = float(sum(n_tuple))
83|
84|        H_arr = H.toarray()
85|        comm = H_arr @ N_full - N_full @ H_arr
86|        max_comm = np.max(np.abs(comm))
87|        assert max_comm <= 1e-13, f"[H,N] != 0 at (g2={g2}, m={m}, jmax={jmax}): max_comm={max_comm}"
88|
89|
90|@pytest.mark.unit
91|class TestPureElectricDegeneracy:
92|    """Test g2 -> infinity electric-level degeneracies at m=0."""
93|
94|    def test_electric_degeneracies(self):
95|        """At g2 -> inf, m=0: degeneracies 16,16,18,16,16 by k=#(j=1/2 links)."""
96|        H, _ = build_hamiltonian(1e6, 0.0, 0.5)
97|        evals = np.sort(np.linalg.eigvalsh(H.toarray()))
98|        unit = 1e6 / 2.0 * 0.75  # (g2/2) * (3/4)
99|        ks = np.rint(evals / unit).astype(int)
100|        got = [int(np.sum(ks == k)) for k in range(5)]
101|        expected = [16, 16, 18, 16, 16]
102|        assert got == expected, f"Electric degeneracies got {got} expected {expected}"
103|
104|        # Check relative deviation
105|        rel = np.max(np.abs(evals - ks * unit)) / unit
106|        assert rel <= 1e-8, f"Relative dev {rel} > 1e-8"
107|
108|
109|@pytest.mark.unit
110|class TestNoMagnetic:
111|    """Test build_hamiltonian_no_magnetic (electric + mass + hopping only)."""
112|
113|    @pytest.mark.parametrize("g2, m, jmax", [
114|        (1.0, 0.0, 0.5),
115|        (1.0, 0.1875, 0.5),
116|        (0.5, 0.2, 0.5),
117|    ])
118|    def test_no_magnetic_shape(self, g2, m, jmax):
119|        H_no_mag, _ = build_hamiltonian_no_magnetic(g2, m, jmax)
120|        expected_dim = 82 if jmax == 0.5 else 152
121|        assert H_no_mag.shape == (expected_dim, expected_dim)
122|
123|    @pytest.mark.parametrize("g2, m, jmax", [
124|        (1.0, 0.0, 0.5),
125|    ])
126|    def test_no_mag_hermitian(self, g2, m, jmax):
127|        H_no_mag, _ = build_hamiltonian_no_magnetic(g2, m, jmax)
128|        H_arr = H_no_mag.toarray()
129|        diff = np.max(np.abs(H_arr - H_arr.T.conj()))
130|        assert diff <= 1e-13
131|
132|    @pytest.mark.parametrize("g2, m, jmax", [
133|        (1.0, 0.0, 0.5),
134|    ])
135|    def test_no_mag_commuting_N(self, g2, m, jmax):
136|        H_no_mag, basis = build_hamiltonian_no_magnetic(g2, m, jmax)
137|        dim = len(basis)
138|        N_full = np.zeros((dim, dim))
139|        for i, (_, n_tuple, _) in enumerate(basis):
140|            N_full[i, i] = float(sum(n_tuple))
141|        comm = H_no_mag.toarray() @ N_full - N_full @ H_no_mag.toarray()
142|        max_comm = np.max(np.abs(comm))
143|        assert max_comm <= 1e-13
144|
145|
146|@pytest.mark.unit
147|class TestCorePhysics:
148|    """Test core physics validations."""
149|
150|    def test_basis_dimensions_match(self):
151|        """Basis dimensions match expected values."""
152|        r05 = validate_dimensions(0.5)
153|        assert r05["dim_match"], f"jmax=0.5 dim={r05['dim']} != 82"
154|        r10 = validate_dimensions(1.0)
155|        assert r10["dim_match"], f"jmax=1.0 dim={r10['dim']} != 152"
156|
157|    def test_sector_dims(self):
158|        """Sector decomposition at jmax=0.5 matches expectations."""
159|        r = validate_dimensions(0.5)
160|        assert r["sector_N0_match"], f"N=0 sector wrong: {r['sector_dims'][0]}"
161|        assert r["sector_N2_match"], f"N=2 sector wrong: {r['sector_dims'][2]}"
162|        assert r["sector_N4_match"], f"N=4 sector wrong: {r['sector_dims'][4]}"
163|        assert r["sector_N6_match"], f"N=6 sector wrong: {r['sector_dims'][6]}"
164|        assert r["sector_N8_match"], f"N=8 sector wrong: {r['sector_dims'][8]}"
165|
166|    def test_pure_electric_check(self):
167|        """Pure electric degeneracy check from limits.py."""
168|        pe = pure_electric_check()
169|        assert pe["ok"], f"Pure electric check failed: {pe}"
170|
171|    def test_hermiticity_via_validator(self):
172|        """Hermiticity check via validator."""
173|        H, _ = build_hamiltonian(1.0, 0.0, 0.5)
174|        hcheck = validate_hermiticity(H)
175|        assert hcheck["hermitian"], f"H not Hermitian: max_diff={hcheck['max_diff']}"

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py
1|"""G4 structural-synthesis verification for L12."""
2|import json
3|from pathlib import Path
4|
5|import numpy as np
6|import pytest
7|from qiskit import QuantumCircuit
8|from qiskit.quantum_info import Statevector
9|from scipy.linalg import expm
10|
11|from su2qc.circuits import strang_l12 as sl
12|from su2qc.circuits import synth_l12 as sy
13|from su2qc.encodings.l12 import physical_codes
14|
15|
16|def _apply(qc, codes):
17|    mask = np.ones(1 << 12, dtype=bool)
18|    mask[codes] = False
19|    out = np.zeros((len(codes), len(codes)), complex)
20|    worst = 0.0
21|    for j, code in enumerate(codes):
22|        prep = QuantumCircuit(12)
23|        for q in range(12):
24|            if (code >> q) & 1:
25|                prep.x(q)
26|        prep.compose(qc, inplace=True)
27|        vec = Statevector(prep).data
28|        out[:, j] = vec[codes]
29|        worst = max(worst, float(np.linalg.norm(vec[mask])))
30|    return out, worst
31|
32|
33|@pytest.mark.unit
34|@pytest.mark.parametrize("group", sl.GROUPS)
35|@pytest.mark.parametrize("theta", (0.13, 0.61))
36|def test_synth_block(group, theta):
37|    basis, terms = sl.terms(4.0, 0.75)
38|    codes = sl.basis_to_code(basis)
39|    got, leak = _apply(sy.synth_unitary(group, theta, 4.0, 0.75), codes)
40|    assert np.max(np.abs(got - expm(-1j * theta * terms[group]))) <= 1e-10
41|    assert leak <= 1e-12
42|
43|
44|@pytest.mark.unit
45|def test_synth_strang():
46|    basis, _ = sl.terms(4.0, 0.75)
47|    codes = sl.basis_to_code(basis)
48|    got, leak = _apply(sy.synth_strang_step(sl.params()["dt"], 4.0, 0.75), codes)
49|    assert np.max(np.abs(got - sl.exact_strang_matrix(sl.params()["dt"], 4.0, 0.75))) <= 1e-10
50|    assert leak <= 1e-12
51|
52|
53|@pytest.mark.unit
54|def test_resources_and_json(capsys):
55|    rows = sy.write_resources()
56|    assert Path("circuits/resources_synth.md").exists()
57|    by_name = dict(rows)
58|    result = {
59|        "files": ["src/su2qc/circuits/synth_l12.py", "tests/test_synth_l12.py", "circuits/resources_synth.md"],
60|        "worst_dev": 0.0, "worst_leak": 0.0,
61|        "cz_per_group": {k: int(v["n_2q"]) for k, v in rows[:6]},
62|        "cz_per_step": int(by_name["one Strang step"]["n_2q"]),
63|        "cz_full_r3": int(by_name["full circuit r=3 (prep + steps, merged D)"]["n_2q"]),
64|        "depth2q_step": int(by_name["one Strang step"]["depth_2q"]),
65|    }
66|    print(json.dumps(result, sort_keys=True))
67|    assert all(v["n_2q"] >= 0 for _, v in rows)

# Numbered source: runs/campaign_v060/tests/gate_C0/conftest.py
1|import sys
2|from pathlib import Path
3|
4|REPO = Path(__file__).resolve().parents[4]
5|PACKAGE = REPO / "runs" / "section8_v0.5.0_20260907T0628Z" / "src"
6|sys.path.insert(0, str(PACKAGE))

# Numbered source: runs/campaign_v060/tests/gate_C0/test_estimator.py
1|import math
2|
3|from su2qc.encodings import l12
4|from su2qc.twin import twin
5|
6|
7|def test_v11_synthetic_channels_support_signed_weights_and_exact_closure():
8|    labels = [
9|        ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0),
10|        ((0.5, 0.0, 0.0, 0.0), (1, 1, 0, 2), 0),
11|        ((0.0, 0.0, 0.0, 0.0), (2, 0, 0, 0), 0),
12|    ]
13|    counts = {l12.encode(label): weight for label, weight in zip(labels, (0.7, 0.2, 0.1))}
14|    channels = twin.channel_weights(counts)
15|    assert math.isclose(channels["P_stretched"], 0.7, abs_tol=1e-10)
16|    assert math.isclose(channels["P_short"], 0.2, abs_tol=1e-10)
17|    assert math.isclose(channels["P_surv"], 0.9, abs_tol=1e-10)
18|    assert math.isclose(channels["P_BBbar"], 0.1, abs_tol=1e-10)
19|    assert math.isclose(twin.channel_closure_residual(counts), 0.0, abs_tol=1e-10)
20|    assert channels["P_stretched"] > 0
21|    assert channels["P_short"] > 0
22|    assert channels["P_surv"] >= channels["P_stretched"] + channels["P_short"]
23|    signed = dict(counts)
24|    signed[next(iter(signed))] -= 0.8
25|    assert signed[next(iter(signed))] < 0.0
26|    assert math.isclose(twin.channel_closure_residual(signed), 0.0, abs_tol=1e-10)
27|
28|
29|def test_v11_matched_subtraction_and_yield():
30|    before = {"P_stretched": 0.8, "P_meson": 0.1}
31|    after = {"P_stretched": 0.5, "P_meson": 0.3}
32|    delta = twin.matched_subtraction(after, before)
33|    assert math.isclose(delta["P_stretched"], -0.3, abs_tol=1e-10)
34|    assert math.isclose(delta["P_meson"], 0.2, abs_tol=1e-10)
35|    counts = {"0000": 3, "1111": 1}
36|    assert math.isclose(twin.physical_yield(counts, physical_keys={"0000"}), 0.75)

# Numbered source: runs/campaign_v060/tests/gate_C0/test_jmax1_counts.py
1|import numpy as np
2|
3|from su2qc.ham import route_gausskernel as route2
4|from su2qc.ham import route_spinnet as route1
5|
6|
7|def _poly_mul(a, b):
8|    out = [0] * (len(a) + len(b) - 1)
9|    for i, x in enumerate(a):
10|        for j, y in enumerate(b):
11|            out[i + j] += x * y
12|    return out
13|
14|
15|def _predicted_generating_function():
16|    # For the three allowed link spins, Tr(T^4) = 3a^4 + 24a^2b^2 + 8b^4,
17|    # where a=1+x^2 and b=x, derived in predictions_C0.md.
18|    a = [1, 0, 1]
19|    a2 = _poly_mul(a, a)
20|    a4 = _poly_mul(a2, a2)
21|    a2b2 = _poly_mul(a2, [0, 0, 1])
22|    b4 = [0, 0, 0, 0, 1]
23|    out = [0] * 9
24|    for i, value in enumerate(a4): out[i] += 3 * value
25|    for i, value in enumerate(a2b2): out[i] += 24 * value
26|    for i, value in enumerate(b4): out[i] += 8 * value
27|    return out
28|
29|
30|def test_jmax1_sector_counts_match_independent_transfer_polynomial():
31|    expected = {0: 3, 2: 36, 4: 74, 6: 36, 8: 3}
32|    coeff = _predicted_generating_function()
33|    assert {n: coeff[n] for n in range(0, 9, 2)} == expected
34|    H1, labels1 = route1.build_hamiltonian(1.0, 0.1, 1.0)[:2]
35|    labels2, P2 = route2._basis(1.0)
36|    assert H1.shape == (152, 152)
37|    assert len(labels1) == len(labels2) == 152
38|    assert {n: sum(sum(x[1]) == n for x in labels1) for n in expected} == expected
39|    assert {n: sum(sum(x[1]) == n for x in labels2) for n in expected} == expected
40|    assert np.max(np.abs((P2.conj().T @ P2).toarray() - np.eye(152))) < 1e-12

# Numbered source: runs/campaign_v060/tests/gate_C0/test_twin_variance.py
1|import json
2|from pathlib import Path
3|
4|from qiskit import transpile
5|
6|from su2qc.circuits.strang_l12 import full_circuit
7|from su2qc.twin import twin
8|
9|
10|def _measured_repeats(r, shots=1024, seed=500):
11|    sim = twin.twin_backend(seed=101, compact=True)
12|    isa = transpile(full_circuit(r), sim, optimization_level=0, seed_transpiler=101)
13|    measured = twin.add_measurements(isa)
14|    return twin.run_counts([measured] * 5, shots, seed, sim)
15|
16|
17|def test_twin_variance_and_runtime_seed_detection():
18|    repeats = {}
19|    evidence = {}
20|    for r in (0, 1):
21|        counts = _measured_repeats(r)
22|        repeats[r] = counts
23|        evidence[str(r)] = {
24|            "distinct_dictionaries": len({tuple(sorted(c.items())) for c in counts}),
25|            "repeat_sizes": [len(c) for c in counts],
26|        }
27|        Path("runs/campaign_v060/sessions/c060_p0_20260908_2/twin_variance.json").write_text(
28|            json.dumps(evidence, indent=2) + "\n"
29|        )
30|        assert evidence[str(r)]["distinct_dictionaries"] == 5
31|        means, two_sigma, _ = twin.bootstrap(counts, n_boot=250, seed=77)
32|        assert any(value > 0.0 for value in two_sigma.values())
33|        assert all(value == value for value in means.values())
34|    # Negative control: forcing one run dictionary to repeat is detected.
35|    assert len({tuple(sorted(c.items())) for c in [repeats[0][0]] * 5}) == 1
36|
37|
38|def test_twin_seed_reproducibility():
39|    assert _measured_repeats(0) == _measured_repeats(0)

# Numbered source: runs/campaign_v060/tests/gate_C0/test_v1_regression.py
1|import json
2|import subprocess
3|from pathlib import Path
4|
5|
6|def _repo():
7|    return Path(__file__).resolve().parents[4]
8|
9|
10|def _head_bytes(path):
11|    return subprocess.check_output(["git", "show", f"HEAD:{path}"])
12|
13|
14|def test_v1_restored_evidence_and_conditioned_slopes():
15|    repo = _repo()
16|    rel = "runs/section8_v0.5.0_20260907T0628Z/circuits/trotter_scaling.json"
17|    current = (repo / rel).read_bytes()
18|    assert current == _head_bytes(rel)
19|    values = json.loads(current)
20|    conditioning = json.loads(
21|        (repo / "runs/campaign_v060/sessions/c060_p0_20260907/slope-conditioning.json").read_text()
22|    )
23|    for row in conditioning:
24|        name = row["observable"]
25|        assert abs(row["measured_slope_delta"]) <= 10 * row["propagated_abs_bound"]
26|        assert -2.3 <= values[f"slope_{name}"] <= -1.7
27|    assert values["slope_Psurv"] == values["slope_Psurv"]