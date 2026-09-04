"""Dry-run-first IBM experiment. Submission needs three independent guards."""

from __future__ import annotations

import argparse
import json
import os
import random
from collections import defaultdict

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from .core import measurement_family, optimize_with_pyzx, strang_evolution
from .paths import project_path

TIMES = (0.00, 0.08, 0.16, 0.24, 0.32)
VARIANTS = ("qiskit", "basic")


def validate_path(backend, path: list[int]) -> None:
    if len(path) != 5 or len(set(path)) != 5:
        raise ValueError("physical path must contain five distinct qubits")
    edges = {frozenset(edge) for edge in backend.coupling_map.get_edges()}
    missing = [
        pair
        for pair in zip(path, path[1:], strict=False)
        if frozenset(pair) not in edges
    ]
    if missing:
        raise ValueError(f"path has non-adjacent pairs: {missing}")


def instruction_error(backend, qargs: tuple[int, ...]) -> float:
    errors = []
    for operation in backend.operation_names:
        try:
            properties = backend.target[operation].get(qargs)
        except (AttributeError, KeyError):
            properties = None
        if properties is not None and properties.error is not None:
            errors.append(float(properties.error))
    return min(errors, default=0.1)


def best_five_qubit_path(backend) -> list[int]:
    adjacency: dict[int, set[int]] = defaultdict(set)
    for left, right in backend.coupling_map.get_edges():
        adjacency[left].add(right)
        adjacency[right].add(left)

    paths: list[list[int]] = []

    def visit(path: list[int]) -> None:
        if len(path) == 5:
            paths.append(path.copy())
            return
        for neighbor in adjacency[path[-1]]:
            if neighbor not in path:
                visit([*path, neighbor])

    for start in adjacency:
        visit([start])
    if not paths:
        raise RuntimeError("backend has no simple connected five-qubit path")

    def score(path: list[int]) -> float:
        edge = sum(
            min(
                instruction_error(backend, (a, b)),
                instruction_error(backend, (b, a)),
            )
            for a, b in zip(path, path[1:], strict=False)
        )
        readout = sum(instruction_error(backend, (qubit,)) for qubit in path)
        return edge + 0.25 * readout

    return min(paths, key=score)


def build_isa_circuits(backend, path: list[int], repetitions: int):
    manager = generate_preset_pass_manager(
        backend=backend,
        optimization_level=3,
        initial_layout=path,
        layout_method="trivial",
        seed_transpiler=7,
    )
    circuits = []
    manifest = []
    for time in TIMES:
        source = strang_evolution(5, 2.0, time, repetitions, initial_ones=(2,))
        logical = {
            "qiskit": source,
            "basic": optimize_with_pyzx(source, "basic"),
        }
        for variant in VARIANTS:
            for measured in measurement_family(logical[variant]):
                basis = measured.metadata["measurement_basis"]
                measured.name = f"{variant}_t{time:.2f}_{basis}"
                isa = manager.run(measured)
                circuits.append(isa)
                manifest.append(
                    {
                        "name": isa.name,
                        "variant": variant,
                        "time": time,
                        "basis": basis,
                        "depth": isa.depth(),
                        "two_qubit_gates": sum(
                            len(instruction.qubits) == 2 for instruction in isa.data
                        ),
                    }
                )
    order = list(range(len(circuits)))
    random.Random(20260831).shuffle(order)
    return [circuits[index] for index in order], [manifest[index] for index in order]


def confirmation_token(backend: str, path: list[int], shots: int) -> str:
    return (
        f"I_APPROVE_IBM_QPU:{backend}:path={','.join(map(str, path))}:"
        f"shots={shots}:physics=60:m3=8"
    )


def execution_properties(job):
    try:
        properties = job.properties()
        return None if properties is None else properties.to_dict()
    except Exception as error:  # supplementary metadata must not hide main data
        return {"error": repr(error)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", default="auto")
    parser.add_argument("--physical-path", default="auto")
    parser.add_argument("--shots", type=int, default=4096)
    parser.add_argument("--repetitions", type=int, default=2)
    parser.add_argument("--output", default="artifacts/qpu/ibm_su2_run.json")
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--confirm", default="")
    args = parser.parse_args()

    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    from qiskit_ibm_runtime.options import SamplerOptions

    service = QiskitRuntimeService()
    backend = (
        service.least_busy(operational=True, simulator=False, min_num_qubits=5)
        if args.backend == "auto"
        else service.backend(args.backend)
    )
    path = (
        best_five_qubit_path(backend)
        if args.physical_path == "auto"
        else [int(value) for value in args.physical_path.split(",")]
    )
    validate_path(backend, path)
    circuits, manifest = build_isa_circuits(backend, path, args.repetitions)
    token = confirmation_token(backend.name, path, args.shots)
    counts = sorted(item["two_qubit_gates"] for item in manifest)
    summary = {
        "backend": backend.name,
        "path": path,
        "shots_per_circuit": args.shots,
        "physics_circuits": len(circuits),
        "balanced_m3_calibration_circuits": 8,
        "total_circuits": len(circuits) + 8,
        "total_requested_shots": (len(circuits) + 8) * args.shots,
        "median_native_two_qubit_gates": counts[len(counts) // 2],
        "dynamical_decoupling": "XpXm",
        "gate_twirling": False,
        "confirmation_token": token,
    }
    print(json.dumps(summary, indent=2))

    if not args.submit:
        print("DRY RUN ONLY: no QPU job or M3 calibration was submitted.")
        return
    if os.environ.get("ALLOW_IBM_QPU_SUBMISSION") != "1":
        raise SystemExit("submission blocked: ALLOW_IBM_QPU_SUBMISSION is not 1")
    if args.confirm != token:
        raise SystemExit("submission blocked: confirmation token does not match")

    options = SamplerOptions()
    options.default_shots = args.shots
    options.dynamical_decoupling.enable = True
    options.dynamical_decoupling.sequence_type = "XpXm"
    options.twirling.enable_gates = False
    job = SamplerV2(mode=backend, options=options).run(circuits, shots=args.shots)
    print(f"physics job id: {job.job_id()}")
    result = job.result()
    raw_counts = [publication.data.meas.get_counts() for publication in result]

    import mthree

    mapping = mthree.utils.final_measurement_mapping(circuits[0])
    mitigation = mthree.M3Mitigation(backend)
    calibration_jobs = mitigation.cals_from_system(
        mapping, shots=args.shots, method="balanced", async_cal=False
    )
    mitigated = [
        dict(mitigation.apply_correction(item, mapping)) for item in raw_counts
    ]
    payload = {
        "backend": backend.name,
        "physical_path": path,
        "shots": args.shots,
        "repetitions": args.repetitions,
        "physics_job_id": job.job_id(),
        "calibration_job_ids": [item.job_id() for item in calibration_jobs],
        "usage": job.usage(),
        "properties_at_execution": execution_properties(job),
        "submission_order": manifest,
        "raw_counts": raw_counts,
        "m3_quasiprobabilities": mitigated,
    }
    output = project_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"saved {output}")


if __name__ == "__main__":
    main()
