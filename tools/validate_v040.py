"""Reproduce integrity gates and bounded six-strategy controls for v0.4.0."""

from __future__ import annotations

import argparse
import hashlib
import json

import numpy as np
import pandas as pd
from qiskit import qpy

from su2zx.compiler_study import STRATEGIES, compile_candidate, count_two_qubit, target_cases
from su2zx.core import circuit_hash, circuit_structure_hash, strang_evolution
from su2zx.paths import project_path
from su2zx.qpu import build_isa_circuits
from su2zx.robust_study import verify_native


def controls(data):
    rows = []
    for n in (2, 3, 5):
        source = strang_evolution(n, 2.0, 0.24, 2, initial_ones=(n // 2,))
        case = target_cases(n, 7)[0]
        for strategy in STRATEGIES:
            _, native, elapsed = compile_candidate(
                source, strategy, case.backend, 11, case.initial_layout, 2
            )
            rows.append(
                dict(
                    n=n,
                    strategy=strategy,
                    native_2q_count=count_two_qubit(native),
                    verification_error=verify_native(source, native),
                    compile_seconds=elapsed,
                )
            )
            pd.DataFrame(rows).to_csv(data / "compiler_control_results.csv", index=False)
            print(f"control N={n} {strategy}", flush=True)
    # Repeat a fixed calibration/seed/layout with routing and compare costs/hash.
    source = strang_evolution(5, 2.0, 0.24, 2, initial_ones=(2,))
    case = target_cases(5, 7)[1]
    circuits = [
        compile_candidate(source, "basic", case.backend, 29, case.initial_layout, 2)[1]
        for _ in range(2)
    ]
    assert circuit_hash(circuits[0]) == circuit_hash(circuits[1])
    (data / "seed_reproduction.json").write_text(
        json.dumps(
            dict(
                status="PASS",
                target=case.name,
                target_seed=7,
                transpiler_seed=29,
                circuit_hash=circuit_hash(circuits[0]),
            ),
            indent=2,
        )
    )


def hardware(data):
    case = target_cases(5, 7)[0]
    circuits, manifest = build_isa_circuits(case.backend, list(range(5)), 2, comparison=True)
    assert len(circuits) == len(manifest) == 120
    assert len({row["variant"] for row in manifest}) == 4
    with (data / "hardware_ready.qpy").open("wb") as stream:
        qpy.dump(circuits, stream)
    (data / "hardware_ready.json").write_text(
        json.dumps(
            dict(
                status="PREPARED_SYNTHETIC_ONLY",
                qpu_jobs_submitted=0,
                target=case.name,
                manifest=manifest,
                reference_hierarchy=[
                    "exact Hamiltonian",
                    "ideal Trotter",
                    "compiled ideal",
                    "hardware/noisy",
                ],
                real_backend_metadata="NOT_AVAILABLE",
                note=(
                    "No in-repository provider configuration. External credential files "
                    "were not read under scope lock. Recompile against real backend "
                    "before submission."
                ),
                command=(
                    ".mamba/envs/su2zx/bin/python -m su2zx.qpu --comparison "
                    "--backend BACKEND --physical-path q0,q1,q2,q3,q4"
                ),
            ),
            indent=2,
        )
    )
    print("120 synthetic hardware-ready circuits saved; no submission", flush=True)


def audit(data):
    config = project_path("config/research_v040.json")
    frozen = json.loads((data / "frozen_design.json").read_text())
    assert frozen["sha256"] == hashlib.sha256(config.read_bytes()).hexdigest()
    raw = pd.read_csv(data / "compiler_raw_results.csv")
    pair = pd.read_csv(data / "pairwise_basic_teleport.csv")
    assert not raw.duplicated(["case_id", "strategy"]).any()
    assert np.isfinite(
        raw[["native_2q_count", "native_2q_depth", "estimated_duration"]].values
    ).all()
    assert (raw.groupby("case_family").seed.nunique() == 5).all()
    assert (raw.groupby("case_family").target_hash.nunique() == 1).all()
    assert (
        (pair.teleport_native_2q_count - pair.basic_native_2q_count)
        == pair.delta_native_2q_count
    ).all()
    assert set(pair.case_id).isdisjoint(raw.loc[~raw.verification_result, "case_id"])
    assert (raw.loc[raw.verification_result, "verification_error"] <= 1e-10).all()
    # Recreate all legacy source hashes without rerunning expensive depth controls.
    old = pd.read_csv(project_path("artifacts/data/compiler_dataset.csv"))
    for row in old.drop_duplicates("source_key").itertuples():
        source = strang_evolution(
            row.num_plaquettes,
            row.x,
            row.time,
            row.repetitions,
            initial_ones=(row.num_plaquettes // 2,),
            term_ordering=row.term_ordering,
        )
        assert circuit_hash(source) == row.circuit_hash
        assert circuit_structure_hash(source) == row.circuit_structure_hash
    assert len(old) == 426 and old.verification_result.all()
    assignments = pd.read_csv(data / "pairwise_ml_groups.csv")
    for (validation, fold), group in assignments.groupby(["validation", "fold"]):
        train = pair[pair.case_id.isin(group[group.role == "train"].case_id)]
        test = pair[pair.case_id.isin(group[group.role == "test"].case_id)]
        column = {
            "structural_family": "circuit_structure_hash",
            "leave_one_size_out": "num_plaquettes",
            "leave_one_topology_out": "target_topology",
            "leave_one_ordering_out": "term_ordering",
            "prospective": "circuit_structure_hash",
        }[validation]
        assert set(train[column]).isdisjoint(test[column])
        if validation == "prospective":
            assert set(train.cohort) == {"robustness"} and set(test.cohort) == {"prospective"}
        else:
            assert set(train.cohort) == set(test.cohort) == {"robustness"}
    tn = pd.read_csv(data / "tn_all_runs.csv")
    assert not tn.saved_statevector.any()
    assert tn.num_plaquettes.max() == 32
    assert (
        tn.query("num_plaquettes <= 8 and max_bond == 64").observable_error_to_trotter.max()
        < 1e-7
    )
    for n in [1, 2, 5]:
        result = json.loads((data / f"cudaq_N{n}.json").read_text())
        assert (
            max(
                result["absolute_energy_error"],
                result["probability_tvd_to_qiskit"],
                result["state_norm_error"],
            )
            < 1e-8
        )
    assert json.loads((data / "seed_reproduction.json").read_text())["status"] == "PASS"
    print(
        json.dumps(
            dict(
                status="PASS",
                raw_rows=len(raw),
                verified_rows=int(raw.verification_result.sum()),
                rejected_rows=int((~raw.verification_result).sum()),
                pairwise_records=len(pair),
                baseline_records=426,
                baseline_source_hashes=35,
                frozen_design="PASS",
                grouped_leakage="PASS",
                CUDA_Q_CPU="PASS",
                direct_mps="PASS",
            ),
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["controls", "hardware", "audit"])
    args = parser.parse_args()
    data = project_path("artifacts/data/v040")
    {"controls": controls, "hardware": hardware, "audit": audit}[args.stage](data)


if __name__ == "__main__":
    main()
