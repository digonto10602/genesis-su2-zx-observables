"""Physics, circuits, and observables for the j_max=1/2 SU(2) plaquette chain.

Conventions:
* H_tilde = 2 H / g^2 and x = 2 / g^4.
* Qiskit Pauli labels and bitstrings are q_(N-1) ... q_0.
* Each qubit is one gauge-reduced spatial plaquette-loop degree of freedom.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike
from qiskit import QuantumCircuit, qasm2
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector
from scipy.linalg import expm


@dataclass(frozen=True)
class PauliTerm:
    word: str
    coefficient: float


def pauli_word(num_qubits: int, operations: Mapping[int, str]) -> str:
    """Return a Qiskit-order Pauli word from logical-qubit operations."""
    chars = ["I"] * num_qubits
    for qubit, pauli in operations.items():
        if not 0 <= qubit < num_qubits:
            raise ValueError(f"qubit {qubit} outside [0,{num_qubits})")
        if pauli not in {"I", "X", "Y", "Z"}:
            raise ValueError(f"invalid Pauli {pauli!r}")
        chars[num_qubits - 1 - qubit] = pauli
    return "".join(chars)


def plaquette_chain_terms(
    num_plaquettes: int,
    x: float,
    *,
    include_identity: bool = True,
) -> list[PauliTerm]:
    """Open-chain SU(2) Hamiltonian terms in the minimal truncation."""
    n = num_plaquettes
    if n < 1:
        raise ValueError("num_plaquettes must be positive")

    if n == 1:
        single_terms = [PauliTerm("I", 1.5)] if include_identity else []
        return single_terms + [PauliTerm("Z", -1.5), PauliTerm("X", -2.0 * x)]

    terms: list[PauliTerm] = []
    if include_identity:
        terms.append(PauliTerm("I" * n, 3.0 * (3 * n + 1) / 8.0))

    for q in range(n):
        coefficient = -9.0 / 8.0 if q in (0, n - 1) else -3.0 / 4.0
        terms.append(PauliTerm(pauli_word(n, {q: "Z"}), coefficient))
    for q in range(n - 1):
        terms.append(PauliTerm(pauli_word(n, {q: "Z", q + 1: "Z"}), -3.0 / 8.0))

    terms.extend(
        [
            PauliTerm(pauli_word(n, {0: "X"}), -3.0 * x / 2.0),
            PauliTerm(pauli_word(n, {0: "X", 1: "Z"}), -x / 2.0),
            PauliTerm(pauli_word(n, {n - 1: "X"}), -3.0 * x / 2.0),
            PauliTerm(
                pauli_word(n, {n - 1: "X", n - 2: "Z"}),
                -x / 2.0,
            ),
        ]
    )

    for q in range(1, n - 1):
        terms.extend(
            [
                PauliTerm(pauli_word(n, {q: "X"}), -9.0 * x / 8.0),
                PauliTerm(
                    pauli_word(n, {q: "X", q - 1: "Z"}),
                    -3.0 * x / 8.0,
                ),
                PauliTerm(
                    pauli_word(n, {q: "X", q + 1: "Z"}),
                    -3.0 * x / 8.0,
                ),
                PauliTerm(
                    pauli_word(n, {q: "X", q - 1: "Z", q + 1: "Z"}),
                    -x / 8.0,
                ),
            ]
        )
    return terms


def hamiltonian(num_plaquettes: int, x: float) -> SparsePauliOp:
    terms = plaquette_chain_terms(num_plaquettes, x, include_identity=True)
    return SparsePauliOp.from_list([(term.word, term.coefficient) for term in terms])


def hamiltonian_components(
    num_plaquettes: int, x: float
) -> tuple[SparsePauliOp, SparsePauliOp]:
    """Return electric (I/Z) and magnetic (contains X) operators."""
    terms = plaquette_chain_terms(num_plaquettes, x, include_identity=True)
    electric = [(term.word, term.coefficient) for term in terms if "X" not in term.word]
    magnetic = [(term.word, term.coefficient) for term in terms if "X" in term.word]
    return SparsePauliOp.from_list(electric), SparsePauliOp.from_list(magnetic)


def pauli_rotation(circuit: QuantumCircuit, word: str, theta: float) -> None:
    """Append exp(-i theta P) using basis changes, parity, and Rz."""
    if len(word) != circuit.num_qubits:
        raise ValueError("Pauli word length does not match circuit")

    active: list[int] = []
    for q in range(circuit.num_qubits):
        pauli = word[circuit.num_qubits - 1 - q]
        if pauli == "X":
            circuit.h(q)
        elif pauli == "Y":
            circuit.sdg(q)
            circuit.h(q)
        if pauli != "I":
            active.append(q)

    if not active:
        return

    ladder = list(zip(active, active[1:], strict=False))
    for control, target in ladder:
        circuit.cx(control, target)
    circuit.rz(2.0 * theta, active[-1])
    for control, target in reversed(ladder):
        circuit.cx(control, target)

    for q in range(circuit.num_qubits):
        pauli = word[circuit.num_qubits - 1 - q]
        if pauli == "X":
            circuit.h(q)
        elif pauli == "Y":
            circuit.h(q)
            circuit.s(q)


def ordered_hamiltonian_terms(
    num_plaquettes: int, x: float, ordering: str = "current"
) -> list[PauliTerm]:
    """Return the unchanged Hamiltonian terms in a documented product order.

    ``symmetry`` groups each Pauli word with its spatial reflection.  Members of
    every such orbit commute for this Hamiltonian, so each grouped exponential is
    reflection invariant even though different orbit sums need not commute.
    """
    terms = plaquette_chain_terms(num_plaquettes, x, include_identity=False)
    if ordering == "current":
        return terms
    if ordering == "reversed":
        return list(reversed(terms))
    if ordering != "symmetry":
        raise ValueError(f"unknown term ordering {ordering!r}")

    orbits: dict[str, list[PauliTerm]] = {}
    for term in terms:
        key = min(term.word, term.word[::-1])
        orbits.setdefault(key, []).append(term)
    return [
        term
        for key in sorted(orbits)
        for term in sorted(orbits[key], key=lambda item: item.word)
    ]


def strang_evolution(
    num_plaquettes: int,
    x: float,
    time: float,
    repetitions: int,
    *,
    initial_ones: Sequence[int] = (),
    term_ordering: str = "current",
) -> QuantumCircuit:
    """Second-order product formula for exp(-i H_tilde time)."""
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    circuit = QuantumCircuit(num_plaquettes, name="su2_strang")
    for q in initial_ones:
        circuit.x(q)

    terms = ordered_hamiltonian_terms(num_plaquettes, x, term_ordering)
    dt = time / repetitions
    for _ in range(repetitions):
        for term in terms:
            pauli_rotation(circuit, term.word, term.coefficient * dt / 2.0)
        for term in reversed(terms):
            pauli_rotation(circuit, term.word, term.coefficient * dt / 2.0)

    circuit.metadata = {
        "num_plaquettes": num_plaquettes,
        "x": x,
        "time": time,
        "repetitions": repetitions,
        "initial_ones": list(initial_ones),
        "term_ordering": term_ordering,
    }
    return circuit


def circuit_hash(circuit: QuantumCircuit, *, normalize_parameters: bool = False) -> str:
    """Hash ordered gates/connectivity, optionally discarding continuous angles."""
    instructions = []
    for item in circuit.data:
        params = []
        if not normalize_parameters:
            params = [format(float(value), ".16g") for value in item.operation.params]
        instructions.append(
            {
                "name": item.operation.name,
                "qubits": [circuit.find_bit(qubit).index for qubit in item.qubits],
                "clbits": [circuit.find_bit(bit).index for bit in item.clbits],
                "params": params,
            }
        )
    payload = {
        "num_qubits": circuit.num_qubits,
        "num_clbits": circuit.num_clbits,
        "instructions": instructions,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def circuit_structure_hash(circuit: QuantumCircuit) -> str:
    """Hash gate order and connectivity while normalizing continuous parameters."""
    return circuit_hash(circuit, normalize_parameters=True)


def initial_state(num_qubits: int, initial_ones: Sequence[int]) -> np.ndarray:
    index = sum(1 << q for q in initial_ones)
    state = np.zeros(2**num_qubits, dtype=complex)
    state[index] = 1.0
    return state


def exact_state(
    num_plaquettes: int,
    x: float,
    time: float,
    *,
    initial_ones: Sequence[int] = (),
) -> np.ndarray:
    state = initial_state(num_plaquettes, initial_ones)
    return expm(-1j * hamiltonian(num_plaquettes, x).to_matrix() * time) @ state


def circuit_state(circuit: QuantumCircuit) -> np.ndarray:
    return np.asarray(Statevector(circuit).data)


def expectation(state: np.ndarray, operator: SparsePauliOp) -> float:
    value = np.vdot(state, operator.to_matrix() @ state)
    if abs(value.imag) > 1e-9:
        raise ValueError(f"unexpected imaginary expectation {value.imag}")
    return float(value.real)


def probabilities(state: np.ndarray) -> np.ndarray:
    return np.abs(state) ** 2


def local_occupations(state: np.ndarray, num_qubits: int) -> np.ndarray:
    distribution = probabilities(state)
    return np.asarray(
        [
            sum(weight for index, weight in enumerate(distribution) if (index >> q) & 1)
            for q in range(num_qubits)
        ]
    )


def total_variation(left: ArrayLike, right: ArrayLike) -> float:
    return 0.5 * float(np.abs(np.asarray(left) - np.asarray(right)).sum())


def measurement_circuit(unitary: QuantumCircuit, x_qubit: int | None) -> QuantumCircuit:
    circuit = unitary.copy()
    label = "Z" if x_qubit is None else f"X{x_qubit}"
    if x_qubit is not None:
        circuit.h(x_qubit)
    circuit.measure_all()
    circuit.name = f"{unitary.name}_{label}"
    circuit.metadata = dict(unitary.metadata or {}) | {"measurement_basis": label}
    return circuit


def measurement_family(unitary: QuantumCircuit) -> list[QuantumCircuit]:
    return [measurement_circuit(unitary, None)] + [
        measurement_circuit(unitary, q) for q in range(unitary.num_qubits)
    ]


def normalized_counts(counts: Mapping[str, float]) -> dict[str, float]:
    total = float(sum(counts.values()))
    if total <= 0:
        raise ValueError("counts have non-positive total")
    return {key.replace(" ", ""): float(value) / total for key, value in counts.items()}


def diagonal_pauli_expectation(
    distribution: Mapping[str, float], support: Sequence[int]
) -> float:
    answer = 0.0
    for bitstring, weight in distribution.items():
        clean = bitstring.replace(" ", "")
        eigenvalue = 1
        for q in support:
            eigenvalue *= -1 if clean[-1 - q] == "1" else 1
        answer += float(weight) * eigenvalue
    return answer


def ideal_measurement_distributions(
    unitary: QuantumCircuit,
) -> dict[str, dict[str, float]]:
    """Exact distributions after each of the N+1 basis rotations."""
    output: dict[str, dict[str, float]] = {}
    for x_qubit in [None, *range(unitary.num_qubits)]:
        rotated = unitary.copy()
        label = "Z" if x_qubit is None else f"X{x_qubit}"
        if x_qubit is not None:
            rotated.h(x_qubit)
        probs = probabilities(circuit_state(rotated))
        output[label] = {
            format(index, f"0{unitary.num_qubits}b"): float(value)
            for index, value in enumerate(probs)
        }
    return output


def reconstruct_energy(
    distributions: Mapping[str, Mapping[str, float]],
    num_plaquettes: int,
    x: float,
) -> float:
    energy = 0.0
    for term in plaquette_chain_terms(num_plaquettes, x, include_identity=True):
        support = [q for q in range(num_plaquettes) if term.word[num_plaquettes - 1 - q] != "I"]
        x_support = [q for q in support if term.word[num_plaquettes - 1 - q] == "X"]
        if not support:
            value = 1.0
        else:
            basis = "Z" if not x_support else f"X{x_support[0]}"
            value = diagonal_pauli_expectation(distributions[basis], support)
        energy += term.coefficient * value
    return float(energy)


def project_to_probability_simplex(
    quasiprobabilities: Mapping[str, float],
) -> dict[str, float]:
    keys = list(quasiprobabilities)
    values = np.asarray([quasiprobabilities[key] for key in keys], dtype=float)
    ordered = np.sort(values)[::-1]
    cumulative = np.cumsum(ordered)
    candidates = np.nonzero(ordered * np.arange(1, len(ordered) + 1) > cumulative - 1.0)[0]
    if len(candidates) == 0:
        raise RuntimeError("simplex projection failed")
    rho = int(candidates[-1])
    theta = (cumulative[rho] - 1.0) / (rho + 1)
    projected = np.maximum(values - theta, 0.0)
    return {key: float(value) for key, value in zip(keys, projected, strict=True)}


def optimize_with_pyzx(source: QuantumCircuit, strategy: str) -> QuantumCircuit:
    """Apply a PyZX strategy and reject an inequivalent result."""
    import pyzx as zx

    # The default 2**20 denominator loses ~1e-10 in repeated small angles.
    # Increase only the QASM import precision and restore the library setting.
    denominator = zx.settings.float_to_fraction_max_denominator
    try:
        zx.settings.float_to_fraction_max_denominator = 2**40
        zxc = zx.Circuit.from_qasm(qasm2.dumps(source))
    finally:
        zx.settings.float_to_fraction_max_denominator = denominator
    if strategy == "basic":
        candidate_zx = zx.optimize.basic_optimization(zxc.copy(), do_swaps=False, quiet=True)
    elif strategy == "basic_swaps":
        candidate_zx = zx.optimize.basic_optimization(zxc.copy(), do_swaps=True, quiet=True)
    elif strategy == "teleport":
        graph = zx.simplify.teleport_reduce(zxc.to_graph().copy())
        candidate_zx = zx.Circuit.from_graph(graph).to_basic_gates()
    elif strategy == "full_reduce":
        graph = zxc.to_graph()
        zx.simplify.full_reduce(graph, quiet=True)
        candidate_zx = zx.extract.extract_circuit(
            graph.copy(), up_to_perm=False, quiet=True
        ).to_basic_gates()
    elif strategy == "full_reduce_depth":
        graph = zxc.to_graph()
        zx.simplify.full_reduce(graph, quiet=True)
        candidate_zx = zx.extract.lookahead_extract(
            graph.copy(), optimize_for_depth=True, up_to_perm=False
        ).to_basic_gates()
    else:
        raise ValueError(f"unknown PyZX strategy {strategy!r}")

    candidate = qasm2.loads(candidate_zx.to_qasm())
    candidate.metadata = dict(source.metadata or {}) | {"zx_strategy": strategy}
    if not Operator(source).equiv(Operator(candidate), atol=1e-10, rtol=1e-10):
        raise RuntimeError(f"PyZX strategy {strategy} failed exact equivalence")
    return candidate
