"""Symmetry physics and direct MPS observables without dense-state scaling."""

from __future__ import annotations

import argparse
import json
import resource
import time
from pathlib import Path

import numpy as np
import pandas as pd
from qiskit.quantum_info import Pauli, Statevector
from qiskit_aer import AerSimulator
from scipy.sparse.linalg import expm_multiply
from scipy.stats import linregress

from .compiler_study import (
    _duration,
    compile_candidate,
    count_two_qubit,
    target_cases,
    two_qubit_depth,
)
from .core import (
    hamiltonian,
    hamiltonian_components,
    initial_state,
    local_occupations,
    pauli_word,
    probabilities,
    strang_evolution,
    total_variation,
)
from .paths import load_json, project_path
from .robust_study import source_features, verify_native


def symmetric_initial(n: int) -> tuple[int, ...]:
    return tuple(sorted({(n - 1) // 2, n // 2}))


def observable_operators(n: int, x: float) -> dict:
    electric, magnetic = hamiltonian_components(n, x)
    return {
        **{f"Z{q}": Pauli(pauli_word(n, {q: "Z"})) for q in range(n)},
        **{f"X{q}": Pauli(pauli_word(n, {q: "X"})) for q in range(n)},
        **{f"ZZ{q}": Pauli(pauli_word(n, {q: "Z", q + 1: "Z"})) for q in range(n - 1)},
        "electric_energy": electric,
        "magnetic_energy": magnetic,
        "total_energy": hamiltonian(n, x),
        "norm": Pauli("I" * n),
    }


def direct_mps(circuit, x: float, bond: int, threshold: float) -> tuple[dict, dict]:
    """Save local Pauli expectations and compact MPS tensors only.

    Identity expectation is a normalized-state diagnostic, not discarded weight.
    Tensor bytes measure the returned MPS, not total simulator workspace.
    """
    saved = circuit.copy()
    for label, operator in observable_operators(circuit.num_qubits, x).items():
        saved.save_expectation_value(operator, list(range(circuit.num_qubits)), label=label)
    saved.save_matrix_product_state(label="mps")
    assert not any("statevector" in item.operation.name for item in saved.data)
    simulator = AerSimulator(
        method="matrix_product_state",
        max_parallel_threads=2,
        max_memory_mb=2048,
        matrix_product_state_max_bond_dimension=bond,
        matrix_product_state_truncation_threshold=threshold,
        mps_log_data=True,
    )
    start = time.perf_counter()
    result = simulator.run(saved, shots=1, seed_simulator=11).result()
    if not result.success:
        raise RuntimeError(str(result.status))
    elapsed = time.perf_counter() - start
    values = result.data(0)
    tensors, lambdas = values.pop("mps")
    tensor_bytes = sum(np.asarray(a).nbytes for pair in tensors for a in pair)
    tensor_bytes += sum(np.asarray(a).nbytes for a in lambdas)
    stats = dict(
        runtime_seconds=elapsed,
        mps_tensor_bytes=tensor_bytes,
        observed_max_bond=max((len(a) for a in lambdas), default=1),
        peak_process_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
        saved_statevector=False,
        max_bond=bond,
        truncation_threshold=threshold,
        mps_log=str(result.results[0].metadata.get("MPS_log_data", "")),
    )
    return {k: float(np.real(v)) for k, v in values.items()}, stats


def tn_run(data: Path) -> dict:
    rows: list[dict] = []
    observables: list[dict] = []
    settings = [(8, 1e-10), (32, 1e-14), (64, 1e-14)]
    for n in [5, 8, 12, 16, 20, 24, 32]:
        source = strang_evolution(
            n, 2.0, 0.32, 2, initial_ones=symmetric_initial(n), term_ordering="symmetry"
        )
        operators = observable_operators(n, 2.0)
        ideal = Statevector(source) if n <= 8 else None
        exact = (
            Statevector(
                expm_multiply(
                    -1j * 0.32 * hamiltonian(n, 2.0).to_matrix(sparse=True),
                    initial_state(n, symmetric_initial(n)),
                )
            )
            if n <= 8
            else None
        )
        previous = None
        for bond, threshold in settings:
            values, stats = direct_mps(source, 2.0, bond, threshold)
            row = dict(
                num_plaquettes=n,
                x=2.0,
                time=0.32,
                repetitions=2,
                term_ordering="symmetry",
                **stats,
                norm_error=abs(values["norm"] - 1),
                observable_error_to_trotter=max(
                    abs(values[k] - float(np.real(ideal.expectation_value(op))))
                    for k, op in operators.items()
                )
                if ideal is not None
                else None,
                observable_error_to_exact=max(
                    abs(values[k] - float(np.real(exact.expectation_value(op))))
                    for k, op in operators.items()
                )
                if exact is not None
                else None,
                max_observable_change_from_previous=max(
                    abs(values[k] - previous[k]) for k in values
                )
                if previous is not None
                else None,
            )
            rows.append(row)
            observables.extend(
                dict(
                    num_plaquettes=n,
                    max_bond=bond,
                    truncation_threshold=threshold,
                    observable=k,
                    value=v,
                    ideal_trotter=float(np.real(ideal.expectation_value(operators[k])))
                    if ideal is not None
                    else None,
                    exact_hamiltonian=float(np.real(exact.expectation_value(operators[k])))
                    if exact is not None
                    else None,
                )
                for k, v in values.items()
            )
            previous = values
            pd.DataFrame(rows).to_csv(data / "tn_all_runs.csv", index=False)
            print(
                f"MPS N={n} bond={bond}: {stats['runtime_seconds']:.2f}s, "
                f"actual bond {stats['observed_max_bond']}",
                flush=True,
            )
            if stats["runtime_seconds"] > 120 or stats["peak_process_rss_mib"] > 3000:
                raise RuntimeError("Conservative TN resource bound reached; partial data saved")
        if n == 8:
            validated = pd.DataFrame(rows).query("max_bond == 64")
            assert validated.observable_error_to_trotter.max() < 1e-7
    frame = pd.DataFrame(rows)
    frame[frame.num_plaquettes <= 8].to_csv(data / "tn_observable_validation.csv", index=False)
    frame[frame.num_plaquettes > 8].to_csv(data / "tn_scaling.csv", index=False)
    pd.DataFrame(observables).to_csv(data / "tn_observables.csv", index=False)
    summary = dict(
        status="SCALING_DEMONSTRATED",
        validation="VALIDATED",
        largest_n=32,
        max_validation_error=frame.query(
            "num_plaquettes <= 8 and max_bond == 64"
        ).observable_error_to_trotter.max(),
        max_scaling_bond_stability_error=frame.query(
            "num_plaquettes > 8 and max_bond == 64"
        ).max_observable_change_from_previous.max(),
        scope=(
            "Short-time r=2 ideal Trotter scaling; "
            "no large-N exact-Hamiltonian accuracy claim. "
            "RSS is cumulative process high-water, tensor bytes are compact-state size; "
            "normalized identity does not bound discarded weight."
        ),
    )
    (data / "tn_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def physics_run(config: dict, data: Path) -> dict:
    rows, compiled_rows = [], []
    for n in config["physics"]["sizes"]:
        init = symmetric_initial(n)
        vector = initial_state(n, init)
        for x, t in config["physics"]["parameters"]:
            h = hamiltonian(n, x)
            exact = Statevector(expm_multiply(-1j * t * h.to_matrix(sparse=True), vector))
            exact_p = probabilities(exact.data)
            exact_occ = local_occupations(exact.data, n)
            energy0 = float(np.real(Statevector(vector).expectation_value(h)))
            for r in config["physics"]["repetitions"]:
                for order in ["current", "reversed", "symmetry"]:
                    source = strang_evolution(
                        n, x, t, r, initial_ones=init, term_ordering=order
                    )
                    state = Statevector(source)
                    occupation = local_occupations(state.data, n)
                    electric, magnetic = hamiltonian_components(n, x)
                    row = dict(
                        source_features(source, n, x, t, r, order),
                        initial_ones=json.dumps(init),
                        tvd=total_variation(probabilities(state.data), exact_p),
                        energy_drift=abs(float(np.real(state.expectation_value(h))) - energy0),
                        mirror_asymmetry=float(np.max(abs(occupation - occupation[::-1]))),
                        exact_mirror_asymmetry=float(np.max(abs(exact_occ - exact_occ[::-1]))),
                        survival_error=abs(
                            probabilities(state.data)[sum(1 << q for q in init)]
                            - exact_p[sum(1 << q for q in init)]
                        ),
                        survival=float(probabilities(state.data)[sum(1 << q for q in init)]),
                        local_occupation_error=float(np.max(abs(occupation - exact_occ))),
                        occupations=json.dumps(occupation.tolist()),
                        electric_energy=float(np.real(state.expectation_value(electric))),
                        magnetic_energy=float(np.real(state.expectation_value(magnetic))),
                        total_energy=float(np.real(state.expectation_value(h))),
                        norm_error=abs(float(np.vdot(state.data, state.data).real) - 1),
                    )
                    rows.append(row)
                    if n in [3, 5, 7] and r in [1, 2, 4] and x == 2.0:
                        case = target_cases(n, config["target_seed"])[0]
                        for strategy in ["qiskit", "basic", "teleport"]:
                            logical, compiled, elapsed = compile_candidate(
                                source,
                                strategy,
                                case.backend,
                                11,
                                case.initial_layout,
                                config["optimization_level"],
                            )
                            error = verify_native(source, compiled)
                            compiled_rows.append(
                                dict(
                                    row,
                                    strategy=strategy,
                                    target_name=case.name,
                                    native_2q_count=count_two_qubit(compiled),
                                    native_2q_depth=two_qubit_depth(compiled),
                                    native_depth=compiled.depth(),
                                    estimated_duration=_duration(compiled, case.backend),
                                    routing_2q_overhead=count_two_qubit(compiled)
                                    - count_two_qubit(logical),
                                    verification_result=True,
                                    verification_error=error,
                                    verification_tolerance=1e-10,
                                    verification_method=(
                                        "logical exact + routed zero/3 random states"
                                    ),
                                    compile_seconds=elapsed,
                                )
                            )
            pd.DataFrame(rows).to_csv(data / "symmetry_trotter_results.csv", index=False)
            pd.DataFrame(compiled_rows).to_csv(
                data / "symmetry_compiler_results.csv", index=False
            )
            print(f"physics N={n} x={x}: {len(rows)} rows", flush=True)
    frame = pd.DataFrame(rows)
    assert frame.norm_error.max() < 1e-10
    assert frame.exact_mirror_asymmetry.max() < 1e-10
    assert frame[frame.term_ordering == "symmetry"].mirror_asymmetry.max() < 1e-10
    fits = []
    for keys, group in frame.groupby(["num_plaquettes", "x", "time", "term_ordering"]):
        for name, minimum in [("full", 1), ("asymptotic", 2)]:
            subset = group[group.repetitions >= minimum]
            fit = linregress(np.log(subset.repetitions), np.log(subset.tvd))
            fits.append(
                dict(
                    zip(["num_plaquettes", "x", "time", "term_ordering"], keys, strict=True),
                    fit=name,
                    exponent=-fit.slope,
                    standard_error=fit.stderr,
                    r_squared=fit.rvalue**2,
                    repetitions=json.dumps(subset.repetitions.tolist()),
                )
            )
    pd.DataFrame(fits).to_csv(data / "trotter_fits.csv", index=False)
    frontier = pd.DataFrame(compiled_rows)
    metrics = [
        "tvd",
        "mirror_asymmetry",
        "native_2q_count",
        "native_2q_depth",
        "estimated_duration",
    ]
    frontier["pareto_optimal"] = False
    for _, group in frontier.groupby(["num_plaquettes", "x", "time"]):
        costs = group[metrics].to_numpy()
        # Symmetry deviations below numerical tolerance are treated as equal.
        costs[:, 1] = np.where(costs[:, 1] < 1e-10, 0, costs[:, 1])
        for idx, cost in zip(group.index, costs, strict=True):
            frontier.loc[idx, "pareto_optimal"] = not np.any(
                np.all(costs <= cost, axis=1) & np.any(costs < cost, axis=1)
            )
    frontier.to_csv(data / "physics_compiler_frontier.csv", index=False)
    matched = frame.pivot(
        index=["num_plaquettes", "x", "time", "repetitions"],
        columns="term_ordering",
        values=["tvd", "energy_drift", "mirror_asymmetry", "source_depth"],
    )
    summary = {
        "status": "MIXED",
        "physics_rows": len(frame),
        "compiler_rows": len(frontier),
        "metrics": {
            metric: dict(
                symmetry_better=int(
                    (matched[metric].symmetry < matched[metric].current - 1e-12).sum()
                ),
                symmetry_worse=int(
                    (matched[metric].symmetry > matched[metric].current + 1e-12).sum()
                ),
                total=len(matched),
                current_max=float(matched[metric].current.max()),
                symmetry_max=float(matched[metric].symmetry.max()),
            )
            for metric in ["tvd", "energy_drift", "mirror_asymmetry", "source_depth"]
        },
    }
    (data / "symmetry_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["physics", "tn"])
    parser.add_argument("--output", default="artifacts/data/v040")
    args = parser.parse_args()
    data = project_path(args.output)
    data.mkdir(parents=True, exist_ok=True)
    print(
        json.dumps(
            tn_run(data)
            if args.stage == "tn"
            else physics_run(load_json("config/research_v040.json"), data),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
