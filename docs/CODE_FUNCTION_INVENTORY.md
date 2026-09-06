# Python function and test inventory

Generated from the shipped source AST. Calls are syntactic expressions,
not a resolved runtime call graph. Full code is included at each linked path.
Test assertions describe checks; execution outcomes are in the JUnit/log files.

## [src/su2zx/__init__.py](../src/su2zx/__init__.py)

SU2ZX research foundation.

## [src/su2zx/compiler_study.py](../src/su2zx/compiler_study.py)

Diverse, exact, target-aware compiler study for SU2ZX v0.3.0.

### `generic_ecr_backend(seed: int)` — line 63

Legacy five-node linear target retained for the QPU dry-run tests.

Direct call expressions: `CouplingMap.from_line`, `GenericBackendV2`

### `_bidirectional(edges: list[tuple[int, int]])` — line 73

Direct call expressions: `sorted`

### `_target_case(topology: str, num_qubits: int, seed: int, layout_name: str, initial_layout: tuple[int, ...] | None)` — line 77

Direct call expressions: `CouplingMap`, `CouplingMap.from_grid`, `CouplingMap.from_line`, `CouplingMap.from_ring`, `GenericBackendV2`, `TargetCase`, `ValueError`, `_bidirectional`, `math.ceil`, `max`, `range`

### `target_cases(num_qubits: int, seed: int)` — line 124

Return reproducible topology/layout cases, including two line placements.

Direct call expressions: `_target_case`, `max`, `range`, `round`, `tuple`

### `count_two_qubit(circuit: QuantumCircuit)` — line 142

Direct call expressions: `len`, `sum`

### `count_one_qubit(circuit: QuantumCircuit)` — line 146

Direct call expressions: `len`, `sum`

### `two_qubit_depth(circuit: QuantumCircuit)` — line 150

Direct call expressions: `circuit.depth`, `len`

### `calibration_budget(circuit: QuantumCircuit, backend: GenericBackendV2)` — line 154

Direct call expressions: `circuit.find_bit`, `float`, `len`, `math.log1p`, `tuple`

### `compile_candidate(source: QuantumCircuit, strategy: str, backend: GenericBackendV2, seed: int, initial_layout: tuple[int, ...] | list[int] | None=None, optimization_level: int=3, layout_method: str='trivial')` — line 170

Apply an exact logical rewrite, then compile under common target controls.

Direct call expressions: `generate_preset_pass_manager`, `list`, `manager.run`, `optimize_with_pyzx`, `range`, `time.perf_counter`

### `_interaction_features(source: QuantumCircuit)` — line 200

Direct call expressions: `abs`, `degrees.max`, `degrees.mean`, `float`, `int`, `len`, `max`, `np.zeros`, `pairs.add`, `set`, `sorted`, `source.find_bit`

### `_target_features(case: TargetCase, source: QuantumCircuit)` — line 218

Direct call expressions: `case.coupling.get_edges`, `float`, `int`, `len`, `mapped_distances.append`, `np.isfinite`, `np.max`, `np.mean`, `range`, `source.find_bit`, `tuple`

### `_duration(compiled: QuantumCircuit, backend: GenericBackendV2)` — line 243

Direct call expressions: `compiled.estimate_duration`, `float`

### `_source_specs()` — line 250

Bounded design covering N=2..6, r=1/2/4/8, and three term orders.

Direct call expressions: `range`, `specs.append`

### `_selected_cases(n: int, index: int, seed: int)` — line 264

Balanced incomplete design plus full cross-target anchor cases.

Direct call expressions: `len`, `target_cases`

### `build_dataset(config: dict, backend: GenericBackendV2 | None=None)` — line 273

Build the bounded v0.3.0 compiler dataset.

``backend`` retains the compact legacy path used by tests and downstream
callers.  The production run passes no backend and uses the diverse design.

Direct call expressions: `','.join`, `CouplingMap.from_line`, `TargetCase`, `_duration`, `_interaction_features`, `_selected_cases`, `_source_specs`, `_target_features`, `calibration_budget`, `circuit_hash`, `circuit_structure_hash`, `compile_candidate`, `compiled.depth`, `compiled.size`, `config.get`, `count_one_qubit`, `count_two_qubit`, `enumerate`, `float`, `frame.merge`, `frame[frame.verification_result].copy`, `int`, `len`, `logical.size`, `map`, `max`, `np.isfinite`, `np.mean`, `pd.DataFrame`, `plaquette_chain_terms`, `range`, `repr`, `rows.append`, `source.depth`, `source.size`, `strang_evolution`, `sum`, `tuple`, `two_qubit_depth`, `verified.groupby`, `verified.groupby('case_id').cost.idxmin`, `winners.rename`

### `design_matrix(frame: pd.DataFrame)` — line 451

Direct call expressions: `frame[FEATURES].reset_index`, `frame[FEATURES].reset_index(drop=True).astype`, `pd.concat`, `pd.get_dummies`, `pd.get_dummies(frame[['strategy', 'term_ordering', 'target_topology', 'layout_name']], dtype=float).reset_index`

### `_policy_metrics(evaluated: pd.DataFrame, predicted: pd.Series)` — line 460

Direct call expressions: `accuracy_score`, `evaluated[['case_id', 'strategy', 'cost']].copy`, `float`, `np.isclose`, `np.maximum`, `np.mean`, `predicted.to_numpy`, `regret.max`, `regret.mean`, `regret.median`, `table.groupby`, `table.groupby('case_id').cost.idxmin`, `table.groupby('case_id').prediction.idxmin`, `true_best.merge`

### `_grouped_predictions(frame: pd.DataFrame, groups: pd.Series, seed: int)` — line 478

Direct call expressions: `GroupKFold`, `RandomForestRegressor`, `design_matrix`, `float`, `groups.nunique`, `len`, `max`, `min`, `model.fit`, `model.predict`, `np.full`, `np.zeros`, `sorted`, `splitter.split`, `zip`

### `_fixed_regrets(frame: pd.DataFrame)` — line 506

Direct call expressions: `((fixed - optimum) / np.maximum(optimum, 1e-12)).dropna`, `((fixed - optimum) / np.maximum(optimum, 1e-12)).dropna().mean`, `float`, `frame.groupby`, `frame.groupby('case_id').cost.idxmin`, `frame.loc[frame.groupby('case_id').cost.idxmin()].set_index`, `frame[frame.strategy == strategy].set_index`, `frame[frame.strategy == strategy].set_index('case_id').cost.reindex`, `np.maximum`

### `_case_policy_regret(frame: pd.DataFrame, choices: pd.Series)` — line 519

Direct call expressions: `((selected - optimum) / np.maximum(optimum, 1e-12)).mean`, `choices.items`, `costs.min`, `float`, `frame.pivot`, `np.maximum`, `pd.Series`

### `selector_summary(frame: pd.DataFrame, seed: int)` — line 529

Direct call expressions: `_case_policy_regret`, `_fixed_regrets`, `_grouped_predictions`, `_policy_metrics`, `base['fixed_normalized_regret'].values`, `count_best.native_2q_depth.min`, `counts.items`, `destination.get`, `frame.circuit_hash.nunique`, `frame.circuit_structure_hash.nunique`, `frame.source_key.nunique`, `frame.target_topology.nunique`, `frame[['target_name', 'num_plaquettes']].drop_duplicates`, `frame[frame.verification_result].dropna`, `frame[frame.verification_result].dropna(subset=['cost']).reset_index`, `group.cost.idxmin`, `group.native_2q_count.min`, `int`, `len`, `list`, `min`, `np.where`, `pd.Series`, `strict_two_qubit_wins.get`, `strict_two_qubit_wins.items`, `structural.groupby`, `structural.groupby('structural_target_case').cost.idxmin`, `verified.case_id.nunique`, `verified.circuit_structure_hash.astype`, `verified.drop_duplicates`, `verified.drop_duplicates('case_id').set_index`, `verified.groupby`, `verified.groupby(['structural_target_case', 'strategy'], as_index=False).agg`, `verified.groupby(['structural_target_case', 'strategy'], as_index=False).agg(cost=('cost', 'median'), native_2q_count=('native_2q_count', 'median'), native_2q_depth=('native_2q_depth', 'median')).reset_index`, `verified.num_plaquettes.astype`, `winners.strategy.mode`, `winners.strategy.value_counts`, `winners.strategy.value_counts().to_dict`, `winners.structural_target_case.nunique`, `{'structural_family_holdout': verified.circuit_structure_hash, 'leave_one_size_out': verified.num_plaquettes.astype(str), 'leave_one_topology_out': verified.target_topology}.items`

### `build_seed_sensitivity(config: dict)` — line 644

Probe the stochastic-routing sensitivity on three representative targets.

Direct call expressions: `compile_candidate`, `config.get`, `count_two_qubit`, `int`, `pd.DataFrame`, `repr`, `rows.append`, `strang_evolution`, `target_cases`, `two_qubit_depth`

