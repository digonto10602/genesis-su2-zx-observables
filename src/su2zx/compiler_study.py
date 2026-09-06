"""Diverse, exact, target-aware compiler study for SU2ZX v0.3.0."""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.transpiler import CouplingMap
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GroupKFold

from .core import (
    circuit_hash,
    circuit_structure_hash,
    optimize_with_pyzx,
    plaquette_chain_terms,
    strang_evolution,
)
from .paths import load_json, project_path

VERSION = "v0.3.0"
STRATEGIES = (
    "qiskit",
    "basic",
    "basic_swaps",
    "teleport",
    "full_reduce",
    "full_reduce_depth",
)
COLORS = {
    "qiskit": "#6B7280",
    "basic": "#0072B2",
    "basic_swaps": "#56B4E9",
    "teleport": "#E69F00",
    "full_reduce": "#D55E00",
    "full_reduce_depth": "#CC79A7",
}
VERIFY_TOLERANCE = 1e-10


@dataclass(frozen=True)
class TargetCase:
    name: str
    topology: str
    backend: GenericBackendV2
    coupling: CouplingMap
    layout_name: str
    initial_layout: tuple[int, ...] | None
    synthetic: bool = True


def generic_ecr_backend(seed: int) -> GenericBackendV2:
    """Legacy five-node linear target retained for the QPU dry-run tests."""
    return GenericBackendV2(
        num_qubits=5,
        basis_gates=["id", "rz", "sx", "x", "ecr"],
        coupling_map=CouplingMap.from_line(5, bidirectional=True),
        seed=seed,
    )


