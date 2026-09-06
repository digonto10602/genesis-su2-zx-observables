"""Fixed-target routing robustness and prospective pairwise compiler selection."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix
from sklearn.model_selection import GroupKFold, LeaveOneGroupOut
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

from .compiler_study import (
    FEATURES,
    _duration,
    _interaction_features,
    _target_features,
    compile_candidate,
    count_one_qubit,
    count_two_qubit,
    target_cases,
    two_qubit_depth,
)
from .core import circuit_hash, circuit_structure_hash, plaquette_chain_terms, strang_evolution
from .paths import load_json, project_path


def verify_native(
    source: QuantumCircuit, compiled: QuantumCircuit, seed: int = 20260905
) -> float:
    """Check the routed isometry on zero plus three random states, including ancillas.

    This is a randomized numerical check, not an exhaustive unitary proof.
    Initial and final virtual-to-physical maps are both applied explicitly.
    """
    n, m = source.num_qubits, compiled.num_qubits
    if compiled.layout is None:
        before = after = list(range(n))
    else:
        before = compiled.layout.initial_index_layout(filter_ancillas=True)
        after = compiled.layout.final_index_layout()
    indices = np.arange(2**n)
    mapped = [
        sum(((indices >> q) & 1) << p for q, p in enumerate(layout))
        for layout in (before, after)
    ]
    rng = np.random.default_rng(seed)
    error = 0.0
    for trial in range(4):
        vector = (
            np.eye(1, 2**n, dtype=complex).ravel()
            if trial == 0
            else rng.normal(size=2**n) + 1j * rng.normal(size=2**n)
        )
        vector /= np.linalg.norm(vector)
        physical = np.zeros(2**m, dtype=complex)
        physical[mapped[0]] = vector
        actual = Statevector(physical).evolve(compiled).data
        ideal = np.zeros(2**m, dtype=complex)
        ideal[mapped[1]] = Statevector(vector).evolve(source).data
        overlap = np.vdot(ideal, actual)
        phase = overlap / abs(overlap) if abs(overlap) else 1.0
        error = max(error, float(np.max(abs(actual - phase * ideal))))
    if error > 1e-10:
        raise RuntimeError(f"routed equivalence failed: {error}")
    return error


def source_features(
    source: QuantumCircuit, n: int, x: float, t: float, r: int, order: str
) -> dict:
    terms = plaquette_chain_terms(n, x, include_identity=False)
    return dict(
        num_plaquettes=n,
        x=x,
        time=t,
        repetitions=r,
        term_ordering=order,
        circuit_hash=circuit_hash(source),
        circuit_structure_hash=circuit_structure_hash(source),
        source_gate_count=source.size(),
        source_depth=source.depth(),
        source_1q_count=count_one_qubit(source),
        source_2q_count=count_two_qubit(source),
        pauli_term_count=len(terms),
        mean_pauli_weight=np.mean([sum(p != "I" for p in term.word) for term in terms]),
        **_interaction_features(source),
    )


def compiler_run(config: dict, data: Path) -> pd.DataFrame:
    old = pd.read_csv(project_path("artifacts/data/compiler_dataset.csv"))
    pivot = old.pivot(index="case_id", columns="strategy", values="native_2q_count")
    strict = pivot.apply(lambda row: (row == row.min()).sum() == 1, axis=1)
    selected = set(pivot.index[strict])
    pair_delta = pivot.teleport - pivot.basic
    selected.update(pair_delta[pair_delta == 0].index[:3])
    selected.update(pair_delta.nlargest(2).index)
    selected.update(pair_delta.nsmallest(2).index)
    design = []
    for row in old[old.case_id.isin(selected)].drop_duplicates("case_id").itertuples():
        design.append(
            dict(
                n=row.num_plaquettes,
                x=row.x,
                t=row.time,
                r=row.repetitions,
                order=row.term_ordering,
                target=row.target_name,
                cohort="robustness",
                initial=[row.num_plaquettes // 2],
                prior_case_id=row.case_id,
            )
        )
    holdout = config["prospective"]
    for n in holdout["sizes"]:
        for order in ("current", "reversed", "symmetry"):
            for case in target_cases(n, config["target_seed"]):
                design.append(
                    dict(
                        n=n,
                        x=holdout["x"],
                        t=holdout["time"],
                        r=holdout["repetitions"],
                        order=order,
                        target=case.name,
                        cohort="prospective",
                        initial=[n // 2],
                        prior_case_id="",
                    )
                )
    (data / "compiler_design.json").write_text(json.dumps(design, indent=2))
    rows = []
    targets = {}
    for i, spec in enumerate(design):
        n, x, t, r, order = (spec[k] for k in ("n", "x", "t", "r", "order"))
        source = strang_evolution(n, x, t, r, initial_ones=spec["initial"], term_ordering=order)
        if n not in targets:
            targets[n] = {c.name: c for c in target_cases(n, config["target_seed"])}
        case = targets[n][spec["target"]]
        base = source_features(source, n, x, t, r, order)
        target_description = {
            "edges": sorted(case.coupling.get_edges()),
            "seed": config["target_seed"],
            "basis": ["id", "rz", "sx", "x", "ecr"],
            "nodes": case.backend.num_qubits,
        }
        base.update(_target_features(case, source))
        base.update(
            cohort=spec["cohort"],
            target_name=case.name,
            target_topology=case.topology,
            layout_name=case.layout_name,
            target_kind="SYNTHETIC_TARGET",
            target_definition=json.dumps(target_description),
            target_hash=hashlib.sha256(json.dumps(target_description).encode()).hexdigest(),
            physical_qubits=json.dumps(case.initial_layout),
            prior_case_id=spec["prior_case_id"],
            mapping_feature_note="identity proxy before selection when layout is transpiler",
            case_family=f"{base['circuit_hash']}_{case.name}",
        )
        # Exact logical rewrites are generated once per circuit and independently
        # rechecked with explicit absolute/relative tolerance before routing.
        logicals = {}
        from .core import optimize_with_pyzx

        for strategy in ("basic", "teleport"):
            logicals[strategy] = optimize_with_pyzx(source, strategy)
            assert Operator(source).equiv(Operator(logicals[strategy]), atol=1e-10, rtol=1e-10)
        for seed in config["transpiler_seeds"]:
            for strategy, logical in logicals.items():
                _, compiled, elapsed = compile_candidate(
                    logical,
                    "qiskit",
                    case.backend,
                    seed,
                    case.initial_layout,
                    config["optimization_level"],
                    "sabre" if case.initial_layout is None else "trivial",
                )
                failure = ""
                try:
                    error = verify_native(source, compiled, config["verification_seed"])
                except RuntimeError as exc:
                    failure = str(exc)
                    error = float(failure.rsplit(": ", 1)[1])
                rows.append(
                    dict(
                        base,
                        strategy=strategy,
                        seed=seed,
                        version="v0.4.0",
                        case_id=f"{base['case_family']}_{seed}",
                        native_2q_count=count_two_qubit(compiled),
                        native_2q_depth=two_qubit_depth(compiled),
                        native_depth=compiled.depth(),
                        estimated_duration=_duration(compiled, case.backend),
                        routing_2q_overhead=count_two_qubit(compiled)
                        - count_two_qubit(logical),
                        compile_seconds=elapsed,
                        verification_result=not failure,
                        failure=failure,
                        verification_error=error,
                        verification_tolerance=1e-10,
                        verification_method=(
                            "logical Operator.equiv + routed zero/3 random states"
                        ),
                        final_layout=json.dumps(compiled.layout.final_index_layout()),
                    )
                )
        pd.DataFrame(rows).to_csv(data / "compiler_raw_results.csv", index=False)
        print(f"compiler {i + 1}/{len(design)}: {len(rows)} evaluated rows", flush=True)
    return pd.DataFrame(rows)


def pairwise(raw: pd.DataFrame) -> pd.DataFrame:
    complete = raw.groupby("case_id").verification_result.agg(["all", "size"])
    valid_ids = complete.index[complete["all"] & (complete["size"] == 2)]
    raw = raw[raw.case_id.isin(valid_ids)].copy()
    assert not raw.duplicated(["case_id", "strategy"]).any()
    base = raw[raw.strategy == "basic"].copy().set_index("case_id")
    other = raw[raw.strategy == "teleport"].set_index("case_id")
    assert set(base.index) == set(other.index)
    for name in ["circuit_hash", "target_hash", "seed", "physical_qubits"]:
        assert (base[name].fillna("null") == other.loc[base.index, name].fillna("null")).all()
    for metric in ["native_2q_count", "native_2q_depth", "estimated_duration"]:
        base[f"basic_{metric}"] = base[metric]
        base[f"teleport_{metric}"] = other[metric]
        base[f"delta_{metric}"] = other[metric] - base[metric]
    base["label"] = np.sign(base.delta_native_2q_count).map(
        {-1: "teleport", 0: "tie", 1: "basic"}
    )
    base["lexicographic_label"] = [
        "teleport" if tuple(b) < tuple(a) else "basic" if tuple(a) < tuple(b) else "tie"
        for a, b in zip(
            base[
                ["basic_native_2q_count", "basic_native_2q_depth", "basic_estimated_duration"]
            ].values,
            base[
                [
                    "teleport_native_2q_count",
                    "teleport_native_2q_depth",
                    "teleport_estimated_duration",
                ]
            ].values,
            strict=True,
        )
    ]
    return base.reset_index()


def robustness(pairs: pd.DataFrame, threshold: float) -> pd.DataFrame:
    rows = []
    for family, group in pairs.groupby("case_family"):
        fractions = group.label.value_counts(normalize=True).reindex(
            ["basic", "teleport", "tie"], fill_value=0
        )
        median = float(group.delta_native_2q_count.median())
        status = (
            "INCONCLUSIVE"
            if len(group) < 5
            else "ROBUST_BASIC"
            if fractions.basic >= threshold and median > 0
            else "ROBUST_TELEPORT"
            if fractions.teleport >= threshold and median < 0
            else "TIED"
            if fractions.tie == 1
            else "SEED_SENSITIVE"
        )
        rows.append(
            dict(
                case_family=family,
                cohort=group.cohort.iloc[0],
                num_plaquettes=group.num_plaquettes.iloc[0],
                term_ordering=group.term_ordering.iloc[0],
                target_topology=group.target_topology.iloc[0],
                layout_name=group.layout_name.iloc[0],
                circuit_hash=group.circuit_hash.iloc[0],
                seeds=len(group),
                status=status,
                basic_win_fraction=fractions.basic,
                teleport_win_fraction=fractions.teleport,
                tie_fraction=fractions.tie,
                median_delta_2q=median,
                mean_delta_2q=group.delta_native_2q_count.mean(),
                median_delta_2q_depth=group.delta_native_2q_depth.median(),
                mean_delta_2q_depth=group.delta_native_2q_depth.mean(),
                winner_entropy=-sum(p * np.log2(p) for p in fractions if p > 0),
            )
        )
    return pd.DataFrame(rows)


def frozen_choices(frame: pd.DataFrame, rule: dict) -> np.ndarray:
    return np.where(
        (frame.num_plaquettes <= rule["teleport_max_n"])
        & (frame.term_ordering == rule["teleport_ordering"]),
        "teleport",
        "basic",
    )


def policy_metrics(frame: pd.DataFrame, choices: np.ndarray) -> dict:
    basic, teleport = (
        frame.basic_native_2q_count.to_numpy(),
        frame.teleport_native_2q_count.to_numpy(),
    )
    # Tie predictions deterministically select Basic; tie-aware equality reported separately.
    chosen = np.where(choices == "teleport", teleport, basic)
    best = np.minimum(basic, teleport)
    regret = (chosen - best) / np.maximum(best, 1)
    target = frame.label.to_numpy()
    return dict(
        strategy_accuracy=float(accuracy_score(target, choices)),
        balanced_accuracy=float(balanced_accuracy_score(target, choices)),
        confusion_matrix=confusion_matrix(
            target, choices, labels=["basic", "teleport", "tie"]
        ).tolist(),
        mean_regret=float(regret.mean()),
        median_regret=float(np.median(regret)),
        worst_regret=float(regret.max()),
        oracle_match_fraction=float(np.mean(chosen == best)),
        mean_native_2q_penalty_vs_oracle=float(np.mean(chosen - best)),
    )


def evaluate_ml(pairs: pd.DataFrame, config: dict, data: Path) -> dict:
    numeric = FEATURES
    categorical = ["term_ordering", "target_topology", "layout_name"]
    # Explicit allow-list: hashes are split keys, never predictors. No compiled columns.
    x = pd.concat(
        [pairs[numeric].astype(float), pd.get_dummies(pairs[categorical], dtype=float)], axis=1
    )
    assert not any(
        any(s in c for s in ["native", "delta", "winner", "duration"]) for c in x.columns
    )
    settings = config["models"]
    models = {
        "logistic": make_pipeline(
            StandardScaler(), LogisticRegression(max_iter=3000, random_state=settings["seed"])
        ),
        "tree": DecisionTreeClassifier(
            max_depth=settings["tree_max_depth"], random_state=settings["seed"]
        ),
        "forest_classifier": RandomForestClassifier(
            n_estimators=settings["forest_trees"],
            min_samples_leaf=settings["forest_min_samples_leaf"],
            random_state=settings["seed"],
            n_jobs=1,
        ),
        "forest_delta_regressor": RandomForestRegressor(
            n_estimators=settings["forest_trees"],
            min_samples_leaf=settings["forest_min_samples_leaf"],
            random_state=settings["seed"],
            n_jobs=1,
        ),
    }
    validations = {
        "structural_family": ("circuit_structure_hash", GroupKFold(n_splits=5)),
        "leave_one_size_out": ("num_plaquettes", LeaveOneGroupOut()),
        "leave_one_topology_out": ("target_topology", LeaveOneGroupOut()),
        "leave_one_ordering_out": ("term_ordering", LeaveOneGroupOut()),
    }
    metrics: list[dict] = []
    assignments: list[dict] = []
    predictions: list[dict] = []
    importance: list[dict] = []
    old_idx = np.flatnonzero(pairs.cohort.to_numpy() == "robustness")
    new_idx = np.flatnonzero(pairs.cohort.to_numpy() == "prospective")
    splits = {"prospective": [(old_idx, new_idx)]}
    for name, (column, splitter) in validations.items():
        splits[name] = [
            (old_idx[train], old_idx[test])
            for train, test in splitter.split(
                x.iloc[old_idx], pairs.label.iloc[old_idx], groups=pairs[column].iloc[old_idx]
            )
        ]
    for name, folds in splits.items():
        output: dict[str, list] = {
            key: []
            for key in [
                *models,
                "always_basic",
                "always_teleport",
                "majority",
                "frozen_rule",
                "oracle",
            ]
        }
        test_order: list[int] = []
        for fold, (train, test) in enumerate(folds):
            if name == "structural_family":
                assert set(pairs.iloc[train].circuit_structure_hash).isdisjoint(
                    pairs.iloc[test].circuit_structure_hash
                )
            test_order.extend(test)
            assignments.extend(
                dict(validation=name, fold=fold, case_id=pairs.iloc[i].case_id, role=role)
                for role, ids in [("train", train), ("test", test)]
                for i in ids
            )
            majority = pairs.iloc[train].label.mode().iloc[0]
            choices = {
                "always_basic": np.full(len(test), "basic"),
                "always_teleport": np.full(len(test), "teleport"),
                "majority": np.full(len(test), majority),
                "frozen_rule": frozen_choices(pairs.iloc[test], config["frozen_rule"]),
                "oracle": pairs.iloc[test].label.to_numpy(),
            }
            for model_name, model in models.items():
                y = (
                    pairs.delta_native_2q_count
                    if model_name.endswith("regressor")
                    else pairs.label
                )
                model.fit(x.iloc[train], y.iloc[train])
                if name == "prospective" and model_name == "tree":
                    (data / "prospective_tree_rules.txt").write_text(
                        export_text(model, feature_names=list(x.columns))
                    )
                if name == "prospective" and model_name == "logistic":
                    logistic = model.steps[-1][1]
                    pd.DataFrame(logistic.coef_, columns=x.columns).assign(
                        classes="|".join(logistic.classes_)
                    ).to_csv(data / "prospective_logistic_coefficients.csv", index=False)
                pred = model.predict(x.iloc[test])
                if model_name.endswith("regressor"):
                    pred = np.where(
                        pred < -0.5, "teleport", np.where(pred > 0.5, "basic", "tie")
                    )
                choices[model_name] = pred
                if name == "prospective" and hasattr(model, "feature_importances_"):
                    importance.extend(
                        dict(model=model_name, feature=feature, importance=float(value))
                        for feature, value in zip(
                            x.columns, model.feature_importances_, strict=True
                        )
                    )
            for model_name, pred in choices.items():
                output[model_name].extend(pred)
                predictions.extend(
                    dict(
                        validation=name,
                        fold=fold,
                        model=model_name,
                        case_id=pairs.iloc[i].case_id,
                        prediction=str(choice),
                    )
                    for i, choice in zip(test, pred, strict=True)
                )
        for model_name, pred in output.items():
            metrics.append(
                dict(
                    validation=name,
                    model=model_name,
                    **policy_metrics(pairs.iloc[test_order], np.asarray(pred)),
                )
            )
    frame = pd.DataFrame(metrics)
    frame.to_csv(data / "pairwise_ml_results.csv", index=False)
    pd.DataFrame(assignments).to_csv(data / "pairwise_ml_groups.csv", index=False)
    pd.DataFrame(predictions).to_csv(data / "pairwise_ml_predictions.csv", index=False)
    pd.DataFrame(importance).to_csv(data / "pairwise_feature_importance.csv", index=False)
    (data / "pairwise_features.json").write_text(
        json.dumps(
            dict(
                numeric=numeric,
                categorical=categorical,
                matrix_columns=list(x.columns),
                leakage_check="PASS",
                label="native 2Q sign; ties separate",
                regret=(
                    "native 2Q relative penalty; "
                    "depth/duration lexicographic choice reported separately"
                ),
            ),
            indent=2,
        )
    )
    primary = frame[frame.validation == "structural_family"]
    best = primary[primary.model.isin(models)].sort_values("mean_regret").iloc[0]
    baseline = primary[
        primary.model.isin(["always_basic", "always_teleport", "majority", "frozen_rule"])
    ].mean_regret.min()
    prospective = frame[(frame.validation == "prospective") & (frame.model == best.model)].iloc[
        0
    ]
    prospect_baseline = frame[
        (frame.validation == "prospective")
        & frame.model.isin(["always_basic", "always_teleport", "majority", "frozen_rule"])
    ].mean_regret.min()
    status = (
        "POSITIVE"
        if best.mean_regret < baseline and prospective.mean_regret < prospect_baseline
        else "NULL"
    )
    summary = dict(
        status=status,
        best_grouped_model=best.model,
        grouped_mean_regret=best.mean_regret,
        strongest_simple_grouped_regret=baseline,
        prospective_mean_regret=prospective.mean_regret,
        strongest_simple_prospective_regret=prospect_baseline,
        selection_caveat=(
            "Best model selected post-hoc by grouped result; no nested tuning. "
            "Positive requires prospective improvement too."
        ),
    )
    (data / "pairwise_ml_summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["compile", "analyze"], default="compile")
    parser.add_argument("--config", default="config/research_v040.json")
    parser.add_argument("--output", default="artifacts/data/v040")
    args = parser.parse_args()
    data = project_path(args.output)
    data.mkdir(parents=True, exist_ok=True)
    config = load_json(args.config)
    frozen = json.loads((data / "frozen_design.json").read_text())
    assert (
        frozen["sha256"] == hashlib.sha256(project_path(args.config).read_bytes()).hexdigest()
    )
    start = time.perf_counter()
    raw = (
        compiler_run(config, data)
        if args.stage == "compile"
        else pd.read_csv(data / "compiler_raw_results.csv")
    )
    pairs = pairwise(raw)
    pairs.to_csv(data / "pairwise_basic_teleport.csv", index=False)
    robust = robustness(pairs, config["robust_fraction"])
    robust.to_csv(data / "compiler_seed_robustness.csv", index=False)
    structural = pairs.groupby(["circuit_structure_hash", "target_name"], as_index=False)[
        ["delta_native_2q_count", "delta_native_2q_depth"]
    ].median()
    structural.to_csv(data / "compiler_structural_results.csv", index=False)
    structural[structural.delta_native_2q_count != 0].to_csv(
        data / "compiler_strict_winners.csv", index=False
    )
    sensitivity = []
    for factor, columns in [
        ("layout", ["circuit_hash", "target_topology"]),
        ("topology", ["circuit_hash", "layout_name"]),
    ]:
        for key, group in robust.groupby(columns):
            signs = set(np.sign(group.median_delta_2q)) - {0}
            sensitivity.append(
                dict(
                    factor=factor,
                    group=str(key),
                    comparisons=len(group),
                    status=f"{factor.upper()}_SENSITIVE"
                    if signs == {-1, 1}
                    else "INCONCLUSIVE",
                    basic_cases=int((group.median_delta_2q > 0).sum()),
                    teleport_cases=int((group.median_delta_2q < 0).sum()),
                )
            )
    pd.DataFrame(sensitivity).to_csv(
        data / "compiler_layout_topology_sensitivity.csv", index=False
    )
    print(json.dumps(evaluate_ml(pairs, config, data), indent=2))
    print(f"elapsed {time.perf_counter() - start:.1f} seconds")


if __name__ == "__main__":
    main()