### `save_plots(frame: pd.DataFrame, summary: dict, figures: Path)` — line 694

Direct call expressions: `ax.bar`, `ax.grid`, `ax.legend`, `ax.set`, `ax.tick_params`, `axes[0].bar`, `axes[0].set`, `axes[1].bar`, `axes[1].set`, `axis.grid`, `axis.tick_params`, `fig.savefig`, `fig.suptitle`, `figures.mkdir`, `frame[frame.verification_result].copy`, `len`, `np.zeros`, `pd.crosstab`, `pd.crosstab(winners.target_topology, winners.strategy).reindex`, `plt.close`, `plt.subplots`, `summary.get`, `table[strategy].to_numpy`, `verified.groupby`, `verified.groupby('case_id').cost.idxmin`, `verified.groupby('strategy', sort=False).routing_penalty_ratio.median`, `verified.groupby('strategy', sort=False)[['native_2q_count', 'native_2q_depth']].mean`, `winners.strategy.value_counts`, `winners.strategy.value_counts().reindex`

### `save_audit_tables(frame: pd.DataFrame, data: Path)` — line 770

Persist winner, split, and feature-definition tables used by the report.

Direct call expressions: `(data / 'ml_feature_definitions.json').write_text`, `GroupKFold`, `assignments.circuit_structure_hash.nunique`, `assignments.columns.get_loc`, `assignments.to_csv`, `enumerate`, `frame[frame.verification_result].dropna`, `frame[frame.verification_result].dropna(subset=['cost']).copy`, `json.dumps`, `len`, `min`, `np.zeros`, `raw_winners[['case_id', 'circuit_structure_hash', 'target_name', 'layout_name', 'strategy', 'native_2q_count', 'native_2q_depth', 'estimated_duration', 'cost']].to_csv`, `splitter.split`, `verified.groupby`, `verified.groupby('case_id').cost.idxmin`, `verified[['case_id', 'circuit_structure_hash', 'num_plaquettes', 'target_topology']].drop_duplicates`

### `main()` — line 819

Direct call expressions: `(output / 'data' / 'selector_summary.json').write_text`, `(output / 'data').mkdir`, `argparse.ArgumentParser`, `build_dataset`, `build_seed_sensitivity`, `config.get`, `frame.to_csv`, `int`, `json.dumps`, `load_json`, `parser.add_argument`, `parser.parse_args`, `print`, `project_path`, `save_audit_tables`, `save_plots`, `seed_frame.to_csv`, `selector_summary`

## [src/su2zx/core.py](../src/su2zx/core.py)

Physics, circuits, and observables for the j_max=1/2 SU(2) plaquette chain.

Conventions:
* H_tilde = 2 H / g^2 and x = 2 / g^4.
* Qiskit Pauli labels and bitstrings are q_(N-1) ... q_0.
* Each qubit is one gauge-reduced spatial plaquette-loop degree of freedom.

### `pauli_word(num_qubits: int, operations: Mapping[int, str])` — line 29

Return a Qiskit-order Pauli word from logical-qubit operations.

Direct call expressions: `''.join`, `ValueError`, `operations.items`

### `plaquette_chain_terms(num_plaquettes: int, x: float, *, include_identity: bool=True)` — line 41

Open-chain SU(2) Hamiltonian terms in the minimal truncation.

Direct call expressions: `PauliTerm`, `ValueError`, `pauli_word`, `range`, `terms.append`, `terms.extend`

### `hamiltonian(num_plaquettes: int, x: float)` — line 99

Direct call expressions: `SparsePauliOp.from_list`, `plaquette_chain_terms`

### `hamiltonian_components(num_plaquettes: int, x: float)` — line 104

Return electric (I/Z) and magnetic (contains X) operators.

Direct call expressions: `SparsePauliOp.from_list`, `plaquette_chain_terms`

### `pauli_rotation(circuit: QuantumCircuit, word: str, theta: float)` — line 114

Append exp(-i theta P) using basis changes, parity, and Rz.

Direct call expressions: `ValueError`, `active.append`, `circuit.cx`, `circuit.h`, `circuit.rz`, `circuit.s`, `circuit.sdg`, `len`, `list`, `range`, `reversed`, `zip`

### `ordered_hamiltonian_terms(num_plaquettes: int, x: float, ordering: str='current')` — line 149

Return the unchanged Hamiltonian terms in a documented product order.

``symmetry`` groups each Pauli word with its spatial reflection.  Members of
every such orbit commute for this Hamiltonian, so each grouped exponential is
reflection invariant even though different orbit sums need not commute.

Direct call expressions: `ValueError`, `list`, `min`, `orbits.setdefault`, `orbits.setdefault(key, []).append`, `plaquette_chain_terms`, `reversed`, `sorted`

### `strang_evolution(num_plaquettes: int, x: float, time: float, repetitions: int, *, initial_ones: Sequence[int]=(), term_ordering: str='current')` — line 177

Second-order product formula for exp(-i H_tilde time).

Direct call expressions: `QuantumCircuit`, `ValueError`, `circuit.x`, `list`, `ordered_hamiltonian_terms`, `pauli_rotation`, `range`, `reversed`

### `circuit_hash(circuit: QuantumCircuit, *, normalize_parameters: bool=False)` — line 212

Hash ordered gates/connectivity, optionally discarding continuous angles.

Direct call expressions: `circuit.find_bit`, `float`, `format`, `hashlib.sha256`, `hashlib.sha256(encoded).hexdigest`, `instructions.append`, `json.dumps`, `json.dumps(payload, sort_keys=True, separators=(',', ':')).encode`

### `circuit_structure_hash(circuit: QuantumCircuit)` — line 236

Hash gate order and connectivity while normalizing continuous parameters.

Direct call expressions: `circuit_hash`

### `initial_state(num_qubits: int, initial_ones: Sequence[int])` — line 241

Direct call expressions: `np.zeros`, `sum`

### `exact_state(num_plaquettes: int, x: float, time: float, *, initial_ones: Sequence[int]=())` — line 248

Direct call expressions: `expm`, `hamiltonian`, `hamiltonian(num_plaquettes, x).to_matrix`, `initial_state`

### `circuit_state(circuit: QuantumCircuit)` — line 259

Direct call expressions: `Statevector`, `np.asarray`

### `expectation(state: np.ndarray, operator: SparsePauliOp)` — line 263

Direct call expressions: `ValueError`, `abs`, `float`, `np.vdot`, `operator.to_matrix`

### `probabilities(state: np.ndarray)` — line 270

Direct call expressions: `np.abs`

### `local_occupations(state: np.ndarray, num_qubits: int)` — line 274

Direct call expressions: `enumerate`, `np.asarray`, `probabilities`, `range`, `sum`

### `total_variation(left: ArrayLike, right: ArrayLike)` — line 284

Direct call expressions: `float`, `np.abs`, `np.abs(np.asarray(left) - np.asarray(right)).sum`, `np.asarray`

### `measurement_circuit(unitary: QuantumCircuit, x_qubit: int | None)` — line 288

Direct call expressions: `circuit.h`, `circuit.measure_all`, `dict`, `unitary.copy`

### `measurement_family(unitary: QuantumCircuit)` — line 299

Direct call expressions: `measurement_circuit`, `range`

### `normalized_counts(counts: Mapping[str, float])` — line 305

Direct call expressions: `ValueError`, `counts.items`, `counts.values`, `float`, `key.replace`, `sum`

### `diagonal_pauli_expectation(distribution: Mapping[str, float], support: Sequence[int])` — line 312

Direct call expressions: `bitstring.replace`, `distribution.items`, `float`

### `ideal_measurement_distributions(unitary: QuantumCircuit)` — line 325

Exact distributions after each of the N+1 basis rotations.

Direct call expressions: `circuit_state`, `enumerate`, `float`, `format`, `probabilities`, `range`, `rotated.h`, `unitary.copy`

### `reconstruct_energy(distributions: Mapping[str, Mapping[str, float]], num_plaquettes: int, x: float)` — line 343

Direct call expressions: `diagonal_pauli_expectation`, `float`, `plaquette_chain_terms`, `range`

### `project_to_probability_simplex(quasiprobabilities: Mapping[str, float])` — line 361

Direct call expressions: `RuntimeError`, `float`, `int`, `len`, `list`, `np.arange`, `np.asarray`, `np.cumsum`, `np.maximum`, `np.nonzero`, `np.sort`, `zip`

### `optimize_with_pyzx(source: QuantumCircuit, strategy: str)` — line 377

Apply a PyZX strategy and reject an inequivalent result.

