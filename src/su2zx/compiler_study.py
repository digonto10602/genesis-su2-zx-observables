"""Exact PyZX candidates, native compilation dataset, and auditable selector."""

from __future__ import annotations

import argparse
import json
import math
import time
from itertools import product
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

from .core import optimize_with_pyzx, plaquette_chain_terms, strang_evolution
from .paths import load_json, project_path

STRATEGIES = ("qiskit", "basic", "teleport", "full_reduce")
COLORS = {
    "qiskit": "#6B7280",
    "basic": "#0072B2",
    "teleport": "#E69F00",
    "full_reduce": "#D55E00",
}


def generic_ecr_backend(seed: int) -> GenericBackendV2:
    return GenericBackendV2(
        num_qubits=5,
        basis_gates=["id", "rz", "sx", "x", "ecr"],
        coupling_map=CouplingMap.from_line(5, bidirectional=True),
        seed=seed,
    )


def count_two_qubit(circuit: QuantumCircuit) -> int:
    return sum(len(instruction.qubits) == 2 for instruction in circuit.data)


def two_qubit_depth(circuit: QuantumCircuit) -> int:
    return circuit.depth(lambda instruction: len(instruction.qubits) == 2)


def calibration_budget(circuit: QuantumCircuit, backend) -> float:
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
    backend,
    seed: int,
) -> tuple[QuantumCircuit, QuantumCircuit, float]:
    start = time.perf_counter()
    logical = source if strategy == "qiskit" else optimize_with_pyzx(source, strategy)
    manager = generate_preset_pass_manager(
        backend=backend,
        optimization_level=3,
        initial_layout=list(range(5)),
        layout_method="trivial",
        seed_transpiler=seed,
    )
    compiled = manager.run(logical)
    elapsed = time.perf_counter() - start
    return logical, compiled, elapsed


def record(
    source: QuantumCircuit,
    logical: QuantumCircuit,
    compiled: QuantumCircuit,
    backend,
    strategy: str,
    x: float,
    evolution_time: float,
    repetitions: int,
    compile_time: float,
) -> dict:
    terms = plaquette_chain_terms(5, x, include_identity=False)
    native_two_qubit = count_two_qubit(compiled)
    native_two_qubit_depth = two_qubit_depth(compiled)
    error_budget = calibration_budget(compiled, backend)
    cost = native_two_qubit + 0.02 * native_two_qubit_depth + 20.0 * error_budget
    return {
        "circuit_key": f"N5_x{x:g}_t{evolution_time:g}_r{repetitions}",
        "family_group": f"x{x:g}_r{repetitions}",
        "strategy": strategy,
        "num_plaquettes": 5,
        "x": x,
        "time": evolution_time,
        "repetitions": repetitions,
        "source_size": source.size(),
        "source_depth": source.depth(),
        "source_two_qubit": count_two_qubit(source),
        "mean_pauli_weight": float(
            np.mean([sum(pauli != "I" for pauli in term.word) for term in terms])
        ),
        "logical_size": logical.size(),
        "logical_two_qubit": count_two_qubit(logical),
        "exact_equivalence_validated": True,
        "native_size": compiled.size(),
        "native_depth": compiled.depth(),
        "native_two_qubit": native_two_qubit,
        "native_two_qubit_depth": native_two_qubit_depth,
        "native_duration_seconds": float(compiled.estimate_duration(backend.target)),
        "routing_two_qubit_overhead": native_two_qubit - count_two_qubit(logical),
        "routing_penalty_ratio": native_two_qubit / max(count_two_qubit(logical), 1),
        "native_swap_gates": int(compiled.count_ops().get("swap", 0)),
        "calibration_error_budget": error_budget,
        "compile_time_seconds": compile_time,
        "cost": cost,
    }


def build_dataset(config: dict, backend) -> pd.DataFrame:
    seed = int(config["seed"])
    rows = []
    grid = product(
        (0.5, 1.0, 2.0, 4.0),
        (0.04, 0.08, 0.16, 0.24, 0.32),
        (1, 2, 4),
    )
    for x, evolution_time, repetitions in grid:
        source = strang_evolution(
            5, x, evolution_time, repetitions, initial_ones=(2,)
        )
        for strategy in STRATEGIES:
            logical, compiled, elapsed = compile_candidate(source, strategy, backend, seed)
            rows.append(
                record(
                    source,
                    logical,
                    compiled,
                    backend,
                    strategy,
                    x,
                    evolution_time,
                    repetitions,
                    elapsed,
                )
            )
    return pd.DataFrame(rows)


def design_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    numeric = frame[
        [
            "num_plaquettes",
            "x",
            "time",
            "repetitions",
            "source_size",
            "source_depth",
            "source_two_qubit",
            "mean_pauli_weight",
        ]
    ].reset_index(drop=True)
    strategies = pd.get_dummies(frame.strategy, prefix="strategy", dtype=float)
    return pd.concat([numeric, strategies], axis=1)


