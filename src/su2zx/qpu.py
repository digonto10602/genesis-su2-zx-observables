"""Dry-run-first IBM experiment. Submission needs three independent guards."""

from __future__ import annotations

import argparse
import json
import os
import random
import secrets
import time as wall_time
from collections import defaultdict

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from .core import circuit_hash, measurement_family, optimize_with_pyzx, strang_evolution
from .paths import project_path

TIMES = (0.00, 0.08, 0.16, 0.24, 0.32)
VARIANTS = ("qiskit", "basic")


def validate_path(backend, path: list[int]) -> None:
    if len(path) != 5 or len(set(path)) != 5:
        raise ValueError("physical path must contain five distinct qubits")
    edges = {frozenset(edge) for edge in backend.coupling_map.get_edges()}
    missing = [
        pair for pair in zip(path, path[1:], strict=False) if frozenset(pair) not in edges
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


def build_isa_circuits(backend, path: list[int], repetitions: int, comparison: bool = False):
    manager = generate_preset_pass_manager(
        backend=backend,
        # Level 1 avoids small-angle two-qubit resynthesis approximations.
        optimization_level=1,
        initial_layout=path,
        layout_method="trivial",
        seed_transpiler=7,
    )
    circuits = []
    manifest = []
    for time in TIMES:
        variants = (
            [
                (f"{order}_{strategy}", order, strategy)
                for order in ("current", "symmetry")
                for strategy in ("basic", "teleport")
            ]
            if comparison
            else [(variant, "current", variant) for variant in VARIANTS]
        )
        for variant, ordering, strategy in variants:
            source = strang_evolution(
                5, 2.0, time, repetitions, initial_ones=(2,), term_ordering=ordering
            )
            logical = source if strategy == "qiskit" else optimize_with_pyzx(source, strategy)
            from .robust_study import verify_native

            verify_native(source, manager.run(logical))
            for measured in measurement_family(logical):
                basis = measured.metadata["measurement_basis"]
                measured.name = f"{variant}_t{time:.2f}_{basis}"
                isa = manager.run(measured)
                circuits.append(isa)
                manifest.append(
                    {
                        "name": isa.name,
                        "circuit_hash": circuit_hash(isa),
                        "variant": variant,
                        "term_ordering": ordering,
                        "strategy": strategy,
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
    parser.add_argument("--comparison", action="store_true")
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
    circuits, manifest = build_isa_circuits(backend, path, args.repetitions, args.comparison)
    # Bind approval to the exact fresh dry-run configuration and compiled bundle.
    import hashlib

    binding = hashlib.sha256(
        json.dumps(
            {
                "backend": backend.name,
                "path": path,
                "shots": args.shots,
                "repetitions": args.repetitions,
                "manifest": manifest,
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()
    approval_path = project_path(".work/qpu_dry_run.json")
    if args.submit:
        approval = json.loads(approval_path.read_text())
        if approval["binding"] != binding or wall_time.time() - approval["created"] > 900:
            raise SystemExit("submission blocked: dry run changed or expired; rerun dry run")
        token = approval["token"]
    else:
        token = f"I_APPROVE_IBM_QPU:{binding}:{secrets.token_hex(16)}"
        approval_path.parent.mkdir(parents=True, exist_ok=True)
        approval_path.write_text(
            json.dumps({"binding": binding, "token": token, "created": wall_time.time()})
        )
    import mthree
    from mthree.generators import HadamardGenerator

    mappings = mthree.utils.final_measurement_mapping(circuits)
    calibration_qubits = sorted({qubit for mapping in mappings for qubit in mapping.values()})
    calibration_count = HadamardGenerator(len(calibration_qubits)).length
    calibration_shots = (2 * args.shots + calibration_count - 1) // calibration_count
    counts = sorted(item["two_qubit_gates"] for item in manifest)
    summary = {
        "backend": backend.name,
        "path": path,
        "shots_per_circuit": args.shots,
        "physics_circuits": len(circuits),
        "balanced_m3_calibration_circuits": calibration_count,
        "calibration_shots_per_circuit": calibration_shots,
        "total_circuits": len(circuits) + calibration_count,
        "total_requested_shots": len(circuits) * args.shots
        + calibration_count * calibration_shots,
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

    approval_path.unlink()  # one use, only after all three guards pass
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

    mitigation = mthree.M3Mitigation(backend)
    calibration_jobs = mitigation.cals_from_system(
        calibration_qubits, shots=args.shots, method="balanced", async_cal=False
    )
    mitigated = [
        dict(mitigation.apply_correction(item, mapping))
        for item, mapping in zip(raw_counts, mappings, strict=True)
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