Direct call expressions: `Operator`, `Operator(source).equiv`, `RuntimeError`, `ValueError`, `candidate_zx.to_qasm`, `dict`, `graph.copy`, `qasm2.dumps`, `qasm2.loads`, `zx.Circuit.from_graph`, `zx.Circuit.from_graph(graph).to_basic_gates`, `zx.Circuit.from_qasm`, `zx.extract.extract_circuit`, `zx.extract.extract_circuit(graph.copy(), up_to_perm=False, quiet=True).to_basic_gates`, `zx.extract.lookahead_extract`, `zx.extract.lookahead_extract(graph.copy(), optimize_for_depth=True, up_to_perm=False).to_basic_gates`, `zx.optimize.basic_optimization`, `zx.simplify.full_reduce`, `zx.simplify.teleport_reduce`, `zxc.copy`, `zxc.to_graph`, `zxc.to_graph().copy`

## [src/su2zx/paths.py](../src/su2zx/paths.py)

Small path guard shared by command-line modules.

### `project_path(value: str | Path)` — line 9

Direct call expressions: `(root / value).resolve`, `Path`, `Path(value).is_absolute`, `Path(value).resolve`, `Path.cwd`, `Path.cwd().resolve`, `ValueError`

### `load_json(value: str | Path)` — line 19

Direct call expressions: `json.loads`, `project_path`, `project_path(value).read_text`

## [src/su2zx/qpu.py](../src/su2zx/qpu.py)

Dry-run-first IBM experiment. Submission needs three independent guards.

### `validate_path(backend, path: list[int])` — line 22

Direct call expressions: `ValueError`, `backend.coupling_map.get_edges`, `frozenset`, `len`, `set`, `zip`

### `instruction_error(backend, qargs: tuple[int, ...])` — line 33

Direct call expressions: `backend.target[operation].get`, `errors.append`, `float`, `min`

### `best_five_qubit_path(backend)` — line 45

Direct call expressions: `RuntimeError`, `adjacency[left].add`, `adjacency[right].add`, `backend.coupling_map.get_edges`, `defaultdict`, `instruction_error`, `len`, `min`, `path.copy`, `paths.append`, `sum`, `visit`, `zip`

### `build_isa_circuits(backend, path: list[int], repetitions: int, comparison: bool=False)` — line 80

Direct call expressions: `circuit_hash`, `circuits.append`, `generate_preset_pass_manager`, `isa.depth`, `len`, `list`, `manager.run`, `manifest.append`, `measurement_family`, `optimize_with_pyzx`, `random.Random`, `random.Random(20260831).shuffle`, `range`, `strang_evolution`, `sum`, `verify_native`

### `confirmation_token(backend: str, path: list[int], shots: int)` — line 134

Direct call expressions: `','.join`, `map`

### `execution_properties(job)` — line 141

Direct call expressions: `job.properties`, `properties.to_dict`, `repr`

### `main()` — line 149

Direct call expressions: `HadamardGenerator`, `QiskitRuntimeService`, `SamplerOptions`, `SamplerV2`, `SamplerV2(mode=backend, options=options).run`, `SystemExit`, `approval_path.parent.mkdir`, `approval_path.read_text`, `approval_path.unlink`, `approval_path.write_text`, `argparse.ArgumentParser`, `args.physical_path.split`, `best_five_qubit_path`, `build_isa_circuits`, `dict`, `execution_properties`, `hashlib.sha256`, `hashlib.sha256(json.dumps({'backend': backend.name, 'path': path, 'shots': args.shots, 'repetitions': args.repetitions, 'manifest': manifest}, sort_keys=True).encode()).hexdigest`, `int`, `item.job_id`, `job.job_id`, `job.result`, `job.usage`, `json.dumps`, `json.dumps({'backend': backend.name, 'path': path, 'shots': args.shots, 'repetitions': args.repetitions, 'manifest': manifest}, sort_keys=True).encode`, `json.loads`, `len`, `mapping.values`, `mitigation.apply_correction`, `mitigation.cals_from_system`, `mthree.M3Mitigation`, `mthree.utils.final_measurement_mapping`, `os.environ.get`, `output.parent.mkdir`, `output.write_text`, `parser.add_argument`, `parser.parse_args`, `print`, `project_path`, `publication.data.meas.get_counts`, `secrets.token_hex`, `service.backend`, `service.least_busy`, `sorted`, `validate_path`, `wall_time.time`, `zip`

### `visit(path: list[int])` — line 53

Direct call expressions: `len`, `path.copy`, `paths.append`, `visit`

### `score(path: list[int])` — line 66

Direct call expressions: `instruction_error`, `min`, `sum`, `zip`

## [src/su2zx/qpu_analysis.py](../src/su2zx/qpu_analysis.py)

Analyze raw and M3-mitigated IBM data against the ideal Trotter circuit.

### `complete(distribution, num_qubits: int=5)` — line 25

Direct call expressions: `distribution.get`, `float`, `format`, `range`

### `paired_interval(values, samples: int=20000, seed: int=29)` — line 34

Direct call expressions: `float`, `generator.choice`, `generator.choice(data, size=(samples, len(data)), replace=True).mean`, `len`, `np.asarray`, `np.quantile`, `np.random.default_rng`

### `analyze(payload: dict)` — line 41

Direct call expressions: `abs`, `circuit_state`, `complete`, `diagonal_pauli_expectation`, `enumerate`, `exact_state`, `float`, `format`, `list`, `metric_distribution.values`, `normalized_counts`, `np.abs`, `pd.DataFrame`, `project_to_probability_simplex`, `range`, `reconstruct_energy`, `reference.values`, `rows.append`, `sorted`, `strang_evolution`, `total_variation`, `variant.startswith`

### `summarize(frame: pd.DataFrame)` — line 104

Direct call expressions: `(pivot[variant] - pivot[baseline]).to_numpy`, `differences.mean`, `float`, `paired_interval`, `pivot[variant].mean`, `subset.pivot`

### `plots(frame: pd.DataFrame, figures)` — line 122

Direct call expressions: `ax.grid`, `ax.legend`, `ax.plot`, `ax.set`, `axes[0].plot`, `axes[0].set`, `axes[1].plot`, `axes[1].set`, `axis.grid`, `axis.legend`, `axis.plot`, `axis.set`, `fig.savefig`, `figures.mkdir`, `frame.groupby`, `frame[frame.treatment == 'raw'].groupby`, `frame[frame.treatment == treatment].groupby`, `group.groupby`, `group.groupby('variant').tvd_to_exact_trotter.mean`, `plt.close`, `plt.subplots`, `zip`

### `main()` — line 160

Direct call expressions: `(output / 'data' / 'qpu_summary.json').write_text`, `analyze`, `argparse.ArgumentParser`, `frame.to_csv`, `json.dumps`, `json.loads`, `parser.add_argument`, `parser.parse_args`, `plots`, `project_path`, `project_path(args.input).read_text`, `summarize`

## [src/su2zx/report.py](../src/su2zx/report.py)

Generate the v0.3.0 research narrative from machine-readable artifacts.

### `commit_sha(root: Path)` — line 17

Direct call expressions: `result.stdout.strip`, `subprocess.run`

### `load_optional(path: Path)` — line 24

Direct call expressions: `json.loads`, `path.exists`, `path.read_text`

### `strategy_table(frame: pd.DataFrame)` — line 28

Direct call expressions: `'\n'.join`, `frame.groupby`, `frame.groupby('strategy')[['native_2q_count', 'native_2q_depth', 'routing_penalty_ratio']].median`, `lines.append`, `medians.iterrows`

### `figure(name: str, caption: str, output: Path)` — line 43

Direct call expressions: `Path.cwd`, `path.as_posix`, `path.exists`, `path.relative_to`, `path.relative_to(Path.cwd()).as_posix`

### `main()` — line 51

Direct call expressions: `Path.cwd`, `Path.cwd().resolve`, `accelerator.get`, `accelerator.get('gpu', {}).get`, `argparse.ArgumentParser`, `commit_sha`, `current.get`, `datetime.now`, `datetime.now(UTC).isoformat`, `destination.write_text`, `figure`, `float`, `int`, `json.dumps`, `len`, `line.strip`, `load_json`, `load_optional`, `next`, `parser.add_argument`, `parser.parse_args`, `pd.read_csv`, `physics.get`, `physics.get('trotter_convergence_fit', {}).get`, `print`, `project_path`, `reversed`, `seed_span.max`, `seeds.groupby`, `seeds.groupby(['target_topology', 'strategy']).native_2q_count.agg`, `seeds.verification_result.sum`, `selector.get`, `selector.get('fixed_normalized_regret', {}).get`, `selector.get('validation', {}).get`, `strategy_table`, `strict.get`, `symmetric.get`, `symmetry.get`, `test_evidence.splitlines`, `test_log.exists`, `test_log.read_text`, `tn.get`, `validation.get`, `verified.verification_result.sum`, `winner.get`, `x.max`, `x.min`

## [src/su2zx/robust_study.py](../src/su2zx/robust_study.py)

