"""Analyze raw and M3-mitigated IBM data against the ideal Trotter circuit."""

from __future__ import annotations

import argparse
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .core import (
    circuit_state,
    diagonal_pauli_expectation,
    normalized_counts,
    project_to_probability_simplex,
    reconstruct_energy,
    strang_evolution,
    total_variation,
)
from .paths import project_path


def complete(distribution, num_qubits: int = 5) -> dict[str, float]:
    return {
        format(index, f"0{num_qubits}b"): float(
            distribution.get(format(index, f"0{num_qubits}b"), 0.0)
        )
        for index in range(2**num_qubits)
    }


def paired_interval(values, samples: int = 20_000, seed: int = 29) -> list[float]:
    data = np.asarray(values, dtype=float)
    generator = np.random.default_rng(seed)
    means = generator.choice(data, size=(samples, len(data)), replace=True).mean(axis=1)
    return [float(value) for value in np.quantile(means, [0.025, 0.975])]


def analyze(payload: dict) -> pd.DataFrame:
    records = {}
    for index, metadata in enumerate(payload["submission_order"]):
        key = (metadata["variant"], float(metadata["time"]), metadata["basis"])
        records[key] = {
            "raw": complete(normalized_counts(payload["raw_counts"][index])),
            "m3_quasi": complete(payload["m3_quasiprobabilities"][index]),
        }

    rows = []
    for variant in ("qiskit", "basic"):
        for time in sorted({key[1] for key in records}):
            state = circuit_state(
                strang_evolution(
                    5, 2.0, time, payload["repetitions"], initial_ones=(2,)
                )
            )
            reference = {
                format(index, "05b"): float(value)
                for index, value in enumerate(np.abs(state) ** 2)
            }
            for treatment in ("raw", "m3_quasi"):
                distributions = {
                    basis: records[(variant, time, basis)][treatment]
                    for basis in ("Z", "X0", "X1", "X2", "X3", "X4")
                }
                metric_distribution = distributions["Z"]
                if treatment == "m3_quasi":
                    metric_distribution = project_to_probability_simplex(
                        metric_distribution
                    )
                occupations = [
                    (
                        1.0
                        - diagonal_pauli_expectation(distributions["Z"], [qubit])
                    )
                    / 2.0
                    for qubit in range(5)
                ]
                rows.append(
                    {
                        "variant": variant,
                        "time": time,
                        "treatment": treatment,
                        "tvd_to_exact_trotter": total_variation(
                            list(metric_distribution.values()), list(reference.values())
                        ),
                        "energy": reconstruct_energy(distributions, 5, 2.0),
                        "survival": metric_distribution["00100"],
                        "mirror_asymmetry": (
                            abs(occupations[0] - occupations[4])
                            + abs(occupations[1] - occupations[3])
                        )
                        / 2.0,
                        **{
                            f"occupation_{qubit}": occupations[qubit]
                            for qubit in range(5)
                        },
                    }
                )
    return pd.DataFrame(rows)


def summarize(frame: pd.DataFrame) -> dict:
    output = {}
    for treatment in ("raw", "m3_quasi"):
        subset = frame[(frame.treatment == treatment) & (frame.time > 0)]
        pivot = subset.pivot(
            index="time", columns="variant", values="tvd_to_exact_trotter"
        )
        differences = (pivot.basic - pivot.qiskit).to_numpy()
        output[treatment] = {
            "mean_tvd_qiskit": float(pivot.qiskit.mean()),
            "mean_tvd_basic": float(pivot.basic.mean()),
            "paired_delta_basic_minus_qiskit": float(differences.mean()),
            "paired_bootstrap_95_percent": paired_interval(differences),
        }
    return output


def plots(frame: pd.DataFrame, figures) -> None:
    figures.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for axis, treatment in zip(axes, ("raw", "m3_quasi"), strict=True):
        for variant, group in frame[frame.treatment == treatment].groupby("variant"):
            axis.plot(group.time, group.tvd_to_exact_trotter, marker="o", label=variant)
        axis.set(title=treatment, xlabel="time", ylabel="TVD to ideal Trotter")
        axis.legend(frameon=False)
        axis.grid(axis="y", alpha=0.25)
    fig.savefig(figures / "hardware_tvd_comparison.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "hardware_tvd_comparison.pdf", bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for variant, group in frame[frame.treatment == "raw"].groupby("variant"):
        axes[0].plot(group.time, group.survival, marker="o", label=variant)
        axes[1].plot(group.time, group.energy, marker="o", label=variant)
    axes[0].set(title="Raw survival", xlabel="time", ylabel="probability")
    axes[1].set(title="Raw reconstructed energy", xlabel="time", ylabel="energy")
    for axis in axes:
        axis.legend(frameon=False)
        axis.grid(axis="y", alpha=0.25)
    fig.savefig(figures / "hardware_observables.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "hardware_observables.pdf", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    for treatment, group in frame.groupby("treatment"):
        means = group.groupby("variant").tvd_to_exact_trotter.mean()
        ax.plot(means.index, means.values, marker="o", label=treatment)
    ax.set(ylabel="mean TVD", title="Raw versus M3-projected TVD")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(figures / "raw_vs_m3.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "raw_vs_m3.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", default="artifacts")
    args = parser.parse_args()
    payload = json.loads(project_path(args.input).read_text(encoding="utf-8"))
    output = project_path(args.output)
    frame = analyze(payload)
    frame.to_csv(output / "data" / "qpu_observables.csv", index=False)
    (output / "data" / "qpu_summary.json").write_text(
        json.dumps(summarize(frame), indent=2), encoding="utf-8"
    )
    plots(frame, output / "figures")


if __name__ == "__main__":
    main()