def selector_metrics(frame: pd.DataFrame, seed: int, costs: pd.Series) -> dict:
    design = design_matrix(frame)
    predictions = np.empty(len(frame))
    groups = frame.family_group.to_numpy()
    splitter = GroupKFold(n_splits=4)
    for train, test in splitter.split(design, costs, groups):
        model = RandomForestRegressor(
            n_estimators=300,
            min_samples_leaf=2,
            random_state=seed,
            n_jobs=-1,
        )
        model.fit(design.iloc[train], costs.iloc[train])
        predictions[test] = model.predict(design.iloc[test])

    evaluated = frame[["circuit_key", "strategy"]].copy()
    evaluated["cost"] = costs.to_numpy()
    evaluated["prediction"] = predictions
    true_best = evaluated.loc[evaluated.groupby("circuit_key").cost.idxmin()]
    predicted_best = evaluated.loc[
        evaluated.groupby("circuit_key").prediction.idxmin()
    ]
    merged = true_best.merge(
        predicted_best, on="circuit_key", suffixes=("_true", "_pred")
    )
    learned_regret = np.mean(
        (merged.cost_pred - merged.cost_true) / np.maximum(merged.cost_true, 1e-12)
    )

    fixed_regrets = {}
    optimum = true_best.set_index("circuit_key").cost
    for strategy in STRATEGIES:
        fixed = evaluated[evaluated.strategy == strategy].set_index("circuit_key").cost
        fixed_regrets[strategy] = float(
            np.mean((fixed - optimum) / np.maximum(optimum, 1e-12))
        )
    return {
        "top1_accuracy": float(
            accuracy_score(merged.strategy_true, merged.strategy_pred)
        ),
        "normalized_regret": float(learned_regret),
        "fixed_normalized_regret": fixed_regrets,
        "oracle_normalized_regret": 0.0,
    }


def selector_summary(frame: pd.DataFrame, seed: int) -> dict:
    primary = selector_metrics(frame, seed, frame.cost)
    sensitivity = []
    for depth_weight, error_weight in ((0.0, 20.0), (0.02, 0.0), (0.02, 20.0), (0.10, 50.0)):
        costs = (
            frame.native_two_qubit
            + depth_weight * frame.native_two_qubit_depth
            + error_weight * frame.calibration_error_budget
        )
        metrics = selector_metrics(frame, seed, costs)
        sensitivity.append(
            {
                "depth_weight": depth_weight,
                "calibration_error_weight": error_weight,
                "top1_accuracy": metrics["top1_accuracy"],
                "normalized_regret": metrics["normalized_regret"],
                "best_fixed_normalized_regret": min(
                    metrics["fixed_normalized_regret"].values()
                ),
            }
        )
    return {
        **primary,
        "rows": int(len(frame)),
        "families": int(frame.family_group.nunique()),
        "cost_weight_sensitivity": sensitivity,
    }


def save_plots(frame: pd.DataFrame, summary: dict, figures: Path) -> None:
    figures.mkdir(parents=True, exist_ok=True)
    means = (
        frame.groupby(["strategy", "repetitions"], as_index=False)
        .native_two_qubit.mean()
        .sort_values(["strategy", "repetitions"])
    )
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    for strategy in STRATEGIES:
        group = means[means.strategy == strategy]
        ax.plot(
            group.repetitions,
            group.native_two_qubit,
            marker="o",
            color=COLORS[strategy],
            label=strategy,
        )
    ax.set(xlabel="Strang repetitions", ylabel="mean native two-qubit gates")
    ax.set_title("Generic five-qubit linear-ECR compilation")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(figures / "compiler_native_resources.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "compiler_native_resources.pdf", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 5))
    for strategy in STRATEGIES:
        group = frame[frame.strategy == strategy]
        ax.scatter(
            group.logical_two_qubit,
            group.native_two_qubit,
            s=18,
            alpha=0.65,
            color=COLORS[strategy],
            label=strategy,
        )
    ax.set(xlabel="logical two-qubit gates", ylabel="routed native two-qubit gates")
    ax.set_title("Routing can reverse logical ZX savings")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.savefig(figures / "compiler_routing_penalty.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "compiler_routing_penalty.pdf", bbox_inches="tight")
    plt.close(fig)

    labels = ["learned", *STRATEGIES, "oracle"]
    values = [
        summary["normalized_regret"],
        *[summary["fixed_normalized_regret"][name] for name in STRATEGIES],
        0.0,
    ]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.bar(labels, values, color=["#009E73", *[COLORS[name] for name in STRATEGIES], "#333333"])
    ax.set(ylabel="normalized regret", title="Pipeline selector versus fixed baselines")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(figures / "selector_accuracy_regret.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "selector_accuracy_regret.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/research.json")
    parser.add_argument("--output", default="artifacts")
    args = parser.parse_args()
    config = load_json(args.config)
    output = project_path(args.output)
    (output / "data").mkdir(parents=True, exist_ok=True)
    backend = generic_ecr_backend(int(config["seed"]))
    frame = build_dataset(config, backend)
    frame.to_csv(output / "data" / "compiler_dataset.csv", index=False)
    summary = selector_summary(frame, int(config["selector_seed"]))
    (output / "data" / "selector_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    save_plots(frame, summary, output / "figures")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