Fixed-target routing robustness and prospective pairwise compiler selection.

### `verify_native(source: QuantumCircuit, compiled: QuantumCircuit, seed: int=20260905)` — line 38

Check the routed isometry on zero plus three random states, including ancillas.

This is a randomized numerical check, not an exhaustive unitary proof.
Initial and final virtual-to-physical maps are both applied explicitly.

Direct call expressions: `RuntimeError`, `Statevector`, `Statevector(physical).evolve`, `Statevector(vector).evolve`, `abs`, `compiled.layout.final_index_layout`, `compiled.layout.initial_index_layout`, `enumerate`, `float`, `list`, `max`, `np.arange`, `np.eye`, `np.eye(1, 2 ** n, dtype=complex).ravel`, `np.linalg.norm`, `np.max`, `np.random.default_rng`, `np.vdot`, `np.zeros`, `range`, `rng.normal`, `sum`

### `source_features(source: QuantumCircuit, n: int, x: float, t: float, r: int, order: str)` — line 79

Direct call expressions: `_interaction_features`, `circuit_hash`, `circuit_structure_hash`, `count_one_qubit`, `count_two_qubit`, `dict`, `len`, `np.mean`, `plaquette_chain_terms`, `source.depth`, `source.size`, `sum`

### `compiler_run(config: dict, data: Path)` — line 101

Direct call expressions: `(data / 'compiler_design.json').write_text`, `(row == row.min()).sum`, `Operator`, `Operator(source).equiv`, `_duration`, `_target_features`, `base.update`, `case.coupling.get_edges`, `compile_candidate`, `compiled.depth`, `compiled.layout.final_index_layout`, `count_two_qubit`, `design.append`, `dict`, `enumerate`, `failure.rsplit`, `float`, `hashlib.sha256`, `hashlib.sha256(json.dumps(target_description).encode()).hexdigest`, `json.dumps`, `json.dumps(target_description).encode`, `len`, `logicals.items`, `old.case_id.isin`, `old.pivot`, `old[old.case_id.isin(selected)].drop_duplicates`, `old[old.case_id.isin(selected)].drop_duplicates('case_id').itertuples`, `optimize_with_pyzx`, `pair_delta.nlargest`, `pair_delta.nsmallest`, `pd.DataFrame`, `pd.DataFrame(rows).to_csv`, `pd.read_csv`, `pivot.apply`, `print`, `project_path`, `row.min`, `rows.append`, `selected.update`, `set`, `sorted`, `source_features`, `str`, `strang_evolution`, `target_cases`, `two_qubit_depth`, `verify_native`

### `pairwise(raw: pd.DataFrame)` — line 226

Direct call expressions: `(base[name].fillna('null') == other.loc[base.index, name].fillna('null')).all`, `base.reset_index`, `base[name].fillna`, `np.sign`, `np.sign(base.delta_native_2q_count).map`, `other.loc[base.index, name].fillna`, `raw.case_id.isin`, `raw.duplicated`, `raw.duplicated(['case_id', 'strategy']).any`, `raw.groupby`, `raw.groupby('case_id').verification_result.agg`, `raw[raw.case_id.isin(valid_ids)].copy`, `raw[raw.strategy == 'basic'].copy`, `raw[raw.strategy == 'basic'].copy().set_index`, `raw[raw.strategy == 'teleport'].set_index`, `set`, `tuple`, `zip`

### `robustness(pairs: pd.DataFrame, threshold: float)` — line 262

Direct call expressions: `dict`, `float`, `group.delta_native_2q_count.mean`, `group.delta_native_2q_count.median`, `group.delta_native_2q_depth.mean`, `group.delta_native_2q_depth.median`, `group.label.value_counts`, `group.label.value_counts(normalize=True).reindex`, `len`, `np.log2`, `pairs.groupby`, `pd.DataFrame`, `rows.append`, `sum`

### `frozen_choices(frame: pd.DataFrame, rule: dict)` — line 304

Direct call expressions: `np.where`

### `policy_metrics(frame: pd.DataFrame, choices: np.ndarray)` — line 313

Direct call expressions: `accuracy_score`, `balanced_accuracy_score`, `confusion_matrix`, `confusion_matrix(target, choices, labels=['basic', 'teleport', 'tie']).tolist`, `dict`, `float`, `frame.basic_native_2q_count.to_numpy`, `frame.label.to_numpy`, `frame.teleport_native_2q_count.to_numpy`, `np.maximum`, `np.mean`, `np.median`, `np.minimum`, `np.where`, `regret.max`, `regret.mean`

### `evaluate_ml(pairs: pd.DataFrame, config: dict, data: Path)` — line 337

Direct call expressions: `'|'.join`, `(data / 'pairwise_features.json').write_text`, `(data / 'pairwise_ml_summary.json').write_text`, `(data / 'prospective_tree_rules.txt').write_text`, `DecisionTreeClassifier`, `GroupKFold`, `LeaveOneGroupOut`, `LogisticRegression`, `RandomForestClassifier`, `RandomForestRegressor`, `StandardScaler`, `any`, `assignments.extend`, `choices.items`, `dict`, `enumerate`, `export_text`, `float`, `frame.model.isin`, `frame.to_csv`, `frame[(frame.validation == 'prospective') & frame.model.isin(['always_basic', 'always_teleport', 'majority', 'frozen_rule'])].mean_regret.min`, `frozen_choices`, `hasattr`, `importance.extend`, `json.dumps`, `len`, `list`, `make_pipeline`, `metrics.append`, `model.fit`, `model.predict`, `model_name.endswith`, `models.items`, `np.asarray`, `np.flatnonzero`, `np.full`, `np.where`, `output.items`, `output[model_name].extend`, `pairs.cohort.to_numpy`, `pairs.iloc[test].label.to_numpy`, `pairs.iloc[train].label.mode`, `pairs[numeric].astype`, `pd.DataFrame`, `pd.DataFrame(assignments).to_csv`, `pd.DataFrame(importance).to_csv`, `pd.DataFrame(logistic.coef_, columns=x.columns).assign`, `pd.DataFrame(logistic.coef_, columns=x.columns).assign(classes='|'.join(logistic.classes_)).to_csv`, `pd.DataFrame(predictions).to_csv`, `pd.concat`, `pd.get_dummies`, `policy_metrics`, `predictions.extend`, `primary.model.isin`, `primary[primary.model.isin(['always_basic', 'always_teleport', 'majority', 'frozen_rule'])].mean_regret.min`, `primary[primary.model.isin(models)].sort_values`, `set`, `set(pairs.iloc[train].circuit_structure_hash).isdisjoint`, `splits.items`, `splitter.split`, `str`, `test_order.extend`, `validations.items`, `zip`

### `main()` — line 523

Direct call expressions: `(data / 'frozen_design.json').read_text`, `(group.median_delta_2q < 0).sum`, `(group.median_delta_2q > 0).sum`, `argparse.ArgumentParser`, `compiler_run`, `data.mkdir`, `dict`, `evaluate_ml`, `factor.upper`, `hashlib.sha256`, `hashlib.sha256(project_path(args.config).read_bytes()).hexdigest`, `int`, `json.dumps`, `json.loads`, `len`, `load_json`, `np.sign`, `pairs.groupby`, `pairs.groupby(['circuit_structure_hash', 'target_name'], as_index=False)[['delta_native_2q_count', 'delta_native_2q_depth']].median`, `pairs.to_csv`, `pairwise`, `parser.add_argument`, `parser.parse_args`, `pd.DataFrame`, `pd.DataFrame(sensitivity).to_csv`, `pd.read_csv`, `print`, `project_path`, `project_path(args.config).read_bytes`, `robust.groupby`, `robust.to_csv`, `robustness`, `sensitivity.append`, `set`, `str`, `structural.to_csv`, `structural[structural.delta_native_2q_count != 0].to_csv`, `time.perf_counter`

## [src/su2zx/scaling_study.py](../src/su2zx/scaling_study.py)

Symmetry physics and direct MPS observables without dense-state scaling.

### `symmetric_initial(n: int)` — line 39

Direct call expressions: `sorted`, `tuple`

### `observable_operators(n: int, x: float)` — line 43

Direct call expressions: `Pauli`, `hamiltonian`, `hamiltonian_components`, `pauli_word`, `range`

### `direct_mps(circuit, x: float, bond: int, threshold: float)` — line 56

Save local Pauli expectations and compact MPS tensors only.

Identity expectation is a normalized-state diagnostic, not discarded weight.
Tensor bytes measure the returned MPS, not total simulator workspace.

