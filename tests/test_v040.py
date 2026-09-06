"""Regression gates for routed equivalence, pair integrity and direct MPS."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from su2zx.compiler_study import compile_candidate, target_cases
from su2zx.core import strang_evolution
from su2zx.robust_study import frozen_choices, pairwise, verify_native
from su2zx.scaling_study import direct_mps, observable_operators, symmetric_initial


def test_routed_equivalence_tracks_layout_and_rejects_corruption():
    source = QuantumCircuit(3)
    source.h(0)
    source.cx(0, 2)
    source.ry(0.27, 1)
    case = target_cases(3, 7)[1]
    _, compiled, _ = compile_candidate(
        source, "qiskit", case.backend, 19, case.initial_layout, 1
    )
    assert verify_native(source, compiled) < 1e-10
    corrupt = compiled.copy()
    corrupt.x(compiled.layout.final_index_layout()[1])
    with pytest.raises(RuntimeError, match="routed equivalence failed"):
        verify_native(source, corrupt)


def test_pairwise_excludes_whole_pair_when_one_output_fails():
    rows = []
    for case, verified in [("valid", True), ("invalid", False)]:
        for strategy, cost in [("basic", 10), ("teleport", 8)]:
            rows.append(
                dict(
                    case_id=case,
                    strategy=strategy,
                    verification_result=verified or strategy == "basic",
                    circuit_hash="same",
                    target_hash="fixed",
                    seed=11,
                    physical_qubits="[0,1]",
                    native_2q_count=cost,
                    native_2q_depth=cost,
                    estimated_duration=1e-6,
                )
            )
    result = pairwise(pd.DataFrame(rows))
    assert result.case_id.tolist() == ["valid"]
    assert result.label.tolist() == ["teleport"]
    assert result.delta_native_2q_count.tolist() == [-2]


@pytest.mark.parametrize("n", [5, 8])
def test_direct_mps_observables_do_not_save_dense_state(monkeypatch, n):
    def forbidden(*args, **kwargs):
        raise AssertionError("full statevector save forbidden")

    monkeypatch.setattr(QuantumCircuit, "save_statevector", forbidden)
    source = strang_evolution(
        n, 2.0, 0.32, 2, initial_ones=symmetric_initial(n), term_ordering="symmetry"
    )
    ideal = Statevector(source)
    values, stats = direct_mps(source, 2.0, 64, 1e-14)
    for name, op in observable_operators(n, 2.0).items():
        assert abs(values[name] - ideal.expectation_value(op)) < 1e-7
    assert not stats["saved_statevector"]
    assert stats["observed_max_bond"] <= 64
    assert (
        abs(values["total_energy"] - values["electric_energy"] - values["magnetic_energy"])
        < 1e-10
    )


def test_frozen_rule_boundary_and_order():
    frame = pd.DataFrame(
        dict(
            num_plaquettes=[2, 3, 4, 2],
            term_ordering=["current", "current", "current", "symmetry"],
        )
    )
    assert frozen_choices(
        frame, dict(teleport_max_n=3, teleport_ordering="current")
    ).tolist() == ["teleport", "teleport", "basic", "basic"]


@pytest.mark.parametrize("n", [3, 4])
def test_symmetry_initial_and_evolution_are_reflection_invariant(n):
    source = strang_evolution(
        n, 2.0, 0.32, 2, initial_ones=symmetric_initial(n), term_ordering="symmetry"
    )
    probs = abs(Statevector(source).data) ** 2
    reflected = [int(format(i, f"0{n}b")[::-1], 2) for i in range(2**n)]
    assert np.max(abs(probs - probs[reflected])) < 1e-12


def test_pyzx_import_precision_and_settings_are_preserved():
    import pyzx as zx
    from qiskit.quantum_info import Operator

    from su2zx.core import optimize_with_pyzx

    denominator = zx.settings.float_to_fraction_max_denominator
    source = strang_evolution(3, 2.0, 0.24, 8, initial_ones=(1,))
    for strategy in ["basic", "teleport"]:
        candidate = optimize_with_pyzx(source, strategy)
        assert Operator(source).equiv(Operator(candidate), atol=1e-12, rtol=1e-12)
        assert zx.settings.float_to_fraction_max_denominator == denominator


def test_qpu_fresh_approval_guards_never_submit(monkeypatch):
    import json
    import sys

    import qiskit_ibm_runtime

    from su2zx import qpu
    from su2zx.compiler_study import generic_ecr_backend
    from su2zx.paths import project_path

    approval = project_path(".work/v040/test_qpu_approval.json")
    assert not approval.exists()
    backend = generic_ecr_backend(7)
    circuit = QuantumCircuit(5)
    circuit.measure_all()
    manifest = [dict(name="test", two_qubit_gates=0, circuit_hash="fixed")]

    class Service:
        def backend(self, name):
            return backend

    def forbidden(*args, **kwargs):
        raise AssertionError("submission must never be reached")

    monkeypatch.setattr(qiskit_ibm_runtime, "QiskitRuntimeService", Service)
    monkeypatch.setattr(qiskit_ibm_runtime, "SamplerV2", forbidden)
    monkeypatch.setattr(qpu, "build_isa_circuits", lambda *args: ([circuit], manifest))
    monkeypatch.setattr(qpu, "project_path", lambda name: approval)
    arguments = ["su2zx.qpu", "--backend", "test", "--physical-path", "0,1,2,3,4"]
    try:
        monkeypatch.setattr(sys, "argv", arguments)
        qpu.main()
        record = json.loads(approval.read_text())
        monkeypatch.delenv("ALLOW_IBM_QPU_SUBMISSION", raising=False)
        monkeypatch.setattr(sys, "argv", arguments + ["--submit", "--confirm", record["token"]])
        with pytest.raises(SystemExit, match="ALLOW_IBM_QPU_SUBMISSION"):
            qpu.main()
        monkeypatch.setenv("ALLOW_IBM_QPU_SUBMISSION", "1")
        monkeypatch.setattr(sys, "argv", arguments + ["--submit", "--confirm", "wrong"])
        with pytest.raises(SystemExit, match="token does not match"):
            qpu.main()
        assert approval.exists()
        record["created"] = 0
        approval.write_text(json.dumps(record))
        with pytest.raises(SystemExit, match="expired"):
            qpu.main()
    finally:
        approval.unlink(missing_ok=True)
