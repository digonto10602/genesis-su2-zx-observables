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
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py",
    "module": "conventions.py",
    "name": "parity",
    "signature": "parity(v: int)",
    "line": 23,
    "end_line": 26,
    "docstring": "(-1)^{x+y} for vertex index v in 0..3.  v1,v3 even (+1); v2,v4 odd (-1).",
    "returns": [
      "1 if (x + y) % 2 == 0 else -1"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py",
    "module": "conventions.py",
    "name": "eta",
    "signature": "eta(l: int)",
    "line": 37,
    "end_line": 42,
    "docstring": "Staggered phase of link l: eta_x = 1, eta_y = (-1)^x  (x of the source).",
    "returns": [
      "1 if VERTICES[s][0] % 2 == 0 else -1",
      "1"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py",
    "module": "conventions.py",
    "name": "charge",
    "signature": "charge(v: int, n: int)",
    "line": 55,
    "end_line": 57,
    "docstring": "Local charge relative to the staggered vacuum: q_v = n_v - n_vac(v).",
    "returns": [
      "n - N_VAC[v]"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py",
    "module": "conventions.py",
    "name": "casimir",
    "signature": "casimir(j: float)",
    "line": 67,
    "end_line": 69,
    "docstring": "SU(2) quadratic Casimir j(j+1).",
    "returns": [
      "j * (j + 1.0)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py",
    "module": "conventions.py",
    "name": "coupling_electric",
    "signature": "coupling_electric(g2: float)",
    "line": 77,
    "end_line": 79,
    "docstring": "Coefficient of sum_l E_l^2.",
    "returns": [
      "g2 / 2.0"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py",
    "module": "conventions.py",
    "name": "coupling_magnetic",
    "signature": "coupling_magnetic(g2: float)",
    "line": 81,
    "end_line": 83,
    "docstring": "Coefficient of -Tr(U_box + U_box^dag) (i.e. H_B = -c * Tr(...)).",
    "returns": [
      "1.0 / (2.0 * g2)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py",
    "module": "conventions.py",
    "name": "tree_level_resonance",
    "signature": "tree_level_resonance(g2: float)",
    "line": 89,
    "end_line": 90,
    "docstring": null,
    "returns": [
      "3.0 * g2 / 16.0"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/compare.py",
    "module": "ham/compare.py",
    "name": "spectra_comparison",
    "signature": "spectra_comparison(jmax=0.5, points=COUPLING_POINTS)",
    "line": 45,
    "end_line": 60,
    "docstring": "Max relative deviation of sorted spectra between routes per point.",
    "returns": [
      "rows"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/compare.py",
    "module": "ham/compare.py",
    "name": "time_series_comparison",
    "signature": "time_series_comparison(g2=1.0, m=0.1875, jmax=0.5, times=TIMES)",
    "line": 88,
    "end_line": 106,
    "docstring": "Max abs deviation of stretched-string observables between routes.",
    "returns": [
      "(dev, s1)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py",
    "module": "ham/limits.py",
    "name": "pure_electric_check",
    "signature": "pure_electric_check(g2_big=1000000.0)",
    "line": 28,
    "end_line": 43,
    "docstring": "Spectrum at g2 -> inf, m = 0: electric levels with k-degeneracies.",
    "returns": [
      "{'degeneracies': got, 'rel_dev': float(rel), 'ok': bool(ok)}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py",
    "module": "ham/limits.py",
    "name": "frozen_matter_check",
    "signature": "frozen_matter_check(tol=1e-09)",
    "line": 46,
    "end_line": 99,
    "docstring": "m -> inf: the 2-state block (links all-0 / all-1/2, matter at vacuum)\nequals the monograph's one-plaquette H~1 after reconciliation.\n\nMonograph (repo core.py, n=1): H~1 = 1.5 I - 1.5 Z - 2x X, x = 2/g^4,\nH~ = 2H/g^2  =>  H1 = (g2/2)(1.5 I - 1.5 Z) - (2/g2) X  acting on\n(|0000>, |hhhh>) with Z|0000> = +|0000>.\nPatch H on the same 2 states: diag(0, 4*(g2/2)*(3/4)) = diag(0, 1.5 g2)\nfrom the electric term, mass term = m*const (equal on both, shift),\nmagnetic term couples them with element -(1/(2g2)) * w where w is the\nplaquette vertex-factor product; expected |w| = 2 (Tr over the two color\npaths), giving off-diagonal -1/g2... The reconciliation (documented in\nphysics/conventions_reconciliation.md) fixes the mapping:\n  H_patch|_2x2 = a I + b (H1_monograph) with b = 1 expected up to the\n  magnetic normalization ratio r = offdiag_patch / (-2/g2).\nThis check extracts the effective 2x2 block at large m numerically via\n2nd-order perturbation (large-m suppresses matter excitations) by exact\nprojection: keep the two basis states, project H (matter untouched by B,\nhopping leaves the block at O(1/m)).",
    "returns": [
      "{'dev': dev_diag, 'offdiag_times_g2': c, 'tol': tol, 'ok': bool(ok), 'note': 'off-diagonal coefficient recorded for reconciliation doc'}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py",
    "module": "ham/limits.py",
    "name": "magnetic_off_check",
    "signature": "magnetic_off_check(tol=1e-10)",
    "line": 102,
    "end_line": 122,
    "docstring": "B = 0 spectrum vs an independent periodic 1D 4-site SU(2) chain.",
    "returns": [
      "{'dev': dev, 'ok': dev <= tol, 'note': src}",
      "{'dev': float('nan'), 'ok': False, 'note': 'route1 lacks build_hamiltonian_no_magnetic'}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "kernel_dimension",
    "signature": "kernel_dimension(jmax)",
    "line": 165,
    "end_line": 166,
    "docstring": null,
    "returns": [
      "len(_basis(jmax)[0])"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "gauss_commutator_norms",
    "signature": "gauss_commutator_norms(jmax)",
    "line": 390,
    "end_line": 407,
    "docstring": "Max over v, a of max-abs entry of [G^a_v, H_term], per term group.",
    "returns": [
      "out"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "build_hamiltonian",
    "signature": "build_hamiltonian(g2, m, jmax)",
    "line": 422,
    "end_line": 431,
    "docstring": null,
    "returns": [
      "(H, labels, P)"
    ],
    "raises": [
      "NotImplementedError('route 2 builds the projected H only at jmax=1/2 tonight; at jmax=1 use kernel_dimension(1.0) (=152). See module docstring / DECISIONS.')"
    ]
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "build_hamiltonian_no_magnetic",
    "signature": "build_hamiltonian_no_magnetic(g2, m, jmax)",
    "line": 434,
    "end_line": 441,
    "docstring": null,
    "returns": [
      "(H, labels, P)"
    ],
    "raises": [
      "NotImplementedError('see build_hamiltonian')"
    ]
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "get_state",
    "signature": "get_state(label, basis_labels)",
    "line": 444,
    "end_line": 445,
    "docstring": null,
    "returns": [
      "basis_labels.index(label)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "E2_link",
    "signature": "E2_link(l, basis_labels)",
    "line": 466,
    "end_line": 467,
    "docstring": null,
    "returns": [
      "_obs(basis_labels)[0][l]"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "n_op",
    "signature": "n_op(v, basis_labels)",
    "line": 470,
    "end_line": 471,
    "docstring": null,
    "returns": [
      "_obs(basis_labels)[1][v]"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "N_total",
    "signature": "N_total(basis_labels)",
    "line": 474,
    "end_line": 475,
    "docstring": null,
    "returns": [
      "_obs(basis_labels)[2]"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "P_surv",
    "signature": "P_surv(basis_labels)",
    "line": 478,
    "end_line": 479,
    "docstring": null,
    "returns": [
      "_obs(basis_labels)[3]"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "P_meson",
    "signature": "P_meson(basis_labels)",
    "line": 482,
    "end_line": 483,
    "docstring": null,
    "returns": [
      "_obs(basis_labels)[4]"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py",
    "module": "ham/route_gausskernel.py",
    "name": "P_BBbar",
    "signature": "P_BBbar(basis_labels)",
    "line": 486,
    "end_line": 487,
    "docstring": null,
    "returns": [
      "_obs(basis_labels)[5]"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "enumerate_basis",
    "signature": "enumerate_basis(jmax: float)",
    "line": 234,
    "end_line": 312,
    "docstring": "Return list of basis labels ((j1,j2,j3,j4), (n1,n2,n3,n4), 0) for the given jmax.\n\nThe basis is constructed by iterating all allowed link spins and then, for each,\nall matter assignments that satisfy the 4 vertex constraints.",
    "returns": [
      "basis"
    ],
    "raises": [
      "ValueError(f'Unsupported jmax={jmax}; use 0.5 or 1.0')"
    ]
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "build_hamiltonian",
    "signature": "build_hamiltonian(g2: float, m: float, jmax: float)",
    "line": 433,
    "end_line": 528,
    "docstring": "Build the full route-1 Hamiltonian for the single plaquette.\n\nReturns (H_sparse, basis) where basis is the list of labels in the same order\nas the matrix rows/cols.\n\nPhysics:\n  H = H_elec + H_mass + H_hop + H_mag\n  H_elec = (g2/2) sum_l j_l(j_l+1)                     (diagonal)\n  H_mass = m sum_v parity_v n_v                          (diagonal, parity=+ - + -)\n  H_hop  = (1/2) sum_l ( eta_l psi^dag_{s(l)} U_l psi_{t(l)} + h.c. )  (off-diagonal)\n  H_mag  = -(1/(2g2)) Tr(U_box + U_box^dag)            (off-diagonal)",
    "returns": [
      "(H, basis)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "build_hamiltonian_no_magnetic",
    "signature": "build_hamiltonian_no_magnetic(g2: float, m: float, jmax: float)",
    "line": 531,
    "end_line": 577,
    "docstring": "Build the Hamiltonian without the magnetic term (electric + mass + hopping only).\n\nSame basis ordering as build_hamiltonian, useful for limit checks.",
    "returns": [
      "(H, basis)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "number_op",
    "signature": "number_op(v: int)",
    "line": 582,
    "end_line": 592,
    "docstring": "Return the number operator n_v for vertex v (diagonal in the basis).\n\nThe returned function takes (dim, basis) and returns a CSR matrix.",
    "returns": [
      "_no",
      "H.tocsr()"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "total_number",
    "signature": "total_number()",
    "line": 595,
    "end_line": 602,
    "docstring": "Return the total fermion number sum_v n_v (diagonal in the basis).",
    "returns": [
      "_no",
      "H.tocsr()"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "casimir_link",
    "signature": "casimir_link(l: int)",
    "line": 605,
    "end_line": 612,
    "docstring": "Return the electric casimir operator j_l(j_l+1) for link l (diagonal in the basis).",
    "returns": [
      "_no",
      "H.tocsr()"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "P_stretched",
    "signature": "P_stretched(g2: float, m: float, jmax: float)",
    "line": 634,
    "end_line": 638,
    "docstring": "Projector onto states with q = (+1, -1, 0, 0).",
    "returns": [
      "_charge_projector((1, -1, 0, 0), basis, dim)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "P_short",
    "signature": "P_short(g2: float, m: float, jmax: float)",
    "line": 641,
    "end_line": 645,
    "docstring": "Projector onto states with q = (+1, -1, 0, 0) \u2014 the short sector.",
    "returns": [
      "_charge_projector((1, -1, 0, 0), basis, dim)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "P_surv",
    "signature": "P_surv(g2: float, m: float, jmax: float)",
    "line": 648,
    "end_line": 652,
    "docstring": "Projector onto states with q = (+1, -1, 0, 0) (surviving stretched string).",
    "returns": [
      "_charge_projector((1, -1, 0, 0), basis, dim)"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "P_meson",
    "signature": "P_meson(g2: float, m: float, jmax: float)",
    "line": 655,
    "end_line": 664,
    "docstring": "Projector onto states with |q_v| = 1 for all v.",
    "returns": [
      "H.tocsr()"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "P_BBbar",
    "signature": "P_BBbar(g2: float, m: float, jmax: float)",
    "line": 667,
    "end_line": 676,
    "docstring": "Projector onto any state with |q_v| = 2 for some v (takes precedence).",
    "returns": [
      "H.tocsr()"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "charge",
    "signature": "charge(v: int, n: int)",
    "line": 680,
    "end_line": 682,
    "docstring": "Local charge relative to the staggered vacuum: q_v = n_v - n_vac(v).",
    "returns": [
      "n - N_VAC[v]"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "validate_dimensions",
    "signature": "validate_dimensions(jmax: float=0.5)",
    "line": 687,
    "end_line": 714,
    "docstring": "Validate that the basis dimension and sector counts match expectations.",
    "returns": [
      "result"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "validate_hermiticity",
    "signature": "validate_hermiticity(H: csr_matrix, atol: float=1e-13)",
    "line": 717,
    "end_line": 724,
    "docstring": "Check that H is Hermitian within tolerance.",
    "returns": [
      "{'hermitian': diff <= atol, 'max_diff': float(diff)}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "validate_commutator",
    "signature": "validate_commutator(H: csr_matrix, N_op: csr_matrix, atol: float=1e-13)",
    "line": 727,
    "end_line": 736,
    "docstring": "Check [H, N] = 0 within tolerance.",
    "returns": [
      "{'[H,N]': max_comm <= atol, 'max_comm': float(max_comm)}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py",
    "module": "ham/route_spinnet.py",
    "name": "pure_electric_check",
    "signature": "pure_electric_check(g2_big: float=1000000.0)",
    "line": 739,
    "end_line": 753,
    "docstring": "Spectrum at g2 -> inf, m = 0: electric levels with k-degeneracies.\n\nFrom limits.py pure_electric_check.",
    "returns": [
      "{'degeneracies': got, 'rel_dev': float(rel), 'ok': bool(ok)}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py",
    "module": "replicate.py",
    "name": "sha256_file",
    "signature": "sha256_file(path: str | Path)",
    "line": 13,
    "end_line": 14,
    "docstring": null,
    "returns": [
      "hashlib.sha256(Path(path).read_bytes()).hexdigest()"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py",
    "module": "replicate.py",
    "name": "manifest",
    "signature": "manifest(paths: list[str | Path])",
    "line": 17,
    "end_line": 18,
    "docstring": null,
    "returns": [
      "{str(Path(path)): sha256_file(path) for path in sorted(paths, key=str)}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py",
    "module": "replicate.py",
    "name": "compare_manifests",
    "signature": "compare_manifests(expected: dict[str, str], actual: dict[str, str])",
    "line": 21,
    "end_line": 24,
    "docstring": null,
    "returns": [
      "{'pass': not mismatches, 'mismatches': mismatches, 'count': len(keys)}"
    ],
    "raises": []
  },
  {
    "path": "runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py",
    "module": "replicate.py",
    "name": "write_manifest",
    "signature": "write_manifest(paths: list[str | Path], output: str | Path)",
    "line": 27,
    "end_line": 30,
    "docstring": null,
    "returns": [
      "values"
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

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py
1|"""FROZEN conventions for the SU(2) single-plaquette patch with dynamical matter.
2|
3|Frozen at G0 of run section8_v0.5.0_20260907T0628Z. DO NOT EDIT.
4|Both Hamiltonian routes, all encodings, circuits, and analysis import from here
5|and ONLY from here. Any objection goes to physics/conventions_objection_*.md.
6|
7|Model (Section 5.1 of the v0.5.0 prompt):
8|  Lattice units a = 1. One square plaquette, open boundaries.
9|  H = (g^2/2) sum_l E_l^2
10|    + m sum_v (-1)^{x_v+y_v} psi\dagger_v psi_v
11|    + (1/2) sum_l ( eta_l psi\dagger_{s(l)} U_l psi_{t(l)} + h.c. )
12|    - (1/(2 g^2)) Tr( U_box + U_box\dagger )
13|  U_box = U_l1 U_l2 U_l3\dagger U_l4\dagger   (counter-clockwise v1->v2->v3->v4->v1)
14|  E^2 = j(j+1) per link. Truncation j in {0, 1/2} (hardcore gluon); j_max = 1
15|  is built too for the truncation-error statement.
16|"""
17|
18|# ---------------------------------------------------------------- vertices
19|# index -> (x, y). Vertex numbering v1..v4 maps to python indices 0..3.
20|VERTICES = ((0, 0), (1, 0), (1, 1), (0, 1))  # v1, v2, v3, v4
21|N_VERTICES = 4
22|
23|def parity(v: int) -> int:
24|    """(-1)^{x+y} for vertex index v in 0..3.  v1,v3 even (+1); v2,v4 odd (-1)."""
25|    x, y = VERTICES[v]
26|    return 1 if (x + y) % 2 == 0 else -1
27|
28|PARITY = tuple(parity(v) for v in range(4))          # (+1, -1, +1, -1)
29|
30|# ---------------------------------------------------------------- links
31|# index -> (source_vertex, target_vertex, direction). Link numbering l1..l4
32|# maps to python indices 0..3.  l1: v1->v2 (x, y=0); l2: v2->v3 (y, x=1);
33|# l3: v4->v3 (x, y=1); l4: v1->v4 (y, x=0).
34|LINKS = ((0, 1, "x"), (1, 2, "y"), (3, 2, "x"), (0, 3, "y"))
35|N_LINKS = 4
36|
37|def eta(l: int) -> int:
38|    """Staggered phase of link l: eta_x = 1, eta_y = (-1)^x  (x of the source)."""
39|    s, _t, d = LINKS[l]
40|    if d == "x":
41|        return 1
42|    return 1 if VERTICES[s][0] % 2 == 0 else -1
43|
44|ETA = tuple(eta(l) for l in range(4))                # (+1, -1, +1, +1)
45|
46|# Plaquette orientation: U_box = U_0 U_1 U_2^dag U_3^dag (python link indices).
47|PLAQUETTE_SEQUENCE = ((0, +1), (1, +1), (2, -1), (3, -1))  # (link, +1=U / -1=Udag)
48|
49|# ---------------------------------------------------------------- matter
50|# Two-color staggered fermions, one doublet per vertex. 4 Fock states per site:
51|# n=0 color-singlet vacuum, n=1 doublet, n=2 doubly-occupied singlet (baryon).
52|# Staggered vacuum: even sites empty, odd sites full: n_vac = (0, 2, 0, 2).
53|N_VAC = (0, 2, 0, 2)
54|
55|def charge(v: int, n: int) -> int:
56|    """Local charge relative to the staggered vacuum: q_v = n_v - n_vac(v)."""
57|    return n - N_VAC[v]
58|
59|# Jordan-Wigner mode order for route 2 (redundant Kogut-Susskind space).
60|# Mode index 0..7 = (v1,c1),(v1,c2),(v2,c1),(v2,c2),(v3,c1),(v3,c2),(v4,c1),(v4,c2)
61|JW_ORDER = tuple((v, c) for v in range(4) for c in range(2))
62|
63|# ---------------------------------------------------------------- truncation
64|JMAX_HALF = 0.5   # primary truncation, 82 gauge-invariant states
65|JMAX_ONE = 1.0    # for the truncation-error statement, 152 states
66|
67|def casimir(j: float) -> float:
68|    """SU(2) quadratic Casimir j(j+1)."""
69|    return j * (j + 1.0)
70|
71|# Expected gauge-invariant dimensions (verified independently by both routes).
72|EXPECTED_DIM = {JMAX_HALF: 82, JMAX_ONE: 152}
73|# Fermion-number sector dims at jmax=1/2, N = 0,2,4,6,8:
74|EXPECTED_SECTOR_DIMS = {0: 2, 2: 20, 4: 38, 6: 20, 8: 2}
75|
76|# ---------------------------------------------------------------- couplings
77|def coupling_electric(g2: float) -> float:
78|    """Coefficient of sum_l E_l^2."""
79|    return g2 / 2.0
80|
81|def coupling_magnetic(g2: float) -> float:
82|    """Coefficient of -Tr(U_box + U_box^dag) (i.e. H_B = -c * Tr(...))."""
83|    return 1.0 / (2.0 * g2)
84|
85|HOPPING_PREFACTOR = 0.5   # (1/2) sum_l ( eta_l psi^dag_s U psi_t + h.c. )
86|
87|# Tree-level resonance (a=1): removing one j=1/2 link releases (g^2/2)(3/4);
88|# equals pair cost 2m at m* = 3 g^2 / 16.
89|def tree_level_resonance(g2: float) -> float:
90|    return 3.0 * g2 / 16.0
91|
92|# ---------------------------------------------------------------- bit orders
93|# Qiskit strings and displayed bitstrings use q_(N-1)...q_0 (repo-wide rule).
94|QISKIT_BIT_ORDER = "q_(N-1)...q_0"
95|
96|# Canonical basis-label form shared by both routes and compare.py:
97|# a state is labeled ((j1,j2,j3,j4), (n1,n2,n3,n4), intertwiner_tag) where
98|# j are half-integers as floats, n in {0,1,2}; intertwiner_tag disambiguates
99|# nothing at 2-valent vertices (always 0) but is kept for forward compat.
100|LABEL_DOC = "((j_l1..j_l4), (n_v1..n_v4), tag)"

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/compare.py
1|"""Verifier-owned comparison of the two independent Hamiltonian routes (G1).
2|
3|Basis-independent checks:
4|  * sorted spectra at >= 5 coupling points (incl. m = 0),
5|  * observable time series from the stretched string on t in [0, 10].
6|Owned by the VERIFY lane; neither route builder edits this file.
7|"""
8|
9|from __future__ import annotations
10|
11|import sys
12|from pathlib import Path
13|
14|import numpy as np
15|from scipy.linalg import eigh, expm
16|
17|SRC = Path(__file__).resolve().parents[2]
18|if str(SRC) not in sys.path:
19|    sys.path.insert(0, str(SRC))
20|
21|COUPLING_POINTS = [  # (g2, m), includes m = 0
22|    (1.0, 0.0),
23|    (1.0, 0.1875),   # tree-level resonance at g2=1
24|    (1.0, 0.5),
25|    (2.0, 0.375),
26|    (0.5, 0.2),
27|    (1.5, 1.0),
28|]
29|
30|STRETCHED = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)
31|TIMES = np.linspace(0.0, 10.0, 21)
32|
33|
34|def _get_routes():
35|    from su2qc.ham import route_spinnet as r1
36|    from su2qc.ham import route_gausskernel as r2
37|    return r1, r2
38|
39|
40|def _norm_label(label):
41|    (js, ns) = label[0], label[1]
42|    return (tuple(float(j) for j in js), tuple(int(n) for n in ns))
43|
44|
45|def spectra_comparison(jmax=0.5, points=COUPLING_POINTS):
46|    """Max relative deviation of sorted spectra between routes per point."""
47|    r1, r2 = _get_routes()
48|    rows = []
49|    for g2, m in points:
50|        out1 = r1.build_hamiltonian(g2, m, jmax)
51|        out2 = r2.build_hamiltonian(g2, m, jmax)
52|        H1 = out1[0].toarray()
53|        H2 = out2[0].toarray()
54|        e1 = np.sort(eigh(H1, eigvals_only=True))
55|        e2 = np.sort(eigh(H2, eigvals_only=True))
56|        scale = max(1.0, float(np.max(np.abs(e1))))
57|        dev = float(np.max(np.abs(e1 - e2)) / scale)
58|        rows.append({"g2": g2, "m": m, "max_rel_dev": dev,
59|                     "dim1": H1.shape[0], "dim2": H2.shape[0]})
60|    return rows
61|
62|
63|def _observables(route_mod, H, basis, psi0_index, times):
64|    """Time series of P_surv, n_v, E2_l from basis state psi0_index."""
65|    from su2qc import conventions as cv
66|    dim = H.shape[0]
67|    psi = np.zeros(dim, dtype=complex)
68|    psi[psi0_index] = 1.0
69|    # channel masks from labels (basis-independent definition)
70|    q = np.array([[cv.charge(v, int(lab[1][v])) for v in range(4)] for lab in basis])
71|    surv_mask = np.all(q == np.array([1, -1, 0, 0]), axis=1)
72|    e2 = np.array([[cv.casimir(float(lab[0][l])) for l in range(4)] for lab in basis])
73|    nmat = np.array([[int(lab[1][v]) for v in range(4)] for lab in basis])
74|    dt = times[1] - times[0]
75|    U = expm(-1j * H * dt)
76|    series = []
77|    for i, t in enumerate(times):
78|        p = np.abs(psi) ** 2
79|        series.append(
80|            {"t": float(t),
81|             "P_surv": float(p @ surv_mask),
82|             "n": (p @ nmat).tolist(),
83|             "E2": (p @ e2).tolist()})
84|        psi = U @ psi
85|    return series
86|
87|
88|def time_series_comparison(g2=1.0, m=0.1875, jmax=0.5, times=TIMES):
89|    """Max abs deviation of stretched-string observables between routes."""
90|    r1, r2 = _get_routes()
91|    out1 = r1.build_hamiltonian(g2, m, jmax)
92|    out2 = r2.build_hamiltonian(g2, m, jmax)
93|    H1, b1 = out1[0].toarray(), out1[1]
94|    H2, b2 = out2[0].toarray(), out2[1]
95|    tgt = _norm_label(STRETCHED)
96|    i1 = [k for k, lab in enumerate(b1) if _norm_label(lab) == tgt]
97|    i2 = [k for k, lab in enumerate(b2) if _norm_label(lab) == tgt]
98|    assert len(i1) == 1 and len(i2) == 1, (len(i1), len(i2))
99|    s1 = _observables(r1, H1, b1, i1[0], times)
100|    s2 = _observables(r2, H2, b2, i2[0], times)
101|    dev = 0.0
102|    for a, b in zip(s1, s2):
103|        dev = max(dev, abs(a["P_surv"] - b["P_surv"]))
104|        dev = max(dev, float(np.max(np.abs(np.array(a["n"]) - np.array(b["n"])))))
105|        dev = max(dev, float(np.max(np.abs(np.array(a["E2"]) - np.array(b["E2"])))))
106|    return dev, s1
107|
108|
109|if __name__ == "__main__":
110|    rows = spectra_comparison()
111|    for r in rows:
112|        print(r)
113|    dev, _ = time_series_comparison()
114|    print("time_series_max_abs_dev", dev)

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py
1|"""Verifier-owned limit tests for gate G1.
2|
3|  * pure_electric_check: g2 -> infinity degeneracy pattern 16,16,18,16,16.
4|  * frozen_matter_check: m -> infinity 2x2 block equals the monograph's
5|    one-plaquette H~1 after a documented normalization reconciliation.
6|  * magnetic_off_check: B = 0 spectrum equals an independently constructed
7|    4-site periodic 1+1D SU(2) chain (built in limits_1d.py by a separate
8|    builder; falls back to a cross-route B-off comparison if absent, and
9|    reports which was used).
10|"""
11|
12|from __future__ import annotations
13|
14|import sys
15|from pathlib import Path
16|
17|import numpy as np
18|from scipy.linalg import eigh
19|
20|SRC = Path(__file__).resolve().parents[2]
21|if str(SRC) not in sys.path:
22|    sys.path.insert(0, str(SRC))
23|
24|ROOT = Path(__file__).resolve().parents[4].parent  # SU2ZX repo root
25|sys.path.insert(0, str(ROOT / "src"))
26|
27|
28|def pure_electric_check(g2_big=1e6):
29|    """Spectrum at g2 -> inf, m = 0: electric levels with k-degeneracies."""
30|    from su2qc import conventions as cv
31|    from su2qc.ham import route_spinnet as r1
32|    H, basis = r1.build_hamiltonian(g2_big, 0.0, 0.5)[:2]
33|    evals = np.sort(eigh(H.toarray(), eigvals_only=True))
34|    # electric energy of k excited links: (g2/2)(3/4)k
35|    unit = g2_big / 2.0 * 0.75
36|    ks = np.rint(evals / unit).astype(int)
37|    got = [int(np.sum(ks == k)) for k in range(5)]
38|    # relative check 1e-8 at g2 = 1e6
39|    rel = np.max(np.abs(evals - ks * unit)) / unit
40|    ok = got == [16, 16, 18, 16, 16] and rel <= 1e-8 * g2_big / 1e6 * 100
41|    # NOTE: hopping/magnetic are O(1); rel deviation from pure electric is
42|    # O(1/unit) ~ 2.7e-6/g2 in absolute units -> relative ~ 3.6e-12 at 1e6.
43|    return {"degeneracies": got, "rel_dev": float(rel), "ok": bool(ok)}
44|
45|
46|def frozen_matter_check(tol=1e-9):
47|    """m -> inf: the 2-state block (links all-0 / all-1/2, matter at vacuum)
48|    equals the monograph's one-plaquette H~1 after reconciliation.
49|
50|    Monograph (repo core.py, n=1): H~1 = 1.5 I - 1.5 Z - 2x X, x = 2/g^4,
51|    H~ = 2H/g^2  =>  H1 = (g2/2)(1.5 I - 1.5 Z) - (2/g2) X  acting on
52|    (|0000>, |hhhh>) with Z|0000> = +|0000>.
53|    Patch H on the same 2 states: diag(0, 4*(g2/2)*(3/4)) = diag(0, 1.5 g2)
54|    from the electric term, mass term = m*const (equal on both, shift),
55|    magnetic term couples them with element -(1/(2g2)) * w where w is the
56|    plaquette vertex-factor product; expected |w| = 2 (Tr over the two color
57|    paths), giving off-diagonal -1/g2... The reconciliation (documented in
58|    physics/conventions_reconciliation.md) fixes the mapping:
59|      H_patch|_2x2 = a I + b (H1_monograph) with b = 1 expected up to the
60|      magnetic normalization ratio r = offdiag_patch / (-2/g2).
61|    This check extracts the effective 2x2 block at large m numerically via
62|    2nd-order perturbation (large-m suppresses matter excitations) by exact
63|    projection: keep the two basis states, project H (matter untouched by B,
64|    hopping leaves the block at O(1/m)).
65|    """
66|    from su2qc.ham import route_spinnet as r1
67|    g2 = 1.3
68|    m_big = 1e7
69|    tol = 1e-8  # documented relaxation: residual is the physical O(h^2/m)
70|    # perturbative shift (~2.5e-9 at m=1e7), not a construction error.
71|    H, basis = r1.build_hamiltonian(g2, m_big, 0.5)[:2]
72|    Hd = H.toarray()
73|    vac = ((0.0, 0.0, 0.0, 0.0), (0, 2, 0, 2))
74|    exc = ((0.5, 0.5, 0.5, 0.5), (0, 2, 0, 2))
75|    idx = {}
76|    for k, lab in enumerate(basis):
77|        key = (tuple(float(j) for j in lab[0]), tuple(int(n) for n in lab[1]))
78|        if key in (vac, exc):
79|            idx[key] = k
80|    assert len(idx) == 2, idx
81|    i0, i1 = idx[vac], idx[exc]
82|    block = Hd[np.ix_([i0, i1], [i0, i1])]
83|    # subtract the common mass offset
84|    block = block - block[0, 0] * np.eye(2)
85|    # monograph H1 in physical units on (|0000>,|hhhh>): electric diag(0,1.5 g2)
86|    # magnetic off-diagonal -1/g2 (Tr U_box on the 2-state block = 2 paths /2)
87|    expect = np.array([[0.0, 0.0], [0.0, 1.5 * g2]])
88|    offd = block[0, 1]
89|    # reconciliation: monograph x-term coefficient -2x*(g2/2) = -2/g2^... :
90|    # H~1 X-coeff -2x, H = (g2/2) H~ -> -(g2/2)(2)(2/g^4) = -2/g^3? See
91|    # physics/conventions_reconciliation.md for the resolved factor; here we
92|    # check structure: diagonal matches electric splitting to tol, and the
93|    # off-diagonal is real, negative, and g2-scaled as c/g2 with c recorded.
94|    dev_diag = float(np.max(np.abs(np.diag(block) - np.diag(expect))))
95|    c = float(np.real(offd) * g2)
96|    ok = dev_diag <= tol * max(1.0, 1.5 * g2) and abs(np.imag(offd)) <= 1e-12 \
97|        and np.real(offd) < 0
98|    return {"dev": dev_diag, "offdiag_times_g2": c, "tol": tol, "ok": bool(ok),
99|            "note": "off-diagonal coefficient recorded for reconciliation doc"}
100|
101|
102|def magnetic_off_check(tol=1e-10):
103|    """B = 0 spectrum vs an independent periodic 1D 4-site SU(2) chain."""
104|    from su2qc.ham import route_spinnet as r1
105|    g2, m = 1.1, 0.3
106|    H, basis = r1.build_hamiltonian_no_magnetic(g2, m, 0.5)[:2] \
107|        if hasattr(r1, "build_hamiltonian_no_magnetic") else (None, None)
108|    if H is None:
109|        return {"dev": float("nan"), "ok": False,
110|                "note": "route1 lacks build_hamiltonian_no_magnetic"}
111|    e1 = np.sort(eigh(H.toarray(), eigvals_only=True))
112|    try:
113|        from su2qc.ham import limits_1d
114|        e2 = np.sort(limits_1d.chain_spectrum(g2, m))
115|        src = "independent limits_1d chain"
116|    except ImportError:
117|        from su2qc.ham import route_gausskernel as r2
118|        H2 = r2.build_hamiltonian_no_magnetic(g2, m, 0.5)[0]
119|        e2 = np.sort(eigh(H2.toarray(), eigvals_only=True))
120|        src = "cross-route B-off comparison (limits_1d unavailable)"
121|    dev = float(np.max(np.abs(e1 - e2)) / max(1.0, np.max(np.abs(e1))))
122|    return {"dev": dev, "ok": dev <= tol, "note": src}
123|
124|
125|if __name__ == "__main__":
126|    print(pure_electric_check())
127|    print(frozen_matter_check())
128|    print(magnetic_off_check())

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py
1|"""Route 2: redundant Kogut-Susskind space followed by Gauss-law projection.
2|
3|Construction:
4|  * Each link is a truncated rigid rotor |j, mL, mR> (dim 5 at jmax=1/2).
5|  * Matter: 8 Jordan-Wigner fermionic modes in the frozen order (v-major).
6|  * The physical basis is built from vertex-local Gauss singlets (codex-built,
7|    verified: dims 82/152, sector dims 2,20,38,20,2, electric clusters).
8|  * H is built on the FULL redundant space (electric, mass, 4 hoppings with JW
9|    strings, plaquette trace) and projected: H_phys = P^dag H_red P.
10|  * The U matrix-element convention (which color index is conjugated) is
11|    selected NUMERICALLY as the unique variant that makes [G^a_v, H_hop] = 0;
12|    the choice is recorded in U_CONVENTION after first build.
13|
14|Limitation (recorded in run/DECISIONS.md): at jmax=1 only the kernel dimension
15|(152) is computed by this route; the projected H_1 matrix is route-1-only
16|(redundant dim 14^4*256 ~ 9.8M exceeds the night's memory/time budget).
17|Route agreement is gated at jmax=1/2 per the run prompt (G1 criterion 3).
18|"""
19|from __future__ import annotations
20|
21|import itertools
22|
23|import numpy as np
24|from scipy.linalg import eigh
25|from scipy.sparse import csr_matrix, diags, hstack, identity, kron
26|
27|from ..conventions import (ETA, LINKS, N_VAC, PARITY, casimir,
28|                           coupling_electric, coupling_magnetic,
29|                           HOPPING_PREFACTOR)
30|
31|# ------------------------------------------------------------------ helpers
32|
33|def _spins(jmax):
34|    return tuple(k / 2 for k in range(int(2 * jmax) + 1))
35|
36|
37|def _link_states(jmax):
38|    return [(j, ml, mr) for j in _spins(jmax)
39|            for ml in np.arange(-j, j + 1, 1.0)
40|            for mr in np.arange(-j, j + 1, 1.0)]
41|
42|
43|def _spin(j):
44|    m = np.arange(-j, j + 1, 1.0)
45|    z = np.diag(m).astype(complex)
46|    p = np.zeros((len(m), len(m)), complex)
47|    for i, x in enumerate(m[:-1]):
48|        p[i + 1, i] = np.sqrt(j * (j + 1) - x * (x + 1))
49|    return ((p + p.T.conj()) / 2, -1j * (p - p.T.conj()) / 2, z)
50|
51|
52|def _cg(j, m, a, jp):
53|    """CG(j,m;1/2,a|jp,m+a), a = +-1/2, closed forms."""
54|    d = 2 * j + 1
55|    if abs(jp - j - .5) < 1e-10:
56|        return np.sqrt((j + m + 1) / d) if a > 0 else np.sqrt((j - m + 1) / d)
57|    if abs(jp - j + .5) < 1e-10:
58|        return -np.sqrt((j - m) / d) if a > 0 else np.sqrt((j + m) / d)
59|    return 0.0
60|
61|
62|# ------------------------------------------- vertex singlets (codex, verified)
63|
64|def _local_fermions():
65|    aa = []
66|    for c in range(2):
67|        x = np.zeros((4, 4), complex)
68|        for b in range(4):
69|            if b & (1 << c):
70|                x[b ^ (1 << c), b] = (-1) ** sum((b >> k) & 1 for k in range(c))
71|        aa.append(x)
72|    out = []
73|    for T in (np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2,
74|              np.diag([.5, -.5])):
75|        out.append(sum(T[a, b] * aa[a].conj().T @ aa[b]
76|                       for a in range(2) for b in range(2)))
77|    return out
78|
79|
80|# vertex v -> ((link_a, link_b), (sign_a, sign_b)); end m-index mapping below.
81|_ENDS = (((0, 3), (1, 1)), ((0, 1), (1, 1)), ((1, 2), (1, 1)), ((2, 3), (1, 1)))
82|
83|
84|def _local_singlet(ja, jb, n, signs):
85|    da, db = int(2 * ja + 1), int(2 * jb + 1)
86|    Ia, Ib = np.eye(da), np.eye(db)
87|    q = _local_fermions()
88|    gs = []
89|    for a in range(3):
90|        gs.append(np.kron(np.kron(signs[0] * _spin(ja)[a], Ib), np.eye(4))
91|                  + np.kron(np.kron(Ia, signs[1] * _spin(jb)[a]), np.eye(4))
92|                  + np.kron(np.kron(Ia, Ib), q[a]))
93|    K = sum(x @ x for x in gs)
94|    inds = [(ia * db + ib) * 4 + b for ia in range(da) for ib in range(db)
95|            for b in range(4) if b.bit_count() == n]
96|    w, v = eigh(K[np.ix_(inds, inds)])
97|    if len(np.where(w < 2e-10)[0]):
98|        x = np.zeros(da * db * 4, complex)
99|        x[inds] = v[:, np.where(w < 2e-10)[0][0]]
100|        return x.reshape(da, db, 4)
101|    return None
102|
103|
104|def _physical_basis(jmax):
105|    states = _link_states(jmax)
106|    dl = len(states)
107|    dm = 256
108|    labels = []
109|    cols = []
110|    for js in itertools.product(_spins(jmax), repeat=4):
111|        for ns in itertools.product(range(3), repeat=4):
112|            loc = [_local_singlet(js[a], js[b], ns[v], sgn)
113|                   for v, ((a, b), sgn) in enumerate(_ENDS)]
114|            if any(x is None for x in loc):
115|                continue
116|            entries = {}
117|            nz = [[(tuple(ind), x[tuple(ind)])
118|                   for ind in np.argwhere(abs(x) > 1e-12)] for x in loc]
119|            for items in itertools.product(*nz):
120|                inds = tuple(z[0] for z in items)
121|                amp = np.prod([z[1] for z in items])
122|                if abs(amp) < 1e-11:
123|                    continue
124|                ml = [None] * 4
125|                mr = [None] * 4
126|                fb = 0
127|                for v, ((a, b), _) in enumerate(_ENDS):
128|                    ia, ib, bit = inds[v]
129|                    fb |= bit << (2 * v)
130|                    if v == 0:
131|                        ml[0], ml[3] = ia, ib
132|                    elif v == 1:
133|                        mr[0], ml[1] = ia, ib
134|                    elif v == 2:
135|                        mr[1], mr[2] = ia, ib
136|                    else:
137|                        ml[2], mr[3] = ia, ib
138|                li = []
139|                for l, j in enumerate(js):
140|                    mm = np.arange(-j, j + 1, 1.0)
141|                    li.append(states.index((j, mm[ml[l]], mm[mr[l]])))
142|                idx = (((li[0] * dl + li[1]) * dl + li[2]) * dl + li[3]) * dm + fb
143|                entries[idx] = entries.get(idx, 0) + amp
144|            rows = np.fromiter(entries, dtype=np.int64)
145|            data = np.fromiter(entries.values(), dtype=complex)
146|            col = csr_matrix((data, (rows, np.zeros(len(rows), dtype=np.int64))),
147|                             shape=(dl ** 4 * dm, 1), dtype=complex)
148|            col = col / np.sqrt(float(col.multiply(col.conj()).sum().real))
149|            cols.append(col)
150|            labels.append((tuple(float(x) for x in js),
151|                           tuple(int(x) for x in ns), 0))
152|    return labels, hstack(cols, format="csc")
153|
154|
155|_CACHE = {}
156|
157|
158|def _basis(jmax):
159|    jmax = float(jmax)
160|    if jmax not in _CACHE:
161|        _CACHE[jmax] = _physical_basis(jmax)
162|    return _CACHE[jmax]
163|
164|
165|def kernel_dimension(jmax):
166|    return len(_basis(jmax)[0])
167|
168|
169|# ------------------------------------------------------- full-space operators
170|
171|# color index alpha in {+1/2: c=0, -1/2: c=1}
172|_ALPHAS = (0.5, -0.5)
173|
174|
175|def _link_JLR(jmax):
176|    """(JL[a], JR[a]) dl x dl sparse, a = x,y,z."""
177|    states = _link_states(jmax)
178|    dl = len(states)
179|    idx = {s: i for i, s in enumerate(states)}
180|    JL = [np.zeros((dl, dl), complex) for _ in range(3)]
181|    JR = [np.zeros((dl, dl), complex) for _ in range(3)]
182|    for j in _spins(jmax):
183|        mm = np.arange(-j, j + 1, 1.0)
184|        S = _spin(j)
185|        for a in range(3):
186|            for i1, m1 in enumerate(mm):
187|                for i2, m2 in enumerate(mm):
188|                    if abs(S[a][i1, i2]) < 1e-15:
189|                        continue
190|                    for mo in mm:  # spectator index
191|                        JL[a][idx[(j, m1, mo)], idx[(j, m2, mo)]] += S[a][i1, i2]
192|                        JR[a][idx[(j, mo, m1)], idx[(j, mo, m2)]] += S[a][i1, i2]
193|    return ([csr_matrix(x) for x in JL], [csr_matrix(x) for x in JR])
194|
195|
196|def _link_U(jmax, conjL, conjR):
197|    """U[(alpha,beta)] dl x dl sparse; conjX conjugates that color index."""
198|    states = _link_states(jmax)
199|    dl = len(states)
200|    idx = {s: i for i, s in enumerate(states)}
201|    spins = _spins(jmax)
202|    U = {}
203|    for al in _ALPHAS:
204|        for be in _ALPHAS:
205|            M = np.zeros((dl, dl), complex)
206|            for (j, mL, mR) in states:
207|                for jp in (j + .5, j - .5):
208|                    if jp < -1e-10 or jp > max(spins) + 1e-10:
209|                        continue
210|                    jp = abs(round(jp * 2)) / 2
211|                    if jp not in spins:
212|                        continue
213|                    pref = np.sqrt((2 * j + 1) / (2 * jp + 1))
214|                    aL, sL = (al, 1.0) if not conjL else (-al, (1 if al > 0 else -1))
215|                    aR, sR = (be, 1.0) if not conjR else (-be, (1 if be > 0 else -1))
216|                    mLp, mRp = mL + aL, mR + aR
217|                    if abs(mLp) > jp + 1e-10 or abs(mRp) > jp + 1e-10:
218|                        continue
219|                    fL = _cg(j, mL, aL, jp)
220|                    fR = _cg(j, mR, aR, jp)
221|                    if abs(fL * fR) < 1e-15:
222|                        continue
223|                    M[idx[(jp, mLp, mRp)], idx[(j, mL, mR)]] += \
224|                        pref * sL * sR * fL * fR
225|            U[(al, be)] = csr_matrix(M)
226|    return U
227|
228|
229|def _fermion_ops():
230|    """Global JW annihilation ops a_k on the 256-dim space, k = 2v + c."""
231|    dm = 256
232|    ops = []
233|    for k in range(8):
234|        rows, cols, data = [], [], []
235|        for fb in range(dm):
236|            if fb & (1 << k):
237|                sign = (-1) ** bin(fb & ((1 << k) - 1)).count("1")
238|                rows.append(fb ^ (1 << k))
239|                cols.append(fb)
240|                data.append(sign)
241|        ops.append(csr_matrix((data, (rows, cols)), shape=(dm, dm), dtype=complex))
242|    return ops
243|
244|
245|def _embed_link(op, l, dl, dm):
246|    """kron: identity on links < l, op on link l, identity after, identity fermions."""
247|    mats = [identity(dl, format="csr", dtype=complex)] * 4
248|    mats[l] = op
249|    out = mats[0]
250|    for m in mats[1:]:
251|        out = kron(out, m, format="csr")
252|    return kron(out, identity(dm, format="csr", dtype=complex), format="csr")
253|
254|
255|def _embed_links_fermi(link_ops, fermi_op, dl, dm):
256|    """link_ops: dict l -> op (missing = identity); fermi_op on 256."""
257|    mats = [link_ops.get(l, identity(dl, format="csr", dtype=complex))
258|            for l in range(4)]
259|    out = mats[0]
260|    for m in mats[1:]:
261|        out = kron(out, m, format="csr")
262|    return kron(out, fermi_op, format="csr")
263|
264|
265|_SIGMA = (np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2,
266|          np.diag([0.5, -0.5]).astype(complex))
267|
268|
269|def _gauss_ops(jmax):
270|    """G[a][v] on the full redundant space."""
271|    dl = len(_link_states(jmax))
272|    dm = 256
273|    JL, JR = _link_JLR(jmax)
274|    f = _fermion_ops()
275|    G = [[None] * 4 for _ in range(3)]
276|    for v in range(4):
277|        # link ends at v (per _ENDS / frozen conventions)
278|        ends = []
279|        for l, (s, t, _d) in enumerate(LINKS):
280|            if s == v:
281|                ends.append((l, "L"))
282|            if t == v:
283|                ends.append((l, "R"))
284|        for a in range(3):
285|            Q = csr_matrix((dm, dm), dtype=complex)
286|            for c1 in range(2):
287|                for c2 in range(2):
288|                    if abs(_SIGMA[a][c1, c2]) < 1e-15:
289|                        continue
290|                    Q = Q + _SIGMA[a][c1, c2] * \
291|                        (f[2 * v + c1].conj().T.tocsr() @ f[2 * v + c2])
292|            g = _embed_links_fermi({}, Q, dl, dm)
293|            for (l, end) in ends:
294|                op = JL[a] if end == "L" else JR[a]
295|                g = g + _embed_link(op, l, dl, dm)
296|            G[a][v] = g
297|    return G
298|
299|
300|def _c_of_alpha(al):
301|    return 0 if al > 0 else 1
302|
303|
304|def _build_terms(jmax, conjL, conjR):
305|    """All Hamiltonian term groups on the full redundant space (coefficient-free
306|    where possible): returns dict with electric, mass, hop_l (l=0..3, WITHOUT
307|    the 1/2 eta prefactor), trU (the plaquette trace, not Hermitized)."""
308|    states = _link_states(jmax)
309|    dl = len(states)
310|    dm = 256
311|    U = _link_U(jmax, conjL, conjR)
312|    Udag = {k: v.conj().T.tocsr() for k, v in U.items()}
313|    f = _fermion_ops()
314|    fdag = [x.conj().T.tocsr() for x in f]
315|
316|    e2_link = diags([casimir(s[0]) for s in states], format="csr", dtype=complex)
317|    electric = sum(_embed_link(e2_link, l, dl, dm) for l in range(4))
318|
319|    nmodes = [fdag[k] @ f[k] for k in range(8)]
320|    mass_f = sum(PARITY[v] * (nmodes[2 * v] + nmodes[2 * v + 1]) for v in range(4))
321|    mass = _embed_links_fermi({}, mass_f.tocsr(), dl, dm)
322|
323|    hops = []
324|    for l, (s, t, _d) in enumerate(LINKS):
325|        h = None
326|        for al in _ALPHAS:
327|            for be in _ALPHAS:
328|                fpart = (fdag[2 * s + _c_of_alpha(al)] @ f[2 * t + _c_of_alpha(be)])
329|                term = _embed_links_fermi({l: U[(al, be)]}, fpart.tocsr(), dl, dm)
330|                h = term if h is None else h + term
331|        h = h + h.conj().T.tocsr()  # + h.c.
332|        hops.append(h)
333|
334|    # plaquette trace: sum_{a,b,c,d} U0^{ab} U1^{bc} (U2^dag)^{cd} (U3^dag)^{da}
335|    # color-matrix dagger: (U^dag)^{cd} = adjoint of U^{dc}
336|    trU = None
337|    ident_f = identity(dm, format="csr", dtype=complex)
338|    for a_ in _ALPHAS:
339|        for b_ in _ALPHAS:
340|            for c_ in _ALPHAS:
341|                for d_ in _ALPHAS:
342|                    ops = {0: U[(a_, b_)], 1: U[(b_, c_)],
343|                           2: Udag[(d_, c_)], 3: Udag[(a_, d_)]}
344|                    term = _embed_links_fermi(ops, ident_f, dl, dm)
345|                    trU = term if trU is None else trU + term
346|    return {"electric": electric, "mass": mass, "hops": hops, "trU": trU}
347|
348|
349|_TERMS_CACHE = {}
350|U_CONVENTION = {}
351|
352|
353|def _select_convention(jmax=0.5):
354|    """Pick (conjL, conjR) as the variant with vanishing [G, hop] and [G, trU]."""
355|    key = float(jmax)
356|    if key in U_CONVENTION:
357|        return U_CONVENTION[key]
358|    G = _gauss_ops(jmax)
359|    best = None
360|    for conjL in (False, True):
361|        for conjR in (False, True):
362|            terms = _build_terms(jmax, conjL, conjR)
363|            worst = 0.0
364|            for op in [terms["hops"][0], terms["trU"]]:
365|                for a in range(3):
366|                    for v in range(4):
367|                        c = (G[a][v] @ op - op @ G[a][v])
368|                        if c.nnz:
369|                            worst = max(worst, float(np.max(np.abs(c.data))))
370|                if worst > 1e-10:
371|                    break
372|            if worst <= 1e-10:
373|                best = (conjL, conjR, terms)
374|                break
375|        if best:
376|            break
377|    assert best is not None, "no U convention makes [G,H]=0 -- construction bug"
378|    U_CONVENTION[key] = (best[0], best[1])
379|    _TERMS_CACHE[key] = best[2]
380|    return U_CONVENTION[key]
381|
382|
383|def _terms(jmax):
384|    key = float(jmax)
385|    if key not in _TERMS_CACHE:
386|        _select_convention(key)
387|    return _TERMS_CACHE[key]
388|
389|
390|def gauss_commutator_norms(jmax):
391|    """Max over v, a of max-abs entry of [G^a_v, H_term], per term group."""
392|    jmax = float(jmax)
393|    terms = _terms(jmax)
394|    G = _gauss_ops(jmax)
395|    named = {"electric": terms["electric"], "mass": terms["mass"],
396|             **{f"hop_{l}": terms["hops"][l] for l in range(4)},
397|             "magnetic": (terms["trU"] + terms["trU"].conj().T.tocsr())}
398|    out = {}
399|    for name, op in named.items():
400|        worst = 0.0
401|        for a in range(3):
402|            for v in range(4):
403|                c = G[a][v] @ op - op @ G[a][v]
404|                if c.nnz:
405|                    worst = max(worst, float(np.max(np.abs(c.data))))
406|        out[name] = worst
407|    return out
408|
409|
410|# ------------------------------------------------------------- projected API
411|
412|def _h_red(g2, m, jmax, magnetic=True):
413|    t = _terms(jmax)
414|    H = coupling_electric(g2) * t["electric"] + m * t["mass"]
415|    for l in range(4):
416|        H = H + HOPPING_PREFACTOR * ETA[l] * t["hops"][l]
417|    if magnetic:
418|        H = H - coupling_magnetic(g2) * (t["trU"] + t["trU"].conj().T.tocsr())
419|    return H
420|
421|
422|def build_hamiltonian(g2, m, jmax):
423|    jmax = float(jmax)
424|    if jmax > 0.75:
425|        raise NotImplementedError(
426|            "route 2 builds the projected H only at jmax=1/2 tonight; at jmax=1 "
427|            "use kernel_dimension(1.0) (=152). See module docstring / DECISIONS.")
428|    labels, P = _basis(jmax)
429|    H = (P.conj().T @ _h_red(g2, m, jmax) @ P).tocsr()
430|    H = ((H + H.conj().T) / 2).tocsr()  # kill 1e-17 asymmetry noise
431|    return H, labels, P
432|
433|
434|def build_hamiltonian_no_magnetic(g2, m, jmax):
435|    jmax = float(jmax)
436|    if jmax > 0.75:
437|        raise NotImplementedError("see build_hamiltonian")
438|    labels, P = _basis(jmax)
439|    H = (P.conj().T @ _h_red(g2, m, jmax, magnetic=False) @ P).tocsr()
440|    H = ((H + H.conj().T) / 2).tocsr()
441|    return H, labels, P
442|
443|
444|def get_state(label, basis_labels):
445|    return basis_labels.index(label)
446|
447|
448|# ------------------------------------------------------ diagonal observables
449|
450|def _obs(labels):
451|    n = len(labels)
452|    E = [diags([casimir(x[0][l]) for x in labels], format="csr")
453|         for l in range(4)]
454|    nv = [diags([x[1][v] for x in labels], format="csr") for v in range(4)]
455|    N = sum(nv[1:], nv[0])
456|    q = [[x[1][v] - N_VAC[v] for x in labels] for v in range(4)]
457|    Psurv = diags([int(tuple(q[v][i] for v in range(4)) == (1, -1, 0, 0))
458|                   for i in range(n)], format="csr")
459|    Pmes = diags([int(all(abs(q[v][i]) == 1 for v in range(4)))
460|                  for i in range(n)], format="csr")
461|    Pbb = diags([int(any(abs(q[v][i]) == 2 for v in range(4)))
462|                 for i in range(n)], format="csr")
463|    return E, nv, N, Psurv, Pmes, Pbb
464|
465|
466|def E2_link(l, basis_labels):
467|    return _obs(basis_labels)[0][l]
468|
469|
470|def n_op(v, basis_labels):
471|    return _obs(basis_labels)[1][v]
472|
473|
474|def N_total(basis_labels):
475|    return _obs(basis_labels)[2]
476|
477|
478|def P_surv(basis_labels):
479|    return _obs(basis_labels)[3]
480|
481|
482|def P_meson(basis_labels):
483|    return _obs(basis_labels)[4]
484|
485|
486|def P_BBbar(basis_labels):
487|    return _obs(basis_labels)[5]

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py
1|"""Route 1: analytic spin-network / dressed-site Hamiltonian for SU(2) single plaquette
2|with dynamical two-color staggered fermions.
3|
4|Basis: ((j1,j2,j3,j4), (n1,n2,n3,n4), tag) where:
5|  j_l in {0, 1/2} (jmax=0.5) or {0, 1/2, 1} (jmax=1) as floats
6|  n_v in {0,1,2} with gauge-invariant constraints per vertex
7|  tag = 0 (always for 2-valent vertices)
8|
9|Gauge invariance at each 2-valent vertex with incident link spins (j_a, j_b) and matter n_v:
10|  - if j_a == j_b:     n_v in {0, 2}  (vacuum or baryon)
11|  - if |j_a - j_b| == 1/2: n_v = 1  (doublet)
12|  - if |j_a - j_b| == 1:     NOT allowed (projected out, only jmax=1)
13|
14|Hamiltonian: H = H_elec + H_mass + H_hop + H_mag
15|
16|eta = (+1, -1, +1, +1) per link l1..l4.
17|Staggered vacuum: n_vac = (0,2,0,2).  Vertices v1..v4 at (0,0),(1,0),(1,1),(0,1).
18|Links: l1:v1->v2, l2:v2->v3, l3:v4->v3, l4:v1->v4.
19|Plaquette: U_box = U_l1 U_l2 U_l3^dag U_l4^dag (counter-clockwise v1->v2->v3->v4->v1).
20|"""
21|
22|from __future__ import annotations
23|
24|import sys
25|from pathlib import Path
26|
27|import numpy as np
28|from scipy.sparse import csr_matrix, lil_matrix
29|from scipy.linalg import eigh
30|
31|# ---- conventions ----
32|SRC = Path(__file__).resolve().parents[2]  # .../su2qc
33|if str(SRC) not in sys.path:
34|    sys.path.insert(0, str(SRC))
35|import su2qc.conventions as cv
36|
37|# Shortcuts
38|ETA   = cv.ETA          # (+1, -1, +1, +1)
39|PARITY = cv.PARITY      # (+1, -1, +1, -1)
40|LINKS  = cv.LINKS       # ((0,1,"x"), (1,2,"y"), (3,2,"x"), (0,3,"y"))
41|VERTICES = cv.VERTICES  # ((0,0),(1,0),(1,1),(0,1))
42|N_VERTICES = cv.N_VERTICES
43|N_VAC  = cv.N_VAC       # (0, 2, 0, 2)
44|
45|# Link source/target (python indices 0..3)
46|LINK_ST = [(l[0], l[1]) for l in LINKS]  # (source, target)
47|
48|
49|def _cg_half(j: float, m: float, s: int, jp: float, mp: float) -> float:
50|    """Closed-form CG(j,m;1/2,s/2|jp,mp), with no symbolic dependency."""
51|    if abs(mp - (m + 0.5*s)) > 1e-12:
52|        return 0.0
53|    if abs(jp - (j + 0.5)) < 1e-12:
54|        return np.sqrt(max(0.0, (j + (m if s == 1 else -m) + 1.0) / (2.0*j + 1.0)))
55|    if abs(jp - (j - 0.5)) < 1e-12 and j > 0:
56|        return (-np.sqrt(max(0.0, (j - m) / (2.0*j + 1.0)))
57|                if s == 1 else np.sqrt(max(0.0, (j + m) / (2.0*j + 1.0))))
58|    return 0.0
59|
60|
61|def _mvalues(j: float) -> tuple[float, ...]:
62|    return tuple(-j + k for k in range(int(round(2.0*j)) + 1))
63|
64|
65|def _vertex_state(ja: float, jb: float, n: int) -> np.ndarray:
66|    """Unit-norm invariant vertex state as an array (da, db, 4).
67|
68|    All three indices are state-type (each transforms with +J); the tensor is
69|    the unique singlet of V_ja x V_jb x V_matter(n):
70|      n=0/2 (needs ja==jb): metric tensor (-1)^(ja-ma) delta_{ma,-mb}/sqrt(2ja+1)
71|        with fermion Fock f=0 (n=0) or f=3 (n=2);
72|      n=1 (needs |ja-jb|=1/2): T[ma,mb,c] = (-1)^(ja+ma) *
73|        CG(jb, mb; 1/2, s_c | ja, -ma), s_c=+1 for c=0, -1 for c=1;
74|        Fock f = 1 (c=0 occupied) or 2 (c=1 occupied); unit-normalized.
75|    Fock basis: f = n_c0 + 2 n_c1.
76|    """
77|    ma, mb = _mvalues(ja), _mvalues(jb)
78|    out = np.zeros((len(ma), len(mb), 4), dtype=float)
79|    if n in (0, 2):
80|        if abs(ja - jb) > 1e-12:
81|            return out
82|        f = 0 if n == 0 else 3
83|        for a, x in enumerate(ma):
84|            for b, y in enumerate(mb):
85|                if abs(x + y) < 1e-12:
86|                    out[a, b, f] = (-1.0) ** int(round(ja - x)) / np.sqrt(2.0*ja + 1.0)
87|        return out
88|    if n != 1 or abs(abs(ja - jb) - 0.5) > 1e-12:
89|        return out
90|    for a, x in enumerate(ma):
91|        for b, y in enumerate(mb):
92|            for c, s in enumerate((1, -1)):
93|                out[a, b, 1 if c == 0 else 2] = \
94|                    ((-1.0) ** int(round(ja + x))) * _cg_half(jb, y, s, ja, -x)
95|    norm = np.sqrt(np.sum(out * out))
96|    if norm > 0.0:
97|        out /= norm
98|    return out
99|
100|
101|# 4-dim site-Fock operators (f = n_c0 + 2 n_c1); bare sigma^+/- and Z per color.
102|def _sigma_plus(c: int) -> np.ndarray:
103|    out = np.zeros((4, 4))
104|    for f in range(4):
105|        if not f & (1 << c):
106|            out[f | (1 << c), f] = 1.0
107|    return out
108|
109|
110|def _sigma_minus(c: int) -> np.ndarray:
111|    return _sigma_plus(c).T
112|
113|
114|def _zc(c: int) -> np.ndarray:
115|    return np.diag([(-1.0) ** ((f >> c) & 1) for f in range(4)])
116|
117|
118|# Link-end insertion matrices (convention fixed by the Gauss law of the
119|# redundant KS formulation: the L (source) color index is conjugated).
120|# alpha color c: c=0 <-> spin +1/2, c=1 <-> spin -1/2.
121|def _end_insertion(j: float, jp: float, c: int, end: str,
122|                   dagger: bool = False) -> np.ndarray:
123|    """Matrix (2jp+1)x(2j+1) taking the link-end m index from j to jp.
124|
125|    L end (source vertex): entry[m',m] = sign_c * CG(j,m;1/2,-s_c|jp,m')
126|    R end (target vertex): entry[m',m] = CG(j,m;1/2,+s_c|jp,m')
127|    with s_c = +1 for c=0, -1 for c=1; sign_c = +1 for c=0, -1 for c=1.
128|    The sqrt((2j+1)/(2j'+1)) Wigner prefactor is NOT included here; it is
129|    applied once per link in the amplitude assembly.
130|    dagger=True returns the conjugate-transposed insertion of the reverse
131|    transition (for U^dagger links).
132|    """
133|    if dagger:
134|        return _end_insertion(jp, j, c, end, False).T
135|    mj, mjp = _mvalues(j), _mvalues(jp)
136|    out = np.zeros((len(mjp), len(mj)))
137|    s = 1 if c == 0 else -1
138|    for b, m in enumerate(mj):
139|        for a, mp in enumerate(mjp):
140|            if end == "L":
141|                out[a, b] = (1.0 if c == 0 else -1.0) * _cg_half(j, m, -s, jp, mp)
142|            else:
143|                out[a, b] = _cg_half(j, m, s, jp, mp)
144|    return out
145|
146|
147|_VLINKS = ((3, 0), (0, 1), (1, 2), (2, 3))  # vertex v -> (link_a, link_b)
148|# which rotor index of link l lives at vertex v: "L" if v is source else "R"
149|_VEND = tuple(tuple("L" if LINK_ST[l][0] == v else "R" for l in _VLINKS[v])
150|              for v in range(4))
151|
152|
153|def _vertex_overlap2(ja, jb, n_old, ja2, jb2, n_new,
154|                     ins_a=None, ins_b=None, fop=None) -> float:
155|    """<T'(ja2,jb2,n_new)| (ins_a x ins_b x fop) |T(ja,jb,n_old)>."""
156|    T = _vertex_state(ja, jb, n_old)
157|    T2 = _vertex_state(ja2, jb2, n_new)
158|    A = ins_a if ins_a is not None else np.eye(len(_mvalues(ja)))
159|    B = ins_b if ins_b is not None else np.eye(len(_mvalues(jb)))
160|    F = fop if fop is not None else np.eye(4)
161|    out = np.einsum("abf,ax,by,fg,xyg->", T2, A, B, F, T)
162|    return float(out)
163|
164|
165|def _fermion_sign(source: int, target: int, n: tuple[int, int, int, int]) -> float:
166|    """Parity of the middle sites for psi^dag_source ... psi_target (v-ordered)."""
167|    s, t = source, target
168|    lo, hi = (s, t) if s < t else (t, s)
169|    return (-1.0) ** sum(n[k] for k in range(lo + 1, hi))
170|
171|
172|
173|def _check_vertex_gauge_invariant(n_vals: tuple[int, int, int, int],
174|                                   j_tuple: tuple[float, float, float, float]) -> bool:
175|    """Check whether a full matter assignment satisfies all 4 vertex gauge-invariants.
176|
177|    For vertex v with incident link spins (j_a, j_b):
178|      - j_a == j_b     => n_v in {0, 2}
179|      - |j_a - j_b| == 1/2 => n_v = 1
180|      - |j_a - j_b| == 1   => forbidden (projected out)
181|    """
182|    j1, j2, j3, j4 = j_tuple
183|    n1, n2, n3, n4 = n_vals
184|
185|    # v1: links l4, l1  -> j4, j1
186|    ja, jb = j4, j1
187|    if ja == jb:
188|        if n1 not in (0, 2):
189|            return False
190|    elif abs(ja - jb) == 0.5:
191|        if n1 != 1:
192|            return False
193|    elif abs(ja - jb) == 1.0:
194|        return False
195|    else:
196|        return False
197|
198|    # v2: links l1, l2  -> j1, j2
199|    ja, jb = j1, j2
200|    if ja == jb:
201|        if n2 not in (0, 2):
202|            return False
203|    elif abs(ja - jb) == 0.5:
204|        if n2 != 1:
205|            return False
206|    elif abs(ja - jb) == 1.0:
207|        return False
208|
209|    # v3: links l2, l3  -> j2, j3
210|    ja, jb = j2, j3
211|    if ja == jb:
212|        if n3 not in (0, 2):
213|            return False
214|    elif abs(ja - jb) == 0.5:
215|        if n3 != 1:
216|            return False
217|    elif abs(ja - jb) == 1.0:
218|        return False
219|
220|    # v4: links l3, l4  -> j3, j4
221|    ja, jb = j3, j4
222|    if ja == jb:
223|        if n4 not in (0, 2):
224|            return False
225|    elif abs(ja - jb) == 0.5:
226|        if n4 != 1:
227|            return False
228|    elif abs(ja - jb) == 1.0:
229|        return False
230|
231|    return True
232|
233|
234|def enumerate_basis(jmax: float) -> list[tuple]:
235|    """Return list of basis labels ((j1,j2,j3,j4), (n1,n2,n3,n4), 0) for the given jmax.
236|
237|    The basis is constructed by iterating all allowed link spins and then, for each,
238|    all matter assignments that satisfy the 4 vertex constraints.
239|    """
240|    if jmax == 0.5:
241|        j_vals = [0.0, 0.5]
242|    elif jmax == 1.0:
243|        j_vals = [0.0, 0.5, 1.0]
244|    else:
245|        raise ValueError(f"Unsupported jmax={jmax}; use 0.5 or 1.0")
246|
247|    basis = []
248|    for j1 in j_vals:
249|        for j2 in j_vals:
250|            for j3 in j_vals:
251|                for j4 in j_vals:
252|                    jt = (j1, j2, j3, j4)
253|                    # Determine allowed n values for each vertex
254|                    # v1: n1 allowed if j4==j1 -> {0,2}; |j4-j1|==1/2 -> n1=1
255|                    if j4 == j1:
256|                        n1_opts = [0, 2]
257|                    elif abs(j4 - j1) == 0.5:
258|                        n1_opts = [1]
259|                    elif abs(j4 - j1) == 1.0:
260|                        n1_opts = []
261|                    else:
262|                        n1_opts = []
263|
264|                    if n1_opts == []:
265|                        continue
266|
267|                    if j1 == j2:
268|                        n2_opts = [0, 2]
269|                    elif abs(j1 - j2) == 0.5:
270|                        n2_opts = [1]
271|                    elif abs(j1 - j2) == 1.0:
272|                        n2_opts = []
273|                    else:
274|                        n2_opts = []
275|
276|                    if n2_opts == []:
277|                        continue
278|
279|                    if j2 == j3:
280|                        n3_opts = [0, 2]
281|                    elif abs(j2 - j3) == 0.5:
282|                        n3_opts = [1]
283|                    elif abs(j2 - j3) == 1.0:
284|                        n3_opts = []
285|                    else:
286|                        n3_opts = []
287|
288|                    if n3_opts == []:
289|                        continue
290|
291|                    if j3 == j4:
292|                        n4_opts = [0, 2]
293|                    elif abs(j3 - j4) == 0.5:
294|                        n4_opts = [1]
295|                    elif abs(j3 - j4) == 1.0:
296|                        n4_opts = []
297|                    else:
298|                        n4_opts = []
299|
300|                    if n4_opts == []:
301|                        continue
302|
303|                    for n1 in n1_opts:
304|                        for n2 in n2_opts:
305|                            for n3 in n3_opts:
306|                                for n4 in n4_opts:
307|                                    # Verify gauge invariance
308|                                    if not _check_vertex_gauge_invariant((n1, n2, n3, n4), jt):
309|                                        continue
310|                                    label = ((j1, j2, j3, j4), (n1, n2, n3, n4), 0)
311|                                    basis.append(label)
312|    return basis
313|
314|
315|# ---- Hamiltonian building blocks ----
316|
317|def _electric_diag(j_tuple: tuple[float, float, float, float], g2: float) -> float:
318|    """Electric term: (g2/2) * sum_l j_l(j_l+1).  Diagonal in the basis."""
319|    return g2 / 2.0 * sum(cv.casimir(j) for j in j_tuple)
320|
321|
322|def _mass_diag(n_tuple: tuple[int, int, int, int], m: float) -> float:
323|    """Mass term: m * sum_v parity_v n_v.  Diagonal in the basis."""
324|    return m * sum(PARITY[v] * n_tuple[v] for v in range(4))
325|
326|
327|# ---- hopping operator ----
328|
329|def _hopping_matrix_element(
330|    j_from: tuple[float, float, float, float],
331|    n_from: tuple[int, int, int, int],
332|    link_idx: int,
333|    j_to: tuple[float, float, float, float],
334|    n_to: tuple[int, int, int, int],
335|) -> complex:
336|    """Matrix element <to| (1/2) eta_l psi^dag_s U_l psi_t |from> for one link.
337|
338|    Only the forward direction (n_s + 1, n_t - 1) is computed; the caller adds
339|    the h.c. partner into the transposed entry.
340|    """
341|    s, t = LINK_ST[link_idx]  # source, target
342|
343|    dn_s = n_to[s] - n_from[s]
344|    dn_t = n_to[t] - n_from[t]
345|    if not (dn_s == 1 and dn_t == -1):
346|        return 0.0
347|    j, jp = j_from[link_idx], j_to[link_idx]
348|    if abs(abs(j - jp) - 0.5) > 1e-12:
349|        return 0.0
350|    pref = np.sqrt((2.0*j + 1.0) / (2.0*jp + 1.0))
351|
352|    side_s = "above" if s < t else "below"
353|    side_t = "below" if s < t else "above"
354|    amp = 0.0
355|    for ca in range(2):        # color created at s (L end of the link)
356|        for cb in range(2):    # color annihilated at t (R end)
357|            Fs = _site_create(ca, side_s)
358|            Ft = _site_annihilate(cb, side_t)
359|            insL = _end_insertion(j, jp, ca, "L")
360|            insR = _end_insertion(j, jp, cb, "R")
361|            ov_s = _vertex_overlap_at(s, j_from, n_from, j_to, n_to,
362|                                      {link_idx: insL}, Fs)
363|            ov_t = _vertex_overlap_at(t, j_from, n_from, j_to, n_to,
364|                                      {link_idx: insR}, Ft)
365|            amp += ov_s * ov_t
366|    return complex(0.5 * ETA[link_idx] * _fermion_sign(s, t, n_from)
367|                   * pref * amp)
368|
369|
370|def _site_create(c: int, side: str) -> np.ndarray:
371|    """Site creation op for color c with the JW Z-string on the given side."""
372|    op = _sigma_plus(c)
373|    ks = range(c + 1, 2) if side == "above" else range(0, c)
374|    for k in ks:
375|        op = op @ _zc(k)
376|    return op
377|
378|
379|def _site_annihilate(c: int, side: str) -> np.ndarray:
380|    return _site_create(c, side).T
381|
382|
383|def _vertex_overlap_at(v, j_from, n_from, j_to, n_to, ins_by_link, fop=None):
384|    la, lb = _VLINKS[v]
385|    return _vertex_overlap2(j_from[la], j_from[lb], n_from[v],
386|                            j_to[la], j_to[lb], n_to[v],
387|                            ins_by_link.get(la), ins_by_link.get(lb), fop)
388|
389|
390|def _magnetic_matrix_element(j_from, n, j_to) -> complex:
391|    """<to| Tr(U_l1 U_l2 U_l3^dag U_l4^dag) |from> by four local contractions.
392|
393|    Color loop: sum_{abcd} U0^{ab} U1^{bc} (U2^dag)^{cd} (U3^dag)^{da}; per
394|    vertex the two incident link-end insertions carry the loop colors:
395|      v1: l4(L,a,dag), l1(L,a) | v2: l1(R,b), l2(L,b)
396|      v3: l2(R,c), l3(R,c,dag) | v4: l3(L,d,dag), l4(R,d,dag)
397|    Wigner prefactor per link: sqrt((2j+1)/(2j'+1)) for plain links,
398|    sqrt((2j'+1)/(2j+1)) for daggered links.
399|    """
400|    pref = 1.0
401|    for l in range(4):
402|        j, jp = j_from[l], j_to[l]
403|        if abs(abs(j - jp) - 0.5) > 1e-12:
404|            return 0.0
405|        if l in (2, 3):
406|            pref *= np.sqrt((2.0*jp + 1.0) / (2.0*j + 1.0))
407|        else:
408|            pref *= np.sqrt((2.0*j + 1.0) / (2.0*jp + 1.0))
409|    total = 0.0
410|    for a in range(2):
411|        for b in range(2):
412|            for c in range(2):
413|                for d in range(2):
414|                    specs = (
415|                        (0, {3: (a, "L", True), 0: (a, "L", False)}),
416|                        (1, {0: (b, "R", False), 1: (b, "L", False)}),
417|                        (2, {1: (c, "R", False), 2: (c, "R", True)}),
418|                        (3, {2: (d, "L", True), 3: (d, "R", True)}),
419|                    )
420|                    product = 1.0
421|                    for v, spec in specs:
422|                        ins = {l: _end_insertion(j_from[l], j_to[l], col, end,
423|                                                 dag)
424|                               for l, (col, end, dag) in spec.items()}
425|                        product *= _vertex_overlap_at(v, j_from, n, j_to, n,
426|                                                      ins)
427|                        if product == 0.0:
428|                            break
429|                    total += product
430|    return complex(pref * total)
431|
432|
433|def build_hamiltonian(g2: float, m: float, jmax: float) -> tuple[csr_matrix, list]:
434|    """Build the full route-1 Hamiltonian for the single plaquette.
435|
436|    Returns (H_sparse, basis) where basis is the list of labels in the same order
437|    as the matrix rows/cols.
438|
439|    Physics:
440|      H = H_elec + H_mass + H_hop + H_mag
441|      H_elec = (g2/2) sum_l j_l(j_l+1)                     (diagonal)
442|      H_mass = m sum_v parity_v n_v                          (diagonal, parity=+ - + -)
443|      H_hop  = (1/2) sum_l ( eta_l psi^dag_{s(l)} U_l psi_{t(l)} + h.c. )  (off-diagonal)
444|      H_mag  = -(1/(2g2)) Tr(U_box + U_box^dag)            (off-diagonal)
445|    """
446|    basis = enumerate_basis(jmax)
447|    dim = len(basis)
448|
449|    # Map label -> row index for O(1) lookups
450|    label_to_idx = {lab: i for i, lab in enumerate(basis)}
451|
452|    # Sparse matrix in LIL format for easy insertion
453|    H = lil_matrix((dim, dim), dtype=complex)
454|
455|    # ----- Electric term (diagonal) -----
456|    for i, (j_tuple, n_tuple, _) in enumerate(basis):
457|        H[i, i] = _electric_diag(j_tuple, g2)
458|
459|    # ----- Mass term (diagonal) -----
460|    for i, (j_tuple, n_tuple, _) in enumerate(basis):
461|        H[i, i] += _mass_diag(n_tuple, m)
462|
463|    # ----- Hopping term (off-diagonal) -----
464|    for i, (j_from, n_from, _) in enumerate(basis):
465|        for link_idx in range(4):
466|            s, t = LINK_ST[link_idx]
467|
468|            # Direction A: psi^dag_s U_l psi_t  (n_s+1, n_t-1, j_l -> j_l +- 1/2)
469|            nA = list(n_from)
470|            nA[s] += 1
471|            nA[t] -= 1
472|            if 0 <= nA[s] <= 2 and 0 <= nA[t] <= 2:
473|                for dj in (0.5, -0.5):
474|                    jA = list(j_from)
475|                    jA[link_idx] += dj
476|                    if not (-1e-12 <= jA[link_idx] <= jmax + 1e-12):
477|                        continue
478|                    labelA = (tuple(jA), tuple(nA), 0)
479|                    if labelA in label_to_idx:
480|                        me = _hopping_matrix_element(j_from, n_from, link_idx,
481|                                                      tuple(jA), tuple(nA))
482|                        j_idx = label_to_idx[labelA]
483|                        H[j_idx, i] += complex(me, 0.0)
484|                        H[i, j_idx] += np.conjugate(complex(me, 0.0))  # Hermitian
485|
486|    # ----- Magnetic term (off-diagonal) -----
487|    # -(1/(2g2)) Tr(U_box + U_box^dag)
488|    # Flips all four links simultaneously between configurations where every link changes by ±1/2.
489|    # Matrix element is a product of vertex factors depending on (j_a, j_b, matter state) at each corner.
490|    # Matter is untouched (diagonal in n).
491|
492|    for i, (j_from, n_from, _) in enumerate(basis):
493|        # Enumerate the 16 possible flip sign patterns for the 4 links
494|        for flip_signs in [(1, 1, 1, 1), (1, 1, 1, -1), (1, 1, -1, 1), (1, 1, -1, -1),
495|                          (1, -1, 1, 1), (1, -1, 1, -1), (1, -1, -1, 1), (1, -1, -1, -1),
496|                          (-1, 1, 1, 1), (-1, 1, 1, -1), (-1, 1, -1, 1), (-1, 1, -1, -1),
497|                          (-1, -1, 1, 1), (-1, -1, 1, -1), (-1, -1, -1, 1), (-1, -1, -1, -1)]:
498|            j_flipped = list(j_from)
499|            valid = True
500|            for li in range(4):
501|                j_new = j_from[li] + flip_signs[li] * 0.5
502|                if j_new < 0 or j_new > jmax + 1e-12:
503|                    valid = False
504|                    break
505|                j_flipped[li] = j_new
506|
507|            if not valid:
508|                continue
509|
510|            label_flipped = (tuple(j_flipped), n_from, 0)
511|            if label_flipped in label_to_idx:
512|                j_idx = label_to_idx[label_flipped]
513|                if j_idx <= i:
514|                    continue
515|                me = -(1.0 / (2.0 * g2)) * (
516|                    _magnetic_matrix_element(j_from, n_from, tuple(j_flipped))
517|                    + np.conjugate(_magnetic_matrix_element(
518|                        tuple(j_flipped), n_from, j_from)))
519|                H[i, j_idx] += np.conjugate(me)
520|                H[j_idx, i] += me
521|
522|    # Convert to CSR for efficient operations
523|    H = H.tocsr()
524|
525|    # Hermiticity check: H should equal H^\dagger
526|    # (We already enforced it by adding both i,j and j,i)
527|
528|    return H, basis
529|
530|
531|def build_hamiltonian_no_magnetic(g2: float, m: float, jmax: float) -> tuple[csr_matrix, list]:
532|    """Build the Hamiltonian without the magnetic term (electric + mass + hopping only).
533|
534|    Same basis ordering as build_hamiltonian, useful for limit checks.
535|    """
536|    basis = enumerate_basis(jmax)
537|    dim = len(basis)
538|
539|    label_to_idx = {lab: i for i, lab in enumerate(basis)}
540|    j_labels = np.array([lab[0] for lab in basis], dtype=object)
541|    n_labels = np.array([lab[1] for lab in basis], dtype=object)
542|
543|    H = lil_matrix((dim, dim), dtype=complex)
544|
545|    # Electric diagonal
546|    for i, (j_tuple, n_tuple, _) in enumerate(basis):
547|        H[i, i] = _electric_diag(j_tuple, g2)
548|
549|    # Mass diagonal
550|    for i, (j_tuple, n_tuple, _) in enumerate(basis):
551|        H[i, i] += _mass_diag(n_tuple, m)
552|
553|    # Hopping off-diagonal (same logic as in build_hamiltonian)
554|    for i, (j_from, n_from, _) in enumerate(basis):
555|        for link_idx in range(4):
556|            s, t = LINK_ST[link_idx]
557|
558|            # Direction A: psi^dag_s U_l psi_t  (n_s+1, n_t-1, j_l -> j_l +- 1/2)
559|            nA = list(n_from)
560|            nA[s] += 1
561|            nA[t] -= 1
562|            if 0 <= nA[s] <= 2 and 0 <= nA[t] <= 2:
563|                for dj in (0.5, -0.5):
564|                    jA = list(j_from)
565|                    jA[link_idx] += dj
566|                    if not (-1e-12 <= jA[link_idx] <= jmax + 1e-12):
567|                        continue
568|                    labelA = (tuple(jA), tuple(nA), 0)
569|                    if labelA in label_to_idx:
570|                        me = _hopping_matrix_element(j_from, n_from, link_idx,
571|                                                      tuple(jA), tuple(nA))
572|                        j_idx = label_to_idx[labelA]
573|                        H[j_idx, i] += complex(me, 0.0)
574|                        H[i, j_idx] += np.conjugate(complex(me, 0.0))
575|
576|    H = H.tocsr()
577|    return H, basis
578|
579|
580|# ---- observables ----
581|
582|def number_op(v: int):
583|    """Return the number operator n_v for vertex v (diagonal in the basis).
584|
585|    The returned function takes (dim, basis) and returns a CSR matrix.
586|    """
587|    def _no(dim_: int, basis_: list):
588|        H = lil_matrix((dim_, dim_), dtype=complex)
589|        for i, (j_tuple, n_tuple, _) in enumerate(basis_):
590|            H[i, i] = float(n_tuple[v])
591|        return H.tocsr()
592|    return _no
593|
594|
595|def total_number():
596|    """Return the total fermion number sum_v n_v (diagonal in the basis)."""
597|    def _no(dim_: int, basis_: list):
598|        H = lil_matrix((dim_, dim_), dtype=complex)
599|        for i, (j_tuple, n_tuple, _) in enumerate(basis_):
600|            H[i, i] = float(sum(n_tuple))
601|        return H.tocsr()
602|    return _no
603|
604|
605|def casimir_link(l: int):
606|    """Return the electric casimir operator j_l(j_l+1) for link l (diagonal in the basis)."""
607|    def _no(dim_: int, basis_: list):
608|        H = lil_matrix((dim_, dim_), dtype=complex)
609|        for i, (j_tuple, n_tuple, _) in enumerate(basis_):
610|            H[i, i] = cv.casimir(j_tuple[l])
611|        return H.tocsr()
612|    return _no
613|
614|
615|# ---- projectors ------
616|
617|def _charge_projector(charge_tuple: tuple[int, int, int, int],
618|                      basis: list, dim: int) -> csr_matrix:
619|    """Projector onto states with given local charges q_v = n_v - n_vac(v).
620|
621|    Args:
622|        charge_tuple: (q_v1, q_v2, q_v3, q_v4) where q_v = n_v - n_vac(v)
623|        basis: list of basis labels
624|        dim: dimension of the basis
625|    """
626|    H = lil_matrix((dim, dim), dtype=complex)
627|    for i, (j_tuple, n_tuple, _) in enumerate(basis):
628|        q = tuple(int(n_tuple[v] - N_VAC[v]) for v in range(4))
629|        if q == charge_tuple:
630|            H[i, i] = 1.0
631|    return H.tocsr()
632|
633|
634|def P_stretched(g2: float, m: float, jmax: float) -> csr_matrix:
635|    """Projector onto states with q = (+1, -1, 0, 0)."""
636|    basis = enumerate_basis(jmax)
637|    dim = len(basis)
638|    return _charge_projector((1, -1, 0, 0), basis, dim)
639|
640|
641|def P_short(g2: float, m: float, jmax: float) -> csr_matrix:
642|    """Projector onto states with q = (+1, -1, 0, 0) — the short sector."""
643|    basis = enumerate_basis(jmax)
644|    dim = len(basis)
645|    return _charge_projector((1, -1, 0, 0), basis, dim)
646|
647|
648|def P_surv(g2: float, m: float, jmax: float) -> csr_matrix:
649|    """Projector onto states with q = (+1, -1, 0, 0) (surviving stretched string)."""
650|    basis = enumerate_basis(jmax)
651|    dim = len(basis)
652|    return _charge_projector((1, -1, 0, 0), basis, dim)
653|
654|
655|def P_meson(g2: float, m: float, jmax: float) -> csr_matrix:
656|    """Projector onto states with |q_v| = 1 for all v."""
657|    basis = enumerate_basis(jmax)
658|    dim = len(basis)
659|    H = lil_matrix((dim, dim), dtype=complex)
660|    for i, (j_tuple, n_tuple, _) in enumerate(basis):
661|        q = tuple(int(n_tuple[v] - N_VAC[v]) for v in range(4))
662|        if all(abs(qq) == 1 for qq in q):
663|            H[i, i] = 1.0
664|    return H.tocsr()
665|
666|
667|def P_BBbar(g2: float, m: float, jmax: float) -> csr_matrix:
668|    """Projector onto any state with |q_v| = 2 for some v (takes precedence)."""
669|    basis = enumerate_basis(jmax)
670|    dim = len(basis)
671|    H = lil_matrix((dim, dim), dtype=complex)
672|    for i, (j_tuple, n_tuple, _) in enumerate(basis):
673|        q = tuple(int(n_tuple[v] - N_VAC[v]) for v in range(4))
674|        if any(abs(qq) == 2 for qq in q):
675|            H[i, i] = 1.0
676|    return H.tocsr()
677|
678|
679|# ---- charge from conventions ----
680|def charge(v: int, n: int) -> int:
681|    """Local charge relative to the staggered vacuum: q_v = n_v - n_vac(v)."""
682|    return n - N_VAC[v]
683|
684|
685|# ---- debugging / validation ----
686|
687|def validate_dimensions(jmax: float = 0.5) -> dict:
688|    """Validate that the basis dimension and sector counts match expectations."""
689|    basis = enumerate_basis(jmax)
690|    dim = len(basis)
691|
692|    # Sector dims: count states by total fermion number N = sum n_v
693|    sector_dims = {0: 0, 2: 0, 4: 0, 6: 0, 8: 0}
694|    for _, n_tuple, _ in basis:
695|        N = sum(n_tuple)
696|        if N in sector_dims:
697|            sector_dims[N] += 1
698|
699|    expected_dim = {0.5: 82, 1.0: 152}[jmax]
700|    expected_sectors = {0.5: {0: 2, 2: 20, 4: 38, 6: 20, 8: 2}, 1.0: None}[jmax]
701|
702|    result = {
703|        "jmax": jmax,
704|        "dim": dim,
705|        "expected_dim": expected_dim,
706|        "dim_match": dim == expected_dim,
707|        "sector_dims": sector_dims,
708|        "expected_sectors": expected_sectors,
709|    }
710|    if expected_sectors:
711|        for N in range(0, 9, 2):
712|            result[f"sector_N{N}_match"] = sector_dims.get(N, 0) == expected_sectors.get(N, 0)
713|
714|    return result
715|
716|
717|def validate_hermiticity(H: csr_matrix, atol: float = 1e-13) -> dict:
718|    """Check that H is Hermitian within tolerance."""
719|    H_arr = H.toarray()
720|    diff = np.max(np.abs(H_arr - H_arr.T.conj()))
721|    return {
722|        "hermitian": diff <= atol,
723|        "max_diff": float(diff),
724|    }
725|
726|
727|def validate_commutator(H: csr_matrix, N_op: csr_matrix, atol: float = 1e-13) -> dict:
728|    """Check [H, N] = 0 within tolerance."""
729|    H_arr = H.toarray()
730|    N_arr = N_op.toarray()
731|    comm = H_arr @ N_arr - N_arr @ H_arr
732|    max_comm = np.max(np.abs(comm))
733|    return {
734|        "[H,N]": max_comm <= atol,
735|        "max_comm": float(max_comm),
736|    }
737|
738|
739|def pure_electric_check(g2_big: float = 1e6) -> dict:
740|    """Spectrum at g2 -> inf, m = 0: electric levels with k-degeneracies.
741|
742|    From limits.py pure_electric_check.
743|    """
744|    from su2qc import conventions as cv
745|    from su2qc.ham.route_spinnet import build_hamiltonian as bh
746|    H, basis = bh(g2_big, 0.0, 0.5)[:2]
747|    evals = np.sort(eigh(H.toarray(), eigvals_only=True))
748|    unit = g2_big / 2.0 * 0.75
749|    ks = np.rint(evals / unit).astype(int)
750|    got = [int(np.sum(ks == k)) for k in range(5)]
751|    rel = np.max(np.abs(evals - ks * unit)) / unit
752|    ok = got == [16, 16, 18, 16, 16] and rel <= 1e-8 * g2_big / 1e6 * 100
753|    return {"degeneracies": got, "rel_dev": float(rel), "ok": bool(ok)}
754|
755|
756|if __name__ == "__main__":
757|    # Quick validation
758|    print("=== Validating jmax=0.5 basis ===")
759|    r = validate_dimensions(0.5)
760|    print(f"dim={r['dim']} (expected 82): {'OK' if r['dim_match'] else 'FAIL'}")
761|    for k in [0, 2, 4, 6, 8]:
762|        print(f"  N={k}: got={r['sector_dims'][k]} expected={r['expected_sectors'][k]} {'OK' if r[f'sector_N{k}_match'] else 'FAIL'}")
763|
764|    print("\n=== Validating jmax=1.0 basis ===")
765|    r = validate_dimensions(1.0)
766|    print(f"dim={r['dim']} (expected 152): {'OK' if r['dim_match'] else 'FAIL'}")
767|
768|    print("\n=== Hermiticity check (jmax=0.5) ===")
769|    H, basis = build_hamiltonian(1.0, 0.0, 0.5)
770|    hcheck = validate_hermiticity(H)
771|    print(f"Hermitian: {hcheck['hermitian']}, max_diff={hcheck['max_diff']}")
772|
773|    print("\n=== Pure electric check ===")
774|    pe = pure_electric_check()
775|    print(f"degeneracies={pe['degeneracies']} expected=[16,16,18,16,16] ok={pe['ok']}")

# Numbered source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py
1|"""Minimal replication manifest helper for the campaign.
2|
3|Phase 8 will extend this module to rebuild all tables and figures. Phase 0 only
4|provides deterministic file hashing and committed-vs-rerun comparison.
5|"""
6|from __future__ import annotations
7|
8|import hashlib
9|import json
10|from pathlib import Path
11|
12|
13|def sha256_file(path: str | Path) -> str:
14|    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
15|
16|
17|def manifest(paths: list[str | Path]) -> dict[str, str]:
18|    return {str(Path(path)): sha256_file(path) for path in sorted(paths, key=str)}
19|
20|
21|def compare_manifests(expected: dict[str, str], actual: dict[str, str]) -> dict[str, object]:
22|    keys = sorted(set(expected) | set(actual))
23|    mismatches = [key for key in keys if expected.get(key) != actual.get(key)]
24|    return {"pass": not mismatches, "mismatches": mismatches, "count": len(keys)}
25|
26|
27|def write_manifest(paths: list[str | Path], output: str | Path) -> dict[str, str]:
28|    values = manifest(paths)
29|    Path(output).write_text(json.dumps(values, indent=2, sort_keys=True) + "\n")
30|    return values

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