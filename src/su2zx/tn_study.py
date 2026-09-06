"""CPU matrix-product-state validation for SU2ZX v0.3.0."""

from __future__ import annotations

import argparse
import json
import resource
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from .core import (
    exact_state,
    expectation,
    hamiltonian,
    local_occupations,
    probabilities,
    strang_evolution,
    total_variation,
)
from .paths import project_path


def mps_state(circuit, max_bond: int, tolerance: float) -> tuple[np.ndarray, float]:
    """Simulate a circuit with Aer's CPU MPS method and return its statevector."""
    simulator = AerSimulator(
        method="matrix_product_state",
        matrix_product_state_max_bond_dimension=max_bond,
        matrix_product_state_truncation_threshold=tolerance,
    )
    saved = circuit.copy()
    saved.save_statevector()
    start = time.perf_counter()
    result = simulator.run(saved).result()
    elapsed = time.perf_counter() - start
    return np.asarray(result.get_statevector(saved), dtype=complex), elapsed


def generate_tn_data(output: Path) -> tuple[pd.DataFrame, dict]:
    rows = []
    for n in (5, 8, 12):
        source = strang_evolution(
            n,
            2.0,
            0.32,
            2,
            initial_ones=(n // 2,),
            term_ordering="symmetry",
        )
        ideal = np.asarray(Statevector(source).data)
        exact = exact_state(n, 2.0, 0.32, initial_ones=(n // 2,)) if n <= 8 else None
        for bond in (4, 8, 16, 32):
            tolerance = 1e-14
            mps, elapsed = mps_state(source, bond, tolerance)
            fidelity = abs(np.vdot(ideal, mps)) ** 2
            ideal_energy = expectation(ideal, hamiltonian(n, 2.0))
            mps_energy = expectation(mps, hamiltonian(n, 2.0))
            row = {
                "version": "v0.3.0",
                "method": "qiskit_aer_matrix_product_state_cpu",
                "num_plaquettes": n,
                "repetitions": 2,
                "term_ordering": "symmetry",
                "time": 0.32,
                "max_bond_dimension": bond,
                "truncation_tolerance": tolerance,
                "runtime_seconds": elapsed,
                "peak_process_rss_mib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                / 1024.0,
                "norm_error": abs(float(np.vdot(mps, mps).real) - 1.0),
                "state_fidelity_to_ideal_trotter": float(fidelity),
                "tvd_to_ideal_trotter": total_variation(
                    probabilities(mps), probabilities(ideal)
                ),
                "survival_error_to_ideal_trotter": abs(
                    float(probabilities(mps)[1 << (n // 2)])
                    - float(probabilities(ideal)[1 << (n // 2)])
                ),
                "max_occupation_error_to_ideal_trotter": float(
                    np.max(abs(local_occupations(mps, n) - local_occupations(ideal, n)))
                ),
                "energy_error_to_ideal_trotter": abs(mps_energy - ideal_energy),
                "exact_hamiltonian_reference": exact is not None,
                "tvd_to_exact_hamiltonian": float("nan")
                if exact is None
                else total_variation(probabilities(mps), probabilities(exact)),
                "survival_error_to_exact_hamiltonian": float("nan")
                if exact is None
                else abs(
                    float(probabilities(mps)[1 << (n // 2)])
                    - float(probabilities(exact)[1 << (n // 2)])
                ),
                "max_occupation_error_to_exact_hamiltonian": float("nan")
                if exact is None
                else float(
                    np.max(abs(local_occupations(mps, n) - local_occupations(exact, n)))
                ),
                "observable_error": max(
                    abs(mps_energy - ideal_energy),
                    float(np.max(abs(local_occupations(mps, n) - local_occupations(ideal, n)))),
                ),
            }
            rows.append(row)
    frame = pd.DataFrame(rows)
    validated = frame[(frame.num_plaquettes <= 8) & (frame.max_bond_dimension == 32)]
    summary = {
        "version": "v0.3.0",
        "status": "PASS"
        if validated.tvd_to_ideal_trotter.max() < 1e-7
        and validated.energy_error_to_ideal_trotter.max() < 1e-8
        and validated.norm_error.max() < 1e-9
        else "FAILED",
        "backend": "Qiskit Aer matrix_product_state CPU",
        "validated_sizes": [5, 8],
        "exploratory_sizes": [12],
        "validation_bond_dimension": 32,
        "validation_tolerance": 1e-14,
        "max_validated_tvd_to_ideal_trotter": float(validated.tvd_to_ideal_trotter.max()),
        "max_validated_energy_error_to_ideal_trotter": float(
            validated.energy_error_to_ideal_trotter.max()
        ),
        "minimum_validated_state_fidelity_to_ideal_trotter": float(
            validated.state_fidelity_to_ideal_trotter.min()
        ),
        "note": (
            "N=12 is an exploratory ideal-circuit MPS result; no dense exact-Hamiltonian "
            "reference was computed for that size."
        ),
    }
    data = output / "data"
    figures = output / "figures"
    data.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    frame.to_csv(data / "tensor_network_cpu.csv", index=False)
    (data / "tensor_network_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return frame, summary


def save_tn_plot(frame: pd.DataFrame, figures: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for n, group in frame.groupby("num_plaquettes"):
        axes[0].semilogy(
            group.max_bond_dimension,
            np.maximum(group.tvd_to_ideal_trotter, 1e-18),
            marker="o",
            label=f"N={n}",
        )
        axes[1].plot(
            group.max_bond_dimension,
            group.runtime_seconds,
            marker="o",
            label=f"N={n}",
        )
    axes[0].set(xlabel="maximum bond dimension", ylabel="TVD to ideal Trotter")
    axes[1].set(xlabel="maximum bond dimension", ylabel="runtime (s)")
    for axis in axes:
        axis.set_xscale("log", base=2)
        axis.grid(axis="y", alpha=0.25)
        axis.legend(frameon=False)
    fig.suptitle("CPU MPS validation and bounded scaling")
    fig.savefig(figures / "tensor_network_convergence.png", dpi=220, bbox_inches="tight")
    fig.savefig(figures / "tensor_network_convergence.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts")
    args = parser.parse_args()
    output = project_path(args.output)
    frame, summary = generate_tn_data(output)
    save_tn_plot(frame, output / "figures")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