Direct call expressions: `AerSimulator`, `RuntimeError`, `any`, `circuit.copy`, `dict`, `float`, `len`, `list`, `max`, `np.asarray`, `np.real`, `observable_operators`, `observable_operators(circuit.num_qubits, x).items`, `range`, `resource.getrusage`, `result.data`, `result.results[0].metadata.get`, `saved.save_expectation_value`, `saved.save_matrix_product_state`, `simulator.run`, `simulator.run(saved, shots=1, seed_simulator=11).result`, `str`, `sum`, `time.perf_counter`, `values.items`, `values.pop`

### `tn_run(data: Path)` — line 97

Direct call expressions: `(data / 'tn_summary.json').write_text`, `RuntimeError`, `Statevector`, `abs`, `dict`, `direct_mps`, `exact.expectation_value`, `expm_multiply`, `float`, `frame.query`, `frame.query('num_plaquettes <= 8 and max_bond == 64').observable_error_to_trotter.max`, `frame.query('num_plaquettes > 8 and max_bond == 64').max_observable_change_from_previous.max`, `frame[frame.num_plaquettes <= 8].to_csv`, `frame[frame.num_plaquettes > 8].to_csv`, `hamiltonian`, `hamiltonian(n, 2.0).to_matrix`, `ideal.expectation_value`, `initial_state`, `json.dumps`, `max`, `np.real`, `observable_operators`, `observables.extend`, `operators.items`, `pd.DataFrame`, `pd.DataFrame(observables).to_csv`, `pd.DataFrame(rows).query`, `pd.DataFrame(rows).to_csv`, `print`, `rows.append`, `strang_evolution`, `symmetric_initial`, `validated.observable_error_to_trotter.max`, `values.items`

### `physics_run(config: dict, data: Path)` — line 200

Direct call expressions: `(data / 'symmetry_summary.json').write_text`, `(matched[metric].symmetry < matched[metric].current - 1e-12).sum`, `(matched[metric].symmetry > matched[metric].current + 1e-12).sum`, `Statevector`, `Statevector(vector).expectation_value`, `_duration`, `abs`, `compile_candidate`, `compiled.depth`, `compiled_rows.append`, `count_two_qubit`, `dict`, `expm_multiply`, `fits.append`, `float`, `frame.exact_mirror_asymmetry.max`, `frame.groupby`, `frame.norm_error.max`, `frame.pivot`, `frame[frame.term_ordering == 'symmetry'].mirror_asymmetry.max`, `frontier.groupby`, `frontier.to_csv`, `group[metrics].to_numpy`, `h.to_matrix`, `hamiltonian`, `hamiltonian_components`, `initial_state`, `int`, `json.dumps`, `len`, `linregress`, `local_occupations`, `matched[metric].current.max`, `matched[metric].symmetry.max`, `np.all`, `np.any`, `np.log`, `np.max`, `np.real`, `np.vdot`, `np.where`, `occupation.tolist`, `pd.DataFrame`, `pd.DataFrame(compiled_rows).to_csv`, `pd.DataFrame(fits).to_csv`, `pd.DataFrame(rows).to_csv`, `print`, `probabilities`, `rows.append`, `source_features`, `state.expectation_value`, `strang_evolution`, `subset.repetitions.tolist`, `sum`, `symmetric_initial`, `target_cases`, `total_variation`, `two_qubit_depth`, `verify_native`, `zip`

### `main()` — line 342

Direct call expressions: `argparse.ArgumentParser`, `data.mkdir`, `json.dumps`, `load_json`, `parser.add_argument`, `parser.parse_args`, `physics_run`, `print`, `project_path`, `tn_run`

## [src/su2zx/study.py](../src/su2zx/study.py)

Generate exact/Trotter observables, distributions, and physics plots.

### `configure_plotting()` — line 31

Direct call expressions: `plt.rcParams.update`

### `save_figure(fig: plt.Figure, figures: Path, name: str)` — line 44

Direct call expressions: `fig.savefig`, `plt.close`

### `exact_states(num_qubits: int, x: float, times: np.ndarray, initial_ones: list[int])` — line 50

Direct call expressions: `eigenvectors.conj`, `hamiltonian`, `hamiltonian(num_qubits, x).to_matrix`, `initial_state`, `np.exp`, `np.linalg.eigh`

### `state_row(method: str, time: float, state: np.ndarray, reference: np.ndarray, electric, magnetic)` — line 63

Direct call expressions: `abs`, `expectation`, `float`, `local_occupations`, `np.vdot`, `probabilities`, `range`, `total_variation`

### `generate_data(config: dict, output: Path)` — line 92

Direct call expressions: `(data / 'physics_summary.json').write_text`, `abs`, `circuit.depth`, `circuit.size`, `circuit_state`, `convergence.append`, `convergence_frame.to_csv`, `data.mkdir`, `enumerate`, `exact_states`, `expectation`, `float`, `format`, `group.energy_drift.max`, `group.mirror_asymmetry.max`, `group.tvd_to_exact_hamiltonian.max`, `hamiltonian`, `hamiltonian_components`, `ideal_measurement_distributions`, `int`, `json.dumps`, `len`, `list`, `max`, `np.asarray`, `np.linspace`, `np.log`, `np.polyfit`, `np.sqrt`, `np.sum`, `observables.norm_error.max`, `observables.query`, `observables.to_csv`, `pd.DataFrame`, `pd.DataFrame(reconstruction_rows).to_csv`, `positive.max_tvd.to_numpy`, `positive.repetitions.to_numpy`, `probabilities`, `probabilities_frame.to_csv`, `probability_rows.append`, `reconstruct_energy`, `reconstruction_rows.append`, `rows.append`, `selected.tvd_to_exact_hamiltonian.max`, `state_row`, `strang_evolution`, `sum`, `symmetry_frame.groupby`, `symmetry_frame.to_csv`, `symmetry_rows.append`, `x_fit.mean`, `zip`

### `generate_plots(frame: pd.DataFrame, output: Path, primary_r: int)` — line 240

Direct call expressions: `ax.grid`, `ax.legend`, `ax.plot`, `ax.semilogy`, `ax.set`, `ax.set_title`, `axes[0].legend`, `axes[0].plot`, `axes[0].set_title`, `axes[1].plot`, `axes[1].set_title`, `axis.grid`, `axis.plot`, `axis.set`, `configure_plotting`, `enumerate`, `fig.suptitle`, `figures.mkdir`, `frame.groupby`, `frame[frame.method != 'exact'].groupby`, `np.maximum`, `pd.read_csv`, `plt.subplots`, `save_figure`, `symmetry.groupby`, `symmetry_path.exists`, `zip`

### `main()` — line 323

Direct call expressions: `argparse.ArgumentParser`, `generate_data`, `generate_plots`, `int`, `len`, `load_json`, `output.mkdir`, `parser.add_argument`, `parser.parse_args`, `print`, `project_path`

## [src/su2zx/tn_study.py](../src/su2zx/tn_study.py)

CPU matrix-product-state validation for SU2ZX v0.3.0.

### `mps_state(circuit, max_bond: int, tolerance: float)` — line 29

Simulate a circuit with Aer's CPU MPS method and return its statevector.

Direct call expressions: `AerSimulator`, `circuit.copy`, `np.asarray`, `result.get_statevector`, `saved.save_statevector`, `simulator.run`, `simulator.run(saved).result`, `time.perf_counter`

### `generate_tn_data(output: Path)` — line 44

Direct call expressions: `(data / 'tensor_network_summary.json').write_text`, `Statevector`, `abs`, `data.mkdir`, `exact_state`, `expectation`, `figures.mkdir`, `float`, `frame.to_csv`, `hamiltonian`, `json.dumps`, `local_occupations`, `max`, `mps_state`, `np.asarray`, `np.max`, `np.vdot`, `pd.DataFrame`, `probabilities`, `resource.getrusage`, `rows.append`, `strang_evolution`, `total_variation`, `validated.energy_error_to_ideal_trotter.max`, `validated.norm_error.max`, `validated.state_fidelity_to_ideal_trotter.min`, `validated.tvd_to_ideal_trotter.max`

### `save_tn_plot(frame: pd.DataFrame, figures: Path)` — line 146

Direct call expressions: `axes[0].semilogy`, `axes[0].set`, `axes[1].plot`, `axes[1].set`, `axis.grid`, `axis.legend`, `axis.set_xscale`, `fig.savefig`, `fig.suptitle`, `frame.groupby`, `np.maximum`, `plt.close`, `plt.subplots`

### `main()` — line 173

Direct call expressions: `argparse.ArgumentParser`, `generate_tn_data`, `json.dumps`, `parser.add_argument`, `parser.parse_args`, `print`, `project_path`, `save_tn_plot`

## [tests/test_compiler.py](../tests/test_compiler.py)

### `test_generic_ecr_compilation_and_basic_candidate()` — line 12

Direct call expressions: `compile_candidate`, `count_two_qubit`, `generic_ecr_backend`, `strang_evolution`

```python
assert count_two_qubit(baseline) > 0
assert count_two_qubit(basic) > 0
```

### `test_target_and_layout_diversity()` — line 21

