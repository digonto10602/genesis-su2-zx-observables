"""Regenerate v0.4.0 figures exclusively from persisted CSV source data."""

from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from su2zx.paths import project_path

DATA = project_path("artifacts/data/v040")
FIGURES = project_path("artifacts/figures/v040")
FIGURES.mkdir(parents=True, exist_ok=True)
SOURCES: dict[str, dict] = {}
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def save(name: str, source: str, caption: str) -> None:
    fig = plt.gcf()
    fig.tight_layout()
    fig.savefig(FIGURES / f"{name}.png", dpi=240, bbox_inches="tight")
    fig.savefig(FIGURES / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)
    SOURCES[name] = dict(source=f"artifacts/data/v040/{source}", caption=caption)


def main() -> None:
    pairs = pd.read_csv(DATA / "pairwise_basic_teleport.csv")
    robust = pd.read_csv(DATA / "compiler_seed_robustness.csv")
    ml = pd.read_csv(DATA / "pairwise_ml_results.csv")
    physics = pd.read_csv(DATA / "symmetry_trotter_results.csv")
    compiled = pd.read_csv(DATA / "symmetry_compiler_results.csv")
    fits = pd.read_csv(DATA / "trotter_fits.csv")
    tn = pd.read_csv(DATA / "tn_all_runs.csv")
    fig, ax = plt.subplots(figsize=(7, 4))
    for cohort, group in pairs.groupby("cohort"):
        ax.hist(
            group.delta_native_2q_count, bins=np.arange(-80, 85, 5), alpha=0.65, label=cohort
        )
    ax.set(
        xlabel="Teleport − Basic native 2Q count (gates)",
        ylabel="paired seed records",
        title="Basic–Teleport cost differences",
    )
    ax.legend()
    save(
        "delta_distribution",
        "pairwise_basic_teleport.csv",
        "Seed records are correlated within structural families.",
    )
    table = pd.crosstab(pairs.seed, pairs.label, normalize="index")
    table.plot.bar(stacked=True, figsize=(7, 4))
    plt.ylabel("fraction of paired cases")
    plt.xlabel("transpiler seed")
    plt.title("Strict native 2Q winners by seed")
    save(
        "winner_fraction_seed",
        "pairwise_basic_teleport.csv",
        "Targets and their calibration seed are fixed across routing seeds.",
    )
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, column in zip(
        axes, ["num_plaquettes", "term_ordering", "target_topology"], strict=True
    ):
        pd.crosstab(robust[column], robust.status).plot.bar(stacked=True, ax=ax, legend=False)
        ax.set(
            xlabel=column.replace("_", " "), ylabel="case families", title="Winner robustness"
        )
    axes[-1].legend(fontsize=7)
    save(
        "winner_robustness",
        "compiler_seed_robustness.csv",
        "Robust winner means at least 80% strict wins and matching median sign.",
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, validation in zip(axes, ["structural_family", "prospective"], strict=True):
        subset = ml[ml.validation == validation]
        ax.bar(subset.model, subset.mean_regret, label="normalized 2Q regret")
        ax.set(
            ylabel="mean normalized 2Q regret",
            title=validation.replace("_", " "),
            xlabel="policy",
        )
        ax.tick_params(axis="x", rotation=65)
        ax.legend(fontsize=8)
    save(
        "selector_regret",
        "pairwise_ml_results.csv",
        "Frozen rule and untuned lightweight models against fixed, "
        "training-majority and oracle baselines.",
    )
    best = json.loads((DATA / "pairwise_ml_summary.json").read_text())["best_grouped_model"]
    matrix = np.array(
        json.loads(
            ml[
                (ml.validation == "structural_family") & (ml.model == best)
            ].confusion_matrix.iloc[0]
        )
    )
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(matrix, cmap="Blues")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(matrix[i, j]), ha="center", va="center")
    ax.set(
        xticks=range(3),
        yticks=range(3),
        xticklabels=["Basic", "Teleport", "Tie"],
        yticklabels=["Basic", "Teleport", "Tie"],
        xlabel="prediction",
        ylabel="true native 2Q label",
        title=f"Grouped {best} confusion matrix",
    )
    fig.colorbar(im, ax=ax, label="records")
    save(
        "selector_confusion",
        "pairwise_ml_results.csv",
        "Count ties remain a distinct class; tie predictions execute Basic.",
    )
    for metric, label in [
        ("tvd", "TVD to exact Hamiltonian"),
        ("energy_drift", "absolute energy drift (dimensionless)"),
        ("mirror_asymmetry", "maximum mirrored occupation difference"),
        ("source_depth", "source circuit depth (layers)"),
    ]:
        fig, ax = plt.subplots(figsize=(7, 4))
        for order, group in physics.groupby("term_ordering"):
            median = group.groupby("num_plaquettes")[metric].median()
            ax.plot(median.index, np.maximum(median, 1e-17), marker="o", label=order)
        if metric != "source_depth":
            ax.set_yscale("log")
        ax.set(
            xlabel="plaquettes N",
            ylabel=label,
            title=f"Ordering comparison: {metric.replace('_', ' ')}",
        )
        ax.legend()
        save(
            f"symmetry_{metric}",
            "symmetry_trotter_results.csv",
            "Medians over two x/time pairs and r=1,2,4,8; symmetric central "
            "initial occupations.",
        )
    fig, ax = plt.subplots(figsize=(9, 4))
    table = compiled.groupby(["term_ordering", "strategy"]).native_2q_depth.mean().unstack()
    table.plot.bar(ax=ax)
    ax.set(
        xlabel="ordering",
        ylabel="mean native 2Q depth (layers)",
        title="Ordering and compiler jointly affect routed depth",
    )
    save(
        "symmetry_native_depth",
        "symmetry_compiler_results.csv",
        "Fixed favorable synthetic line, N=3,5,7 and r=1,2,4, seed 11.",
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    subset = physics.query("num_plaquettes == 5 and x == 2")
    for order, group in subset.groupby("term_ordering"):
        ax.loglog(group.repetitions, group.tvd, "o-", label=order)
        f = fits.query("num_plaquettes == 5 and x == 2 and term_ordering == @order")
        exponents = "/".join(f"{v:.3f}" for v in f.exponent)
        ax.text(8, group.sort_values("repetitions").tvd.iloc[-1], f" p={exponents}", fontsize=7)
    ax.set(
        xlabel="Strang repetitions r",
        ylabel="TVD to exact Hamiltonian",
        title="Full / asymptotic convergence exponents, N=5",
    )
    ax.legend()
    save(
        "trotter_convergence",
        "trotter_fits.csv",
        "Fits use r=1,2,4,8 and r=2,4,8; plotted points from symmetry_trotter_results.csv.",
    )
    frontier = pd.read_csv(DATA / "physics_compiler_frontier.csv")
    fig, ax = plt.subplots(figsize=(7, 4))
    for (order, strategy), g in frontier.query("num_plaquettes == 5").groupby(
        ["term_ordering", "strategy"]
    ):
        ax.plot(g.native_2q_count, g.tvd, "o-", label=f"{order}+{strategy}")
    ax.set(
        xlabel="native 2Q count (gates)",
        ylabel="TVD to exact Hamiltonian",
        title="Physics–compiler frontier slice, N=5",
    )
    ax.legend(fontsize=7, ncol=2)
    save(
        "physics_compiler_frontier",
        "physics_compiler_frontier.csv",
        "Full Pareto flags include TVD, mirror asymmetry, 2Q count/depth "
        "and estimated duration; this is a 2D projection.",
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    for n, g in tn.query("num_plaquettes <= 8").groupby("num_plaquettes"):
        ax.loglog(g.max_bond, g.observable_error_to_trotter, "o-", label=f"N={n}")
    ax.set(
        xlabel="maximum permitted MPS bond dimension",
        ylabel="maximum observable error",
        title="Direct MPS validation against ideal Trotter",
    )
    ax.legend()
    save(
        "tn_observable_error",
        "tn_all_runs.csv",
        "Bond 8 uses threshold 1e-10; bonds 32/64 use 1e-14. Includes "
        "Pauli and energy observables.",
    )
    for metric, label in [
        ("runtime_seconds", "runtime (s)"),
        ("mps_tensor_bytes", "returned MPS tensor storage (bytes)"),
        ("observed_max_bond", "observed final maximum bond dimension"),
    ]:
        fig, ax = plt.subplots(figsize=(7, 4))
        for bond, g in tn.groupby("max_bond"):
            ax.plot(g.num_plaquettes, g[metric], "o-", label=f"bond cap={bond}")
        ax.set(
            xlabel="plaquettes N",
            ylabel=label,
            title="Direct-observable MPS scaling, t=0.32, r=2",
        )
        ax.legend()
        save(
            f"tn_{metric}",
            "tn_all_runs.csv",
            "No full statevector saved; final tensor storage is distinct from "
            "total process RSS and peak workspace.",
        )
    (FIGURES / "figure_sources.json").write_text(json.dumps(SOURCES, indent=2))
    print(f"{len(SOURCES)} figures, each PNG/PDF with source mapping")


if __name__ == "__main__":
    main()
