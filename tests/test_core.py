from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from scipy.linalg import expm

from su2zx.core import (
    circuit_hash,
    circuit_state,
    circuit_structure_hash,
    exact_state,
    expectation,
    hamiltonian,
    ideal_measurement_distributions,
    initial_state,
    local_occupations,
    optimize_with_pyzx,
    pauli_rotation,
    pauli_word,
    project_to_probability_simplex,
    reconstruct_energy,
    strang_evolution,
)


def test_one_plaquette_matrix_and_spectrum() -> None:
    matrix = hamiltonian(1, 1.0).to_matrix().real
    np.testing.assert_allclose(matrix, [[0, -2], [-2, 3]], atol=1e-13)
    np.testing.assert_allclose(np.linalg.eigvalsh(matrix), [-1, 4], atol=1e-13)
    values, vectors = np.linalg.eigh(matrix)
    ground = vectors[:, np.argmin(values)]
    expected_ground = np.asarray([2.0, 1.0]) / np.sqrt(5.0)
    np.testing.assert_allclose(abs(np.vdot(ground, expected_ground)), 1.0, atol=1e-13)


def test_one_plaquette_transition_probability() -> None:
    time = 0.37
    state = exact_state(1, 1.0, time)
    analytic = 16.0 / 25.0 * np.sin(2.5 * time) ** 2
    np.testing.assert_allclose(abs(state[1]) ** 2, analytic, atol=1e-12)


def test_two_plaquette_matrix_and_ground_energy() -> None:
    expected = np.asarray(
        [[0, -2, -2, 0], [-2, 3, 0, -1], [-2, 0, 3, -1], [0, -1, -1, 4.5]]
    )
    matrix = hamiltonian(2, 1.0).to_matrix().real
    np.testing.assert_allclose(matrix, expected, atol=1e-13)
    np.testing.assert_allclose(np.linalg.eigvalsh(matrix)[0], -1.789221846776, atol=1e-12)


def test_hamiltonians_are_hermitian() -> None:
    for n in (1, 2, 5):
        matrix = hamiltonian(n, 2.0).to_matrix()
        np.testing.assert_allclose(matrix, matrix.conj().T, atol=1e-13)


def test_state_norms_and_qiskit_little_endian_order() -> None:
    state = initial_state(5, (0, 2))
    assert np.flatnonzero(state).tolist() == [5]
    assert pauli_word(5, {0: "X", 4: "Z"}) == "ZIIIX"
    for n in (1, 2, 5):
        ones = (n // 2,)
        exact = exact_state(n, 2.0, 0.24, initial_ones=ones)
        trotter = circuit_state(strang_evolution(n, 2.0, 0.24, 2, initial_ones=ones))
        np.testing.assert_allclose(np.linalg.norm(exact), 1.0, atol=1e-12)
        np.testing.assert_allclose(np.linalg.norm(trotter), 1.0, atol=1e-12)


def test_manual_pauli_rotation() -> None:
    circuit = QuantumCircuit(2)
    pauli_rotation(circuit, "ZX", 0.23)
    pauli = np.kron(np.asarray([[1, 0], [0, -1]]), np.asarray([[0, 1], [1, 0]]))
    expected = expm(-1j * 0.23 * pauli)
    assert Operator(circuit).equiv(Operator(expected))


def test_trotter_converges_and_preserves_mirror_symmetry() -> None:
    exact = exact_state(5, 2.0, 0.24, initial_ones=(2,))
    states = [
        circuit_state(strang_evolution(5, 2.0, 0.24, r, initial_ones=(2,)))
        for r in (1, 2, 4, 8)
    ]
    # The circuit intentionally omits the Hamiltonian identity term, hence a
    # global phase. Compare phase-insensitive infidelity.
    infidelities = [1 - abs(np.vdot(exact, state)) ** 2 for state in states]
    assert all(left > right for left, right in zip(infidelities, infidelities[1:]))
    occupations = local_occupations(exact, 5)
    np.testing.assert_allclose(occupations, occupations[::-1], atol=1e-12)


def test_six_basis_energy_reconstruction() -> None:
    circuit = strang_evolution(5, 2.0, 0.24, 2, initial_ones=(2,))
    state = circuit_state(circuit)
    direct = expectation(state, hamiltonian(5, 2.0))
    reconstructed = reconstruct_energy(ideal_measurement_distributions(circuit), 5, 2.0)
    np.testing.assert_allclose(reconstructed, direct, atol=1e-10)


def test_simplex_projection() -> None:
    projected = project_to_probability_simplex({"00": 0.8, "01": 0.3, "10": -0.1})
    assert all(value >= 0 for value in projected.values())
    np.testing.assert_allclose(sum(projected.values()), 1.0, atol=1e-13)


def test_pyzx_candidates_are_exact() -> None:
    for n in (2, 5):
        source = strang_evolution(n, 1.0, 0.08, 1)
        for strategy in ("basic", "teleport", "full_reduce"):
            candidate = optimize_with_pyzx(source, strategy)
            assert Operator(source).equiv(Operator(candidate))


def test_structure_hash_normalizes_angles_but_not_gate_order() -> None:
    left = strang_evolution(5, 1.0, 0.08, 2, initial_ones=(2,))
    right = strang_evolution(5, 4.0, 0.32, 2, initial_ones=(2,))
    symmetric = strang_evolution(
        5, 1.0, 0.08, 2, initial_ones=(2,), term_ordering="symmetry"
    )
    assert circuit_hash(left) != circuit_hash(right)
    assert circuit_structure_hash(left) == circuit_structure_hash(right)
    assert circuit_structure_hash(left) != circuit_structure_hash(symmetric)


def test_additional_pyzx_strategies_are_exact() -> None:
    source = strang_evolution(2, 1.0, 0.08, 1)
    for strategy in ("basic_swaps", "full_reduce_depth"):
        assert Operator(source).equiv(Operator(optimize_with_pyzx(source, strategy)))