Direct call expressions: `target_cases`

```python
assert {case.topology for case in cases} == {'line', 'ring', 'grid', 'heavy_hex_like', 'irregular'}
assert {case.layout_name for case in cases} == {'favorable', 'spread', 'transpiler'}
```

## [tests/test_core.py](../tests/test_core.py)

### `test_one_plaquette_matrix_and_spectrum()` — line 27

Direct call expressions: `abs`, `hamiltonian`, `hamiltonian(1, 1.0).to_matrix`, `np.argmin`, `np.asarray`, `np.linalg.eigh`, `np.linalg.eigvalsh`, `np.sqrt`, `np.testing.assert_allclose`, `np.vdot`

```python
np.testing.assert_allclose(matrix, [[0, -2], [-2, 3]], atol=1e-13)
np.testing.assert_allclose(np.linalg.eigvalsh(matrix), [-1, 4], atol=1e-13)
np.testing.assert_allclose(abs(np.vdot(ground, expected_ground)), 1.0, atol=1e-13)
```

### `test_one_plaquette_transition_probability()` — line 37

Direct call expressions: `abs`, `exact_state`, `np.sin`, `np.testing.assert_allclose`

```python
np.testing.assert_allclose(abs(state[1]) ** 2, analytic, atol=1e-12)
```

### `test_two_plaquette_matrix_and_ground_energy()` — line 44

Direct call expressions: `hamiltonian`, `hamiltonian(2, 1.0).to_matrix`, `np.asarray`, `np.linalg.eigvalsh`, `np.testing.assert_allclose`

```python
np.testing.assert_allclose(matrix, expected, atol=1e-13)
np.testing.assert_allclose(np.linalg.eigvalsh(matrix)[0], -1.789221846776, atol=1e-12)
```

### `test_hamiltonians_are_hermitian()` — line 51

Direct call expressions: `hamiltonian`, `hamiltonian(n, 2.0).to_matrix`, `matrix.conj`, `np.testing.assert_allclose`

```python
np.testing.assert_allclose(matrix, matrix.conj().T, atol=1e-13)
```

### `test_state_norms_and_qiskit_little_endian_order()` — line 57

Direct call expressions: `circuit_state`, `exact_state`, `initial_state`, `np.flatnonzero`, `np.flatnonzero(state).tolist`, `np.linalg.norm`, `np.testing.assert_allclose`, `pauli_word`, `strang_evolution`

```python
assert np.flatnonzero(state).tolist() == [5]
assert pauli_word(5, {0: 'X', 4: 'Z'}) == 'ZIIIX'
np.testing.assert_allclose(np.linalg.norm(exact), 1.0, atol=1e-12)
np.testing.assert_allclose(np.linalg.norm(trotter), 1.0, atol=1e-12)
```

### `test_manual_pauli_rotation()` — line 69

Direct call expressions: `Operator`, `Operator(circuit).equiv`, `QuantumCircuit`, `expm`, `np.asarray`, `np.kron`, `pauli_rotation`

```python
assert Operator(circuit).equiv(Operator(expected))
```

### `test_trotter_converges_and_preserves_mirror_symmetry()` — line 77

Direct call expressions: `abs`, `all`, `circuit_state`, `exact_state`, `local_occupations`, `np.testing.assert_allclose`, `np.vdot`, `strang_evolution`, `zip`

```python
assert all((left > right for left, right in zip(infidelities, infidelities[1:])))
np.testing.assert_allclose(occupations, occupations[::-1], atol=1e-12)
```

### `test_six_basis_energy_reconstruction()` — line 91

Direct call expressions: `circuit_state`, `expectation`, `hamiltonian`, `ideal_measurement_distributions`, `np.testing.assert_allclose`, `reconstruct_energy`, `strang_evolution`

```python
np.testing.assert_allclose(reconstructed, direct, atol=1e-10)
```

### `test_simplex_projection()` — line 99

Direct call expressions: `all`, `np.testing.assert_allclose`, `project_to_probability_simplex`, `projected.values`, `sum`

```python
assert all((value >= 0 for value in projected.values()))
np.testing.assert_allclose(sum(projected.values()), 1.0, atol=1e-13)
```

### `test_pyzx_candidates_are_exact()` — line 105

Direct call expressions: `Operator`, `Operator(source).equiv`, `optimize_with_pyzx`, `strang_evolution`

```python
assert Operator(source).equiv(Operator(candidate))
```

### `test_structure_hash_normalizes_angles_but_not_gate_order()` — line 113

Direct call expressions: `circuit_hash`, `circuit_structure_hash`, `strang_evolution`

```python
assert circuit_hash(left) != circuit_hash(right)
assert circuit_structure_hash(left) == circuit_structure_hash(right)
assert circuit_structure_hash(left) != circuit_structure_hash(symmetric)
```

### `test_additional_pyzx_strategies_are_exact()` — line 122

Direct call expressions: `Operator`, `Operator(source).equiv`, `optimize_with_pyzx`, `strang_evolution`

```python
assert Operator(source).equiv(Operator(optimize_with_pyzx(source, strategy)))
```

## [tests/test_qpu.py](../tests/test_qpu.py)

### `test_qpu_dry_run_manifest_and_confirmation_guard()` — line 7

Direct call expressions: `build_isa_circuits`, `confirmation_token`, `generic_ecr_backend`, `len`, `validate_path`

```python
assert len(circuits) == len(manifest) == 60
assert len({(item['variant'], item['time'], item['basis']) for item in manifest}) == 60
assert confirmation_token('test', path, 4096) == 'I_APPROVE_IBM_QPU:test:path=0,1,2,3,4:shots=4096:physics=60:m3=8'
```

## [tests/test_study.py](../tests/test_study.py)

### `test_small_data_generation(tmp_path)` — line 10

Direct call expressions: `(tmp_path / 'data' / 'physics_summary.json').read_text`, `frame.select_dtypes`, `frame.select_dtypes(include=[float, int]).to_numpy`, `generate_data`, `json.loads`, `len`, `np.isfinite`, `np.isfinite(frame.select_dtypes(include=[float, int]).to_numpy()).all`, `np.testing.assert_allclose`

```python
assert len(frame) == 9
assert len(probabilities) == 2 * 2 * 32
assert np.isfinite(frame.select_dtypes(include=[float, int]).to_numpy()).all()
assert summary['max_six_basis_energy_error'] < 1e-10
np.testing.assert_allclose(summary['initial_energy'], 3.0, atol=1e-12)
```

## [tests/test_tn.py](../tests/test_tn.py)

### `test_cpu_mps_matches_statevector_for_two_plaquettes()` — line 9

Direct call expressions: `circuit_state`, `mps_state`, `np.testing.assert_allclose`, `strang_evolution`

```python
np.testing.assert_allclose(mps, circuit_state(circuit), atol=1e-10)
```

## [tests/test_v040.py](../tests/test_v040.py)

Regression gates for routed equivalence, pair integrity and direct MPS.

### `test_routed_equivalence_tracks_layout_and_rejects_corruption()` — line 17

Direct call expressions: `QuantumCircuit`, `compile_candidate`, `compiled.copy`, `compiled.layout.final_index_layout`, `corrupt.x`, `pytest.raises`, `source.cx`, `source.h`, `source.ry`, `target_cases`, `verify_native`

```python
assert verify_native(source, compiled) < 1e-10
pytest.raises(RuntimeError, match='routed equivalence failed')
```

### `test_pairwise_excludes_whole_pair_when_one_output_fails()` — line 33

Direct call expressions: `dict`, `pairwise`, `pd.DataFrame`, `result.case_id.tolist`, `result.delta_native_2q_count.tolist`, `result.label.tolist`, `rows.append`

```python
assert result.case_id.tolist() == ['valid']
assert result.label.tolist() == ['teleport']
assert result.delta_native_2q_count.tolist() == [-2]
```

### `test_direct_mps_observables_do_not_save_dense_state(monkeypatch, n)` — line 58

Direct call expressions: `AssertionError`, `Statevector`, `abs`, `direct_mps`, `ideal.expectation_value`, `monkeypatch.setattr`, `observable_operators`, `observable_operators(n, 2.0).items`, `pytest.mark.parametrize`, `strang_evolution`, `symmetric_initial`

Decorator: `pytest.mark.parametrize('n', [5, 8])`

```python
assert not stats['saved_statevector']
assert stats['observed_max_bond'] <= 64
assert abs(values['total_energy'] - values['electric_energy'] - values['magnetic_energy']) < 1e-10
assert abs(values[name] - ideal.expectation_value(op)) < 1e-07
```

### `test_frozen_rule_boundary_and_order()` — line 78

Direct call expressions: `dict`, `frozen_choices`, `frozen_choices(frame, dict(teleport_max_n=3, teleport_ordering='current')).tolist`, `pd.DataFrame`

