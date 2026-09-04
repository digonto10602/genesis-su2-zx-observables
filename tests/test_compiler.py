from __future__ import annotations

from su2zx.compiler_study import (
    compile_candidate,
    count_two_qubit,
    generic_ecr_backend,
    target_cases,
)
from su2zx.core import strang_evolution


def test_generic_ecr_compilation_and_basic_candidate() -> None:
    backend = generic_ecr_backend(7)
    source = strang_evolution(5, 2.0, 0.08, 1, initial_ones=(2,))
    _, baseline, _ = compile_candidate(source, "qiskit", backend, 7)
    _, basic, _ = compile_candidate(source, "basic", backend, 7)
    assert count_two_qubit(baseline) > 0
    assert count_two_qubit(basic) > 0


def test_target_and_layout_diversity() -> None:
    cases = target_cases(5, 7)
    assert {case.topology for case in cases} == {
        "line",
        "ring",
        "grid",
        "heavy_hex_like",
        "irregular",
    }
    assert {case.layout_name for case in cases} == {
        "favorable",
        "spread",
        "transpiler",
    }
