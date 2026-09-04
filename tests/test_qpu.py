from __future__ import annotations

from su2zx.compiler_study import generic_ecr_backend
from su2zx.qpu import build_isa_circuits, confirmation_token, validate_path


def test_qpu_dry_run_manifest_and_confirmation_guard() -> None:
    backend = generic_ecr_backend(7)
    path = [0, 1, 2, 3, 4]
    validate_path(backend, path)
    circuits, manifest = build_isa_circuits(backend, path, repetitions=2)
    assert len(circuits) == len(manifest) == 60
    assert len({(item["variant"], item["time"], item["basis"]) for item in manifest}) == 60
    assert confirmation_token("test", path, 4096) == (
        "I_APPROVE_IBM_QPU:test:path=0,1,2,3,4:shots=4096:physics=60:m3=8"
    )