```python
assert frozen_choices(frame, dict(teleport_max_n=3, teleport_ordering='current')).tolist() == ['teleport', 'teleport', 'basic', 'basic']
```

### `test_symmetry_initial_and_evolution_are_reflection_invariant(n)` — line 91

Direct call expressions: `Statevector`, `abs`, `format`, `int`, `np.max`, `pytest.mark.parametrize`, `range`, `strang_evolution`, `symmetric_initial`

Decorator: `pytest.mark.parametrize('n', [3, 4])`

```python
assert np.max(abs(probs - probs[reflected])) < 1e-12
```

### `test_pyzx_import_precision_and_settings_are_preserved()` — line 100

Direct call expressions: `Operator`, `Operator(source).equiv`, `optimize_with_pyzx`, `strang_evolution`

```python
assert Operator(source).equiv(Operator(candidate), atol=1e-12, rtol=1e-12)
assert zx.settings.float_to_fraction_max_denominator == denominator
```

### `test_qpu_fresh_approval_guards_never_submit(monkeypatch)` — line 114

Direct call expressions: `AssertionError`, `QuantumCircuit`, `approval.exists`, `approval.read_text`, `approval.unlink`, `approval.write_text`, `circuit.measure_all`, `dict`, `generic_ecr_backend`, `json.dumps`, `json.loads`, `monkeypatch.delenv`, `monkeypatch.setattr`, `monkeypatch.setenv`, `project_path`, `pytest.raises`, `qpu.main`

```python
assert not approval.exists()
assert approval.exists()
pytest.raises(SystemExit, match='ALLOW_IBM_QPU_SUBMISSION')
pytest.raises(SystemExit, match='token does not match')
pytest.raises(SystemExit, match='expired')
```

### `forbidden(*args, **kwargs)` — line 59

Direct call expressions: `AssertionError`

### `forbidden(*args, **kwargs)` — line 135

Direct call expressions: `AssertionError`

### `backend(self, name)` — line 132

Direct call expressions: none

## [tools/archive_v040.py](../tools/archive_v040.py)

Curated, scanned, non-overwriting final archive with exact-file integrity receipt.

### `archive_files(root)` — line 17

Direct call expressions: `(root / directory).rglob`, `RuntimeError`, `files.append`, `files.extend`, `path.is_file`, `path.is_symlink`, `path.relative_to`, `path.resolve`, `set`, `sorted`

### `scan(files)` — line 68

Direct call expressions: `RuntimeError`, `any`, `failures.append`, `path.name.lower`, `path.name.startswith`, `path.read_bytes`, `pattern.search`, `patterns.items`, `re.compile`, `str`

### `main()` — line 92

Direct call expressions: `(check_logs / 'data_integrity.log').read_text`, `(check_logs / filename).read_text`, `(root / 'RUN_MANIFEST.md').write_text`, `(root / 'artifacts/logs/v040/archive_integrity.json').write_text`, `(root / 'artifacts/logs/v040/graph_validation.json').read_text`, `(root / 'artifacts/provenance/publication_v040.json').write_text`, `(root / 'graphify-out/graph.json').read_bytes`, `FileExistsError`, `archive.namelist`, `archive.read`, `archive.testzip`, `archive.write`, `archive_files`, `argparse.ArgumentParser`, `check_logs.is_dir`, `datetime.now`, `datetime.now(UTC).strftime`, `destination.exists`, `destination.parent.mkdir`, `destination.read_bytes`, `destination.relative_to`, `destination.relative_to(root).as_posix`, `destination.stat`, `destination.with_suffix`, `destination.with_suffix('.zip.integrity.json').write_text`, `destination.with_suffix('.zip.sha256').write_text`, `dict`, `hashlib.sha256`, `hashlib.sha256((root / 'graphify-out/graph.json').read_bytes()).hexdigest`, `hashlib.sha256(archive.read(path.relative_to(root).as_posix())).digest`, `hashlib.sha256(destination.read_bytes()).hexdigest`, `hashlib.sha256(path.read_bytes()).digest`, `json.dumps`, `json.loads`, `len`, `manifest.replace`, `manifest.replace('release commit follows archival by required execution order.', 'verified published main revision; this final reports ZIP was created after push.').replace`, `parser.add_argument`, `parser.parse_args`, `path.read_bytes`, `path.relative_to`, `path.relative_to(root).as_posix`, `print`, `project_path`, `receipt.items`, `scan`, `scan_log.write_text`, `set`, `sorted`, `subprocess.check_output`, `subprocess.check_output(['git', 'ls-remote', 'origin', 'refs/heads/main'], text=True).split`, `subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip`, `subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip`, `zipfile.ZipFile`

## [tools/cudaq_reference.py](../tools/cudaq_reference.py)

CUDA-Q reference for the same second-order product formula.

### `arguments()` — line 13

Direct call expressions: `argparse.ArgumentParser`, `parser.add_argument`, `parser.parse_args`

### `evolve(coefficients: list[float], words: list[cudaq.pauli_word], num_qubits: int, repetitions: int, evolution_time: float, initial_qubit: int)` — line 49

Direct call expressions: `cudaq.qvector`, `exp_pauli`, `len`, `range`, `x`

### `evolve_and_measure(coefficients: list[float], words: list[cudaq.pauli_word], num_qubits: int, repetitions: int, evolution_time: float, initial_qubit: int)` — line 70

Direct call expressions: `cudaq.qvector`, `exp_pauli`, `len`, `mz`, `range`, `x`

### `cudaq_hamiltonian(num_plaquettes: int, x_value: float)` — line 90

Direct call expressions: `cudaq.spin.i`, `cudaq.spin.x`, `cudaq.spin.y`, `cudaq.spin.z`, `enumerate`, `factors.append`, `plaquette_chain_terms`

### `main()` — line 108

Direct call expressions: `abs`, `circuit_state`, `cudaq.get_state`, `cudaq.observe`, `cudaq.observe(evolve, cudaq_hamiltonian(ARGS.plaquettes, ARGS.x), *call).expectation`, `cudaq.pauli_word`, `cudaq.set_random_seed`, `cudaq.set_target`, `cudaq_hamiltonian`, `expectation`, `float`, `hamiltonian`, `json.dumps`, `np.asarray`, `np.vdot`, `plaquette_chain_terms`, `print`, `probabilities`, `strang_evolution`, `total_variation`

## [tools/cutensornet_reference.py](../tools/cutensornet_reference.py)

Direct cuTensorNet contraction of a Qiskit SU2ZX circuit.

### `scalar(value)` — line 13

Direct call expressions: `complex`, `hasattr`, `value.item`

### `main()` — line 17

Direct call expressions: `''.join`, `CircuitToEinsum`, `abs`, `argparse.ArgumentParser`, `contract`, `contract_path`, `converter.amplitude`, `converter.expectation`, `json.dumps`, `parser.add_argument`, `parser.parse_args`, `plaquette_chain_terms`, `print`, `range`, `scalar`, `str`, `strang_evolution`

## [tools/function_inventory.py](../tools/function_inventory.py)

Generate a source-linked callable and test-assertion inventory for the final report.

### `main()` — line 10

Direct call expressions: `', '.join`, `'\n'.join`, `(root / directory).rglob`, `any`, `ast.get_docstring`, `ast.parse`, `ast.unparse`, `ast.walk`, `isinstance`, `lines.extend`, `path.read_text`, `path.relative_to`, `path.relative_to(root).as_posix`, `project_path`, `project_path('docs/CODE_FUNCTION_INVENTORY.md').write_text`, `sorted`

## [tools/plot_v040.py](../tools/plot_v040.py)

Regenerate v0.4.0 figures exclusively from persisted CSV source data.

### `save(name: str, source: str, caption: str)` — line 20

Direct call expressions: `dict`, `fig.savefig`, `fig.tight_layout`, `plt.close`, `plt.gcf`

### `main()` — line 29

Direct call expressions: `'/'.join`, `(DATA / 'pairwise_ml_summary.json').read_text`, `(FIGURES / 'figure_sources.json').write_text`, `ax.bar`, `ax.hist`, `ax.imshow`, `ax.legend`, `ax.loglog`, `ax.plot`, `ax.set`, `ax.set_yscale`, `ax.text`, `ax.tick_params`, `axes[-1].legend`, `column.replace`, `compiled.groupby`, `compiled.groupby(['term_ordering', 'strategy']).native_2q_depth.mean`, `compiled.groupby(['term_ordering', 'strategy']).native_2q_depth.mean().unstack`, `fig.colorbar`, `fits.query`, `frontier.query`, `frontier.query('num_plaquettes == 5').groupby`, `group.groupby`, `group.groupby('num_plaquettes')[metric].median`, `group.sort_values`, `json.dumps`, `json.loads`, `len`, `metric.replace`, `np.arange`, `np.array`, `np.maximum`, `pairs.groupby`, `pd.crosstab`, `pd.crosstab(robust[column], robust.status).plot.bar`, `pd.read_csv`, `physics.groupby`, `physics.query`, `plt.subplots`, `plt.title`, `plt.xlabel`, `plt.ylabel`, `print`, `range`, `save`, `str`, `subset.groupby`, `table.plot.bar`, `tn.groupby`, `tn.query`, `tn.query('num_plaquettes <= 8').groupby`, `validation.replace`, `zip`

