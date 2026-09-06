# ruff: noqa: F821
"""CUDA-Q reference for the same second-order product formula."""

from __future__ import annotations

import argparse
import json
import os

import numpy as np


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        choices=("qpp-cpu", "nvidia", "tensornet", "tensornet-mps"),
        default="qpp-cpu",
    )
    parser.add_argument("--plaquettes", type=int, default=5)
    parser.add_argument("--x", type=float, default=2.0)
    parser.add_argument("--time", type=float, default=0.32)
    parser.add_argument("--repetitions", type=int, default=2)
    parser.add_argument("--shots", type=int, default=10_000)
    parser.add_argument("--max-bond", type=int, default=64)
    return parser.parse_args()


ARGS = arguments()
if ARGS.target == "tensornet-mps":
    os.environ["CUDAQ_MPS_MAX_BOND"] = str(ARGS.max_bond)
    os.environ["CUDAQ_MPS_ABS_CUTOFF"] = "1e-10"
    os.environ["CUDAQ_MPS_RELATIVE_CUTOFF"] = "1e-10"

import cudaq  # noqa: E402

from su2zx.core import (  # noqa: E402
    circuit_state,
    expectation,
    hamiltonian,
    plaquette_chain_terms,
    probabilities,
    strang_evolution,
    total_variation,
)


@cudaq.kernel
def evolve(
    coefficients: list[float],
    words: list[cudaq.pauli_word],
    num_qubits: int,
    repetitions: int,
    evolution_time: float,
    initial_qubit: int,
):
    qubits = cudaq.qvector(num_qubits)
    x(qubits[initial_qubit])
    dt = evolution_time / repetitions
    for _ in range(repetitions):
        for index in range(len(coefficients)):
            # CUDA-Q exp_pauli(theta,P) = exp(+i theta P).
            exp_pauli(-coefficients[index] * dt / 2.0, qubits, words[index])
        for offset in range(len(coefficients)):
            index = len(coefficients) - 1 - offset
            exp_pauli(-coefficients[index] * dt / 2.0, qubits, words[index])


@cudaq.kernel
def evolve_and_measure(
    coefficients: list[float],
    words: list[cudaq.pauli_word],
    num_qubits: int,
    repetitions: int,
    evolution_time: float,
    initial_qubit: int,
):
    qubits = cudaq.qvector(num_qubits)
    x(qubits[initial_qubit])
    dt = evolution_time / repetitions
    for _ in range(repetitions):
        for index in range(len(coefficients)):
            exp_pauli(-coefficients[index] * dt / 2.0, qubits, words[index])
        for offset in range(len(coefficients)):
            index = len(coefficients) - 1 - offset
            exp_pauli(-coefficients[index] * dt / 2.0, qubits, words[index])
    mz(qubits)


def cudaq_hamiltonian(num_plaquettes: int, x_value: float):
    operator = 0.0 * cudaq.spin.i(0)
    for term in plaquette_chain_terms(num_plaquettes, x_value, include_identity=True):
        factors = []
        for qubit, pauli in enumerate(term.word[::-1]):
            if pauli == "X":
                factors.append(cudaq.spin.x(qubit))
            elif pauli == "Y":
                factors.append(cudaq.spin.y(qubit))
            elif pauli == "Z":
                factors.append(cudaq.spin.z(qubit))
        product = cudaq.spin.i(0) if not factors else factors[0]
        for factor in factors[1:]:
            product *= factor
        operator += term.coefficient * product
    return operator


def main() -> None:
    cudaq.set_random_seed(17)
    cudaq.set_target(ARGS.target)
    terms = plaquette_chain_terms(ARGS.plaquettes, ARGS.x, include_identity=False)
    coefficients = [term.coefficient for term in terms]
    words = [cudaq.pauli_word(term.word[::-1]) for term in terms]
    call = (
        coefficients,
        words,
        ARGS.plaquettes,
        ARGS.repetitions,
        ARGS.time,
        ARGS.plaquettes // 2,
    )
    energy = cudaq.observe(
        evolve, cudaq_hamiltonian(ARGS.plaquettes, ARGS.x), *call
    ).expectation()
    cudaq_state = np.asarray(cudaq.get_state(evolve, *call), dtype=complex)
    qiskit_circuit = strang_evolution(
        ARGS.plaquettes,
        ARGS.x,
        ARGS.time,
        ARGS.repetitions,
        initial_ones=(ARGS.plaquettes // 2,),
    )
    qiskit_state = circuit_state(qiskit_circuit)
    qiskit_energy = expectation(qiskit_state, hamiltonian(ARGS.plaquettes, ARGS.x))
    probability_tvd = total_variation(probabilities(cudaq_state), probabilities(qiskit_state))
    survival = float(probabilities(cudaq_state)[1 << (ARGS.plaquettes // 2)])
    print(
        json.dumps(
            {
                "target": ARGS.target,
                "plaquettes": ARGS.plaquettes,
                "x": ARGS.x,
                "time": ARGS.time,
                "repetitions": ARGS.repetitions,
                "max_bond": ARGS.max_bond if ARGS.target == "tensornet-mps" else None,
                "energy": float(energy.real),
                "qiskit_energy": qiskit_energy,
                "absolute_energy_error": abs(float(energy.real) - qiskit_energy),
                "survival_probability": survival,
                "probability_tvd_to_qiskit": probability_tvd,
                "state_norm_error": abs(float(np.vdot(cudaq_state, cudaq_state).real) - 1.0),
                "shots": 0,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
