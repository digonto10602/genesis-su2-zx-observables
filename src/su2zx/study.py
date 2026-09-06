"""Generate exact/Trotter observables, distributions, and physics plots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .core import (
    circuit_state,
    expectation,
    hamiltonian,
    hamiltonian_components,
    ideal_measurement_distributions,
    initial_state,
    local_occupations,
    probabilities,
    reconstruct_energy,
    strang_evolution,
    total_variation,
)
from .paths import load_json, project_path

COLORS = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00"]


def configure_plotting() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
            "savefig.bbox": "tight",
        }
    )


def save_figure(fig: plt.Figure, figures: Path, name: str) -> None:
    fig.savefig(figures / f"{name}.png", dpi=220)
    fig.savefig(figures / f"{name}.pdf")
    plt.close(fig)


def exact_states(
    num_qubits: int,
    x: float,
    times: np.ndarray,
    initial_ones: list[int],
) -> list[np.ndarray]:
    matrix = hamiltonian(num_qubits, x).to_matrix()
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    initial = initial_state(num_qubits, initial_ones)
    coefficients = eigenvectors.conj().T @ initial
    return [eigenvectors @ (np.exp(-1j * eigenvalues * time) * coefficients) for time in times]


def state_row(
    method: str,
    time: float,
    state: np.ndarray,
    reference: np.ndarray,
    electric,
    magnetic,
) -> dict[str, float | str]:
    occupations = local_occupations(state, 5)
    electric_energy = expectation(state, electric)
    magnetic_energy = expectation(state, magnetic)
    return {
        "method": method,
        "time": float(time),
        "survival": float(probabilities(state)[1 << 2]),
        "electric_energy": electric_energy,
        "magnetic_energy": magnetic_energy,
        "total_energy": electric_energy + magnetic_energy,
        "tvd_to_exact_hamiltonian": total_variation(
            probabilities(state), probabilities(reference)
        ),
        "mirror_asymmetry": float(
            (abs(occupations[0] - occupations[4]) + abs(occupations[1] - occupations[3])) / 2.0
        ),
        "norm_error": float(abs(np.vdot(state, state).real - 1.0)),
        **{f"occupation_{q}": float(occupations[q]) for q in range(5)},
    }


def generate_data(config: dict, output: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = output / "data"
    data.mkdir(parents=True, exist_ok=True)
    n = int(config["num_plaquettes"])
    x = float(config["x"])
    initial_ones = list(config["initial_ones"])
    repetitions = [int(value) for value in config["trotter_repetitions"]]
    times = np.linspace(
        float(config["time_min"]),
        float(config["time_max"]),
        int(config["time_points"]),
    )

    exact = exact_states(n, x, times, initial_ones)
    electric, magnetic = hamiltonian_components(n, x)
    rows: list[dict] = []
    for time, state in zip(times, exact, strict=True):
        rows.append(state_row("exact", time, state, state, electric, magnetic))
    for r in repetitions:
        for time, reference in zip(times, exact, strict=True):
            circuit = strang_evolution(n, x, float(time), r, initial_ones=initial_ones)
            state = circuit_state(circuit)
            rows.append(state_row(f"strang_r{r}", time, state, reference, electric, magnetic))

    observables = pd.DataFrame(rows)
    observables.to_csv(data / "physics_observables.csv", index=False)

    convergence = []
    for r in repetitions:
        selected = observables[(observables.method == f"strang_r{r}") & (observables.time > 0)]
        convergence.append(
            {
                "repetitions": r,
                "max_tvd": float(selected.tvd_to_exact_hamiltonian.max()),
                "final_tvd": float(selected.iloc[-1].tvd_to_exact_hamiltonian),
            }
        )
    convergence_frame = pd.DataFrame(convergence)
    convergence_frame.to_csv(data / "trotter_convergence.csv", index=False)
    positive = convergence_frame[convergence_frame.max_tvd > 0]
    if len(positive) >= 3:
        x_fit = np.log(positive.repetitions.to_numpy(dtype=float))
        y_fit = np.log(positive.max_tvd.to_numpy(dtype=float))
        slope, intercept = np.polyfit(x_fit, y_fit, 1)
        residual = y_fit - (slope * x_fit + intercept)
        denominator = float(np.sum((x_fit - x_fit.mean()) ** 2))
        slope_error = (
            float(np.sqrt(np.sum(residual**2) / (len(x_fit) - 2) / denominator))
            if len(x_fit) > 2 and denominator > 0
            else float("nan")
        )
        convergence_order = float(-slope)
        convergence_uncertainty = slope_error
    else:
        convergence_order = float("nan")
        convergence_uncertainty = float("nan")

    symmetry_rows: list[dict] = []
    for ordering in ("current", "symmetry"):
        for time, reference in zip(times, exact, strict=True):
            circuit = strang_evolution(
                n,
                x,
                float(time),
                int(config["primary_repetitions"]),
                initial_ones=initial_ones,
                term_ordering=ordering,
            )
            state = circuit_state(circuit)
            row = state_row(ordering, float(time), state, reference, electric, magnetic)
            symmetry_rows.append(
                {
                    "term_ordering": ordering,
                    "time": float(time),
                    "tvd_to_exact_hamiltonian": row["tvd_to_exact_hamiltonian"],
                    "energy_drift": abs(float(row["total_energy"]) - 3.0),
                    "mirror_asymmetry": row["mirror_asymmetry"],
                    "source_gate_count": circuit.size(),
                    "source_depth": circuit.depth(),
                    "source_2q_count": sum(
                        len(instruction.qubits) == 2 for instruction in circuit.data
                    ),
                }
            )
    symmetry_frame = pd.DataFrame(symmetry_rows)
    symmetry_frame.to_csv(data / "symmetry_ordering.csv", index=False)

    probability_rows: list[dict] = []
    reconstruction_rows: list[dict] = []
    hardware_times = [float(value) for value in config["hardware_times"]]
    primary_r = int(config["primary_repetitions"])
    for time in hardware_times:
        exact_state = exact_states(n, x, np.asarray([time]), initial_ones)[0]
        trotter_circuit = strang_evolution(n, x, time, primary_r, initial_ones=initial_ones)
        trotter_state = circuit_state(trotter_circuit)
        for method, state in (("exact", exact_state), (f"strang_r{primary_r}", trotter_state)):
            for index, value in enumerate(probabilities(state)):
                probability_rows.append(
                    {
                        "method": method,
                        "time": time,
                        "bitstring_q4_to_q0": format(index, "05b"),
                        "probability": float(value),
                    }
                )
        distributions = ideal_measurement_distributions(trotter_circuit)
        direct = expectation(trotter_state, hamiltonian(n, x))
        reconstructed = reconstruct_energy(distributions, n, x)
        reconstruction_rows.append(
            {
                "time": time,
                "direct_energy": direct,
                "six_basis_energy": reconstructed,
                "absolute_error": abs(direct - reconstructed),
            }
        )

    probabilities_frame = pd.DataFrame(probability_rows)
    probabilities_frame.to_csv(data / "basis_probabilities.csv", index=False)
    pd.DataFrame(reconstruction_rows).to_csv(
        data / "measurement_reconstruction.csv", index=False
    )
    summary = {
        "initial_energy": float(observables.query("method == 'exact'").iloc[0].total_energy),
        "max_norm_error": float(observables.norm_error.max()),
        "max_six_basis_energy_error": float(
            max(row["absolute_error"] for row in reconstruction_rows)
        ),
        "trotter_convergence_fit": {
            "error_metric": "maximum TVD over sampled nonzero times",
            "fit": "ordinary least squares of log(error) on log(repetitions)",
            "order_p": convergence_order,
            "slope_standard_error": convergence_uncertainty,
            "repetitions": repetitions,
        },
        "symmetry_ordering": {
            ordering: {
                "max_tvd": float(group.tvd_to_exact_hamiltonian.max()),
                "max_energy_drift": float(group.energy_drift.max()),
                "max_mirror_asymmetry": float(group.mirror_asymmetry.max()),
            }
            for ordering, group in symmetry_frame.groupby("term_ordering")
        },
    }
    (data / "physics_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return observables, probabilities_frame


def generate_plots(frame: pd.DataFrame, output: Path, primary_r: int) -> None:
    configure_plotting()
    figures = output / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    exact = frame[frame.method == "exact"]
    primary = frame[frame.method == f"strang_r{primary_r}"]

    fig, ax = plt.subplots(figsize=(8, 4.3))
    for q, color in enumerate(COLORS):
        ax.plot(exact.time, exact[f"occupation_{q}"], color=color, label=f"p={q}")
        ax.plot(primary.time, primary[f"occupation_{q}"], color=color, linestyle="--")
    ax.set(xlabel="dimensionless time t", ylabel="loop occupation", ylim=(-0.02, 1.02))
    ax.set_title(f"Five-plaquette occupations: exact (solid), Strang r={primary_r} (dashed)")
    ax.legend(ncol=5, frameon=False)
    ax.grid(axis="y", alpha=0.25)
    save_figure(fig, figures, "loop_occupations_exact_vs_trotter")

    fig, ax = plt.subplots(figsize=(7, 4))
    for method, group in frame.groupby("method", sort=False):
        style = "-" if method == "exact" else "--"
        ax.plot(group.time, group.survival, style, label=method)
    ax.set(xlabel="dimensionless time t", ylabel="survival probability L(t)")
    ax.set_title("Central-loop survival")
    ax.legend(frameon=False, ncol=2)
    ax.grid(axis="y", alpha=0.25)
    save_figure(fig, figures, "survival_probability")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(exact.time, exact.electric_energy, label="electric")
    axes[0].plot(exact.time, exact.magnetic_energy, label="magnetic")
    axes[0].plot(exact.time, exact.total_energy, label="total", color="black")
    axes[0].set_title("Exact Hamiltonian evolution")
    axes[1].plot(primary.time, primary.electric_energy, label="electric")
    axes[1].plot(primary.time, primary.magnetic_energy, label="magnetic")
    axes[1].plot(primary.time, primary.total_energy, label="total", color="black")
    axes[1].set_title(f"Strang r={primary_r}")
    for ax in axes:
        ax.set(xlabel="dimensionless time t", ylabel="dimensionless energy")
        ax.grid(axis="y", alpha=0.25)
        ax.legend(frameon=False)
    save_figure(fig, figures, "energy_components")

    fig, ax = plt.subplots(figsize=(7, 4))
    for method, group in frame[frame.method != "exact"].groupby("method", sort=False):
        ax.plot(group.time, group.tvd_to_exact_hamiltonian, label=method)
    ax.set(xlabel="dimensionless time t", ylabel="TVD to exact Hamiltonian")
    ax.set_title("Second-order product-formula convergence")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    save_figure(fig, figures, "trotter_tvd_convergence")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.semilogy(exact.time, np.maximum(exact.mirror_asymmetry, 1e-17), label="exact")
    ax.semilogy(
        primary.time,
        np.maximum(primary.mirror_asymmetry, 1e-17),
        label=f"Strang r={primary_r}",
    )
    ax.set(xlabel="dimensionless time t", ylabel="mirror asymmetry")
    ax.set_title("Mirror-symmetry diagnostic")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    save_figure(fig, figures, "mirror_asymmetry")

    symmetry_path = output / "data" / "symmetry_ordering.csv"
    if symmetry_path.exists():
        symmetry = pd.read_csv(symmetry_path)
        fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
        metrics = (
            ("tvd_to_exact_hamiltonian", "TVD to exact Hamiltonian"),
            ("energy_drift", "absolute energy drift"),
            ("mirror_asymmetry", "mirror asymmetry"),
        )
        for ordering, group in symmetry.groupby("term_ordering", sort=False):
            for axis, (column, ylabel) in zip(axes, metrics, strict=True):
                axis.plot(group.time, group[column], label=ordering)
                axis.set(xlabel="dimensionless time t", ylabel=ylabel)
                axis.grid(axis="y", alpha=0.25)
        axes[0].legend(frameon=False)
        fig.suptitle(f"Term-ordering comparison at Strang r={primary_r}")
        save_figure(fig, figures, "symmetry_aware_ordering")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/research.json")
    parser.add_argument("--output", default="artifacts")
    args = parser.parse_args()
    config = load_json(args.config)
    output = project_path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    frame, _ = generate_data(config, output)
    generate_plots(frame, output, int(config["primary_repetitions"]))
    print(f"wrote {len(frame)} observable rows to {output}")


if __name__ == "__main__":
    main()