## [tools/provenance.py](../tools/provenance.py)

Write secret-free machine-readable provenance for the v0.3.0 run.

### `command(arguments: list[str])` — line 15

Direct call expressions: `result.stdout.strip`, `subprocess.run`

### `package_version(*names: str)` — line 20

Direct call expressions: `version`

### `main()` — line 29

Direct call expressions: `(root / 'artifacts' / 'data').glob`, `(root / 'artifacts' / 'figures').glob`, `(root / 'artifacts' / 'provenance' / 'run_v0.3.0.json').resolve`, `Path.cwd`, `Path.cwd().resolve`, `SystemExit`, `bool`, `command`, `command(['nvidia-smi', '--query-gpu=name,compute_cap,driver_version,memory.total,memory.free', '--format=csv,noheader']).split`, `datetime.now`, `datetime.now(UTC).isoformat`, `gpu_fields[0].strip`, `gpu_fields[1].strip`, `gpu_fields[2].strip`, `gpu_fields[3].strip`, `gpu_fields[4].strip`, `json.dumps`, `len`, `os.cpu_count`, `output.parent.mkdir`, `output.relative_to`, `output.write_text`, `package_version`, `path.is_file`, `path.relative_to`, `path.relative_to(root).as_posix`, `platform.machine`, `platform.platform`, `platform.release`, `print`, `sorted`, `{'qiskit': ('qiskit',), 'qiskit_aer': ('qiskit-aer',), 'qiskit_ibm_runtime': ('qiskit-ibm-runtime',), 'pyzx': ('pyzx',), 'cudaq': ('cudaq', 'cuda-quantum'), 'numpy': ('numpy',), 'scipy': ('scipy',), 'pandas': ('pandas',), 'scikit_learn': ('scikit-learn',), 'matplotlib': ('matplotlib',), 'pytest': ('pytest',), 'ruff': ('ruff',), 'mypy': ('mypy',)}.items`

## [tools/refresh_graph_v040.py](../tools/refresh_graph_v040.py)

Merge the archived semantic fragment using installed Graphify, then validate.

Run with .mamba/bin/python after .mamba/bin/graphify update .

### `main()` — line 17

Direct call expressions: `(root / 'GRAPHIFY_UPDATE.md').write_text`, `(root / 'artifacts/logs/v040/graph_validation.json').write_text`, `(root / node['source_file']).resolve`, `Path.cwd`, `Path.cwd().resolve`, `RuntimeError`, `all`, `any`, `build_merge`, `datetime.now`, `datetime.now(UTC).isoformat`, `dict`, `graph.read_bytes`, `graph.read_text`, `hashlib.sha256`, `hashlib.sha256(graph.read_bytes()).hexdigest`, `json.dumps`, `json.loads`, `len`, `node.get`, `path.is_file`, `payload.get`, `print`, `semantic.read_text`, `sorted`, `str`, `subprocess.run`, `to_json`, `tuple`, `version`

## [tools/report_v040.py](../tools/report_v040.py)

Render evidence-backed release documents and secret-free run provenance.

### `command(args)` — line 18

Direct call expressions: `result.stdout.strip`, `subprocess.run`

### `main()` — line 23

Direct call expressions: `'\n'.join`, `(data / 'pairwise_ml_summary.json').read_text`, `(data / 'symmetry_compiler_summary.json').write_text`, `(data / 'symmetry_summary.json').read_text`, `(data / 'tn_summary.json').read_text`, `(logs / 'data_integrity.log').read_text`, `(logs / 'pytest.log').read_text`, `(logs / 'pytest.log').read_text().splitlines`, `(root / 'README.md').write_text`, `(root / 'RELEASE_NOTES_v0.4.0.md').write_text`, `(root / 'RESEARCH_RESULTS.md').write_text`, `(root / 'VALIDATION.md').write_text`, `(root / 'artifacts/figures/v040').iterdir`, `(root / 'artifacts/provenance/run_v0.4.0.json').write_text`, `(root / 'config/research_v040.json').read_text`, `(table[metric].symmetry < table[metric].current).sum`, `(table[metric].symmetry == table[metric].current).sum`, `(table[metric].symmetry > table[metric].current).sum`, `bool`, `command`, `data.iterdir`, `datetime.now`, `datetime.now(UTC).isoformat`, `dict`, `fits.query`, `fits.query('num_plaquettes == 5 and x == 2').itertuples`, `int`, `json.dumps`, `json.loads`, `native.pivot`, `next`, `p.is_file`, `p.iterrows`, `p.relative_to`, `pd.read_csv`, `platform.platform`, `policies[policies.validation == 'prospective'].set_index`, `print`, `project_path`, `sorted`, `str`, `sym['metrics'].items`, `version`

## [tools/tn_sweep.py](../tools/tn_sweep.py)

Launch each CUDA-Q MPS bond dimension in a fresh process and plot convergence.

### `main()` — line 15

Direct call expressions: `(output / 'data').mkdir`, `(output / 'figures').mkdir`, `(root / args.output).resolve`, `Path.cwd`, `Path.cwd().resolve`, `RuntimeError`, `ValueError`, `argparse.ArgumentParser`, `args.bonds.split`, `args.plaquettes.split`, `axes[0].plot`, `axes[0].set`, `axes[1].plot`, `axes[1].set`, `axis.grid`, `axis.legend`, `axis.set_xscale`, `fig.savefig`, `fig.suptitle`, `float`, `frame.to_csv`, `int`, `json.loads`, `parser.add_argument`, `parser.parse_args`, `pd.DataFrame`, `plt.subplots`, `rows.append`, `str`, `subprocess.run`, `valid.groupby`

## [tools/validate_v040.py](../tools/validate_v040.py)

Reproduce integrity gates and bounded six-strategy controls for v0.4.0.

### `controls(data)` — line 20

Direct call expressions: `(data / 'seed_reproduction.json').write_text`, `circuit_hash`, `compile_candidate`, `count_two_qubit`, `dict`, `json.dumps`, `pd.DataFrame`, `pd.DataFrame(rows).to_csv`, `print`, `range`, `rows.append`, `strang_evolution`, `target_cases`, `verify_native`

### `hardware(data)` — line 62

Direct call expressions: `(data / 'hardware_ready.json').write_text`, `(data / 'hardware_ready.qpy').open`, `build_isa_circuits`, `dict`, `json.dumps`, `len`, `list`, `print`, `qpy.dump`, `range`, `target_cases`

### `audit(data)` — line 99

Direct call expressions: `(data / 'frozen_design.json').read_text`, `(data / 'seed_reproduction.json').read_text`, `(data / f'cudaq_N{n}.json').read_text`, `(pair.teleport_native_2q_count - pair.basic_native_2q_count == pair.delta_native_2q_count).all`, `(raw.groupby('case_family').seed.nunique() == 5).all`, `(raw.groupby('case_family').target_hash.nunique() == 1).all`, `(raw.loc[raw.verification_result, 'verification_error'] <= 1e-10).all`, `(~raw.verification_result).sum`, `assignments.groupby`, `circuit_hash`, `circuit_structure_hash`, `config.read_bytes`, `dict`, `hashlib.sha256`, `hashlib.sha256(config.read_bytes()).hexdigest`, `int`, `json.dumps`, `json.loads`, `len`, `max`, `np.isfinite`, `np.isfinite(raw[['native_2q_count', 'native_2q_depth', 'estimated_duration']].values).all`, `old.drop_duplicates`, `old.drop_duplicates('source_key').itertuples`, `old.verification_result.all`, `pair.case_id.isin`, `pd.read_csv`, `print`, `project_path`, `raw.duplicated`, `raw.duplicated(['case_id', 'strategy']).any`, `raw.groupby`, `raw.groupby('case_family').seed.nunique`, `raw.groupby('case_family').target_hash.nunique`, `raw.verification_result.sum`, `set`, `set(pair.case_id).isdisjoint`, `set(train[column]).isdisjoint`, `strang_evolution`, `tn.num_plaquettes.max`, `tn.query`, `tn.query('num_plaquettes <= 8 and max_bond == 64').observable_error_to_trotter.max`, `tn.saved_statevector.any`

### `main()` — line 185

Direct call expressions: `argparse.ArgumentParser`, `parser.add_argument`, `parser.parse_args`, `project_path`, `{'controls': controls, 'hardware': hardware, 'audit': audit}[args.stage]`