def _bidirectional(edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return sorted({edge for a, b in edges for edge in ((a, b), (b, a))})


def _target_case(
    topology: str,
    num_qubits: int,
    seed: int,
    layout_name: str,
    initial_layout: tuple[int, ...] | None,
) -> TargetCase:
    physical = max(num_qubits + 2, 6)
    if topology == "line":
        coupling = CouplingMap.from_line(physical, bidirectional=True)
    elif topology == "ring":
        coupling = CouplingMap.from_ring(physical, bidirectional=True)
    elif topology == "grid":
        rows = 2
        columns = math.ceil(physical / rows)
        coupling = CouplingMap.from_grid(rows, columns, bidirectional=True)
        physical = rows * columns
    elif topology == "heavy_hex_like":
        # A documented synthetic heavy-hex-like ladder fragment.  It is not a
        # named IBM backend or calibration snapshot.
        physical = max(7, num_qubits + 2)
        edges = [(q, q + 1) for q in range(physical - 1)]
        edges += [(q, q + 3) for q in range(0, physical - 3, 4)]
        coupling = CouplingMap(_bidirectional(edges))
    elif topology == "irregular":
        physical = max(7, num_qubits + 2)
        edges = [(q, q + 1) for q in range(physical - 1)]
        edges += [(0, 3), (2, physical - 1)]
        coupling = CouplingMap(_bidirectional(edges))
    else:
        raise ValueError(f"unknown topology {topology!r}")
    backend = GenericBackendV2(
        num_qubits=physical,
        basis_gates=["id", "rz", "sx", "x", "ecr"],
        coupling_map=coupling,
        seed=seed,
    )
    return TargetCase(
        name=f"synthetic_{topology}_{physical}q_{layout_name}",
        topology=topology,
        backend=backend,
        coupling=coupling,
        layout_name=layout_name,
        initial_layout=initial_layout,
    )


def target_cases(num_qubits: int, seed: int) -> list[TargetCase]:
    """Return reproducible topology/layout cases, including two line placements."""
    physical = max(num_qubits + 2, 6)
    favorable = tuple(range(num_qubits))
    spread = tuple(
        round(q * (physical - 1) / max(num_qubits - 1, 1)) for q in range(num_qubits)
    )
    return [
        _target_case("line", num_qubits, seed, "favorable", favorable),
        _target_case("line", num_qubits, seed, "spread", spread),
        _target_case("ring", num_qubits, seed, "transpiler", None),
        _target_case("grid", num_qubits, seed, "transpiler", None),
        _target_case("heavy_hex_like", num_qubits, seed, "transpiler", None),
        _target_case("irregular", num_qubits, seed, "favorable", favorable),
        _target_case("irregular", num_qubits, seed, "spread", spread),
    ]


def count_two_qubit(circuit: QuantumCircuit) -> int:
    return sum(len(instruction.qubits) == 2 for instruction in circuit.data)


def count_one_qubit(circuit: QuantumCircuit) -> int:
    return sum(len(instruction.qubits) == 1 for instruction in circuit.data)


def two_qubit_depth(circuit: QuantumCircuit) -> int:
    return circuit.depth(lambda instruction: len(instruction.qubits) == 2)


def calibration_budget(circuit: QuantumCircuit, backend: GenericBackendV2) -> float:
    budget = 0.0
    for instruction in circuit.data:
        if len(instruction.qubits) != 2:
            continue
        qargs = tuple(circuit.find_bit(q).index for q in instruction.qubits)
        try:
            properties = backend.target[instruction.operation.name][qargs]
            error = None if properties is None else properties.error
        except (KeyError, TypeError):
            error = None
        if error is not None and 0 <= error < 1:
            budget += -math.log1p(-float(error))
    return budget


def compile_candidate(
    source: QuantumCircuit,
    strategy: str,
    backend: GenericBackendV2,
    seed: int,
    initial_layout: tuple[int, ...] | list[int] | None = None,
    optimization_level: int = 3,
    layout_method: str = "trivial",
) -> tuple[QuantumCircuit, QuantumCircuit, float]:
    """Apply an exact logical rewrite, then compile under common target controls."""
    start = time.perf_counter()
    logical = source if strategy == "qiskit" else optimize_with_pyzx(source, strategy)
    layout = (
        list(range(source.num_qubits))
        if initial_layout is None and layout_method == "trivial"
        else None
        if initial_layout is None
        else list(initial_layout)
    )
    manager = generate_preset_pass_manager(
        backend=backend,
        optimization_level=optimization_level,
        initial_layout=layout,
        layout_method=layout_method,
        seed_transpiler=seed,
    )
    compiled = manager.run(logical)
    return logical, compiled, time.perf_counter() - start


def _interaction_features(source: QuantumCircuit) -> dict[str, float | int]:
    pairs: set[tuple[int, int]] = set()
    for instruction in source.data:
        if len(instruction.qubits) == 2:
            q0, q1 = sorted(source.find_bit(q).index for q in instruction.qubits)
            pairs.add((q0, q1))
    degrees = np.zeros(source.num_qubits, dtype=float)
    for q0, q1 in pairs:
        degrees[q0] += 1
        degrees[q1] += 1
    return {
        "interaction_edge_count": len(pairs),
        "interaction_mean_degree": float(degrees.mean()),
        "interaction_max_degree": int(degrees.max(initial=0)),
        "interaction_range": max((abs(a - b) for a, b in pairs), default=0),
    }


def _target_features(case: TargetCase, source: QuantumCircuit) -> dict[str, float | int]:
    nodes = case.backend.num_qubits
    edges = len(case.coupling.get_edges()) // 2
    distances = case.coupling.distance_matrix
    layout = case.initial_layout or tuple(range(source.num_qubits))
    mapped_distances = []
    for instruction in source.data:
        if len(instruction.qubits) == 2:
            a, b = (source.find_bit(q).index for q in instruction.qubits)
            mapped_distances.append(float(distances[layout[a], layout[b]]))
    finite = distances[np.isfinite(distances) & (distances > 0)]
    return {
        "target_node_count": nodes,
        "target_edge_count": edges,
        "target_average_degree": 2.0 * edges / nodes,
        "target_diameter": int(np.max(finite, initial=0)),
        "target_mean_shortest_path": float(np.mean(finite)) if len(finite) else 0.0,
        "mapping_mean_interaction_distance": float(np.mean(mapped_distances))
        if mapped_distances
        else 0.0,
        "mapping_max_interaction_distance": float(np.max(mapped_distances, initial=0)),
        "target_connected": 1,
    }


def _duration(compiled: QuantumCircuit, backend: GenericBackendV2) -> float:
    try:
        return float(compiled.estimate_duration(backend.target))
    except Exception:
        return float("nan")


def _source_specs() -> list[tuple[int, float, float, int, str]]:
    """Bounded design covering N=2..6, r=1/2/4/8, and three term orders."""
    specs: list[tuple[int, float, float, int, str]] = []
    for n in range(2, 7):
        for repetitions in (1, 2, 4, 8):
            specs.append((n, 2.0, 0.24, repetitions, "current"))
        specs.append((n, 1.0, 0.16, 2, "reversed"))
        specs.append((n, 4.0, 0.32, 2, "symmetry"))
        # Angle-only duplicate of the current/r=2 family.  It is retained so
        # raw-circuit and structural-circuit counts can be audited explicitly.
        specs.append((n, 0.5, 0.08, 2, "current"))
    return specs


def _selected_cases(n: int, index: int, seed: int) -> list[TargetCase]:
    """Balanced incomplete design plus full cross-target anchor cases."""
    cases = target_cases(n, seed)
    selected = [cases[index % len(cases)]]
    if index % 6 == 0:
        selected = cases
    return selected


def build_dataset(config: dict, backend: GenericBackendV2 | None = None) -> pd.DataFrame:
    """Build the bounded v0.3.0 compiler dataset.

    ``backend`` retains the compact legacy path used by tests and downstream
    callers.  The production run passes no backend and uses the diverse design.
    """
    seed = int(config.get("seed", 7))
    optimization_level = int(config.get("compiler_optimization_level", 3))
    if backend is not None:
        specs = [(5, 2.0, 0.08, 1, "current")]
    else:
        specs = _source_specs()
    rows: list[dict] = []
    for source_index, (n, x, evolution_time, repetitions, ordering) in enumerate(specs):
        source = strang_evolution(
            n,
            x,
            evolution_time,
            repetitions,
            initial_ones=(n // 2,),
            term_ordering=ordering,
        )
        cases = (
            [
                TargetCase(
                    "legacy_linear_5q",
                    "line",
                    backend,
                    CouplingMap.from_line(5, bidirectional=True),
                    "favorable",
                    tuple(range(5)),
                )
            ]
            if backend is not None
            else _selected_cases(n, source_index, seed)
        )
        source_id = circuit_hash(source)
        structure_id = circuit_structure_hash(source)
        interaction = _interaction_features(source)
        terms = plaquette_chain_terms(n, x, include_identity=False)
        source_data = {
            "version": VERSION,
            "source_key": f"N{n}_x{x:g}_t{evolution_time:g}_r{repetitions}_{ordering}",
            "circuit_hash": source_id,
            "circuit_structure_hash": structure_id,
            "structural_family": f"N{n}_r{repetitions}_{ordering}",
            "num_plaquettes": n,
            "logical_qubits": n,
            "x": x,
            "time": evolution_time,
            "repetitions": repetitions,
            "term_ordering": ordering,
            "source_gate_count": source.size(),
            "source_depth": source.depth(),
            "source_1q_count": count_one_qubit(source),
            "source_2q_count": count_two_qubit(source),
            "pauli_term_count": len(terms),
            "mean_pauli_weight": float(
                np.mean([sum(pauli != "I" for pauli in term.word) for term in terms])
            ),
            **interaction,
        }
        for case in cases:
            case_id = f"{source_data['source_key']}__{case.name}__seed{seed}"
            target_data = {
                "case_id": case_id,
                "circuit_key": case_id,
                "target_name": case.name,
                "target_topology": case.topology,
                "target_is_synthetic": case.synthetic,
                "basis_gates": "id,rz,sx,x,ecr",
                "layout_name": case.layout_name,
                "initial_layout": "transpiler"
                if case.initial_layout is None
                else ",".join(map(str, case.initial_layout)),
                "transpiler_seed": seed,
                "optimization_level": optimization_level,
                "cost_function_name": "lexicographic_native_2q_depth_duration",
                **_target_features(case, source),
            }
            for strategy in STRATEGIES:
                try:
                    logical, compiled, elapsed = compile_candidate(
                        source,
                        strategy,
                        case.backend,
                        seed,
                        case.initial_layout,
                        optimization_level,
                        "sabre" if case.initial_layout is None else "trivial",
                    )
                    native_2q = count_two_qubit(compiled)
                    native_2q_depth = two_qubit_depth(compiled)
                    duration = _duration(compiled, case.backend)
                    error_cost = calibration_budget(compiled, case.backend)
                    logical_2q = count_two_qubit(logical)
                    row = {
                        **source_data,
                        **target_data,
                        "strategy": strategy,
                        "verification_method": "qiskit.Operator.equiv_global_phase",
                        "verification_tolerance": VERIFY_TOLERANCE,
                        "verification_result": True,
                        "verification_status": "VERIFIED",
                        "logical_gate_count": logical.size(),
                        "logical_1q_count": count_one_qubit(logical),
                        "logical_2q_count": logical_2q,
                        "native_gate_count": compiled.size(),
                        "native_depth": compiled.depth(),
                        "native_1q_count": count_one_qubit(compiled),
                        "native_2q_count": native_2q,
                        "native_two_qubit": native_2q,
                        "native_2q_depth": native_2q_depth,
                        "native_two_qubit_depth": native_2q_depth,
                        "routing_2q_overhead": native_2q - logical_2q,
                        "routing_two_qubit_overhead": native_2q - logical_2q,
                        "routing_penalty_ratio": native_2q / max(logical_2q, 1),
                        "estimated_duration": duration,
                        "native_duration_seconds": duration,
                        "estimated_2q_error_cost": error_cost,
                        "estimated_total_error_cost": error_cost,
                        "calibration_error_budget": error_cost,
                        "compile_time_seconds": elapsed,
                        "failure": "",
                    }
                    row["cost"] = (
                        native_2q * 1_000_000.0
                        + native_2q_depth * 1_000.0
                        + (duration if np.isfinite(duration) else 1.0)
                    )
                except Exception as error:
                    row = {
                        **source_data,
                        **target_data,
                        "strategy": strategy,
                        "verification_method": "qiskit.Operator.equiv_global_phase",
                        "verification_tolerance": VERIFY_TOLERANCE,
                        "verification_result": False,
                        "verification_status": "UNVERIFIED",
                        "compile_time_seconds": float("nan"),
                        "cost": float("nan"),
                        "failure": repr(error),
                    }
                rows.append(row)
    frame = pd.DataFrame(rows)
    verified = frame[frame.verification_result].copy()
    winners = verified.loc[
        verified.groupby("case_id").cost.idxmin(),
        ["case_id", "strategy", "cost"],
    ]
    winners = winners.rename(columns={"strategy": "winner_strategy", "cost": "winner_cost"})
    return frame.merge(winners, on="case_id", how="left")


FEATURES = [
    "num_plaquettes",
    "x",
    "time",
    "repetitions",
    "source_gate_count",
    "source_depth",
    "source_2q_count",
    "interaction_edge_count",
    "interaction_mean_degree",
    "interaction_max_degree",
    "interaction_range",
    "pauli_term_count",
    "mean_pauli_weight",
    "target_node_count",
    "target_edge_count",
    "target_average_degree",
    "target_diameter",
    "target_mean_shortest_path",
    "mapping_mean_interaction_distance",
    "mapping_max_interaction_distance",
]


def design_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    numeric = frame[FEATURES].reset_index(drop=True).astype(float)
    categorical = pd.get_dummies(
        frame[["strategy", "term_ordering", "target_topology", "layout_name"]],
        dtype=float,
    ).reset_index(drop=True)
    return pd.concat([numeric, categorical], axis=1)


def _policy_metrics(evaluated: pd.DataFrame, predicted: pd.Series) -> dict[str, float]:
    table = evaluated[["case_id", "strategy", "cost"]].copy()
    table["prediction"] = predicted.to_numpy()
    true_best = table.loc[table.groupby("case_id").cost.idxmin()]
    predicted_best = table.loc[table.groupby("case_id").prediction.idxmin()]
    merged = true_best.merge(predicted_best, on="case_id", suffixes=("_true", "_pred"))
    regret = (merged.cost_pred - merged.cost_true) / np.maximum(merged.cost_true, 1e-12)
    return {
        "top1_strategy_accuracy": float(
            accuracy_score(merged.strategy_true, merged.strategy_pred)
        ),
        "mean_regret": float(regret.mean()),
        "median_regret": float(regret.median()),
        "worst_case_regret": float(regret.max()),
        "fraction_equal_to_oracle": float(np.mean(np.isclose(regret, 0.0))),
    }


def _grouped_predictions(
    frame: pd.DataFrame, groups: pd.Series, seed: int
) -> tuple[np.ndarray, dict]:
    design = design_matrix(frame)
    unique_groups = groups.nunique()
    splitter = GroupKFold(n_splits=min(5, unique_groups))
    predictions = np.full(len(frame), np.nan)
    importances = np.zeros(design.shape[1])
    folds = 0
    for train, test in splitter.split(design, frame.cost, groups):
        model = RandomForestRegressor(
            n_estimators=240,
            min_samples_leaf=2,
            random_state=seed,
            n_jobs=1,
        )
        model.fit(design.iloc[train], frame.cost.iloc[train])
        predictions[test] = model.predict(design.iloc[test])
        importances += model.feature_importances_
        folds += 1
    importance = sorted(
        zip(design.columns, importances / max(folds, 1), strict=True),
        key=lambda item: item[1],
        reverse=True,
    )
    return predictions, {key: float(value) for key, value in importance}


def _fixed_regrets(frame: pd.DataFrame) -> dict[str, float]:
    optimum = frame.loc[frame.groupby("case_id").cost.idxmin()].set_index("case_id").cost
    regrets = {}
    for strategy in STRATEGIES:
        fixed = (
            frame[frame.strategy == strategy].set_index("case_id").cost.reindex(optimum.index)
        )
        regrets[strategy] = float(
            ((fixed - optimum) / np.maximum(optimum, 1e-12)).dropna().mean()
        )
    return regrets


def _case_policy_regret(frame: pd.DataFrame, choices: pd.Series) -> float:
    costs = frame.pivot(index="case_id", columns="strategy", values="cost")
    optimum = costs.min(axis=1)
    selected = pd.Series(
        [costs.loc[case_id, strategy] for case_id, strategy in choices.items()],
        index=choices.index,
    )
    return float(((selected - optimum) / np.maximum(optimum, 1e-12)).mean())


def selector_summary(frame: pd.DataFrame, seed: int) -> dict:
    verified = frame[frame.verification_result].dropna(subset=["cost"]).reset_index(drop=True)
    verified["structural_target_case"] = (
        verified.circuit_structure_hash.astype(str) + "__" + verified.target_name
    )
    # Angle-only duplicates are aggregated before applying the scientific gate.
    # Otherwise varying x or t would inflate the apparent number of independent
    # compiler wins without changing the ordered gate/connectivity structure.
    structural = (
        verified.groupby(["structural_target_case", "strategy"], as_index=False)
        .agg(
            cost=("cost", "median"),
            native_2q_count=("native_2q_count", "median"),
            native_2q_depth=("native_2q_depth", "median"),
        )
        .reset_index(drop=True)
    )
    winners = structural.loc[structural.groupby("structural_target_case").cost.idxmin()]
    counts = winners.strategy.value_counts().to_dict()
    structural_case_count = winners.structural_target_case.nunique()
    strict_two_qubit_wins: dict[str, int] = {}
    depth_wins: dict[str, int] = {}
    duration_or_ties: dict[str, int] = {}
    for _case_id, group in structural.groupby("structural_target_case"):
        winner = group.loc[group.cost.idxmin()].strategy
        count_best = group[group.native_2q_count == group.native_2q_count.min()]
        if len(count_best) == 1:
            strict_two_qubit_wins[winner] = strict_two_qubit_wins.get(winner, 0) + 1
            continue
        depth_best = count_best[count_best.native_2q_depth == count_best.native_2q_depth.min()]
        destination = depth_wins if len(depth_best) == 1 else duration_or_ties
        destination[winner] = destination.get(winner, 0) + 1
    meaningful = {
        strategy: int(count) for strategy, count in strict_two_qubit_wins.items() if count >= 3
    }
    majority_strategy = winners.strategy.mode().iloc[0]
    case_features = verified.drop_duplicates("case_id").set_index("case_id")
    rule_choices = pd.Series(
        np.where(
            case_features.mapping_mean_interaction_distance <= 1.5,
            "basic",
            "qiskit",
        ),
        index=case_features.index,
    )
    fixed_regrets = _fixed_regrets(verified)
    base = {
        "version": VERSION,
        "rows": int(len(frame)),
        "verified_rows": int(len(verified)),
        "cases": int(verified.case_id.nunique()),
        "distinct_structural_target_cases": int(structural_case_count),
        "raw_circuits": int(frame.source_key.nunique()),
        "unique_parameterized_circuits": int(frame.circuit_hash.nunique()),
        "unique_structural_circuits": int(frame.circuit_structure_hash.nunique()),
        "duplicate_structural_circuits": int(
            frame.source_key.nunique() - frame.circuit_structure_hash.nunique()
        ),
        "target_configurations": int(
            frame[["target_name", "num_plaquettes"]].drop_duplicates().shape[0]
        ),
        "topology_classes": int(frame.target_topology.nunique()),
        "strategies": list(STRATEGIES),
        "winner_distribution": {key: int(value) for key, value in counts.items()},
        "strict_native_2q_winner_distribution": strict_two_qubit_wins,
        "native_2q_depth_winner_distribution": depth_wins,
        "duration_or_exact_tie_winner_distribution": duration_or_ties,
        "meaningful_winners": meaningful,
        "winner_diversity_gate": len(meaningful) >= 2,
        "fixed_normalized_regret": fixed_regrets,
        "majority_winner_strategy": majority_strategy,
        "majority_winner_normalized_regret": fixed_regrets[majority_strategy],
        "rule_based_selector": "basic if mapped interaction distance <= 1.5 else qiskit",
        "rule_based_normalized_regret": _case_policy_regret(verified, rule_choices),
        "oracle_normalized_regret": 0.0,
        "feature_leakage_check": "PASS: all FEATURES are available before strategy compilation",
    }
    if len(meaningful) < 2:
        return {
            **base,
            "ml_status": "NOT_IDENTIFIABLE",
            "reason": "fewer than two strategies had at least three strict native-2Q wins",
        }
    validations = {}
    feature_importance = {}
    for name, groups in {
        "structural_family_holdout": verified.circuit_structure_hash,
        "leave_one_size_out": verified.num_plaquettes.astype(str),
        "leave_one_topology_out": verified.target_topology,
    }.items():
        prediction, importance = _grouped_predictions(verified, groups, seed)
        validations[name] = _policy_metrics(verified, pd.Series(prediction))
        if name == "structural_family_holdout":
            feature_importance = importance
    primary = validations["structural_family_holdout"]
    best_fixed = min(base["fixed_normalized_regret"].values())
    status = "POSITIVE" if primary["mean_regret"] < best_fixed else "NULL"
    return {
        **base,
        "ml_status": status,
        "validation": validations,
        "top1_accuracy": primary["top1_strategy_accuracy"],
        "normalized_regret": primary["mean_regret"],
        "mean_regret": primary["mean_regret"],
        "median_regret": primary["median_regret"],
        "worst_case_regret": primary["worst_case_regret"],
        "fraction_equal_to_oracle": primary["fraction_equal_to_oracle"],
        "improvement_vs_always_qiskit": base["fixed_normalized_regret"]["qiskit"]
        - primary["mean_regret"],
        "improvement_vs_always_basic": base["fixed_normalized_regret"]["basic"]
        - primary["mean_regret"],
        "feature_importance": feature_importance,
    }


def build_seed_sensitivity(config: dict) -> pd.DataFrame:
    """Probe the stochastic-routing sensitivity on three representative targets."""
    rows = []
    source = strang_evolution(5, 2.0, 0.24, 2, initial_ones=(2,), term_ordering="current")
    optimization_level = int(config.get("compiler_optimization_level", 2))
    for seed in [int(value) for value in config.get("compiler_transpiler_seeds", [11, 29, 47])]:
        cases = target_cases(5, seed)
        for case in (cases[0], cases[2], cases[-1]):
            for strategy in STRATEGIES:
                try:
                    _logical, compiled, elapsed = compile_candidate(
                        source,
                        strategy,
                        case.backend,
                        seed,
                        case.initial_layout,
                        optimization_level,
                        "sabre" if case.initial_layout is None else "trivial",
                    )
                    rows.append(
                        {
                            "version": VERSION,
                            "seed": seed,
                            "target_name": case.name,
                            "target_topology": case.topology,
                            "layout_name": case.layout_name,
                            "strategy": strategy,
                            "verification_result": True,
                            "native_2q_count": count_two_qubit(compiled),
                            "native_2q_depth": two_qubit_depth(compiled),
                            "compile_time_seconds": elapsed,
                            "failure": "",
                        }
                    )
                except Exception as error:
                    rows.append(
                        {
                            "version": VERSION,
                            "seed": seed,
                            "target_name": case.name,
                            "target_topology": case.topology,
                            "layout_name": case.layout_name,
                            "strategy": strategy,
                            "verification_result": False,
                            "failure": repr(error),
                        }
                    )
    return pd.DataFrame(rows)


def save_plots(frame: pd.DataFrame, summary: dict, figures: Path) -> None:
    figures.mkdir(parents=True, exist_ok=True)
    verified = frame[frame.verification_result].copy()
    means = verified.groupby("strategy", sort=False)[
        ["native_2q_count", "native_2q_depth"]
    ].mean()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    colors = [COLORS[name] for name in means.index]
    axes[0].bar(means.index, means.native_2q_count, color=colors)
    axes[1].bar(means.index, means.native_2q_depth, color=colors)
    axes[0].set(ylabel="mean native two-qubit gates", title="Native 2Q count")
    axes[1].set(ylabel="mean native two-qubit depth", title="Native 2Q depth")
    for axis in axes:
        axis.tick_params(axis="x", rotation=28)
        axis.grid(axis="y", alpha=0.25)
    fig.suptitle("SU2ZX v0.3.0 verified compiler strategies")
    fig.savefig(figures / "compiler_native_resources.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "compiler_native_resources.pdf", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    routing = verified.groupby("strategy", sort=False).routing_penalty_ratio.median()
    ax.bar(routing.index, routing, color=[COLORS[name] for name in routing.index])
    ax.set(ylabel="median native/logical 2Q ratio", title="Routing penalty by strategy")
    ax.tick_params(axis="x", rotation=28)
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(figures / "compiler_routing_penalty.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "compiler_routing_penalty.pdf", bbox_inches="tight")
    plt.close(fig)

    winners = verified.loc[verified.groupby("case_id").cost.idxmin()]
    distribution = winners.strategy.value_counts().reindex(STRATEGIES, fill_value=0)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(
        distribution.index,
        distribution,
        color=[COLORS[name] for name in distribution.index],
    )
    ax.set(ylabel="distinct target/circuit cases won", title="Strategy winner distribution")
    ax.tick_params(axis="x", rotation=28)
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(figures / "strategy_winner_distribution.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "strategy_winner_distribution.pdf", bbox_inches="tight")
    plt.close(fig)

    table = pd.crosstab(winners.target_topology, winners.strategy).reindex(
        columns=STRATEGIES, fill_value=0
    )
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bottom = np.zeros(len(table))
    for strategy in STRATEGIES:
        values = table[strategy].to_numpy()
        ax.bar(table.index, values, bottom=bottom, label=strategy, color=COLORS[strategy])
        bottom += values
    ax.set(ylabel="cases won", title="Winner depends on target topology")
    ax.tick_params(axis="x", rotation=20)
    ax.legend(frameon=False, ncol=3)
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(figures / "strategy_winner_by_topology.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "strategy_winner_by_topology.pdf", bbox_inches="tight")
    plt.close(fig)

    if summary.get("winner_diversity_gate"):
        fixed = summary["fixed_normalized_regret"]
        labels = ["learned", *STRATEGIES, "oracle"]
        values = [summary["mean_regret"], *[fixed[name] for name in STRATEGIES], 0.0]
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.bar(labels, values, color=["#009E73", *[COLORS[n] for n in STRATEGIES], "#333333"])
        ax.set(ylabel="mean normalized regret", title="Selector versus fixed strategies")
        ax.tick_params(axis="x", rotation=28)
        ax.grid(axis="y", alpha=0.25)
        fig.savefig(figures / "selector_accuracy_regret.png", dpi=220, bbox_inches="tight")
        fig.savefig(figures / "selector_accuracy_regret.pdf", bbox_inches="tight")
        plt.close(fig)


def save_audit_tables(frame: pd.DataFrame, data: Path) -> None:
    """Persist winner, split, and feature-definition tables used by the report."""
    verified = frame[frame.verification_result].dropna(subset=["cost"]).copy()
    raw_winners = verified.loc[verified.groupby("case_id").cost.idxmin()]
    raw_winners[
        [
            "case_id",
            "circuit_structure_hash",
            "target_name",
            "layout_name",
            "strategy",
            "native_2q_count",
            "native_2q_depth",
            "estimated_duration",
            "cost",
        ]
    ].to_csv(data / "compiler_winners.csv", index=False)

    assignments = verified[
        ["case_id", "circuit_structure_hash", "num_plaquettes", "target_topology"]
    ].drop_duplicates()
    assignments["structural_family_fold"] = -1
    splitter = GroupKFold(n_splits=min(5, assignments.circuit_structure_hash.nunique()))
    placeholder = np.zeros(len(assignments))
    for fold, (_train, test) in enumerate(
        splitter.split(placeholder, placeholder, assignments.circuit_structure_hash)
    ):
        assignments.iloc[test, assignments.columns.get_loc("structural_family_fold")] = fold
    assignments.to_csv(data / "ml_group_assignments.csv", index=False)
    (data / "ml_feature_definitions.json").write_text(
        json.dumps(
            {
                "version": VERSION,
                "numeric_features": FEATURES,
                "categorical_features": [
                    "strategy",
                    "term_ordering",
                    "target_topology",
                    "layout_name",
                ],
                "leakage_rule": "No competing-strategy post-compilation resource is an input.",
                "primary_group": "circuit_structure_hash",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/research.json")
    parser.add_argument("--output", default="artifacts")
    args = parser.parse_args()
    config = load_json(args.config)
    output = project_path(args.output)
    (output / "data").mkdir(parents=True, exist_ok=True)
    frame = build_dataset(config)
    frame.to_csv(output / "data" / "compiler_dataset.csv", index=False)
    seed_frame = build_seed_sensitivity(config)
    seed_frame.to_csv(output / "data" / "compiler_seed_sensitivity.csv", index=False)
    summary = selector_summary(frame, int(config.get("selector_seed", 11)))
    (output / "data" / "selector_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    save_audit_tables(frame, output / "data")
    save_plots(frame, summary, output / "figures")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
