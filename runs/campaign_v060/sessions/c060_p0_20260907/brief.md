# Phase 0 planning input
User explicitly authorizes preservation of unrelated dirty work. Execute Phase 0 but C0 cleanliness remains blocked; do NOT advance to Phase 1, do NOT stage unrelated work. Prompt-specific commits allowed only for reviewed scoped artifacts. Repo root is current directory; never access outside it or secrets. Phase budget 4h, hard session cutoff 12h, STOP_AT phase, no hardware or push.
Mandatory override: Fable 5.1 plans; Codex BUILD; execute_code mechanical TEST-BENCH; at most two NVIDIA workers; Opus 5 REVIEW/intermediate PHYSICS; Fable final sign-off and any physics doubt. Failed gates block dependencies, no legacy weaker substitute. Gate PASS needs deterministic evidence and Claude sign-off same snapshot.
Full Nine-Month Plan/proposal is not available in repo: v050 prompt quotes relevant objective, and campaign explicitly supersedes that objective. Identify if this blocks Phase 0 planning rather than inventing material. No SOUL.md in repository. Prompt inherited section references do not match actual prompts/v0.5.0.md numbering. Resolve by actual named topic, not guessed files.
Actual reusable matter code remains run-local, not root src/su2qc. Actual regression files are gates/gate_G1.py .. G3.py and tests/test_route_spinnet.py, test_route_gausskernel.py, test_dynamics.py, test_l12.py; requested tests/gate_G1 directories absent. Gates overwrite historical JSON; preserve by isolated evidence sandbox or output redirection, never overwrite historical results. G3 excludes absent S8/C7 criteria in legacy PASS. Plan must distinguish legacy-scope regression from full gate acceptance and formal retirement. Define exact mapping, minimal safe integration without duplicate backends, threshold setup before C1, and clean-state blocked disposition. Physics-signoff historical files are evidence only, not new signoff.
Provide executable PHASE 0 plan only, goals, acceptance criteria, lanes, gate schedule, stop conditions; no implementation or file edits. Establish whether missing proposal blocks planning. Prefer no new runner/framework; supervised bounded subprocesses, not claimed unattended durability.

Baseline eee1e162a0b28b4c8f6f8f917454e795efbea606
T0 2026-09-07T22:09:23.572396+00:00

## Tracked tree (first 300 entries; truncated if longer)
.gitignore
.graphifyignore
AGENTS.md
CITATION.cff
GRAPHIFY_UPDATE.md
LICENSE
README.md
RELEASE_NOTES_v0.3.0.md
RELEASE_NOTES_v0.4.0.md
RESEARCH_RESULTS.md
RUN_MANIFEST.md
VALIDATION.md
artifacts/cudaq_reference_N1.json
artifacts/cudaq_reference_N2.json
artifacts/cudaq_reference_N5.json
artifacts/data/accelerator_status.json
artifacts/data/basis_probabilities.csv
artifacts/data/compiler_dataset.csv
artifacts/data/compiler_seed_sensitivity.csv
artifacts/data/compiler_winners.csv
artifacts/data/measurement_reconstruction.csv
artifacts/data/ml_feature_definitions.json
artifacts/data/ml_group_assignments.csv
artifacts/data/physics_observables.csv
artifacts/data/physics_summary.json
artifacts/data/publication.json
artifacts/data/selector_summary.json
artifacts/data/symmetry_ordering.csv
artifacts/data/tensor_network_cpu.csv
artifacts/data/tensor_network_summary.json
artifacts/data/trotter_convergence.csv
artifacts/data/v040/compiler_control_results.csv
artifacts/data/v040/compiler_design.json
artifacts/data/v040/compiler_layout_topology_sensitivity.csv
artifacts/data/v040/compiler_raw_results.csv
artifacts/data/v040/compiler_seed_robustness.csv
artifacts/data/v040/compiler_strict_winners.csv
artifacts/data/v040/compiler_structural_results.csv
artifacts/data/v040/cudaq_N1.json
artifacts/data/v040/cudaq_N2.json
artifacts/data/v040/cudaq_N5.json
artifacts/data/v040/frozen_design.json
artifacts/data/v040/hardware_ready.json
artifacts/data/v040/hardware_ready.qpy
artifacts/data/v040/pairwise_basic_teleport.csv
artifacts/data/v040/pairwise_feature_importance.csv
artifacts/data/v040/pairwise_features.json
artifacts/data/v040/pairwise_ml_groups.csv
artifacts/data/v040/pairwise_ml_predictions.csv
artifacts/data/v040/pairwise_ml_results.csv
artifacts/data/v040/pairwise_ml_summary.json
artifacts/data/v040/physics_compiler_frontier.csv
artifacts/data/v040/prospective_logistic_coefficients.csv
artifacts/data/v040/prospective_tree_rules.txt
artifacts/data/v040/seed_reproduction.json
artifacts/data/v040/symmetry_compiler_results.csv
artifacts/data/v040/symmetry_compiler_summary.json
artifacts/data/v040/symmetry_summary.json
artifacts/data/v040/symmetry_trotter_results.csv
artifacts/data/v040/tn_all_runs.csv
artifacts/data/v040/tn_observable_validation.csv
artifacts/data/v040/tn_observables.csv
artifacts/data/v040/tn_scaling.csv
artifacts/data/v040/tn_summary.json
artifacts/data/v040/trotter_fits.csv
artifacts/environment-pip-freeze.txt
artifacts/environment.md
artifacts/figures/compiler_native_resources.pdf
artifacts/figures/compiler_native_resources.png
artifacts/figures/compiler_routing_penalty.pdf
artifacts/figures/compiler_routing_penalty.png
artifacts/figures/energy_components.pdf
artifacts/figures/energy_components.png
artifacts/figures/loop_occupations_exact_vs_trotter.pdf
artifacts/figures/loop_occupations_exact_vs_trotter.png
artifacts/figures/mirror_asymmetry.pdf
artifacts/figures/mirror_asymmetry.png
artifacts/figures/selector_accuracy_regret.pdf
artifacts/figures/selector_accuracy_regret.png
artifacts/figures/strategy_winner_by_topology.pdf
artifacts/figures/strategy_winner_by_topology.png
artifacts/figures/strategy_winner_distribution.pdf
artifacts/figures/strategy_winner_distribution.png
artifacts/figures/survival_probability.pdf
artifacts/figures/survival_probability.png
artifacts/figures/symmetry_aware_ordering.pdf
artifacts/figures/symmetry_aware_ordering.png
artifacts/figures/tensor_network_convergence.pdf
artifacts/figures/tensor_network_convergence.png
artifacts/figures/trotter_tvd_convergence.pdf
artifacts/figures/trotter_tvd_convergence.png
artifacts/figures/v040/delta_distribution.pdf
artifacts/figures/v040/delta_distribution.png
artifacts/figures/v040/figure_sources.json
artifacts/figures/v040/physics_compiler_frontier.pdf
artifacts/figures/v040/physics_compiler_frontier.png
artifacts/figures/v040/selector_confusion.pdf
artifacts/figures/v040/selector_confusion.png
artifacts/figures/v040/selector_regret.pdf
artifacts/figures/v040/selector_regret.png
artifacts/figures/v040/symmetry_energy_drift.pdf
artifacts/figures/v040/symmetry_energy_drift.png
artifacts/figures/v040/symmetry_mirror_asymmetry.pdf
artifacts/figures/v040/symmetry_mirror_asymmetry.png
artifacts/figures/v040/symmetry_native_depth.pdf
artifacts/figures/v040/symmetry_native_depth.png
artifacts/figures/v040/symmetry_source_depth.pdf
artifacts/figures/v040/symmetry_source_depth.png
artifacts/figures/v040/symmetry_tvd.pdf
artifacts/figures/v040/symmetry_tvd.png
artifacts/figures/v040/tn_mps_tensor_bytes.pdf
artifacts/figures/v040/tn_mps_tensor_bytes.png
artifacts/figures/v040/tn_observable_error.pdf
artifacts/figures/v040/tn_observable_error.png
artifacts/figures/v040/tn_observed_max_bond.pdf
artifacts/figures/v040/tn_observed_max_bond.png
artifacts/figures/v040/tn_runtime_seconds.pdf
artifacts/figures/v040/tn_runtime_seconds.png
artifacts/figures/v040/trotter_convergence.pdf
artifacts/figures/v040/trotter_convergence.png
artifacts/figures/v040/winner_fraction_seed.pdf
artifacts/figures/v040/winner_fraction_seed.png
artifacts/figures/v040/winner_robustness.pdf
artifacts/figures/v040/winner_robustness.png
artifacts/logs/archive_integrity.log
artifacts/logs/archive_integrity_final.log
artifacts/logs/compiler.log
artifacts/logs/compiler_v0.3.0.log
artifacts/logs/cudaq.log
artifacts/logs/data_integrity.log
artifacts/logs/mypy.log
artifacts/logs/pytest.log
artifacts/logs/report.log
artifacts/logs/ruff.log
artifacts/logs/secret_scan.log
artifacts/logs/secret_scan_final.log
artifacts/logs/study.log
artifacts/logs/v040/archive_integrity.json
artifacts/logs/v040/baseline_mypy.log
artifacts/logs/v040/baseline_physics.log
artifacts/logs/v040/baseline_pytest.log
artifacts/logs/v040/baseline_ruff.log
artifacts/logs/v040/completion/controls.log
artifacts/logs/v040/completion/data_integrity.log
artifacts/logs/v040/completion/format.log
artifacts/logs/v040/completion/graph_refresh.log
artifacts/logs/v040/completion/graph_update.log
artifacts/logs/v040/completion/mypy.log
artifacts/logs/v040/completion/pairwise_ml.log
artifacts/logs/v040/completion/plots.log
artifacts/logs/v040/completion/pytest.log
artifacts/logs/v040/completion/pytest.xml
artifacts/logs/v040/completion/ruff.log
artifacts/logs/v040/completion/tn.log
artifacts/logs/v040/controls.log
artifacts/logs/v040/cudaq.log
artifacts/logs/v040/data_integrity.log
artifacts/logs/v040/format.log
artifacts/logs/v040/format_applied.log
artifacts/logs/v040/graph_diagnostic.json
artifacts/logs/v040/graph_merge.log
artifacts/logs/v040/graph_query.log
artifacts/logs/v040/graph_update.log
artifacts/logs/v040/graph_validation.json
artifacts/logs/v040/hardware.log
artifacts/logs/v040/mypy.log
artifacts/logs/v040/new_guards.log
artifacts/logs/v040/pairwise_ml.log
artifacts/logs/v040/plots.log
artifacts/logs/v040/pytest.log
artifacts/logs/v040/report.log
artifacts/logs/v040/robust_study.log
artifacts/logs/v040/ruff.log
artifacts/logs/v040/secret_scan.json
artifacts/logs/v040/symmetry.log
artifacts/logs/v040/tn.log
artifacts/provenance/completion_v040.json
artifacts/provenance/graph_semantic_v040.json
artifacts/provenance/publication_v040.json
artifacts/provenance/run_v0.3.0.json
artifacts/provenance/run_v0.4.0.json
config/research.json
config/research_v040.json
docs/CODE_FUNCTION_INVENTORY.md
docs/CODE_LOGIC_AND_TESTS.md
docs/REFERENCES.md
docs/V040_COMPLETION_AUDIT.md
prompts/CODEX_AUTONOMOUS_SU2ZX_RESEARCH_PROMPT.md
prompts/CODEX_AUTONOMOUS_SU2ZX_RESEARCH_PROMPT_Laptop.md
prompts/SU2ZX_CODEX_AUTONOMOUS_RESEARCH_PROMPT_v0.3.0.md
prompts/SU2ZX_CODEX_AUTONOMOUS_RESEARCH_PROMPT_v0.4.0.md
prompts/v0.5.0.md
pyproject.toml
runs/section8_v0.5.0_20260907T0628Z/OUTPUT_CONTRACT.json
runs/section8_v0.5.0_20260907T0628Z/analysis/figures/exact_casimir.png
runs/section8_v0.5.0_20260907T0628Z/analysis/figures/exact_channels.png
runs/section8_v0.5.0_20260907T0628Z/analysis/figures/exact_density.png
runs/section8_v0.5.0_20260907T0628Z/analysis/tables/exact_mass_scan.csv
runs/section8_v0.5.0_20260907T0628Z/analysis/tables/exact_timeseries.csv
runs/section8_v0.5.0_20260907T0628Z/bin_clock.sh
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r0.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r1.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r2.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r3.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/resources_logical.md
runs/section8_v0.5.0_20260907T0628Z/circuits/trotter_scaling.json
runs/section8_v0.5.0_20260907T0628Z/env/requirements.lock.txt
runs/section8_v0.5.0_20260907T0628Z/gates/GATE_G0.json
runs/section8_v0.5.0_20260907T0628Z/gates/GATE_G1.json
runs/section8_v0.5.0_20260907T0628Z/gates/GATE_G2.json
runs/section8_v0.5.0_20260907T0628Z/gates/GATE_G3.json
runs/section8_v0.5.0_20260907T0628Z/gates/attempts/G1_attempt1.md
runs/section8_v0.5.0_20260907T0628Z/gates/attempts/G1_attempt2.md
runs/section8_v0.5.0_20260907T0628Z/gates/gate_G0.py
runs/section8_v0.5.0_20260907T0628Z/gates/gate_G1.py
runs/section8_v0.5.0_20260907T0628Z/gates/gate_G2.py
runs/section8_v0.5.0_20260907T0628Z/gates/gate_G3.py
runs/section8_v0.5.0_20260907T0628Z/logs/agents/l12_builder.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/l12_builder.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route1_fix_escalation.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route1_fix_escalation.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route2_attempt2.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route2_attempt2.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/cmd/run_g2.log
runs/section8_v0.5.0_20260907T0628Z/logs/cmd/test_l12.log
runs/section8_v0.5.0_20260907T0628Z/physics/DISCREPANCIES.md
runs/section8_v0.5.0_20260907T0628Z/physics/conventions_reconciliation.md
runs/section8_v0.5.0_20260907T0628Z/physics/predictions_G1.json
runs/section8_v0.5.0_20260907T0628Z/physics/predictions_G1.md
runs/section8_v0.5.0_20260907T0628Z/physics/predictions_G2.md
runs/section8_v0.5.0_20260907T0628Z/physics/resonance.json
runs/section8_v0.5.0_20260907T0628Z/physics/signoff_G1.json
runs/section8_v0.5.0_20260907T0628Z/physics/signoff_G1.md
runs/section8_v0.5.0_20260907T0628Z/physics/signoff_G2.json
runs/section8_v0.5.0_20260907T0628Z/physics/signoff_G2.md
runs/section8_v0.5.0_20260907T0628Z/physics/truncation_error.json
runs/section8_v0.5.0_20260907T0628Z/physics/truncation_error.md
runs/section8_v0.5.0_20260907T0628Z/physics/window.json
runs/section8_v0.5.0_20260907T0628Z/reports/REPORT.md
runs/section8_v0.5.0_20260907T0628Z/reports/SUMMARY.md
runs/section8_v0.5.0_20260907T0628Z/reviews/p1_route_spinnet_1.md
runs/section8_v0.5.0_20260907T0628Z/run/CONFIG_ENV.md
runs/section8_v0.5.0_20260907T0628Z/run/DECISIONS.md
runs/section8_v0.5.0_20260907T0628Z/run/GATES.md
runs/section8_v0.5.0_20260907T0628Z/run/HEARTBEAT.md
runs/section8_v0.5.0_20260907T0628Z/run/INVENTORY.md
runs/section8_v0.5.0_20260907T0628Z/run/MODELS.md
runs/section8_v0.5.0_20260907T0628Z/run/PLAN.md
runs/section8_v0.5.0_20260907T0628Z/run/PROMPT_HASH
runs/section8_v0.5.0_20260907T0628Z/run/T0
runs/section8_v0.5.0_20260907T0628Z/run/TASKBOARD.md
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/export_l12.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/strang_l12.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/engine.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/run_g2.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/dynamics/scan.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/compare.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/limits.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_gausskernel.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/ham/route_spinnet.py
runs/section8_v0.5.0_20260907T0628Z/tests/conftest.py
runs/section8_v0.5.0_20260907T0628Z/tests/pytest.ini
runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_route_gausskernel.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_route_spinnet.py
scripts/bootstrap_env.sh
scripts/run_all.sh
scripts/run_v040.sh
solutions/0.5.0.md
src/su2zx/__init__.py
src/su2zx/compiler_study.py
src/su2zx/core.py
src/su2zx/paths.py
src/su2zx/qpu.py
src/su2zx/qpu_analysis.py
src/su2zx/report.py
src/su2zx/robust_study.py
src/su2zx/scaling_study.py
src/su2zx/study.py
src/su2zx/tn_study.py
tests/test_compiler.py
tests/test_core.py
tests/test_qpu.py
tests/test_study.py
tests/test_tn.py
tests/test_v040.py
tools/archive_v040.py
tools/cudaq_reference.py
tools/cutensornet_reference.py
tools/function_inventory.py
tools/plot_v040.py
tools/provenance.py


## Source: prompts/gi_cost_campaign_v.0.6.0.md
# SU2ZX · GI-Cost Campaign · The measured price of exact gauge invariance

**Hermes prompt v0.6.0 · path: `SU2ZX/prompts/gi_cost_campaign_v.0.6.0.md`**
**Supersedes the *objective* of `prompts/section8_overnight_v.0.5.0.md` (hereafter "v0.5.0"); inherits its machinery. Sources of truth for what changed: the v0.5.0 status review (7 Sept 2026) and the overlap analysis of the Sufian report "2+1D SU(2) Gauge Dynamics" (25 Aug 2026), both in the SU2QC Ideas project; copy both into `$REPO/docs/refs/` before the first session.**

**Launch (human, one line, from the SU2ZX repository root):** `hermes` then
`@prompts/gi_cost_campaign_v.0.6.0.md  Run phase 0. T0 is now.` — or, for any later session, `Run next phase.`
Everything below is addressed to you, the Hermes orchestrator session.

**How to read this file (orchestrator).** Sections 0–3 now, in full, every session. Section 4 one phase at a time. Sections 5–9 are reference (thresholds, decision rules, session protocol, tree, summary format). **Inherit unchanged from v0.5.0:** §5 (lanes, Hermes mechanics, two-stage review plus physics audit, independence rules), §9.3–9.5 (dry-run lints, submission and polling, provenance labels), §10.4–10.5 (re-plan, resume and watchdog), §13 D1–D2 and D6–D11 (decision rules), Appendix A (delegation templates), Appendix C (conventions). Where this file and v0.5.0 disagree, this file wins. Numbers marked "preliminary" tell you what to expect, not what to report.

---

## 0. What changed and why (read once per session)

v0.5.0 finished the science half and it stands: 82 gauge-invariant states at j_max = 1/2 by two independent routes agreeing at 10⁻¹⁵ (sectors 2, 20, 38, 20, 2; 152 at j_max = 1), exact gauge-invariant Strang circuits with zero noiseless leakage, the stretched-string codeword 3793 in the 12-qubit local encoding, the resonance μ* = 3/8 (m* = 3g²/16). The engineering half stopped at a structural gap: **2,156 two-qubit gates per Strang step before routing** (D = 16, h0–h3 = 248/248/239/241, B = 174; routed 3,976 on heavy-hex) against a 250 budget, an **8.6× logical gap that no synthesis trick closes**. The review also found that the primary endpoint could not pass as coded (r = 0: exact 1.000 versus twin 0.946, a 5.4 % device error judged against a 0.004 statistical error bar).

Meanwhile an independent report (Sufian, 25 Aug 2026) ran the same hard-core SU(2) Kogut–Susskind model on IBM Kingston at **13 native CZ** by projecting onto a state-adapted Krylov subspace (K = 6 or 8, three qubits) and synthesizing a generic unitary. That circuit is valid for one initial state at one time, needs the full classical solution to construct, and by the report's own §18.2 is not a scalable algorithm. Its model differs from ours by two static fundamental charges at opposite corners (one plaquette: 112 total / 54 half-filled; two plaquettes: 2,417 / 977; ours: 82 / 38 and 1,727 / —). Its coupling point is far into strong coupling (hopping and magnetic terms 0.02 of the electric term; ours 0.5 and 0.25).

The campaign's object is therefore no longer "first with-matter hardware time series". It is:

> **The measured price of exact gate-level gauge invariance.** On one Hamiltonian, one observable set and one device, compare an extensible gauge-invariant product-formula circuit (arm **GI**) with a validated state-adapted Krylov playback circuit (arm **KR**), and report cost, accuracy, gauge-error detectability and extensibility as measured quantities, at two coupling points.

The 8.6× gap is the headline number, not the failure. Every phase below either sharpens that number, makes the KR baseline strong enough that the comparison is fair, or turns a review finding into a passed test.

**Non-negotiables (v0.5.0 §0 rules 1–9 still hold; these are added).**

10. **Two arms or nothing.** No hardware submission of one arm without the other on the same backend, same qubit set where the qubit counts allow it, same calibration window, matched t = 0 controls, equal total shots per observable group. A one-arm result is EMULATED-only until the other arm exists.
11. **The KR baseline must be the best KR, not a strawman.** Its K-scan, synthesis search and layout search are preregistered with a budget at least equal to the Sufian report's (K-scan at every time point; exact and approximate synthesis; ≥ 3 optimization levels × ≥ 20 transpiler seeds × all operational Heron backends).
12. **Every session begins by rerunning every previous gate's tests.** A gate that stops passing halts the campaign until fixed (Section 7). Long tests may be cached by hash; the cache is invalidated by any change to the files the test reads.
13. **Never compare across coupling points, models or sources in one number.** Tables carry `point ∈ {P-A, P-S}`, `model ∈ {OURS-82, STATIC-112}`, `arm ∈ {GI, KR}`, `source ∈ {EXACT, NOISELESS, EMULATED, HARDWARE}` columns.

---

## 1. Hypotheses, endpoints, claim table (preregistered in Phase 1; verbatim into `PREREGISTRATION.md`)

### 1.1 Hypotheses

> **H-COST.** For the hard-core SU(2) single plaquette with four staggered two-color fermion sites (82 gauge-invariant states, 38 in the N = 4 sector), an exactly gauge-invariant second-order product-formula circuit in the 12-qubit local encoding costs, after routing to a Heron heavy-hex map, more than 10× the two-qubit gates of a state-adapted Krylov playback circuit validated to the same 10⁻³ full-space accuracy at the same time point and coupling point, at both coupling points P-A and P-S.

> **H-DETECT.** On hardware, the GI arm's leakage flags detect a nonzero gauge-violation rate that the KR arm cannot measure at all, and post-selection on those flags changes at least one primary observable by more than 2σ.

> **H-CROSS.** The Krylov dimension K needed for 10⁻³ accuracy grows with time and with system size (82 → 1,727 states) faster than the GI cost per step (fixed per step, linear in the number of links and plaquettes), so that a crossover time or size exists within exact reach at coupling point P-A, and either exists or is shown absent at P-S.

### 1.2 Endpoints (each is one table with the four columns of rule 13)

- **E1 Resource frontier (deterministic).** For each (point, arm, time point): qubits, logical two-qubit gates, routed CZ, two-qubit depth, state-preparation CZ, basis-change CZ, and the noiseless full-space accuracy the circuit was validated to (state infidelity, maximum observable error, process infidelity where defined, leakage). The cost ratio CZ_GI / CZ_KR per row.
- **E2 Hardware accuracy (restated from the review, option i).** For each arm, observable and time point: |HARDWARE_mitigated − NOISELESS_arm| ≤ 2σ_stat + δ_dev, where σ_stat is the bootstrap standard error over repetitions and time blocks and δ_dev = |TWIN − NOISELESS_arm| is the calibration-derived noisy-twin bias computed and frozen before submission. NOISELESS_arm − EXACT (Trotter bias for GI; Krylov truncation bias for KR) is tabulated beside every value and never subtracted. Both arms also go on one figure: absolute observable error versus routed CZ, same device, same day.
- **E3 Trend endpoint (option iii, robust to uniform depolarizing).** At each hardware time point, for each arm: the sign pattern ΔP_S3 < 0, ΔC_string < 0, Δ⟨N⟩ on the two intermediate vertices > 0, ΔP_baryonic > 0 holds at ≥ 2σ; and the ordering P_baryonic > P_meson holds at ≥ 2σ (preliminary: the one-plaquette ratio is about 11 at P-A).
- **E4 Gauge-error detectability.** GI arm: leakage-flag rate per circuit (HARDWARE), yield after post-selection, and the change in each primary observable from post-selection with its 2σ. KR arm: the entry is "not measurable: no gauge redundancy in the encoding", stated as a measured limitation, not omitted.
- **E5 Extensibility (deterministic, classical).** K_min(t) for 10⁻³ accuracy at 82 states and at 1,727 states (the 2×3 ladder), at both coupling points; GI logical two-qubit gates per step at one plaquette (measured) and at 2×3 (synthesized, not routed, from the term-group structure: 7 hopping groups, 2 plaquette groups, one diagonal layer); the crossover (t, size) where routed CZ_KR ≥ routed CZ_GI at r = 1, or a statement that none exists within exact reach; and the classical-dependence flag: KR requires exp(−iHt)|S3⟩ in the full space to construct Q_K, GI does not.

### 1.3 Claim table (copy into `CLAIM_TABLE.md` unchanged)

| Supported if the gates pass | Not supported by this campaign |
|---|---|
| A measured cost ratio between exactly gauge-invariant and Krylov-playback circuits for SU(2) with dynamical matter on a plaquette, at two coupling points, on one device | Any statement about string tension, a continuum limit, hadron phenomenology, or the 8×8 physics of Cataldi et al. |
| A hardware accuracy-versus-cost curve for both arms with a decomposed error budget (truncation, Trotter or Krylov, compile, device, shot) | A classically intractable calculation; every number has an exact reference |
| A hardware-measured gauge-violation rate and its effect under post-selection, and the statement that the playback arm cannot measure it | Quantum advantage, AI advantage, or the superiority of either arm in general |
| The Krylov-dimension growth with time and with size from 82 to 1,727 states, and the crossover or its absence within exact reach | Baryon blockade, the 2+1D claim (reserved for 2×3 and beyond on hardware), or any hardware result above one plaquette |
| The v0.5.0 Section 8 physics (channel structure, resonance, truncation error) as the shared reference of both arms | That the 8.6× gap is closable; only that it was not closed inside the preregistered synthesis budget |

---

## 2. The two arms, the two coupling points, the shared physics

### 2.1 Shared reference (from v0.5.0 §2, unchanged)

Hamiltonian v0.5.0 §2.1 in code units H/g_E with coefficients (electric, mass, hopping, magnetic) = (1, μ, 1/(2g_E), 1/(4g_E²)); conventions file `00_conventions.md` as frozen in the last v0.5.0 run (rule D2); gauge-invariant space and sector table v0.5.0 §2.2; named states, channel projectors and bare energies v0.5.0 §2.3; observables v0.5.0 §2.4; Trotter tolerance 0.05 (density) and 0.0375 (Casimir). Initial state S3 (stretched string, codeword 3793 in the 12-qubit encoding; verify it again at every session boot).

**Primary observables (both arms, identical operators, identical estimator):** the four site densities ⟨N_n⟩, the four link Casimirs ⟨j_ℓ(j_ℓ+1)⟩, P_S3, P_S1, P_pair, P_meson, P_baryonic (and its sub-projectors P_BB̄, P_antivac), P_vacmatter, the string-link Casimir average C_string over ℓ₁, ℓ₂, ℓ₃, the energy ⟨H⟩ where the settings allow it. For the KR arm every observable is O_K = Q_K† O Q_K, built from the exact-basis operator, never re-derived in the reduced space.

### 2.2 Coupling points (frozen in Phase 1)

| Point | electric : hopping : magnetic | μ | equivalent | time points | why |
|---|---|---|---|---|---|
| **P-A** | 1 : 0.5 : 0.25 | 3/8 | our g_E = 1 | the r ≤ 2 GI-admissible points of the v0.5.0 `window.json` (preliminary: t ∈ {0.75, 1.5}/g_E; add 2.25 if r = 2 passes there) | our regime; hopping comparable to bare gaps; Krylov space fills fast |
| **P-S** | 1 : 0.02 : 0.02 | 3/8 | the Sufian benchmark w = g_B = 1, g_E = 50, m = 18.75 rescaled to electric units | τ = t·g_E ∈ {5, 12.5} (Sufian's t = 0.10, 0.25) | their regime; perturbative in hopping; the regime where 13 CZ was possible |

P-S is **not** on our one-parameter family (hopping 1/(2g_E) and magnetic 1/(4g_E²) cannot both equal 0.02): the Hamiltonian builders must accept the four coefficients independently. Extend `H(gE, mu, jmax)` to `H(coeffs=(cE, cM, cH, cB), jmax)` with the old signature kept as a wrapper; re-run the v0.5.0 G1 agreement test on the new signature at both points (gate C2).

### 2.3 Arm GI (gauge-invariant, extensible) — the v0.5.0 circuits, REDUCED

The v0.5.0 Phase 3 circuits (strategy BU or HY, whichever passed G3 with leakage ≤ 10⁻¹²), 12-qubit local encoding with leakage flags, second-order Strang with gauge-invariant term grouping, each grouped factor an exact block unitary. **REDUCED scope (review N7):** r ∈ {1, 2} only; time points restricted to those where the Trotter tolerance holds at that r and the G2 visibility criterion still holds (the "surviving signal"). At P-S the Trotter error at r = 1 is expected to be small even at τ = 12.5 because the non-commuting terms are 0.02 of the electric term; verify, do not assume.

**One bounded synthesis sprint (Phase 4, ≤ 4 h wall clock, one session).** Target: reduce the per-step logical two-qubit count below 2,156 by exact, leak-free means only (the pair-structure multiplexed-rotation construction of v0.5.0 Phase 3 BU; first-order Lie–Trotter at r = 1 as a separate, labeled variant; reuse of the diagonal layer across steps; nothing that re-splits into Pauli strings). Whatever the count is when the box closes is the count. The review's verdict stands as the prior: no single hot spot (hoppings 976 versus plaquette 174), so expect at most a modest factor. Record the attempt and its result in `04_gi_arm/synthesis_sprint.md`; H-COST is judged on the best leak-free circuit that exists at the end of the sprint.

### 2.4 Arm KR (Krylov playback) — rebuilt from the Sufian method on our model

For each (point, time point): Lanczos/Arnoldi from |S3⟩ under H restricted to the N = 4 sector (38 states at j_max = 1/2); orthonormal Q_K; H_K = Q_K† H Q_K; U_K(t) = exp(−i H_K t); n_q = ⌈log₂ K⌉ qubits with unused codewords padded by the identity. Initial state = first Krylov vector = |0…0⟩, so state preparation is free. Circuits: (a) exact synthesis of U_K by Qiskit `UnitaryGate` + transpile; (b) approximate synthesis by a parameterized ansatz (line-connected, depth scanned) fitted to U_K, accepted only under the acceptance rules below. Observables O_K = Q_K† O Q_K measured by Pauli grouping on n_q qubits; report the number of measurement circuits.

**K-scan (mandatory, per point and time point):** the smallest K such that, over the whole interval [0, t] at 101 times, full-space state infidelity 1 − |⟨Ψ(t′)|Q_K Ψ_K(t′)⟩|² ≤ 10⁻³ and max over all primary observables |O_exact − O_K| ≤ 10⁻³, with gauge leakage identically zero (Q_K ⊂ H_phys by construction; assert it numerically ≤ 10⁻¹²). Report the full K(t) curve for K up to 38, not only the chosen K. Preliminary expectation: at P-S, K in the range 4–8 at τ ≤ 12.5 (the Sufian values on their model); at P-A, K substantially larger at t = 1.5/g_E (the v0.5.0 preliminary Krylov dimension from S3 was 28 of 38).

**Acceptance of a KR circuit for hardware (the Sufian criteria, adopted verbatim so the arms are judged the same way):** full-space state infidelity ≤ 10⁻³ against the exact 82-state evolution (not the reduced target); max observable error ≤ 10⁻³; process infidelity reported; probability in unused codewords ≤ 10⁻⁵ noiselessly; gauge leakage zero; ISA-compatible on the frozen backend. Layout search: all operational Heron backends × optimization levels {1, 2, 3} × 20 seeds, ranked by calibrated two-qubit error sum; record that the top ten share a structure if they do (the Sufian null result on layout search is expected to recur).

**What KR cannot do, stated as measured facts in E4 and E5:** no leakage flags (every computational state is physical); no reuse across time points (a new unitary per t); no constructibility without exp(−iHt)|S3⟩ in the full space.

### 2.5 Matched-experiment rules (both arms)

Same backend and calibration window; the KR qubits chosen inside the GI qubit path where the calibration ranking allows, otherwise the best-ranked connected triple and the reason recorded; matched t = 0 control circuits per arm (state preparation + measurement only) and reporting of ΔO(t) = ⟨O⟩_t − ⟨O⟩_0 beside absolute values (adopted from the Sufian protocol); independent readout calibration per arm per job; equal total shots per observable group (4,096 per group, 5 repetitions, shot allocation across groups by variance contribution allowed if the total is conserved); mitigation arms M0 (readout inversion only), M1 (readout + DD + Pauli twirling + ODR), M2 (M1 + linear ZNE at fold scales {1, 3}); quadratic ZNE is not run (the Sufian scale-5 result is cited as the reason); leakage post-selection for GI only, with pre- and post-selection values both reported; bootstrap 1,000 resamples over repetitions and time blocks, including the calibration counts.

---

## 3. Physics-based validation ladder (every gate is one or more of these; every test reads its threshold from `GATE_THRESHOLDS.yaml`)

| ID | Validation | Method | Threshold |
|---|---|---|---|
| V1 | v0.5.0 G1–G3 regression | rerun `tests/gate_G1..G3` from the last v0.5.0 run directory against the current package | all pass, values unchanged to 10⁻¹² |
| V2 | Four-coefficient Hamiltonian | route A and route B agree at P-A and P-S (spectra, aligned matrix elements, S3 observables over [0, 20]); wrapper reproduces the old H(gE, mu, jmax) exactly | 10⁻¹²; 10⁻¹²; 10⁻¹⁰ |
| V3 | j_max = 1 in both routes (review D1/N4) | route B extended to the 9-state link (3 qubits per link no longer suffice: 4 qubits or a direct 9-level register); 152 states; sectors 3, 36, 74, 36, 3; route A/B agreement at j_max = 1; the stale j_max = 1 test assertion corrected | exact counts; 10⁻¹² |
| V4 | Truncation error per observable (review N4) | j_max = 1 versus 1/2 at every hardware time point, both coupling points, every primary observable | reported; the statement "truncation error < device error bar" checked per observable |
| V5 | **Bridge to the Sufian model** | add static fundamental charges (B^a_v, spin-1/2 registers) at v0 and v2 to route B's Gauss law; count the kernel: 112 total, N-sectors 2, 27, 54, 27, 2; then 2×3 with charges at the two far corners: 2,417 total, sectors 4, 119, 597, 977, 597, 119, 4 | exact counts (independent of phase conventions) |
| V6 | Bridge, dynamics | on STATIC-112 at P-S from the lower minimal string (Sufian eq. 67), the K-scan reproduces K = 6 at τ = 12.5 with infidelity ≤ 10⁻³; on STATIC-2,417 from Sufian's index-630 string, K = 4 at τ = 5 and K = 8 at τ = 12.5 | K equal, or within ±2 with the joint phase convention recorded as the candidate cause; not a campaign blocker |
| V7 | 2×3 ladder exact reference (review N5, E5) | 1,727 states at j_max = 1/2 on OURS by both routes; exact dynamics from the stretched string; P_BB̄/P_meson at matched times versus the one-plaquette value; K_min(t) at both points | 10⁻¹² agreement; numbers reported |
| V8 | KR arm correctness | for every accepted KR circuit: full-space infidelity, max observable error, process infidelity, unused-codeword probability, leakage, all against EXACT on OURS-82 | 10⁻³; 10⁻³; reported; 10⁻⁵; 10⁻¹² |
| V9 | GI arm correctness (REDUCED) | grouped-factor unitary checks; Trotter exponent on the max-over-observables error; absolute Trotter error at r ∈ {1, 2} at the chosen points; noiseless leakage; compiled-versus-Strang equivalence; no pipeline with pre-route equivalence < 1 − 10⁻¹⁰ is hardware-eligible (retires `pyzx_basic_TP` unless fixed) | 10⁻¹⁰; [1.8, 2.2]; ≤ tolerance; ≤ 10⁻¹²; 10⁻¹⁰ |
| V10 | Twin variance (review N1) | five repeats of the calibration-derived Aer twin at r = 0 produce five distinct count dictionaries; bootstrap σ > 0 and ≈ the multinomial expectation; the `seed_simulator = 101` construction-time override removed or shown harmless | pass |
| V11 | Estimator | post-selected, readout-mitigated estimator on synthetic quasi-distributions with known answers including negative entries; matched-subtraction ΔO on synthetic data; channel closure re-reported after ODR | 10⁻¹⁰ on exact quantities |
| V12 | Endpoint pre-test | E2 and E3 evaluated on EMULATED data for both arms before any submission; δ_dev frozen per (arm, observable, t) | E2 passes on EMULATED at ≥ 2 time points per arm, else no submission |
| V13 | Independent audit | one row of every results table recomputed from raw exports by a fresh child with a different script | 10⁻¹⁰ (exact), bootstrap resolution (counts) |
| V14 | Replication | `su2qc.replicate` (review Tier 2) rebuilds every table and figure from `raw_immutable/`, exact references and saved noiseless/emulated outputs in a fresh venv; hashes match | all |

---

## 4. Campaign phases (one phase per session by default; Section 7 governs sessions)

| Phase | Object | Gate | Validations | Session budget |
|---|---|---|---|---|
| 0 | Repair and hygiene (review Tier 0 + Tier 2) | C0 | V1, V10, V11 | 4 h |
| 1 | Reframe and preregister | C1 | — (documents + thresholds) | 3 h |
| 2 | Reference extension: four coefficients, j_max = 1, bridge, 2×3 | C2 | V2–V7 | 8 h |
| 3 | Arm KR: K-scans, synthesis, layout search, both points | C3 | V8 | 8 h |
| 4 | Arm GI REDUCED: surviving signal, synthesis sprint, compile, frontier | C4 | V9, E1, E5 | 8 h |
| 5 | Matched design, twin, rehearsal, endpoint pre-test | C5 | V12 | 6 h |
| 6 | Hardware: dry run, pilot, full run, second calibration window | C6 | v0.5.0 lints; G8-style stop/go | 8 h + queue |
| 7 | Analysis, error budget, endpoints E1–E5, audit | C7 | V13 | 6 h |
| 8 | Paper, release, replication | C8 | V14 | 6 h |

### Phase 0 · Repair and hygiene (Tier 0 and Tier 2 of the review)

1. Boot per Section 7. Inventory the last v0.5.0 run directory; locate `GATE_LEDGER.jsonl`, `window.json`, `strang_table.md`, `resource_table.md`, `resources_synth.md`, `run_g4.py`, the twin module, `circuits/`, and the nine untracked Phase-4 paths named in the review. Commit the untracked paths (`git add`, message `campaign: commit phase-4 artifacts from v0.5.0`).
2. **N1, twin variance (V10).** Builder A0a: write `tests/gate_C0/test_twin_variance.py` — five `run_counts` repeats at r = 0 must return five distinct count dicts; bootstrap σ of a density must be within a factor 2 of the multinomial expectation; then locate and remove (or prove harmless) the construction-time `seed_simulator = 101` override. Reviewer B checks the test would have failed on the old code (run it against the pre-fix commit).
3. **N3, close G4 honestly.** Orchestrator: append to the v0.5.0 ledger an INFO row `G4: decision = REDUCED (campaign v0.6.0); gap = 2156/250 = 8.6x logical, 3976 routed` with evidence paths. GO is not available on the numbers; PLAN B is not taken because the campaign's object no longer needs a sub-250 circuit to be a result.
4. **Tier 2.** Ruff and mypy on `src/su2qc` (fix or explicitly ignore with a reason per finding; no blanket ignores); the stale j_max = 1 test assertion corrected against the 152/(3, 36, 74, 36, 3) counts; `pyzx_basic_TP` either fixed to pre-route equivalence ≥ 1 − 10⁻¹⁰ or retired with a ledger row; `su2qc.replicate` skeleton written (full implementation in Phase 8); V11 estimator test written against the existing estimator (`tests/gate_C0/test_estimator.py`), including matched subtraction.
5. **V1 regression.** Gatekeeper reruns v0.5.0 `tests/gate_G1`, `gate_G2`, `gate_G3` from a clean shell against the current package; writes rows.

**C0 exit:** V1, V10, V11 rows pass; Tier 2 items each have a ledger row (`done` or `retired`, with reason); repository clean (`git status` empty); `CAMPAIGN_STATE.json` advanced to phase 1.

### Phase 1 · Reframe and preregister

- **F1 Scribe:** `PREREGISTRATION.md` with Section 1 verbatim (hypotheses, E1–E5, claim table), Section 2.2 coupling points with the four coefficients written out at both points, Section 2.5 matched-experiment rules, the KR search budget (rule 11) and the GI synthesis-sprint box (2.3) as frozen budgets, the mitigation arms, the shot policy, the prespecified defect classes (v0.5.0 Phase 5 list plus: "KR K-scan changes after a Hamiltonian fix → rerun V8, new C3 row"), and empty slots for the frozen backend, qubit path, time points, δ_dev table and hashes (filled at C5). `CLAIM_TABLE.md`. `GATE_THRESHOLDS.yaml` from Section 5 verbatim; record its SHA-256.
- **F1b:** `docs/refs/README.md` listing the two reference documents and the Sufian numbers used by V5–V6 (Appendix A of this file), so that a fresh child can find them without this prompt.
- **Orchestrator:** decide `HARDWARE_MODE` provisionally (v0.5.0 §9.1); write the campaign todo list (one item per phase and per validation).

**C1 exit:** preregistration hash present; thresholds hash present; claim table present; nothing else. Short session by design.

### Phase 2 · Reference extension (V2–V7)

Dispatch in background waves (slots permitting):

- **A2a Route A, four coefficients + j_max = 1 (already supported per the review) + static-charge option + 2×3 geometry.** API: `H(coeffs, jmax, geometry='1x1'|'2x3', static_charges=None|'corners')`; basis labels extended with the geometry's link and vertex lists (Appendix C label format generalizes: link tuple then vertex tuple, in the geometry's frozen order written to `00_conventions.md`).
- **A2b Route B, the same API, independently.** j_max = 1 needs a 9-state link register (4 qubits, codes 9–15 unphysical) or a direct 9-level sparse register; static charges are an extra spin-1/2 register at the charged vertices entering G^a_v as +B^a_v; 2×3 is 6 vertices, 7 links. Route B at 2×3 without static charges is 7 links × 5 states × 4⁶ matter = 320,000 raw states; with j_max = 1/2 only. j_max = 1 at 2×3 is **not required** this campaign (rule D-C2).
- **C2 Physics auditor:** from the conventions file alone, independent generating-function counts for every (geometry, jmax, static) combination in the V5/V7 table; the 2×3 count 1,727 recomputed by a third method (spin-network enumeration); bare energies at both coupling points; the P-S resonance check 2m = ¾ g_E in the report's units mapped to μ = 3/8 in ours.
- **A2c Exact dynamics at 2×3 (V7):** stretched-string initial state along the long way round on the 2×3 ladder (define it in `00_conventions.md`: quark on an even corner, antiquark hole on the adjacent odd vertex, flux along the five-link path; the review's N5 geometry), expm/Krylov evolution in the N = 6 sector at both coupling points; P_BB̄/P_meson versus t; K_min(t) curves; figures.
- **A2d Truncation (V4):** j_max = 1 versus 1/2 at the hardware time points of both coupling points, every primary observable, on one plaquette.
- **A2e Bridge dynamics (V6):** K-scan on STATIC-112 and STATIC-2,417 at P-S from the Sufian initial strings; this child gets the Sufian initial-state definitions from Appendix A and nothing from the KR arm's code (Phase 3 has not started).

**Gate C2 (gatekeeper):** V2 (both points), V3, V5 (all four counts), V6 (recorded pass, near-pass or fail; never a blocker), V7 (1,727 by three methods; dynamics file present; K_min curves present), V4 table present. Failure loop as v0.5.0 G1 (diagnosis child, route-owner fix, 45-minute box); route disagreement after the box → C2 partial, campaign continues on the route that passes the counts, no hardware in Phase 6 until resolved (rule D7).

### Phase 3 · Arm KR (V8)

- **A3a Krylov reduction library** `src/su2qc/krylov/`: Lanczos with full reorthogonalization in the N = 4 (or N = 6) sector; Q_K, H_K, O_K; K-scan per Section 2.4 returning the full K(t) curve; unit tests against expm at K = full dimension (must be exact to 10⁻¹²) and against the V6 bridge values.
- **A3b Synthesis:** exact `UnitaryGate` route and approximate ansatz route for every (point, t, K) that the scan accepts; acceptance per Section 2.4 against EXACT on OURS-82; report logical two-qubit count, and after routing on the frozen-or-fake backend the CZ count and depth for every candidate; keep the rejected candidates in `03_kr_arm/rejected.jsonl` with the failing criterion (the Sufian report's practice of preserving negative results is adopted).
- **A3c Layout search** per rule 11; ranked table; the "top ten share a structure" observation recorded true or false.
- **C3 Auditor:** recompute one accepted K(t) point by a different Krylov implementation (Arnoldi from scratch, no reorthogonalization trick), check O_K = Q†OQ against a direct expectation-value comparison, verify zero leakage by projecting Q_K's columns with the Gauss-law projectors.

**Gate C3:** at least one accepted KR circuit per (point, hardware time point) with the V8 row; K(t) curves at both points on OURS-82 filed; the rejected list present; the layout table present. If at P-A no K ≤ 38 passes at some time point (it must at K = 38, which is exact), record the K and the qubit count; a KR circuit with K > 16 (5 qubits) is still an arm, just an expensive one, and that is a result.

### Phase 4 · Arm GI REDUCED (V9, E1, E5)

- **A4a Surviving signal (review N7):** at both coupling points, for r ∈ {1, 2}, the per-observable Trotter error at every candidate time point and the G2 visibility test; choose the GI time points (≥ 2 per point; preliminary at P-A: {0.75, 1.5}/g_E; at P-S: τ ∈ {5, 12.5} if r = 1 passes the tolerance, which it should).
- **A4b Synthesis sprint** (Section 2.3, 4-hour box, one builder plus one auditor for leakage and unitary checks; the orchestrator closes the box on the clock, not on progress). Deliver `04_gi_arm/synthesis_sprint.md` with the best leak-free per-step count and every variant tried.
- **A4c Compile:** K1 Qiskit level 3 and K2 PyZX topology-preserving on the frozen path (K3 only if it was hardware-eligible in v0.5.0); compiled-versus-Strang equivalence 10⁻¹⁰; resource rows per (point, r, t).
- **A4d E5 synthesis at 2×3:** term groups for the 2×3 ladder from route A's four-coefficient H (7 hopping groups, 2 plaquette groups, diagonal layer); the same block-unitary construction, logical two-qubit count per step, **not routed, not run**.
- **C4 Auditor:** V9 items; the E1 table assembled with the four columns of rule 13; the E5 crossover computed from the C3 K(t) curves and the C4 counts, both plaquette and 2×3.

**Gate C4:** V9 rows; `E1_resource_frontier.md` complete for both arms at both points (NOISELESS accuracy columns filled); `E5_extensibility.md` with K(t, size) curves, GI counts at both sizes, the crossover statement, and the classical-dependence flag; the sprint closed on time with its number. **Decision row:** `GI hardware circuits = <routed CZ, depth> at (point, r, t)`. There is no Plan B in this campaign: a GI circuit that is too deep for a nonzero hardware signal is still submitted once (pilot), because a measured null at a stated depth is the price being measured (rule D-C4).

### Phase 5 · Matched design, twin, rehearsal, endpoint pre-test (V12)

- **A5a Measurement plan** per arm: GI diagonal setting plus the energy settings of v0.5.0 Phase 5 if the per-circuit budget permits (they may be dropped by the fit-to-cap rung; E2 needs only the diagonal setting); KR Pauli groups on n_q qubits; the matched t = 0 control per arm; the number of circuits and the QPU estimate for pilot + full + second window, both arms, three mitigation arms.
- **A5b Twin:** calibration-derived Aer twin (from the frozen backend snapshot) for every hardware circuit of both arms; δ_dev per (arm, observable, t) written to `05_design/delta_dev.json` and frozen into the preregistration; V10 rerun on the actual twin.
- **A5c Rehearsal (detached):** full pipeline on the twin for both arms, all three mitigation arms, EMULATED labels; E2 and E3 evaluated on EMULATED; V11 rerun on the real estimator code path.
- **Fit-to-cap rung (v0.5.0 §9.3 order, applied to both arms symmetrically; never drop one arm's repetitions below the other's).**
- **F5 Preregistration completed:** backend, qubit path (GI 12 + KR n_q, with the overlap rule of 2.5), time points, δ_dev table, shot allocation, hashes; signed.

**Gate C5:** V12 (E2 passes on EMULATED at ≥ 2 time points per arm; E3 sign pattern on EMULATED per arm reported); δ_dev frozen; preregistration hash; QPU estimate inside the cap and the approval file.

### Phase 6 · Hardware

Inherit v0.5.0 Phases 7–10 and §9 verbatim with these substitutions: "pilot" = both arms' t = 0 controls plus one time point per arm, M1 only, 3 × 2,048 shots; stop/go review checks per arm (GI: S3 codeword 3793 recovered above the readout floor, flags mostly zero, yield; KR: |0…0⟩ recovered, unused-codeword population at the readout floor); "full run" = both arms, all time points, all three mitigation arms (M2 dropped first by the rung), 5 × 4,096; "second calibration window" = the full run's diagonal setting repeated for both arms ≥ 24 h later (Sufian §18.4 item 2 adopted: replicate on a second calibration date), and a second backend if the cap allows. Submission blockers: v0.5.0 D7 plus rule 10 (both arms or nothing).

**Gate C6:** pilot PASS per arm (HARDWARE rows); full run returned and immutably exported; second window returned or its job IDs listed with the one-line analysis command.

### Phase 7 · Analysis (E1–E5, V13)

`07_analysis/`: `E1_resource_frontier.md` (final, with HARDWARE accuracy columns added); `E2_accuracy_table.md` per arm, observable, t, mitigation arm, with NOISELESS_arm − EXACT beside, pass/fail per row, and the accuracy-versus-routed-CZ figure with both arms and both calibration windows; `E3_trend_table.md`; `E4_gauge_detectability.md` (flag rates, yields, pre/post-selection deltas with 2σ; the KR "not measurable" row); `E5_extensibility.md` (final); `error_budget.md` per arm (truncation from V4; Trotter or Krylov from NOISELESS − EXACT; compile from compiled − Strang/unitary; device from EMULATED − NOISELESS and HARDWARE − EMULATED; shot from bootstrap); `drift.md` (window 1 versus window 2 per arm). **C7 auditor** recomputes one row of every table from `raw_immutable/` by an independent script (V13).

**Gate C7:** every table with the four columns of rule 13 and provenance; V13 rows; the three hypotheses each marked supported / refuted / not tested with the deciding numbers.

### Phase 8 · Paper, release, replication (V14)

- `08_release/PAPER_DRAFT.md`: title (working: *The price of exact gauge invariance: gauge-invariant versus Krylov-playback circuits for SU(2) with dynamical matter on a quantum processor*); abstract stating the cost ratio, the accuracy-versus-cost result, the gauge-detectability result, the K(t, size) growth and the crossover; methods (both arms, both points, the bridge to the static-charge model as the cross-validation against the Sufian report); results by E1–E5; the claim table with each row marked; limitations (one plaquette; two coupling points; single device family; the sprint box; what a 2×3 hardware run would add); data and code availability. The Sufian report is cited as the source of the KR method and of the negative ZNE and layout-search results; its 13-CZ number is quoted as its own, never as ours.
- `08_release/LIMITATIONS.md`, `CONTINUATION.md` (2×3 GI on Nighthawk-class hardware as the next step; Idea 2 syndromes on the redundant encoding as the natural follow-on of E4).
- `su2qc.replicate` completed; `replication_log.md` (fresh venv, `make reproduce`, hashes match).
- `CAMPAIGN_SUMMARY.md` (Section 9) and the memory pointer set to `complete`.

**Gate C8:** V14; paper draft, limitations, continuation, replication log present; every gate row of the campaign has an evidence path.

---

## 5. Gate thresholds (frozen at C1 into `GATE_THRESHOLDS.yaml`; never loosened)

| Gate | Criteria | Thresholds |
|---|---|---|
| C0 | V1 regression; V10 twin variance; V11 estimator; Tier 2 rows; clean repo | unchanged to 10⁻¹²; distinct counts and σ within 2× multinomial; 10⁻¹⁰; present; `git status` empty |
| C1 | preregistration, claim table, thresholds file with hashes | present |
| C2 | V2 at P-A and P-S; V3 counts 152/(3,36,74,36,3); V5 counts 112/(2,27,54,27,2) and 2,417/(4,119,597,977,597,119,4); V7 count 1,727 by three methods and route agreement; V4 table; V6 recorded | 10⁻¹²/10⁻¹⁰; exact; exact; 10⁻¹²; present; pass/near/fail (never blocking) |
| C3 | V8 per accepted KR circuit; K(t) curves both points; rejected list; layout table | infidelity ≤ 10⁻³, obs error ≤ 10⁻³, unused-codeword ≤ 10⁻⁵, leakage ≤ 10⁻¹²; present |
| C4 | V9; E1 draft; E5 draft; sprint closed ≤ 4 h; decision row | unitary 10⁻¹⁰; exponent [1.8, 2.2]; Trotter ≤ 0.05/0.0375; leakage ≤ 10⁻¹²; equivalence 10⁻¹⁰; present |
| C5 | V12; δ_dev frozen; preregistration signed; QPU estimate in cap | E2 on EMULATED at ≥ 2 t per arm; present; hash; ≤ cap |
| C6 | pilot PASS per arm (HARDWARE); full run exported; second window returned or listed | per-arm stop/go; hashes; present |
| C7 | tables complete with rule-13 columns; V13; hypotheses marked | present; 10⁻¹⁰ / bootstrap; present |
| C8 | V14; paper, limitations, continuation, replication log | hashes match; present |

Ledger row format, `source` values, and the rule that only the gatekeeper writes `pass` are inherited from v0.5.0 §7.

---

## 6. Decision rules added to v0.5.0 §13 (apply, log the rule number, never ask)

- **D-C0 Twin fix ambiguity.** If the twin's five repeats are distinct after removing the `seed_simulator = 101` override but σ is still zero at r = 0, the r = 0 circuit has no two-qubit gates and the readout-noise-only twin may be deterministic under the noise model's readout-error implementation: test at r = 1 as well; record which case applies.
- **D-C2 Scope of j_max = 1.** One plaquette only; 2×3 at j_max = 1 is out of scope; a request for it in any child summary is ignored and logged.
- **D-C3 KR arm at P-A too large.** If the smallest passing K at a P-A time point exceeds 32 (6 qubits) the arm is still built and costed; the E5 crossover statement uses it; hardware submission of that circuit follows the same rules as any other (it is unlikely to be cheaper than GI, which is the finding).
- **D-C4 GI arm too deep for signal.** Submit the pilot anyway (one time point, M1). If the pilot's t = 0 control recovers 3793 above the floor but the t > 0 observables are consistent with the fully mixed state within 2σ, the full run of the GI arm is reduced to the shortest time point at r = 1 and the null is reported as the measured price with its depth; the KR full run proceeds in full.
- **D-C5 Cap too small for both arms.** Apply the fit-to-cap rung symmetrically; if even the last rung does not fit both arms, submit neither (rule 10), report EMULATED for both, and leave the ready command.
- **D-C6 Second backend unavailable.** The second calibration window on the same backend ≥ 24 h later satisfies the replication requirement; a second backend is optional.
- **D-C7 Sufian bridge fails (V6 outside ±2).** Not a blocker; list the joint phase convention and the initial-state definition as candidate causes; the KR arm on OURS-82 is validated by V8 against our own exact reference regardless.
- **D-C8 Review item without a stated method (N6, W̄ estimator).** Time-box 1 h in Phase 2; if unresolved, report μ* by the bare crossing and the two v0.5.0 dynamical estimators only, and mark N6 `retired` with the reason.

---

## 7. Session protocol (how the campaign proceeds step by step)

`CAMPAIGN_STATE.json` in `$REPO/runs/campaign_v060/` holds: `phase`, `gates` (id → pass/fail/partial, utc, evidence), `hashes` (thresholds, preregistration, conventions), `sessions` (list of tag, t0, phase, outcome), `hardware` (mode, backend, job IDs), `next_action`.

**Every session, in order:**

1. **Boot (≤ 20 min).** Record T0 and the session tag `c060_p<phase>_<YYYYMMDD>[_n]`. Read `CAMPAIGN_STATE.json`; a launch message "Run phase n" must match `phase` or be n = phase (a mismatch is logged and the file wins). Verify the three hashes against the files. Environment probe as v0.5.0 Phase 0 step 2. Create the watchdog and `RESUME_LOCK` (v0.5.0 §10.5). Reload skills if any.
2. **Regression (rule 12).** Gatekeeper reruns every previous gate's test directories (`tests/gate_C0..C<phase−1>` and, from C0 on, the v0.5.0 G1–G3 tests) from a clean shell; cached long tests are accepted only if the hash of every file they read is unchanged. Any failure halts the phase: the session becomes a repair session for that gate (time box 2 h), and if unrepaired it stops with the failure as the summary's first line.
3. **Phase work** per Section 4, with the v0.5.0 operating model: background waves, two-stage review, physics audit, hourly `PHYSICS_STATUS.md` (the P-list for this campaign is E1–E5 plus V-items of the phase), 30-minute checkpoints, `wait_for_done.sh` loop, no early turn end before the gate or the session cutoff.
4. **Gate.** Gatekeeper child; rows appended; `CAMPAIGN_STATE.json` updated; commit `campaign: C<k> <pass|fail|partial> <one line>`.
5. **Stop or continue.** Default `STOP_AT: phase`: write `SESSION_SUMMARY.md` (Section 9), update memory, delete the watchdog, end the session. With `AUTOPILOT: true` in `CONFIG.resolved.yaml`, continue to the next phase inside the same session while the session cutoff (default 12 h, hard) allows; Phase 6 always stops after submission so a human sees the job IDs.

Session budgets in Section 4 are targets; the hard session cutoff is 12 h. A phase not gated by its budget continues in the next session from its artifacts; a phase not gated after two sessions triggers the re-plan protocol (v0.5.0 §10.4) with the scope-cut ladder below.

**Scope-cut ladder for this campaign (in order; never loosen a threshold; never drop an arm, a coupling point, the bridge counts V5, or the regression step):** drop M2 (ZNE) → drop the energy settings → drop the second backend (keep the second window) → drop V6 bridge dynamics (keep V5 counts) → reduce the KR layout search to one backend × 3 levels × 20 seeds → reduce 2×3 dynamics to one coupling point (P-A) → reduce hardware time points to one per point per arm → run replication in the existing environment and say so.

---

## 8. Deliverables tree (`$REPO/runs/campaign_v060/`)

```
CAMPAIGN_STATE.json  CONFIG.resolved.yaml  GATE_THRESHOLDS.yaml  GATE_LEDGER.jsonl  PREREGISTRATION.md  CLAIM_TABLE.md
00_conventions.md (copied from the last v0.5.0 run, extended for 2x3 and static charges)
sessions/<tag>/  ENV.md  RUN_LOG.md  TIME_LEDGER.md  PHYSICS_STATUS.md  SESSION_SUMMARY.md  RESUME_LOCK
00_repair/       twin_fix.md  tier2_ledger.md
02_reference/    route_A/ route_B/ agreement_{PA,PS}.json  jmax1/  bridge/{static112,static2417}/  ladder_2x3/{counts,dynamics,kmin}/  truncation_{PA,PS}.json
03_kr_arm/       kscan_{PA,PS}.json  circuits/  rejected.jsonl  layout_search.md  validation_V8.jsonl
04_gi_arm/       surviving_signal.md  synthesis_sprint.md  circuits/  compile/{K1,K2}/  E1_resource_frontier.md  E5_extensibility.md  ladder_2x3_counts.md
05_design/       measurement_plan.md  delta_dev.json  twin/  rehearsal_EMULATED/  fit_to_cap.md
06_hardware/     backend_snapshot_*.json  dryrun/  pilot/  full/  second_window/  raw_immutable/  jobs.log  poll_jobs.py
07_analysis/     E1..E5 tables  error_budget.md  drift.md  figures/  audit/
08_release/      PAPER_DRAFT.md  LIMITATIONS.md  CONTINUATION.md  replication_log.md  requirements.lock  Makefile
tests/           gate_C0 ... gate_C8  (one directory per gate; one command each; thresholds read from GATE_THRESHOLDS.yaml)
docs/refs/       (repo-level) v050_review_20260907.md  sufian_overlap_20260907.md  README.md
```

Reusable code goes into `src/su2qc/` (`hamiltonian/` with the four-coefficient API, `krylov/`, `circuits/`, `analysis/`, `replicate.py`) with tests; the run directory holds configurations, results and logs.

---

## 9. Session summary (`SESSION_SUMMARY.md`, under one page) and campaign summary

1. One sentence: what this session established, or the first failing regression if rule 12 fired.
2. Phase gate row(s): pass/fail/partial with the deciding numbers and evidence paths.
3. Validation table: each V-item of the phase with its value, threshold, source.
4. Headline numbers so far: the per-step GI count (logical, routed), the best KR count per (point, t), the current cost ratio, K(t) at both points, the E5 crossover if computed, δ_dev if frozen, hardware job IDs if any.
5. What the next session will do first (the `next_action` field, verbatim).
6. Anything the human must know before trusting a number.

`CAMPAIGN_SUMMARY.md` (Phase 8) is the same six items over the whole campaign, plus the three hypotheses with verdicts and the claim table with every row marked.

---

## Appendix A · Reference numbers from the Sufian report used by V5–V6 (do not treat as our results)

Model: KS SU(2), hard-core j_max = 1/2, staggered two-color fermions, two static fundamental (j_b = 1/2) background charges entering Gauss's law as +B^a_v. Couplings in the report's units: H_E = g_E Σ E², w = g_B = 1, g_E = 50, m = 18.75 (2m = ¾ g_E). One plaquette: static charges at v0 (bottom-left) and v2 (top-right); staggered vacuum occupations (n0, n1, n2, n3) = (0, 2, 0, 2); minimal strings (j0, j1, j2, j3) = (½, ½, 0, 0) lower and (0, 0, ½, ½) upper; dimensions by N = 0, 2, 4, 6, 8: 2, 27, 54, 27, 2 (total 112); K = 16 accepted over 0 ≤ t ≤ 5, K = 6 at t = 0.25. Two adjacent plaquettes: 6 sites, 7 links, static charges at v0 and v5; dimensions by N = 0…12: 4, 119, 597, 977, 597, 119, 4 (total 2,417); three shortest three-link strings (indices 630, 426, 127 in the report's basis; 630 is the initial state); fixed-window K = 128 for 0 ≤ t ≤ 5; time-adapted K = 4 at t = 0.10 (2 qubits, 3 CZ) and K = 8 at t = 0.25 (3 qubits, 27 CZ exact / 13 CZ approximate). Acceptance: 1 − F ≤ 10⁻³, max observable error ≤ 10⁻³. Hardware: IBM Kingston qubits {82, 83, 96}; mitigation finding: scale 1 for five observables, linear ZNE for endpoint screening only, quadratic ZNE rejected; matched-error reduction 35.3 % (one plaquette) and 48.6 % (two plaquettes) from 27 → 13 CZ. Report time t = 0.25 at g_E = 50 corresponds to τ = t·g_E = 12.5 in our electric units; t = 0.10 to τ = 5.

## Appendix B · References the paper must cite

The v0.5.0 Appendix D list, plus: Sufian, *2+1D SU(2) Gauge Dynamics*, working research-group report, 25 Aug 2026 (the KR method, the static-charge model, the mitigation and layout-search negative results); the SU2QC v0.5.0 status review (7 Sept 2026); the overlap analysis (7 Sept 2026).

---

**Start now.** Record T0, read `CAMPAIGN_STATE.json` (create it at phase 0 if absent), run the regression step, then the phase. The campaign is judged on E1–E5, on the honesty of the ledger, and on whether a physicist can rebuild every number from the tree.


## Source: prompts/v0.5.0.md
---
name: su2qc-section8-overnight
version: 0.5.0
file: SU2ZX/prompts/su2qc_section8_overnight_v.0.5.0.md
scope: Sections 7–8 of "SU2QC Nine-Month Plan" (prepared 7 Sep 2026): the rebuilt one-month project, executed end to end in one night
budget: 12 h target · 16 h hard stop
solutions_series: solutions/0.5.0.md, solutions/0.5.1.md, … (escalation solutions written by Claude Fable 5.1 during this run; solutions/0.4.0.md is the current last one)
---

# SU2QC Section 8 Overnight — SU(2) with dynamical matter on one plaquette, end to end in 12 hours

> Launch (unattended, survives SSH disconnects from a phone):
> ```bash
> cd ~/SU2ZX
> tmux new -d -s su2 'hermes --yolo chat -q "$(cat prompts/su2qc_section8_overnight_v.0.5.0.md)" 2>&1 | tee -a launch_$(date -u +%Y%m%dT%H%MZ).log'
> tmux attach -t su2      # detach with Ctrl-b d
> ```
> Adjust flags to your Hermes version. The run must never wait for an interactive approval.

---

## 0. Mission and stance

You are the **Hermes orchestrator** for one unattended night on the `SU2ZX` repository. Execute **Section 8 of the SU2QC Nine-Month Plan** ("The rebuilt one-month project: SU(2) with dynamical matter on one plaquette") **all the way through**: the 82-state Hamiltonian by two independent routes, exact dynamics and the string-breaking resonance, three encodings with leakage flags, symmetry-verified Strang circuits, compilation and noisy simulation, measurement design and a signed preregistration, dry run, pilot, full run (real hardware if enabled, otherwise a calibrated noise-model twin), analysis with a decomposed error budget, ablations, and a research report with the claim table — in **12 hours**, extendable to **16 hours** only under §1.4.

**Section 7's verdict is your operating stance.** The GPT-5 monograph built an excellent verification scaffold (Trotter/compiler/device error separation, preregistered gates and claim table, frozen qubit path/seeds/shots/mitigation, six-basis energy reconstruction to 1e-10, correct handling of readout-mitigated quasiprobabilities, dry-run-first submission, bootstrap analysis, tensor-network cross-checks, and one real compiler finding: the topology-preserving PyZX pass cut 118 native ECR gates to 94 while unrestricted full reduction inflated the routed count to 180) around the wrong scientific object (a 5-qubit pure-gauge chain, no matter, no string, no Gauss-law syndrome). **Keep the scaffold, change the object, demote the compiler comparison to a secondary endpoint.** Reuse the monograph code wherever it exists in this repo; do not rewrite what already works.

### 0.1 The physics north star (every phase serves this)

The hypothesis you are testing tonight, verbatim from Section 8.1 with the numbers you will freeze at preregistration:

> For the hardcore-gluon SU(2) single-plaquette patch with four staggered two-color fermion sites (82 gauge-invariant states, 12 qubits in a local gauge-invariant encoding), a symmetry-verified second-order product-formula evolution on a Heron-class IBM device reproduces the exact pair-creation and Casimir-reduction dynamics of a flux string within 2σ over at least four time points, with leakage-flag post-selection retaining at least 20 percent of shots, at most about 250 CZ per Strang step, two or three Strang steps per circuit, at most about 1,000 CZ per circuit including state preparation and basis changes, and two-qubit depth below about 200.

The science this must deliver, in priority order:

1. **Gauge invariance by construction.** Every product-formula factor is itself gauge invariant (electric+mass, each covariant hopping term, the plaquette) and is synthesized as an exact block unitary, never re-split into non-commuting Pauli strings. Consequence: Trotter error never leaves the physical subspace, a noiseless simulation of the compiled circuit returns **exactly zero** leakage, and every leakage/Gauss-law violation seen on the device is hardware-induced. This is a unit test of the compile pipeline and the foundation of the "symmetry-verified" claim.
2. **The non-Abelian channel structure of string breaking.** The stretched string has two competing decays: coherent shortening (magnetic term) and breaking by pair creation into two mesons; the baryon–antibaryon channel is a distinctively non-Abelian signature. The exact resonance near m = 3g²/(16a) and the meson-versus-baryon split are the physics the hardware (or twin) must reproduce.
3. **The resource frontier with a decomposed error budget**: what it costs, in qubits and two-qubit depth, to evolve SU(2) with fundamental matter on a plaquette on today's hardware, with error split into truncation, Trotter, compile, device, and shot contributions.
4. **Honest claim boundaries.** The patch is exactly solvable; the hardware adds no knowledge about SU(2). The claim table of Section 8.3 appears in the report verbatim and is filled truthfully. "2+1D" is reserved for the 2×3 ladder and beyond.

### 0.2 Non-negotiables

- **Clock.** 12 h target. Freeze at T+15:00, hard stop at T+16:00. Packaging (§9) happens unconditionally.
- **Gates are scripts, not opinions.** A gate passes only when `gates/gate_<G>.py` exits 0 and writes `gates/GATE_<G>.json` with every criterion's target and measured value. Reviewer sign-off is additionally required where marked. Never edit a gate script to make it pass; never relax a tolerance silently (documented relaxations with root cause are allowed only where §6 says so).
- **Independence is real.** The two Hamiltonian routes are built by two different agents in two different files that share nothing but `conventions.py`. Reviewers use a different model than builders.
- **Preregister before production.** No production run (hardware or twin) before `prereg/PREREG.md` is signed with a config hash. After signing, changes only through `prereg/CHANGELOG.md` and only for prespecified defects.
- **Never present emulated results as hardware.** Every result carries `mode: hardware | twin`.
- **Multiple efforts at all times.** From T+0:20 to the freeze there are always ≥ 2 lanes active (§3); the orchestrator never idles waiting on a single subagent when other work is unblocked.
- **Everything on disk, the report is never blank.** `reports/REPORT.md` is updated at every gate so that a hard stop still leaves a coherent document.
- **No fabricated numbers.** Every number in a report points to an artifact path produced by code.

---

## 1. Clock, heartbeat, budgets, extension

### 1.1 Run identity and clock

```bash
cd ~/SU2ZX
export RUNID=$(date -u +%Y%m%dT%H%MZ)
export RUN=runs/section8_v0.5.0_${RUNID}
mkdir -p $RUN/{run,src/su2qc,tests,gates/attempts,physics,reviews,circuits,compile,prereg,hardware/raw,analysis/{tables,figures},reports,logs/{agents,cmd},env}
date -u +%s > $RUN/run/T0
sha256sum prompts/su2qc_section8_overnight_v.0.5.0.md > $RUN/run/PROMPT_HASH
cat > $RUN/bin_clock.sh <<'EOF'
#!/usr/bin/env bash
T0=$(cat "$(dirname "$0")/run/T0"); NOW=$(date -u +%s); E=$((NOW-T0))
printf "elapsed %02d:%02d | to 12h %+d min | to freeze(15h) %+d min | to stop(16h) %+d min\n" \
  $((E/3600)) $((E%3600/60)) $(( (43200-E)/60 )) $(( (54000-E)/60 )) $(( (57600-E)/60 ))
EOF
chmod +x $RUN/bin_clock.sh
```

Print the clock at the start of every orchestrator turn. All deadlines below are relative to T0.

### 1.2 Heartbeat (every 30 minutes, no exceptions)

Append to `$RUN/run/HEARTBEAT.md`: elapsed, current phase, active lanes and their agents/models, gate ledger snapshot (from `run/GATES.md`), open risks, the next decision time, QPU seconds spent. If a notification channel is configured (`SU2ZX_NOTIFY=1`), send a 3-line summary at: T0, every gate outcome, every escalation, immediately before any hardware submission, at freeze, at stop. Never block waiting for a human reply; if one arrives, incorporate it.

### 1.3 Budgets (environment; defaults in parentheses)

```
SU2ZX_TARGET_HOURS (12)        SU2ZX_HARD_STOP_HOURS (16)
SU2ZX_HW (0)                   # 1 = real IBM hardware allowed for pilot/full run; 0 = twin mode
SU2ZX_BACKEND (unset)          # Heron-class backend name; unset → fake Heron target (§7)
SU2ZX_HW_BUDGET_SEC (600)      # QPU-seconds cap for the entire night
SU2ZX_HW_MAX_SHOTS_PER_JOB (8192)
SU2ZX_HW_OVERRIDE_G1 (0)       # 1 = allow hardware even if only one Hamiltonian route passed (§4.4)
SU2ZX_MAX_CONCURRENT_AGENTS (3)  # raise to 4–5 if your delegation config permits
SU2ZX_ESCALATION_MODEL (claude-fable-5-1)   # Anthropic; highest effort/thinking setting your provider exposes
SU2ZX_NOTIFY (0)
```

Record the effective values in `$RUN/run/CONFIG_ENV.md` at G0.

### 1.4 Extension policy (12 h → up to 16 h)

At **T+11:00** write `run/EXTENSION.md` with one of:

- **Finish at 12 h**: G7 and G8 are passed or failing only on non-critical criteria → proceed to packaging.
- **Extend**: allowed only if (a) a critical-path gate (G1, G3, G4, G7) is still failing **and** an escalation solution with a concrete implementation plan exists, or (b) hardware jobs are queued or running and their results are the primary endpoint. Name the gates, the plan, and the expected finish. Polish, extra ablations, and nicer figures are never reasons to extend.
- Hard rules: no new escalations after **T+14:00**; all lanes except packaging are cancelled at **T+15:00** (freeze); packaging starts no later than T+15:00 even if it must ship a partial state; **T+16:00** is the absolute stop.

---

## 2. Team: roles, model routing, delegation mechanics

### 2.1 Roles and routing

| Role | Model / provider | Toolsets | What it does |
|---|---|---|---|
| **Orchestrator** | this Hermes session | all | owns clock, task board, gate ledger, delegation, escalations, hardware policy; writes little code itself |
| **Builder** (several) | Codex (`openai-codex` provider, or the `codex` CLI if installed) | terminal, file | implements one module each, with tests; owns disjoint files |
| **Code reviewer** | strongest coding model on NIM (`nvidia` provider) — **must differ from the builder's model** | file (+ terminal for running tests) | reviews against the checklist in Appendix C; blocking findings must be fixed before a gate |
| **Physics reviewer** | strongest reasoning model on NIM; for gate-critical derivations (G1, G2, G5) Claude Fable 5.1 at normal effort | file | "predict before compute": derives the expected numbers independently, signs off gates, adjudicates convention disputes |
| **Gatekeeper** | no LLM — deterministic scripts | — | `gates/gate_<G>.py`, `pytest -m gate`, the only thing that can mark a gate PASS |
| **Scribe** | a cheap fast model, or the orchestrator | file | keeps `reports/REPORT.md`, `run/TASKBOARD.md`, `run/GATES.md`, `MANIFEST.json`, heartbeat current |
| **Escalation** | Claude Fable 5.1, maximum effort/thinking (`SU2ZX_ESCALATION_MODEL`) | file (read-only) | writes `solutions/0.5.x.md` **only**; never edits code |

Record the exact model ids each role actually ran with in `$RUN/run/MODELS.md` (from the child summaries/config). If per-role model selection through `delegate_task` does not take effect in your Hermes version, spawn role sessions from the terminal instead and log their output:

```bash
hermes --yolo chat -q "$(cat $RUN/logs/agents/<task>.prompt.md)" -m "<model>" --provider <nvidia|openai-codex|anthropic> \
  > $RUN/logs/agents/<task>.out.md 2>&1 &
```

If the escalation model is unreachable, use the strongest reasoning model available (NIM or Codex, maximum reasoning), state the substitution in the solution file header, and continue.

### 2.2 Delegation mechanics (Hermes `delegate_task`)

Subagents start with **no context**: they know nothing about this prompt, the plan, or earlier turns. Every delegation must carry: `$RUN` and the repo path; the conventions file path; the exact files the agent owns (and that it must not touch others); the acceptance command and expected numbers; the return format (what changed, how it was tested with numbers, open issues, files written); the time box. Run batches at the maximum concurrency your configuration allows (`SU2ZX_MAX_CONCURRENT_AGENTS`). Prefer asynchronous delegation so you keep orchestrating. Only the child's summary enters your context — keep it that way; do not paste large files into delegations, point to paths. Template in Appendix B.

### 2.3 File ownership and the task board

`$RUN/run/TASKBOARD.md` is the single source of truth: `id | lane | owner (role/model) | status | inputs | outputs | deadline (T+) | gate`. Two agents never own the same file. Integration is the orchestrator's job (or a dedicated integrator builder) and happens through the test suite, not through shared editing.

---

## 3. The parallel efforts (lanes) and the iteration loop

These lanes exist for the whole night; a lane with nothing to do is a scheduling bug, fix it.

| Lane | Owner | Continuous output |
|---|---|---|
| **BUILD** | Codex builders | modules in `src/su2qc/`, tests in `tests/` |
| **VERIFY** | gatekeeper scripts + a Codex test-writer | `tests/`, `gates/`, `pytest -m gate` run at least every 60 min and at every gate |
| **REVIEW-CODE** | NIM reviewer | `reviews/<phase>_<file>_<n>.md`; blocking vs advisory findings |
| **REVIEW-PHYSICS** | NIM reasoning / Fable normal effort | `physics/predictions_<G>.md` before code runs; `physics/signoff_<G>.md` after |
| **SCRIBE** | scribe | live `reports/REPORT.md`, ledgers, heartbeat, manifest |
| **OPS** | orchestrator | clock, delegation, escalations, hardware policy, decisions in `run/DECISIONS.md` |

**Iteration loop per deliverable** (one pass = one *attempt* for gate accounting):

```
BUILD → builder self-test → [REVIEW-CODE ∥ REVIEW-PHYSICS] → fix blocking findings → gate script → PASS / FAIL
```

Reviews start the moment a builder returns, in parallel with the next build. Physics predictions for gate G are written **before** the corresponding code finishes so that the code is checked against numbers it did not produce.

Pipelining rule: while gate G is being reviewed/tested, the builders for G+1 are already running against the best current artifact (stub Hamiltonian, draft circuit family), then re-run when G passes.

---

## 4. Gate protocol and escalation

### 4.1 Definitions

- **Gate**: a script + JSON as in Appendix D, plus sign-off where §6 says so.
- **Attempt**: one full iteration loop ending in a gate-script run. Record each in `gates/attempts/<G>_attempt<n>.md` (what was tried, numbers, why it failed).
- **Deadline** and **latest**: each gate has a target time and a latest time (§6). Missing the latest time triggers the gate's fallback (§4.4) unless §1.4 extension applies.

### 4.2 Two attempts, then escalate

1. Attempt 1 fails → attempt 2 with the reviewers' findings and a different hypothesis (not a rerun).
2. Attempt 2 fails → **escalate**: assemble the escalation packet (Appendix E), invoke Claude Fable 5.1 at maximum effort, and have it write the next solution file in `solutions/` — the **first** escalation of this run writes **`solutions/0.5.0.md`**, the next `solutions/0.5.1.md`, then `0.5.2.md`, … (never overwrite; each later file references the earlier ones). Template in Appendix E.
3. Then delegate a **fresh** builder group (new subagents, fresh context) to implement exactly the written solution, with the solution file path in their context; reviewers check the implementation against the solution's acceptance test; the attempt counter for that gate resets to 0 (max 2 more attempts).
4. Still failing → escalate again (next version), attaching the prior solution and why it did not work. Maximum **3 escalations per gate**, **6 per run**, none after T+14:00. Exhausted → apply the gate fallback (§4.4) and record it in `run/DECISIONS.md` and the report.
5. While an escalation is being written, the other lanes keep working; never idle.

Escalation is for gates, not bugs: ordinary defects are fixed by builders; ordinary physics questions go to the physics reviewer at normal effort.

### 4.3 What the orchestrator does when the prompt's expected numbers and the code disagree

The expected numbers in §5 were derived for this prompt. If both Hamiltonian routes agree with each other but disagree with a number here, trust the code, have the physics reviewer show the derivation, and record the discrepancy prominently in `physics/DISCREPANCIES.md` and the report. Never force code to match this prompt.

### 4.4 Gate fallbacks (kill criteria)

| Gate | If still failing after escalations |
|---|---|
| G1 | Proceed with the route that passes all limit tests, the count, and gauge-invariance checks; the other route is reported as failed with the discrepancy as the top finding. Twin runs allowed. **Real hardware requires both routes agreeing** unless `SU2ZX_HW_OVERRIDE_G1=1`. |
| G2 | Use the tree-level resonance m = 3g²/16 (a = 1) and the best available window; note it. |
| G3 | Drop the failing encoding. If every encoding fails exact block-unitary synthesis, fall back to Pauli-string Trotterization of each grouped term: this reintroduces coherent gauge drift, noiseless leakage is no longer zero, and the "symmetry-verified" claim is weakened — measure it, report it. |
| G4 | **Plan B (Section 8.5)**: pure-gauge plaquette chain with two static fundamental charges; flux-tube energy and Casimir profile between the charges for separations of one to four plaquettes; reuse everything built so far; the with-matter patch stays simulator-only tonight and is reported as such with its resource table. |
| G5–G6 | No hardware tonight; twin only; hardware phases marked "prepared, not submitted". |
| G7 | Pilot no-go: fix only prespecified defects once; if still no-go, twin results are primary and hardware is "attempted, not passed" with job ids. |
| G8–G9 | Ship what exists; mark every gap explicitly. |

---

## 5. Physics specification (frozen at G0 in `src/su2qc/conventions.py`)

### 5.1 Model

Lattice units a = 1. One square plaquette, open boundaries: vertices v1=(0,0), v2=(1,0), v3=(1,1), v4=(0,1); parity (−1)^{x+y}: v1, v3 even; v2, v4 odd. Links ℓ1: v1→v2 (x, y=0), ℓ2: v2→v3 (y, x=1), ℓ3: v4→v3 (x, y=1), ℓ4: v1→v4 (y, x=0); plaquette U_□ = U_ℓ1 U_ℓ2 U_ℓ3† U_ℓ4† (counter-clockwise v1→v2→v3→v4→v1). Staggered phases η_x = 1, η_y = (−1)^x. Two-color staggered fermions ψ_v (color doublet) at each vertex.

```
H = (g²/2) Σ_ℓ E_ℓ²  +  m Σ_v (−1)^{x_v+y_v} ψ†_v ψ_v
  + (1/2) Σ_ℓ ( η_ℓ ψ†_{s(ℓ)} U_ℓ ψ_{t(ℓ)} + h.c. )  −  (1/(2g²)) Tr( U_□ + U_□† )
```

E² = j(j+1) per link; truncation **j ∈ {0, ½}** (hardcore gluon); j_max = 1 is built too, for the truncation-error statement. Each matter site has four Fock states: color-singlet vacuum (n=0), doublet (n=1), doubly occupied singlet = baryon (n=2). Staggered vacuum: even sites empty, odd sites full (n = 0, 2, 0, 2). Local charge relative to it: q_v = n_v − n_vac(v); quark = +1 on even, antiquark = −1 on odd, baryon = +2 on even, antibaryon = −2 on odd.

### 5.2 Expected numbers (derived for this prompt; the physics reviewer re-derives them before G1 code is trusted)

- A 2-valent vertex with incident links (j_a, j_b) has f(j_a,j_b) gauge-invariant local states: **2** if j_a = j_b (matter singlet: vacuum or baryon), **1** if j_a ≠ j_b (matter doublet). Local states per vertex: 2+1+1+2 = **6 → 3 qubits**.
- Total gauge-invariant dimension = Tr(T⁴) with T = [[2,1],[1,2]] (eigenvalues 3, 1): **82** at j_max = ½. At j_max = 1, T = [[2,1,0],[1,2,1],[0,1,2]] (eigenvalues 2±√2, 2): **152**.
- Total fermion number N = Σ n_v commutes with H; only **even N** occurs. Sector dimensions N = 0, 2, 4, 6, 8: **2, 20, 38, 20, 2**. The baryon-number-zero sector (N = 4, the staggered vacuum's sector) is **38**-dimensional and contains all string-breaking dynamics.
- Pure-electric limit (g² → ∞, before the mass term splits levels): degeneracies by number k of j = ½ links, k = 0…4: **16, 16, 18, 16, 16** (sum 82).
- Frozen-matter limit (m → ∞): exactly **2** states (all links 0 or all links ½, matter at the staggered vacuum); the 2×2 effective Hamiltonian must equal the monograph's one-plaquette H̃₁ after a documented normalization reconciliation.
- Tree-level resonance: removing one link of j = ½ flux releases (g²/2)(3/4) = 3g²/8, equal to the pair cost 2m at **m* = 3g²/16** (= 3g_E/8 in Cataldi et al.'s H_E = g_E Σ E²). Finite-size shift expected; locate it numerically.

### 5.3 States and channels (all diagonal in the gauge-invariant occupation basis)

- **Stretched string** (initial state): (j_ℓ1, j_ℓ2, j_ℓ3, j_ℓ4) = (0, ½, ½, ½), n = (1, 1, 0, 2), q = (+1, −1, 0, 0): quark on v1, antiquark on v2, joined by the three-link path. A unique basis state (2-valent intertwiners are unique).
- **Short string**: (½, 0, 0, 0), same n.
- **String survival** P_surv = projector onto q = (+1, −1, 0, 0) = stretched + short (a 2-dimensional projector).
- **Meson channel** P_meson = projector onto |q_v| = 1 for all v: the two states with links (0, ½, 0, ½) and (½, 0, ½, 0), i.e. two separated mesons.
- **Baryon–antibaryon channel** P_BB̄ = projector onto states with some |q_v| = 2 (a doubly occupied even vertex and/or a doubly empty odd vertex); takes precedence over meson in mixed states.
- **Other** = 1 − P_surv − P_meson − P_BB̄ within the N = 4 sector (report it; it must be small but is not zero).
- **Casimir per link** E²_ℓ = (3/4)[j_ℓ = ½]; Casimir reduction ΔC(t) = Σ_ℓ⟨E²_ℓ⟩(t) − 9/4.
- **Site-resolved density** ⟨n_v⟩(t); pair-creation onset = ⟨n_3⟩ and ⟨2 − n_4⟩.
- **Energy** ⟨H⟩ (conserved exactly, not by the product formula; needs extra measurement settings); **leakage-flag rate** ℓ.

### 5.4 Encodings

| Code | Qubits | Physical codes | Leakage flags (all diagonal) | Role |
|---|---|---|---|---|
| **L12** local gauge-invariant | 12 (3 per vertex: link-bit a, link-bit b, matter bit c) | 82 | per vertex: (a⊕b)∧c = 1 is unphysical (2 of 8 codes); per link: the two copies of a link bit must agree (4 link-consistency flags) | primary hardware encoding per the plan |
| **S8** shared-link | 8 (4 link qubits + 4 matter-class qubits) | 82 of 256 | per vertex (a⊕b)∧c = 1, with a, b the vertex's two link qubits | reduced encoding; permitted as primary if L12 misses the depth budget (§6, G4) |
| **C7** compact global | 7 | 82 of 128 | 46 unused codes | simulator-only benchmark |

Matter bit convention (L12, S8): links agree → c = 0 vacuum, c = 1 baryon; links disagree → c = 0 doublet, c = 1 **leakage**. With this convention every observable in §5.3 is a function of the computational basis, so all primary observables come from the Z-basis setting.

### 5.5 Term grouping and circuit structure

Gauge-invariant groups: D = electric + mass (diagonal, phases), h_ℓ1…h_ℓ4 (covariant hopping; {h_ℓ1, h_ℓ3} commute and {h_ℓ2, h_ℓ4} commute, so each pair is one parallel layer), B = plaquette. Strang step: e^{−iDδt/2} · [h layers, δt/2] · e^{−iBδt} · [h layers reversed, δt/2] · e^{−iDδt/2}; merge adjacent half-steps across repeated steps. Each group is exponentiated as an **exact block unitary** on the encoded space, using structure rather than generic synthesis: B is a class-dependent generalized flip (link bits flip together, the coefficient is a product of vertex factors that depends only on the domain-wall pattern and possibly signs) → fan-out CNOT ladder + a uniformly-controlled rotation on the minimal control set found numerically; each h_ℓ decomposes into small (≤3×3) blocks on the n_v + n_{v'} = const subspaces. Time series = circuits with r = 0, 1, 2, 3 Strang steps (t = 0, δt, 2δt, 3δt) → four time points.

### 5.6 Route definitions (G1)

- **Route 1 — analytic** (`src/su2qc/ham/route_spinnet.py`): spin-network / loop-string-hadron / dressed-site coefficients (Clebsch–Gordan and 6j), including fermionic parity strings; produces H_½ (82×82) and H_1 (152×152) as sparse matrices plus the labeled basis. Must not import route 2.
- **Route 2 — numeric** (`src/su2qc/ham/route_gausskernel.py`): the redundant Kogut–Susskind formulation — links in the |j, m_L, m_R⟩ electric basis (5 states at j_max = ½, 14 at j_max = 1), matter as 8 Jordan–Wigner modes in the frozen order (v1c1, v1c2, v2c1, v2c2, v3c1, v3c2, v4c1, v4c2) — i.e. the 20-qubit-equivalent space; Gauss generators G^a_v; H projected onto the Gauss-law kernel (block by link-j sector and fermion number; vertex-local null spaces are the recommended algorithm). Must not import route 1. Must verify ‖[G^a_v, H_term]‖ = 0 for every term and the kernel dimension 82 / 152.
- **Comparison** (`src/su2qc/ham/compare.py`, verifier-owned): basis-independent — sorted spectra at ≥ 5 coupling points including m = 0, and observable time series from the stretched string (constructed in route 2 by applying the gauge-invariant string operator ψ† U U U ψ to the gauge-invariant staggered vacuum).

---

## 6. Phase plan: thirty days → twelve hours

Time windows overlap on purpose (pipelining). "Latest" is when the fallback fires.

| Phase | Plan days | Window | Lanes running in parallel | Gate (target / latest) |
|---|---|---|---|---|
| 0 Bootstrap | — | T+0:00–0:20 | OPS, SCRIBE | G0 0:20 / 0:30 |
| 1 Hamiltonian | 1–3 | 0:20–2:00 | B-route1, B-route2, P-predictions, B-encodings-scaffold, B-analysis-scaffold | G1 2:00 / 2:45 |
| 2 Exact dynamics | 4–6 | 2:00–3:30 | B-dynamics, B-scan, P-review, B-strang (starts) | G2 3:30 / 4:15 |
| 3 Circuits | 7–9 | 3:00–5:30 | B-L12, B-S8, B-C7, V-unitary-checks, R-code | G3 5:30 / 6:15 |
| 4 Compile + noise | 10–12 | 5:00–7:00 | B-qiskit-route, B-pyzx, B-noise-twin, R-code | G4 7:00 / 7:45 (Plan-B decision) |
| 5 Measurement + prereg + rehearsal | 13–17 | 6:30–8:00 | B-measure, B-mitigation, P-review, B-crosschecks, SCRIBE-prereg | G5 8:00 / 8:45 |
| 6 Dry run | 18 | 8:00–9:00 | B-isa, V-equivalence, OPS-approval | G6 9:00 / 9:45 |
| 7 Pilot + full run | 19–23 | 9:00–10:30 | OPS-hardware or twin, V-stopgo, B-fixes (prespecified only) | G7 10:30 / 11:30 (hardware may complete asynchronously) |
| 8 Analysis + ablations | 24–27 | 10:00–11:30 | B-analysis, B-ablations, R-code, P-review | G8 11:30 / 12:30 |
| 9 Report + replication + packaging | 28–30 | 11:00–12:00 | SCRIBE, B-replication, OPS-graphify/zip | G9 12:00 / 16:00 (freeze 15:00) |

### Phase 0 — Bootstrap (G0)

1. Inventory the repo: locate the monograph scaffold (Hamiltonian builder, Strang circuits, PyZX pipelines incl. the topology-preserving pass, dry-run-first submission, bootstrap analysis, tensor-network cross-checks, six-basis energy reconstruction, quasiprobability handling, H̃₁), `solutions/0.4.0.md` and earlier, `prompts/*_v.0.4.0.md`, prior `results/`. Write `run/INVENTORY.md` with paths and what is reusable. If the plan document exists in the repo, read Sections 7 and 8 for the original wording.
2. Environment: Python, Qiskit 2.x, qiskit-aer, qiskit-ibm-runtime (fake providers), pyzx, scipy, numpy, mthree (if used), CUDA-Q / cuTensorNet (record NOT AVAILABLE if absent), graphify (`pip install graphifyy` if missing and installs are allowed). `pip freeze > env/requirements.lock.txt`. Fake Heron target available (e.g. FakeTorino/FakeFez/FakeMarrakesh) or the real backend's properties (§7).
3. Tools: verify Codex, NIM, and the escalation model respond; record model ids in `run/MODELS.md`; set concurrency.
4. Write `run/PLAN.md`: this schedule adapted to the inventory (which monograph modules are reused, which are new), the hardware mode, and any deviation with reason. Initialize `run/TASKBOARD.md`, `run/GATES.md`, `run/DECISIONS.md`, `reports/REPORT.md` (template, Appendix F).
5. Freeze `src/su2qc/conventions.py` (§5.1 and the JW order) and start Phase 1 delegations immediately.

**G0 criteria**: clock started; inventory, env lock, models, plan, ledgers exist; fake or real target loads; `pytest` runs.

### Phase 1 — Hamiltonian by two routes, limit tests (G1)

Parallel delegations: route 1 builder; route 2 builder; physics reviewer writes `physics/predictions_G1.md` (re-deriving §5.2 independently); scaffold builders start the encoding maps + leakage-flag functions (§5.4) and adapt the monograph's analysis/bootstrap and measurement-grouping code to a stub H. Verifier writes `compare.py`, `limits.py`, `tests/test_ham.py`, `gates/gate_G1.py`.

**G1 criteria** (script + physics sign-off):
1. dim = 82 (j_max ½) and 152 (j_max 1) on **both** routes; local vertex states 6.
2. Sector dims N = 0,2,4,6,8 → 2, 20, 38, 20, 2; no odd N; [H, N] = 0.
3. Route agreement at j_max = ½ at ≥ 5 coupling points (incl. m = 0): sorted eigenvalues max relative deviation ≤ 1e-12 (documented floor 1e-10 only with a floating-point root cause); stretched-string time series of P_surv, n_v, E²_ℓ on t ∈ [0, 10] agree ≤ 1e-10.
4. Hermiticity ≤ 1e-13; route 2: ‖[G^a_v, H]‖ ≤ 1e-12 for all v, a on the redundant space; kernel dimension 82 / 152.
5. Limit tests: (i) g² → ∞: spectrum = electric + mass values with the k-degeneracies 16,16,18,16,16 before mass splitting (relative 1e-8 at g² = 1e6, or exact projection); (ii) m → ∞: the frozen-matter 2×2 block equals H̃₁ after reconciliation recorded in `physics/conventions_reconciliation.md`; (iii) magnetic term off: spectrum equals an independently built 4-site periodic 1+1D SU(2) chain (LSH or gauge-fixed 1D builder from the repo if present; otherwise a separately written 1D construction) to 1e-10.
6. `physics/signoff_G1.md`: predictions matched or discrepancies adjudicated (§4.3).

### Phase 2 — Exact dynamics, resonance, window (G2)

Builders: dynamics engine (expm on 82 and 152 dims, Krylov cross-check), mass scan and channel weights, window selector; Strang builder starts on the verified H. Physics reviewer writes `physics/predictions_G2.md` (qualitative expectations from Cataldi et al.: both channels open near resonance, BB̄ subdominant, finite-size shift) and reviews.

**G2 criteria**:
1. expm vs Krylov ≤ 1e-9; energy and N conserved ≤ 1e-10.
2. Mass scan m ∈ [0, 0.5 g²] (≥ 21 points) at ≥ 2 values of g²: breaking time t_b(m) (first t with P_surv ≤ 0.5, else time of the minimum in the window) and time-averaged pair-creation weight W̄(m) = ⟨P_meson + P_BB̄⟩_T; resonance m* = argmax W̄; report m*/g² against 3/16.
3. At m*: time series of P_stretched, P_short, P_surv, P_meson, P_BB̄, P_other, E²_ℓ, n_v, ⟨H⟩ → `analysis/tables/exact_*.csv`, figures.
4. Truncation error: the same at j_max = 1; max |Δ| on probabilities reported (`physics/truncation_error.md`); if > 0.1 in the chosen window, choose a different coupling or flag it prominently.
5. Window chosen and written to `physics/window.json`: (g², m, δt, r_max ∈ {2,3}) such that (a) exact P_surv drops by ≥ 0.3 within t = r_max δt, (b) P_meson + P_BB̄ at t ≥ 0.05, (c) Strang error on P_surv, n_v, E²_ℓ ≤ 0.05 at r_max (checked again at G3). If (a)–(c) cannot be met together, keep (c) and report the shortfall as a finding.
6. `physics/signoff_G2.md`.

### Phase 3 — Encodings, block unitaries, Strang circuits, Trotter error (G3)

Builders: L12, S8, C7 circuit families (each owns its files, all share the Strang skeleton and the monograph's exact-unitary checks); verifier writes the unitary and leakage tests; code reviewer reviews as each lands.

**G3 criteria** (script + code review):
1. Encode/decode maps and physical-code lists (82 each) for L12, S8, C7; leakage-flag functions per §5.4.
2. For each group T ∈ {D, h1, h2, h3, h4, B} and θ on a grid: ‖P_phys (U_circ(θ) − e^{−iθT}) P_phys‖ ≤ 1e-12 and ‖P_unphys U_circ(θ) P_phys‖ ≤ 1e-12.
3. Full Strang-step circuit matches the exact Strang propagator (product of expm's) on the physical subspace ≤ 1e-10 from the stretched string.
4. Trotter error vs r ∈ {1,2,4,8,16} at fixed t: fitted slope of log-error vs log-r in [−2.3, −1.7] for P_surv and E²; Strang error at the chosen window ≤ 0.05.
5. Noiseless simulation of the complete circuits (prep + r steps + basis changes): leakage rate **exactly 0** — zero flagged strings in ≥ 1e4 shots and flagged-code probabilities ≤ 1e-14 in the statevector.
6. Logical resource table: 2q count and 2q depth per group, per step, per full circuit, for L12/S8/C7 before routing (`circuits/resources_logical.md`; circuits exported as QPY + OpenQASM 3).

### Phase 4 — Compile, noisy twin, Plan-B decision (G4)

Builders: Qiskit level-3 routing to the target coupling map (fake Heron; also the real backend's target if `SU2ZX_BACKEND` is set); the monograph's PyZX pipelines (topology-preserving pass, and full-reduce for comparison only), judged **after routing**; noise-twin builder (`AerSimulator.from_backend`, from the real backend's current properties when available, else the fake backend) with post-selection and the analysis pipeline.

**G4 criteria** (script + code review; this is the plan's day-12 decision):
1. Routed table `compile/resources_routed.md`: native 2q count and 2q depth per Strang step and per full circuit for L12 and S8 × {Qiskit L3, PyZX-TP, PyZX-full}; qubit path chosen by backend properties and frozen (`compile/layout.json`).
2. Budget: per step ≤ ~250 native 2q; per circuit (prep + r_max steps + basis change) ≤ ~1,000; 2q depth < ~200; "about" tolerates ≤ 10 % overshoot with justification. At least one of L12/S8 meets it → primary encoding (tie → L12; S8 wins only if its depth advantage ≥ 30 % or L12 misses).
3. Routed-vs-logical equivalence: 1 − |⟨ψ_routed|ψ_logical⟩| ≤ 1e-10 including the final layout permutation.
4. Twin run of the full time series with post-selection: yield ≥ 20 % at the deepest circuit; twin observables agree with exact within the twin's bootstrap 2σ at ≥ 4 time points for the mitigated arm. If not, adjust (δt, r_max) once within §5 constraints and rerun; if still not, this predicts a Gate-2 failure on hardware — say so and decide.
5. Decision in `run/DECISIONS.md`: **GO** (encoding, pipeline) / **REDUCED** (S8) / **PLAN B** (§4.4). Plan B, if taken, is executed with the monograph's chain code plus two static fundamental charges and its own mini-gates (energy and Casimir profile vs separation 1–4 plaquettes, exact reference, twin/hardware).

### Phase 5 — Measurement design, mitigation, preregistration, rehearsal, cross-checks (G5)

**G5 criteria** (script + physics and code sign-off):
1. `prereg/MEASUREMENT_PLAN.md`: ≤ 20 settings; all §5.3 primary observables from the Z setting; energy from the additional settings (reuse the monograph's six-basis reconstruction adapted to the encoded Hamiltonian, or commuting-group measurement of the grouped terms); shots per setting; the ODR reference circuits and their cost.
2. Post-selection: per-shot on leakage flags (hard); energy drift per time point as a diagnostic (soft); readout mitigation (M3/TREX-style) composed with post-selection in one documented order, using the monograph's quasiprobability handling.
3. Mitigation arms: **A0** none; **A1** dynamical decoupling + Pauli twirling + operator-decoherence renormalization; **A2** optional zero-noise extrapolation (fold factors 1, 3) only if the budget allows.
4. `prereg/PREREG.md` **signed**: hypothesis with the frozen numbers; primary endpoint (exact P_surv, n_v, E²_ℓ reproduced within 2σ at ≥ 4 time points with yield ≥ 20 %); secondary endpoints (meson/BB̄ split, Casimir reduction, energy drift, encoding ablation, mitigation ablation, compiler comparison); frozen `prereg/config.lock.json` (couplings, δt, r_max, encoding, layout, shots, arms, settings, seeds, analysis commit) with its sha256 in the document; stop/go rules; kill criteria. Changes after signing only via `prereg/CHANGELOG.md`.
5. Rehearsal: the complete twin pipeline end to end (submission wrapper in twin mode → raw counts → post-selection → mitigation → tables and figures) with **no manual steps**; reproduces exact observables within the twin's 2σ.
6. Cross-checks: CUDA-Q statevector and a tensor-network simulation (cuTensorNet, else Aer `matrix_product_state`) of the noiseless circuits agree with the Qiskit statevector ≤ 1e-8; record NOT AVAILABLE honestly where tools are missing.

### Phase 6 — Dry run (G6)

**G6 criteria**: ISA circuits for the frozen config generated and inspected (`hardware/DRYRUN.md`): native gate set only, connectivity respected, layout equals `compile/layout.json`, measurement bit order verified with known-state calibration circuits (prepare a physical code, measure, decode), per-circuit resource summary (2q count, depth, duration estimate, shots, QPU seconds) and totals for pilot and full run against `SU2ZX_HW_BUDGET_SEC`; approval token `hardware/APPROVAL_<sha256-of-ISA-set>.json`; the submission script refuses to run without a token matching the circuits it is about to submit (reuse the monograph's dry-run-first mechanism).

### Phase 7 — Pilot, stop/go, full run (G7)

Mode per §7. **Pilot**: 3 repeats × all settings × 2,048 shots. **Stop/go checklist** (`hardware/STOPGO.md`): decoding sanity on known-state circuits; leakage rate ≤ 2× the twin's prediction; Z-basis TVD vs twin ≤ 0.15 at t = 0 and t = δt; post-selected N = 4 fraction; t = 0 observables match the prepared string within 2σ after mitigation. **Go** → full run: 5 repeats × arms (A0, A1[, A2]) × settings × `SU2ZX_HW_MAX_SHOTS_PER_JOB`-bounded shots, in the priority order pilot → A1 → A0 → A2 if the budget forces cuts. **No-go** → fix only defects prespecified in PREREG once (`prereg/CHANGELOG.md`), re-freeze, one more pilot; else §4.4.

**G7 criteria**: pilot and full run executed (hardware or twin, mode recorded per job in `hardware/jobs.jsonl` with backend, calibration timestamp, job id, circuits hash, shots, QPU seconds); raw immutable export `hardware/raw/*.json` with sha256 in `MANIFEST.json`; stop/go review recorded. Hardware jobs still queued at the freeze: job ids + `hardware/retrieve.py` + the analysis command so the human can complete the tables in the morning.

### Phase 8 — Analysis and ablations (G8)

**G8 criteria**: `analysis/tables/primary_endpoint.csv` (observable × time point: exact, measured mean, 2σ from bootstrap over repeats/time blocks, pass); secondary tables (channels, Casimir, energy drift, yield vs depth); **error budget** per observable and time point: truncation (j_max 1 vs ½), Trotter (Strang vs exact), compile (routed vs logical; expected ~0), device (raw twin/hardware vs noiseless), shot (bootstrap); **ablations**: arms, encodings (L12 vs S8 on the twin; C7 simulator), compiler pipelines (the secondary endpoint: native 2q counts after routing and observable error at equal shots, reproducing the monograph's TP-vs-full-reduce comparison on physically meaningful circuits); figures in `analysis/figures/`.

### Phase 9 — Report, replication, packaging (G9; §9)

---

## 7. Hardware policy

- **Default is twin mode** (`SU2ZX_HW=0`): every "hardware" phase runs against a noise model built from the real backend's current properties (`AerSimulator.from_backend(backend)` if credentials and `SU2ZX_BACKEND` are available — no QPU time spent) or from a fake Heron backend. The twin is a same-day, calibrated stand-in, not a hardware result; it produces the complete pipeline and tables so the night is complete regardless of queues.
- **Hardware mode** (`SU2ZX_HW=1`): requires credentials, `SU2ZX_BACKEND`, G5 and G6 passed, the approval token, estimated QPU seconds within `SU2ZX_HW_BUDGET_SEC`, and both Hamiltonian routes agreeing (or `SU2ZX_HW_OVERRIDE_G1=1`). Submit the pilot as early as G6 allows; submit the full run as one batch immediately after go; keep working on the twin while jobs queue; poll with timeouts (never spin); never resubmit a failed pilot more than once; never exceed the budget — cut shots and repeats in the priority order of Phase 7 instead. A second calibration window is optional and only if quota permits.
- Use Runtime primitives (SamplerV2 for raw bitstrings so post-selection is possible; options for dynamical decoupling and twirling); log options per job. Notify before every submission if `SU2ZX_NOTIFY=1`.

---

## 8. Analysis rules and claim boundaries

- Bootstrap over repeats (time blocks) for every interval; report 2σ; no hand-picked error bars.
- Post-selection yield is a first-class result: report it per circuit depth and arm, and the bias it introduces (compare post-selected vs unselected twin results where the noiseless answer is known).
- The claim table from Section 8.3 goes into the report **verbatim** and is filled with evidence links:

| Supported if the gates pass | Not supported by this experiment |
|---|---|
| A 12-qubit symmetry-verified evolution of SU(2) with dynamical matter on a plaquette is within reach of current hardware at a stated depth and yield | String tension, a continuum limit, or hadron phenomenology |
| The meson-versus-baryon channel split, the string shortening, and the Casimir reduction survive on hardware within the error budget | Any classically intractable calculation; the patch is exactly solvable |
| An error budget decomposed into truncation, Trotter, compile, device, and shot contributions | Baryon blockade and the full 2+1D claim, which need ladders (Idea 1, months 5 and 6) |
| The compiler comparison of the monograph, as a secondary endpoint on physically meaningful circuits | Quantum advantage of any kind |

- A twin-only night supports the first row only as "prepared and predicted", never as "demonstrated". Say so.
- Nulls are results. A failed Gate 2 analog (hardware or twin outside 2σ) is reported with the error budget explaining why.

---

## 9. Packaging (always, even after a hard stop)

Start no later than T+15:00, or immediately after G8 if earlier. Produce, in `$RUN`:

1. **`reports/REPORT.md`** (template Appendix F): executive summary; run timeline (gates, attempts, escalations, extensions, decisions); physics results (exact and measured); resource frontier tables; error budget; the claim table; limitations; the 2×3 continuation plan (1,727 states, 20 qubits in L12, what changes in encoding, depth, and measurement); reproducibility; coverage table (§10); file index. Plus a one-page `reports/SUMMARY.md`.
2. **Clean-environment replication** (`reports/REPLICATION.md`): fresh venv from `env/requirements.lock.txt`, `pytest -m gate`, and `python -m su2qc.replicate --run $RUN` recomputing the key numbers (counts, route agreement, Trotter table, primary-endpoint table from the archived raw counts) and diffing against the archived tables.
3. **graphify**: `graphify $RUN/src` (or `/graphify` from Hermes, `graphify hermes install` once) → `graphify-out/{graph.html, GRAPH_REPORT.md, graph.json}`; if graphify is unavailable, generate the equivalent function/call/import graph with a Python AST walk into the same three files and say so.
4. **Logic flow**: `LOGIC_FLOW.md` (Mermaid flowchart of the pipeline Hamiltonian → dynamics → encodings → circuits → compile → twin/hardware → analysis → report, with the gates, Plan-B branch, and escalation loop) and `logic_flow.json` (nodes with module paths, edges with data passed).
5. **`MANIFEST.json`**: sha256 and size of every file; the prompt hash; model ids; environment lock.
6. **Zip**: `results/section8_v0.5.0_${RUNID}.zip` containing `reports/`, `physics/`, `reviews/`, `gates/`, `prereg/`, `circuits/`, `compile/`, `hardware/` (raw counts always), `analysis/`, `logs/`, `graphify-out/`, `LOGIC_FLOW.md`, `logic_flow.json`, `src/`, `tests/`, `run/`, `env/`, `MANIFEST.json`, and copies of every `solutions/0.5.*.md` created tonight. Verify with `unzip -t`. Copy `REPORT.md` and `SUMMARY.md` to `results/section8_v0.5.0_${RUNID}/` next to the zip. Print the final clock and the paths.

---

## 10. Definition of done — coverage table (fill in the report)

| Plan days | Work | Artifact(s) proving it | Status |
|---|---|---|---|
| 1–3 | conventions frozen; 82-state H by two routes; three limit tests | `conventions.py`, `gates/GATE_G1.json`, `physics/signoff_G1.md` | |
| 4–6 | exact dynamics; resonance; j_max = 1 comparison; window | `analysis/tables/exact_*`, `physics/window.json`, `physics/truncation_error.md` | |
| 7–9 | encodings; grouping; block unitaries; Strang; Trotter r⁻²; noiseless leakage 0 | `circuits/`, `gates/GATE_G3.json` | |
| 10–12 | compile after routing; noisy twin; Plan-B decision | `compile/`, `run/DECISIONS.md`, `gates/GATE_G4.json` | |
| 13–14 | measurement design; readout mitigation; post-selection; prereg signed | `prereg/` | |
| 15–17 | cross-checks; rehearsal; hardware window decided | `physics/crosschecks.md`, `gates/GATE_G5.json` | |
| 18 | dry run; ISA inspection; approval token | `hardware/DRYRUN.md`, `hardware/APPROVAL_*.json` | |
| 19–20 | pilot; stop/go | `hardware/STOPGO.md`, `hardware/jobs.jsonl` | |
| 21–22 | prespecified fixes; re-freeze | `prereg/CHANGELOG.md` | |
| 23 | full run, two arms | `hardware/raw/`, `MANIFEST.json` | |
| 24–26 | analysis; bootstrap; yield; error budget | `analysis/tables/` | |
| 27 | ablations (arms, encodings, compilers) | `analysis/tables/ablation_*` | |
| 28–30 | research note; claim table; 2×3 plan; clean-env replication; release bundle | `reports/`, `results/*.zip` | |

Status values: DONE (hardware) / DONE (twin) / PARTIAL / NOT DONE, each with a one-line reason.

---

## Appendix A — File layout

```
SU2ZX/
  prompts/su2qc_section8_overnight_v.0.5.0.md      this file
  solutions/0.4.0.md (existing) · 0.5.0.md, 0.5.1.md, …  escalation solutions written tonight
  results/section8_v0.5.0_<RUNID>/{REPORT.md,SUMMARY.md} · results/section8_v0.5.0_<RUNID>.zip
  runs/section8_v0.5.0_<RUNID>/
    run/        T0 PROMPT_HASH CONFIG_ENV.md INVENTORY.md PLAN.md MODELS.md TASKBOARD.md GATES.md DECISIONS.md HEARTBEAT.md EXTENSION.md
    src/su2qc/  conventions.py ham/{route_spinnet,route_gausskernel,compare,limits}.py dynamics/ encodings/{l12,s8,c7}.py circuits/ compile/ measure/ twin/ hardware/ analysis/ replicate.py
    tests/      pytest (markers: unit, gate)
    gates/      gate_G0.py … gate_G9.py · GATE_G*.json · attempts/
    physics/    predictions_G*.md signoff_G*.md window.json truncation_error.md conventions_reconciliation.md DISCREPANCIES.md crosschecks.md
    reviews/    <phase>_<file>_<n>.md
    circuits/   resources_logical.md · *.qpy · *.qasm
    compile/    resources_routed.md layout.json
    prereg/     PREREG.md config.lock.json MEASUREMENT_PLAN.md CHANGELOG.md
    hardware/   DRYRUN.md APPROVAL_*.json STOPGO.md jobs.jsonl retrieve.py raw/
    analysis/   tables/ figures/
    reports/    REPORT.md SUMMARY.md REPLICATION.md
    logs/       agents/ cmd/
    env/        requirements.lock.txt
    graphify-out/ · LOGIC_FLOW.md · logic_flow.json · MANIFEST.json
```

## Appendix B — Delegation template (Hermes `delegate_task`)

```
delegate_task(tasks=[
  {"goal": "Implement src/su2qc/ham/route_spinnet.py: the analytic spin-network/LSH construction of H for the SU(2) plaquette with staggered two-color fermions, j_max in {1/2, 1}.",
   "context": """RUN=<abs path of $RUN>. Repo=<abs path>. Read RUN/src/su2qc/conventions.py first; it is frozen (sites, links, plaquette orientation, staggered phases, JW order, units a=1).
Deliver: build_hamiltonian(g2, m, jmax) -> (H sparse Hermitian, basis labels [(j1,j2,j3,j4), (n1..n4)]), plus operators for P_surv, P_meson, P_BBbar, E2 per link, n_v, N.
Expected: dim 82 (jmax 1/2), 152 (jmax 1); local vertex states 6; sector dims N=0,2,4,6,8 -> 2,20,38,20,2; Hermitian; [H,N]=0.
Rules: you own ONLY RUN/src/su2qc/ham/route_spinnet.py and RUN/tests/test_route_spinnet.py. Do not read or import route_gausskernel.py. Do not change conventions.py; if you believe it is wrong, write RUN/physics/conventions_objection_route1.md and continue with it as written.
Acceptance: `cd RUN && pytest tests/test_route_spinnet.py -q` all green; print the numbers above.
Return: files written, the printed numbers, what you could not verify, open questions. Time box: 60 min.""",
   "toolsets": ["terminal", "file"]},
  {"goal": "Implement src/su2qc/ham/route_gausskernel.py: the redundant Kogut–Susskind formulation and its Gauss-law kernel projection.", "context": "...same shape...", "toolsets": ["terminal","file"]},
  {"goal": "Write RUN/physics/predictions_G1.md: derive independently the expected numbers for G1 (state counts via transfer matrix, local vertex states, fermion-number sector dims, pure-electric degeneracies, frozen-matter sector, tree-level resonance) with derivations.", "context": "...", "toolsets": ["file"]}
])
```

Reviewer delegations point to the file(s), the checklist (Appendix C), and require `reviews/<phase>_<file>_<n>.md` with findings tagged BLOCKING / ADVISORY and a one-line verdict.

## Appendix C — Review checklists

**Code review**: matches the spec in §5/§6 (no silent convention changes); tests exist, run, and check numbers not just types; tolerances as specified; determinism (seeds, versions, sorted iteration); qubit ordering / endianness handled once and tested with a known state; no silent fallbacks or try/except-pass; logging to files; runtime fits the time box; no duplicated ownership.

**Physics review**: gauge invariance and Hermiticity; symmetry and sector structure; counts; limits; sign conventions (staggered phases, JW order, plaquette orientation, U vs U†); term grouping is gauge invariant; leakage flags complete for the encoding; observable definitions match §5.3; Trotter window sensible; claims match evidence; the report's numbers trace to artifacts.

## Appendix D — Gate JSON schema and ledger

```json
{"gate":"G1","status":"PASS|FAIL","attempt":2,"started":"<UTC>","finished":"<UTC>","mode":"twin|hardware|n/a",
 "criteria":[{"name":"dim_jmax_half","target":82,"value":82,"pass":true},
             {"name":"route_spectra_rel_dev","target":"<=1e-12","value":3.1e-14,"pass":true}],
 "signoff":{"physics":"physics/signoff_G1.md","code":"reviews/p1_route_spinnet_2.md"},
 "artifacts":["..."],"notes":"..."}
```

`run/GATES.md`: `gate | target | latest | attempts | status | passed_at | escalations | fallback_applied`.

## Appendix E — Escalation packet and `solutions/0.5.x.md` template

**Packet** (written to `logs/agents/escalation_<G>_<n>.prompt.md` and given to the escalation model): the gate definition and criteria table with measured values; `gates/attempts/<G>_attempt1.md` and `_attempt2.md`; paths and key excerpts of the failing code, tests, and logs; `conventions.py`; the relevant `physics/` notes; constraints (time remaining from the clock, budgets, what may not change after PREREG); the earlier solution files if any; the instruction to produce the solution file below and nothing else.

**`solutions/0.5.x.md` template**:

```
# Solution 0.5.x — <gate> — <date/time UTC>
Model: <id, effort>  ·  Supersedes/refs: <solutions/… if any>  ·  Run: <RUNID>
## 1 Diagnosis (what is actually failing, with the numbers)
## 2 Root cause (ranked hypotheses, each with the evidence that supports or kills it)
## 3 Fix plan (numbered, file-level, with the math where physics is involved)
## 4 Acceptance test (exact commands and expected numbers)
## 5 Risks and fallback (what to do if this fails; whether to apply the gate fallback instead)
## 6 Implementation assignments (which builder does what, in what order, expected minutes)
```

After implementation, the builder group's summary and the gate JSON are appended to the solution file under `## 7 Outcome`.

## Appendix F — Report skeleton (`reports/REPORT.md`, kept current from G0)

```
# Section 8 overnight run <RUNID> — SU(2) with dynamical matter on one plaquette
0 Status line (clock, mode, gates passed, escalations, extension)
1 Executive summary (5 bullets: what was shown, at what cost, what failed)
2 Run timeline (phases, gates, attempts, escalations, decisions)
3 Model, conventions, and verification (routes, limits, counts, discrepancies)
4 Exact physics (resonance, channels, Casimir, truncation error, window)
5 Encodings and circuits (resource tables, Trotter scaling, leakage = 0)
6 Compilation and the twin (routed tables, pipeline comparison, yield)
7 Preregistration and measurement plan (hash)
8 Pilot and full run (mode, jobs, stop/go, raw exports)
9 Results vs exact (primary endpoint table, 2σ, error budget)
10 Ablations (arms, encodings, compilers — secondary endpoint)
11 Claim table (Section 8.3, filled) and limitations
12 The 2×3 continuation plan
13 Reproducibility (replication log, environment, commands)
14 Coverage table (§10) and file index
```

## Appendix G — Forbidden behaviors

Relaxing tolerances or editing gate scripts to pass; presenting twin results as hardware; changing the frozen config after PREREG outside `CHANGELOG.md`; polling hardware without timeouts; running a single lane while other work is unblocked; spawning agents without file ownership; pasting large files into delegations; escalating ordinary bugs to the maximum-effort model; skipping packaging; fabricating or rounding numbers not produced by code; claiming "2+1D" for the single plaquette.

## Appendix H — Section 7 in one paragraph (context for every agent that asks "why this object?")

The monograph's five-plaquette pure-gauge chain at j_max = ½ is 32 exactly solvable states with no matter, no string, and no Gauss-law syndrome; the same family has already been run at 5 to 151 qubits on five IBM devices (Chen et al., March 2026), so a five-qubit run adds no physics, and its AI component (a random forest choosing among four exact pipelines, ~15 % effect in native two-qubit count) exercises neither the closed loop nor the learning-curve metric. Its verification scaffold, however, is exactly right. Tonight's object — the with-matter plaquette — is the smallest system on which the proposal's actual promise (string breaking with meson and baryon channels in a non-Abelian theory with dynamical fermions) can be measured against an exact answer on today's hardware.



## Source: docs/refs/v050_review_20260907.md
# SU2QC v0.5.0 — independent review of the 2026-09-07 status report

Reviewed: `STATUS_REPORT_20260907.md` + `SU2ZX_v0.5.0_status_20260907T170902Z.zip`
(270 files, git `eee1e16`). Deliverable produced: 26-page LaTeX graduate notes
(`SU2QC_v0.5.0_graduate_notes.pdf`) with full derivations, plus Overleaf source.

## Two corrections to the status report

**1. The pre-routing gate count is stale by ~7×.** §3.4 quotes 15,360 2q gates per
Strang step and "4 × ~1,850 for the hopping groups". Those come from an intermediate
builder log (`logs/agents/synth_l12.out.md`). The final artifact
`circuits/resources_synth.md` reads **2,156** per step: D=16, h0–h3 = 248/248/239/241,
B=174. Consistent with the routed 3,976 (×1.84 heavy-hex overhead); routing 15,360
could not yield 3,976.

*Consequence:* §5 item 2's optimization plan ("hoppings dominate") is void. Hoppings
total 976 vs plaquette 174 — no single hot spot. The logical gap is 2,156/250 = **8.6×**
before routing, which no synthesis trick closes. The real levers are scope levers
(smaller r_max, larger δt) or Plan B.

**2. The twin seeding suspicion is closed — wrongly diagnosed.** `run_g4.py` calls
`twin.run_counts([meas]*5, 4000, 500+10r, sim)` and `run_counts` uses
`seed_simulator = seed + k`. The five repeats **do** get distinct seeds. Remaining
candidates for 2σ = 0.000: (a) the construction-time `AerSimulator.from_backend(...,
seed_simulator=101)` overriding the per-run keyword; (b) rounding — but the expected
value is ≈0.004, which would print; (c) r=0 is a bare product-state circuit (0 CZ).
Decisive test: compare the five counts dicts for equality.

## New finding: the primary endpoint cannot pass as coded

The twin acceptance test asks whether the twin mean is within 2σ (statistical only)
of the **exact** value. At r=0: exact 1.000, twin 0.946 — a 5.4% pure device error
against a ~0.004 error bar. Only arm A0 (raw + post-selection) is run; A1/A2 exist in
the plan but not in the driver. So the endpoint is guaranteed to fail for reasons
unrelated to physics. Before G5 signs a prereg, restate it as one of:
(i) twin-vs-exact after mitigation with a device-error term in the budget;
(ii) twin-vs-noise-model-prediction, exact as separate reference;
(iii) a ratio/trend statement (e.g. BB̄ ≫ meson ordering) robust to uniform depolarizing.

## Priority order (differs from the report's)

- **Tier 0** — N1 twin variance regression test; N2 restate the endpoint; N3 finish G4
  and record GO/REDUCED/PLAN B (GO is not available on the numbers).
- **Tier 1** — N4 truncation error per observable at the four measurement times, with
  an independently validated j_max=1 Hamiltonian (blocked by D1: route 2 has no j_max=1
  H); N5 test whether BB̄ dominance is geometric on a 2-plaquette patch (prediction:
  P_BB̄/P_meson falls well below the one-plaquette ~11); N6 replace the failed W̄
  estimator with level degeneracy or a background-subtracted weight; N7 decide
  REDUCED vs PLAN B by computing the surviving signal at r_max = 1, 2 *before* choosing.
- **Tier 2** — fix/drop `pyzx_basic_TP` (pre-route equiv 0.996); S8/C7 or formally
  retire the encoding ablation; commit the 9 untracked Phase-4 paths; Ruff/mypy on
  `src/su2qc` (never run); stale j_max=1 test assertion; write `su2qc.replicate`.

## Verified by hand (all reproduce the code exactly)

82 states via cyclic domain-wall counting (32 + 48 + 2); sectors (2,20,38,20,2);
electric degeneracies (16,16,18,16,16); 152 at j_max=1; m* = 3g²/16 from the energy
budget 2m = 3g²/8; the four exactly degenerate partners at (g²,m)=(4,0.75); and the
L12 code word **3793** for the stretched string. These are in the notes as worked
examples — useful as regression targets for any rewrite.

## Assessment

Science half (G1–G3) is finished and unusually strong: two-route agreement at 1e-15
across four independent combinatorial fingerprints plus spectra plus dynamics, exact
gauge invariance term by term, provably leak-free circuits. Three overturned
predictions handled the right way round. Engineering half is blocked by a structural
8.6× logical gap that is the honest price of exact gate-level gauge invariance — and
is itself a reportable result (item 3 of the project's own science list).


## Source: docs/refs/sufian_overlap_20260907.md
# Overlap analysis: Sufian "2+1D SU(2) Gauge Dynamics" (25 Aug 2026) versus SU2QC / SU2ZX v0.5.0

Prepared 7 September 2026. Compared: the 66-page working research-group report by Raza Sufian (`SU2_in_2_1D.pdf`, dated 25 August 2026) against the SU2QC Nine-Month Plan (7 Sept 2026), the v0.5.0 status review (7 Sept 2026), and the Section 8 overnight Hermes prompt v0.5.0. Numbers attributed to the report are quoted from it; numbers attributed to "ours" are from the v0.5.0 review's hand-verified values.

## Verdict in one paragraph

The report is the same physical model, the same regulator, the same resonance point, the same target paper and nearly the same observable list as Idea 1 / the rebuilt one-month project, but it takes the opposite route to hardware (a classically constructed, state-adapted Krylov playback circuit rather than an extensible gauge-invariant product formula), it adds two static background charges that change the Hilbert space, and it has already run on IBM hardware. It removes the "first with-matter hardware time series at one or two plaquettes" claim from the table. It does not touch the gauge-invariant circuit construction, the leakage-flag encoding, the 8.6× cost result, Gauss-law syndromes (Idea 2), tensor-network embedding (Idea 3), Gauge-JEPA, ladders beyond two plaquettes, or the j_max = 1 truncation study.

## What is the same

**Physics object.** Kogut–Susskind SU(2) in 2+1D with two-color staggered fermions, hard-core truncation j ∈ {0, ½}, five-state link |j, m_L, m_R⟩, E² = j(j+1), the four-term split (hopping, mass, electric, magnetic). The report's link transporter is the projected multiplication operator (non-unitary after projection, stated as a regulator artifact), which is the same construction as our route B.

**Resonance.** The report's benchmark couplings w = g_B = 1, g_E = 50, m = 18.75 satisfy 2m = ¾ g_E, i.e. m = 3g_E/8, which is our μ* = 3/8 (m* = 3g²/16 in the proposal's normalization), verified by hand in the v0.5.0 review.

**Geometry ladder.** One plaquette (4 sites, 4 links) → two adjacent plaquettes (6 sites, 7 links). The second is our 2×3 ladder.

**Target paper and framing.** Cataldi–Orlando–Halimeh arXiv:2509.08868; both documents describe their result as a local early-time precursor of string breaking, not a reproduction of the 8×8 tree-tensor-network curves.

**Observables.** Initial-string probability, shortest-string-manifold probability, electric Casimir (per link and patch average), meson-like single-occupancy density, baryon-pair double-occupancy density, with the expected sign pattern ΔP_init < 0, ΔP_str < 0, ΔC < 0, Δp_mes > 0, Δp_bar > 0 stated explicitly. These are our channel projectors and Casimir/density observables.

**Verification culture.** Two independent dimension counts (local Gauss-kernel diagonalization versus Clebsch–Gordan fusion-path propagation) agreeing exactly; Hermiticity and physical-subspace closure residuals at 10⁻¹⁵ and 10⁻²⁹; gauge leakage treated as a measured quantity; hard 10⁻³ acceptance thresholds on state infidelity and observable error; an explicit "supported / not supported" claim list; immutable hardware records with job IDs and hashes; a section on auditing versus asserting. Same discipline as our G1–G3 and gate ledger.

**AI framing.** "AI-assisted, physics-constrained quantum-circuit co-design and validation" with explicit refusal of "AI advantage", "AI invented an algorithm", or "AI outperforms physicists" — the same wording constraint the Nine-Month Plan imposes. The report also lists the evidence a future AI-advantage claim would need (human baseline, compiler-only baseline, scripted search, ablations without physics constraints or hardware feedback).

**ZX negative result.** PyZX rewrites preserved the circuit but did not lower entangling cost (§12.4 item 3). This matches the monograph's finding and the v0.5.0 `pyzx_basic_TP` problem.

**Hardware class and protocol elements.** IBM Heron (Kingston); matched t = 0 control circuits and reporting of ΔO = O(t) − O(0); linear readout inversion with reported quasiprobability artifacts; ZNE by odd local CZ folding at scales {1, 3, 5}; bootstrap over physics and calibration counts.

## What is different

### 1. Static charges: the Hilbert spaces are not the same

The report places two static fundamental (j_b = ½) charges at opposite corners (v0, v2 for one plaquette; v0, v5 for two) entering Gauss's law as fixed background sources. That changes the gauge-invariant counts:

| Quantity | ours (no static charges) | report (static charges) |
|---|---|---|
| 1 plaquette, all N | 82 | 112 |
| 1 plaquette, half-filled (N = 4) | 38 | 54 (6 qubits) |
| 1 plaquette, by N = 0, 2, 4, 6, 8 | 2, 20, 38, 20, 2 | 2, 27, 54, 27, 2 |
| 2×3, all N | 1,727 | 2,417 |
| 2×3, half-filled (N = 6) | — (not yet computed) | 977 (10 qubits) |
| 2×3, by N = 0 … 12 | — | 4, 119, 597, 977, 597, 119, 4 |

Consequences: the report's sixth observable, endpoint screening (a projector onto the singlet of dynamical matter with the static charge at an endpoint), has no analogue in our model; our string-shortening channel (three-link path → one-link path between a dynamical quark and antiquark on adjacent vertices) is not the report's object, whose minimal strings are the two two-link paths between opposite corners.

### 2. The route to hardware is the opposite of ours

| | ours (v0.5.0) | report |
|---|---|---|
| Circuit | second-order Strang with gauge-invariant term grouping; each grouped factor an exact block unitary on the physical subspace | state-adapted Krylov projection K = 4/8/16 (2/3/4 qubits); generic unitary synthesis of exp(−iH_K t) |
| Gauge invariance | exact at gate level; noiseless leakage ≤ 10⁻¹²; leakage flags readable on hardware | exact by construction (K ⊂ H_phys) but no redundancy: gauge errors on hardware are invisible |
| Validity | one circuit family for all t; reusable; extensible | valid for one initial state at one time; new unitary per t; requires the full classical solution to construct Q_K |
| Qubits | 12 (local gauge-invariant encoding) | 2–3 for the hardware circuits |
| Cost | 2,156 logical two-qubit gates per step (D = 16, h0–h3 = 248/248/239/241, B = 174); routed 3,976; 8.6× over the 250 budget | 27 CZ exact / 13 CZ approximate at t = 0.25; 3 CZ at t = 0.10 |
| Scalability | the point of the construction | "not by itself a scalable quantum algorithm" (§2, §18.2) |

### 3. It ran

IBM Kingston, physical qubits {82, 83, 96}, t = 0.10 and 0.25 (in the report's units, g_E = 50), about 440 quantum seconds over five staged jobs plus three final matched jobs, all with job IDs. Matched 27-CZ baseline versus AI-selected 13-CZ: mean absolute observable error down 35.3 % (one plaquette, 9 of 9 observables improved) and 48.6 % (two plaquettes, 5 of 6). The patch-averaged Casimir change on two plaquettes was not resolved after compression. p_bar detected at only 1.90σ in the Stage-2 experiment.

### 4. It has already answered three of our open questions

- **Mitigation policy (our A0/A1/A2 arm question):** scale 1 for five observables, linear ZNE only for endpoint screening, quadratic ZNE rejected on real-device evidence after a scales-1, 3, 5 experiment; calibration-derived Aer had predicted broad ZNE benefit and was wrong.
- **Formulation comparison (our month-2 item):** an isolated-plaquette LSH recoupling is spectrally equivalent to the hard-core KS model and gives no circuit advantage after Krylov reduction; a six-state two-rishon QLM needs a 56-dimensional reduced model (6 qubits, 1,783 all-to-all CX, ≈ 2,971 device entanglers) and was rejected; a binary-tetrahedral discrete-group candidate was not Hamiltonian-matched.
- **Baryon channel (our N5):** their p_bar is a weak detection; their exact two-plaquette data could be used to test whether BB̄ dominance (≈ 11 : 1 on our one plaquette) is geometric.

### 5. Coupling regime

The report's point is deep in strong coupling: in electric units the four coefficients are (electric, hopping, magnetic, mass) = (1, 0.02, 0.02, 0.375). Ours at g_E = 1 are (1, 0.5, 0.25, 0.375). Their time t = 0.25 at g_E = 50 is τ = t·g_E = 12.5 in electric units but only 0.25 in hopping units, which is why a Krylov space of dimension 6–8 suffices. At our coupling the Krylov dimension reached from S3 is about 28 of 38 (v0.5.0 preliminary), so the same method would need far more qubits and gates. Their coupling point is not on our one-parameter family (hopping 1/(2g_E) and magnetic 1/(4g_E²) cannot both be 0.02).

### 6. What the report does not touch

Gauss-law syndromes and closed-loop control (Idea 2) — and its basis has no redundancy, so it cannot host that study, the same objection the plan raised against the monograph's gauge-reduced chain; tensor networks and hybrid embedding (Idea 3); Gauge-JEPA; ladders beyond two plaquettes; j_max = 1 truncation error; baryon blockade; any coupling scan.

### 7. Naming

The report is titled "2+1D" while its §15 concedes one or two isolated plaquettes. The Nine-Month Plan reserves "2+1D" for 2×3 and beyond, where an interior vertex exists. This should be reconciled before either document circulates.

## Collision risks

The report's §18.4 next milestones are: (1) freeze the present data as the Phase-I benchmark; (2) repeat on a second backend/calibration date; (3) three or four plaquettes only after repeating the dimension, sparsity and adaptive-K searches; (4) KS versus LSH on a coordination-four geometry; (5) an AI ablation study with fixed search budgets (human baseline, compiler-only, physics-reduction search, measurement search, full co-design); (6) a reference-free mitigation-selection rule using consistency, conserved quantities and held-out times. Items 5 and 6 are Idea 2's controlled study and its "verification by invariants beyond exact reach" in different words. If the report's author is a collaborator, this is a scope-coordination matter for the advisor before either document goes out; if not, it is a competitor in the Idea 2 direction.

## State of the report

It is a draft under review: live editorial notes remain in the text ("check angle of RZZ gate-KYU", "T-gate count…check", "each link 3—explain why all 3 not required", the red explanatory paragraph under Fig. 4 answering a reviewer's question about identical depths for one and two plaquettes). It should not be treated as a frozen result.

## Reference numbers for cross-validation (from the report; for our V5–V6 bridge tests)

Static-charge model at the report's coupling point (w = g_B = 1, g_E = 50, m = 18.75). One plaquette: staggered vacuum (n0, n1, n2, n3) = (0, 2, 0, 2); minimal strings (j0, j1, j2, j3) = (½, ½, 0, 0) and (0, 0, ½, ½); K = 16 accepted on 0 ≤ t ≤ 5 (max trajectory infidelity 6.91 × 10⁻⁴, max observable error 6.23 × 10⁻⁴); K = 6 at t = 0.25 (process infidelity 2.58 × 10⁻⁵, full-space state infidelity 5.05 × 10⁻⁵, max observable error 3.97 × 10⁻⁴). Two plaquettes: three shortest three-link strings at basis indices 630, 426, 127 (630 initial); sparse H with 10,885 nonzeros; fixed-window K = 128 (7 qubits) on 0 ≤ t ≤ 5; time-adapted K = 4 at t = 0.05 and 0.10, K = 8 at t = 0.25, K = 12 at t = 0.50, K = 32 at t = 1.00. Endpoint-screening projector: rank 297 in the 977-state basis. Acceptance: 1 − F ≤ 10⁻³, max observable error ≤ 10⁻³, zero gauge leakage.

## Recommendation recorded on 7 September 2026

Do not pivot. Reframe the claim from "first with-matter hardware run" to "the measured price of exact gate-level gauge invariance, against a validated non-invariant baseline on the same Hamiltonian, observables and device"; take the REDUCED path (r_max = 1, 2) rather than Plan B; run N5 against the two-plaquette exact data; treat the report's mitigation and formulation results as priors; and settle the Idea 2 collision with the advisor before opening that line. The Hermes campaign prompt v0.6.0 implements this.


## Source: AGENTS.md
# SU2ZX Agent Rules

## Scope lock

- Treat the canonical current directory as the repository root.
- Its basename must be `SU2ZX` when the package is used for research execution.
- Never read, write, search, delete, or run Git operations outside that root.
- Use `.work/` for temporary files, `.mamba/` for the single reusable Mamba prefix, and `artifacts/` for generated research outputs.
- Do not use `cd ..`, `~`, `$HOME`, `/tmp`, or another repository as a command target.
- Preserve pre-existing user files and uncommitted changes.

## Ponytail discipline

Before adding code, prefer in order: no new code, standard library, an existing project function, an installed dependency's native API, then the smallest readable implementation. Avoid wrappers, factories, duplicate backends, speculative abstractions, dashboards, and redundant notebooks. Never remove validation, security, physics tests, or reproducibility controls for brevity.

## Physics gates

- `src/su2zx/core.py` is the single Hamiltonian and convention source of truth.
- Qiskit strings and displayed bitstrings use `q_(N-1)...q_0`.
- The spatial plaquette chain is a truncated 2+1D Hamiltonian system, not pure-gauge 1+1D.
- Never claim continuum SU(2), physical SU(3) QCD, string tension, string breaking, hadronization, or quantum advantage from this model.
- Never accept a compressed circuit without equivalence validation.
- Never present simulator output as QPU data.

## External actions

- The user authorizes creation of one new public repository under `digonto10602` and pushing this project after tests and a secret scan.
- Never publish credentials, tokens, `.env`, provider configuration, `.mamba/`, or caches.
- IBM QPU submission requires `ALLOW_IBM_QPU_SUBMISSION=1`, `--submit`, and the exact fresh dry-run token. GitHub authorization does not authorize QPU usage.

## Completion

Generate `RESEARCH_RESULTS.md`, CSV/JSON data, plots, test results, and an honest status table. Publish only after local validation. If GitHub authentication is unavailable or is not `digonto10602`, write `PUBLISH_BLOCKER.md` and do not push to another account.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Graphify is installed in the repository-local Mamba prefix. Invoke it as `.mamba/bin/graphify`.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `.mamba/bin/graphify query "<question>"` when graphify-out/graph.json exists. Use `.mamba/bin/graphify path "<A>" "<B>"` for relationships and `.mamba/bin/graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `.mamba/bin/graphify update .` to keep the graph current (AST-only, no API cost).


## Source: README.md
# SU2ZX v0.4.0

Reproducible research on exact compiler selection and real-time evolution of a gauge-reduced, j_max=1/2 SU(2) plaquette chain in a truncated 2+1D Hamiltonian geometry. `src/su2zx/core.py` defines the Hamiltonian and q_(N-1)...q_0 convention.

v0.4.0 demonstrates direct-observable CPU MPS scaling through N=32. Basic/Teleport winners survive the sampled fixed-target seeds; ML is NULL on prospective generalization, and symmetry-aware ordering has MIXED physics effects. See [RESEARCH_RESULTS.md](RESEARCH_RESULTS.md) and [VALIDATION.md](VALIDATION.md).

No continuum physics, physical SU(3) QCD, string tension, string breaking, hadronization or quantum advantage is established. Synthetic compilation and simulator outputs are never labeled QPU data.

The [completion audit](docs/V040_COMPLETION_AUDIT.md) maps the v0.4.0 prompt to evidence.
The [code logic and test report](docs/CODE_LOGIC_AND_TESTS.md) explains the complete
workflow, benchmarks, test coverage and limitations; the
[function inventory](docs/CODE_FUNCTION_INVENTORY.md) lists actual callables and assertions.

## Setup and reproduction

Run from the SU2ZX repository root. All working files remain inside it.

```bash
bash scripts/bootstrap_env.sh
bash scripts/run_v040.sh
```

Use the existing single `.mamba/` installation; the interpreter is `.mamba/envs/su2zx/bin/python`. `scripts/run_all.sh` retains the historical v0.3.0 reproduction pipeline and overwrites legacy reports; use run_v040.sh for the current milestone.

## Individual stages

```bash
export TMPDIR="$PWD/.work/tmp" MPLCONFIGDIR="$PWD/.work/matplotlib"
export XDG_CACHE_HOME="$PWD/.work/cache" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2
.mamba/envs/su2zx/bin/python -m pytest
# Historical physics / six-strategy benchmark (use separate output for preservation):
.mamba/envs/su2zx/bin/python -m su2zx.study --config config/research.json --output .work/baseline
.mamba/envs/su2zx/bin/python -m su2zx.compiler_study --config config/research.json --output .work/baseline
# Fixed-target robustness, paired data, grouped ML and frozen-rule prospective test:
.mamba/envs/su2zx/bin/python -m su2zx.robust_study
# Re-analyze saved data without recompilation:
.mamba/envs/su2zx/bin/python -m su2zx.robust_study --stage analyze
# Symmetry physics/compiler grid, full/asymptotic fits and Pareto table:
.mamba/envs/su2zx/bin/python -m su2zx.scaling_study physics
# Direct-observable MPS validation then bounded no-statevector scaling:
.mamba/envs/su2zx/bin/python -m su2zx.scaling_study tn
.mamba/envs/su2zx/bin/python tools/validate_v040.py controls
.mamba/envs/su2zx/bin/python tools/validate_v040.py hardware
.mamba/envs/su2zx/bin/python tools/cudaq_reference.py --target qpp-cpu --plaquettes 5
.mamba/envs/su2zx/bin/python tools/plot_v040.py
.mamba/envs/su2zx/bin/python tools/validate_v040.py audit
.mamba/envs/su2zx/bin/python tools/report_v040.py
```

The frozen design is `config/research_v040.json`, checked against `artifacts/data/v040/frozen_design.json`. Preserve these for reproduction; a new research design needs a new timestamped freeze and a fresh holdout. Five routing seeds reuse calibration seed 7. All primary comparisons exclude any pair with a failed output. Randomized routed equivalence is explicitly distinguished from exact logical unitary validation.

## IBM and optional GPU

```bash
.mamba/envs/su2zx/bin/python -m su2zx.qpu --comparison   --backend BACKEND --physical-path q0,q1,q2,q3,q4
.mamba/envs/su2zx/bin/python -m su2zx.qpu_analysis artifacts/qpu/ibm_su2_run.json
```

The IBM command defaults to a dry run. Live submission requires ALLOW_IBM_QPU_SUBMISSION=1, --submit and the exact fresh --confirm token. Approval is one use, configuration/manifest bound, and expires after 15 minutes. The four-way current/symmetry × Basic/Teleport workflow measures occupations, survival, energy, mirror asymmetry and TVD, with raw/M3 analysis and separate exact/Trotter references. The saved QPY bundle uses a synthetic target; regenerate on the chosen real backend. This release submitted zero QPU jobs.

CUDA-Q CPU works. The detected GTX 1060 Max-Q (compute capability 6.1) blocks GPU execution. Existing CUDA-Q scripts accept supported targets on a future compatible GPU; do not alter drivers or force unsupported targets.

## Outputs, Graphify and archives

Data, figures/source mappings, logs and provenance live under artifacts/. Historical v0.3.0 outputs remain preserved alongside v040/. Sixteen current figures have both PNG and PDF outputs.

```bash
.mamba/bin/graphify query "direct MPS robustness pairwise selector symmetry"
.mamba/bin/graphify update .
# After final reports and Graphify validation:
.mamba/envs/su2zx/bin/python tools/archive_v040.py
```

The archive helper requires a passing Graphify validation record, scans the curated file set for secrets, creates a new UTC timestamped ZIP in zip_results/, tests that exact ZIP, verifies its expected contents and writes SHA256 plus an integrity receipt. It excludes environments, caches, credentials and prior archives. Never overwrite prior archives. Archive details are in RUN_MANIFEST.md and GRAPHIFY_UPDATE.md.


## Source: runs/section8_v0.5.0_20260907T0628Z/run/PLAN.md
# Run plan (adapted schedule)
Mode: TWIN (no IBM credentials; FakeTorino target, CZ native).
Phases per prompt Section 6, with these adaptations:
- All with-matter code is new under $RUN/src/su2qc/ (nothing in repo covers matter).
- Monograph reuse: H~1 block (core.py) for frozen-matter limit; compiler_study PyZX-TP pass
  for Phase 4; qpu.py dry-run/approval mechanism pattern for Phase 6; tn_study MPS harness.
- Concurrency 3 (delegate_task limit). Lanes overlap per Section 6 table.
- Cross-checks: CUDA-Q NOT AVAILABLE; use Aer statevector + Aer MPS.
- Escalations: solutions/0.5.0.md first (repo has no solutions/ dir; will create).


## Source: runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py
"""FROZEN conventions for the SU(2) single-plaquette patch with dynamical matter.

Frozen at G0 of run section8_v0.5.0_20260907T0628Z. DO NOT EDIT.
Both Hamiltonian routes, all encodings, circuits, and analysis import from here
and ONLY from here. Any objection goes to physics/conventions_objection_*.md.

Model (Section 5.1 of the v0.5.0 prompt):
  Lattice units a = 1. One square plaquette, open boundaries.
  H = (g^2/2) sum_l E_l^2
    + m sum_v (-1)^{x_v+y_v} psi\dagger_v psi_v
    + (1/2) sum_l ( eta_l psi\dagger_{s(l)} U_l psi_{t(l)} + h.c. )
    - (1/(2 g^2)) Tr( U_box + U_box\dagger )
  U_box = U_l1 U_l2 U_l3\dagger U_l4\dagger   (counter-clockwise v1->v2->v3->v4->v1)
  E^2 = j(j+1) per link. Truncation j in {0, 1/2} (hardcore gluon); j_max = 1
  is built too for the truncation-error statement.
"""

# ---------------------------------------------------------------- vertices
# index -> (x, y). Vertex numbering v1..v4 maps to python indices 0..3.
VERTICES = ((0, 0), (1, 0), (1, 1), (0, 1))  # v1, v2, v3, v4
N_VERTICES = 4

def parity(v: int) -> int:
    """(-1)^{x+y} for vertex index v in 0..3.  v1,v3 even (+1); v2,v4 odd (-1)."""
    x, y = VERTICES[v]
    return 1 if (x + y) % 2 == 0 else -1

PARITY = tuple(parity(v) for v in range(4))          # (+1, -1, +1, -1)

# ---------------------------------------------------------------- links
# index -> (source_vertex, target_vertex, direction). Link numbering l1..l4
# maps to python indices 0..3.  l1: v1->v2 (x, y=0); l2: v2->v3 (y, x=1);
# l3: v4->v3 (x, y=1); l4: v1->v4 (y, x=0).
LINKS = ((0, 1, "x"), (1, 2, "y"), (3, 2, "x"), (0, 3, "y"))
N_LINKS = 4

def eta(l: int) -> int:
    """Staggered phase of link l: eta_x = 1, eta_y = (-1)^x  (x of the source)."""
    s, _t, d = LINKS[l]
    if d == "x":
        return 1
    return 1 if VERTICES[s][0] % 2 == 0 else -1

ETA = tuple(eta(l) for l in range(4))                # (+1, -1, +1, +1)

# Plaquette orientation: U_box = U_0 U_1 U_2^dag U_3^dag (python link indices).
PLAQUETTE_SEQUENCE = ((0, +1), (1, +1), (2, -1), (3, -1))  # (link, +1=U / -1=Udag)

# ---------------------------------------------------------------- matter
# Two-color staggered fermions, one doublet per vertex. 4 Fock states per site:
# n=0 color-singlet vacuum, n=1 doublet, n=2 doubly-occupied singlet (baryon).
# Staggered vacuum: even sites empty, odd sites full: n_vac = (0, 2, 0, 2).
N_VAC = (0, 2, 0, 2)

def charge(v: int, n: int) -> int:
    """Local charge relative to the staggered vacuum: q_v = n_v - n_vac(v)."""
    return n - N_VAC[v]

# Jordan-Wigner mode order for route 2 (redundant Kogut-Susskind space).
# Mode index 0..7 = (v1,c1),(v1,c2),(v2,c1),(v2,c2),(v3,c1),(v3,c2),(v4,c1),(v4,c2)
JW_ORDER = tuple((v, c) for v in range(4) for c in range(2))

# ---------------------------------------------------------------- truncation
JMAX_HALF = 0.5   # primary truncation, 82 gauge-invariant states
JMAX_ONE = 1.0    # for the truncation-error statement, 152 states

def casimir(j: float) -> float:
    """SU(2) quadratic Casimir j(j+1)."""
    return j * (j + 1.0)

# Expected gauge-invariant dimensions (verified independently by both routes).
EXPECTED_DIM = {JMAX_HALF: 82, JMAX_ONE: 152}
# Fermion-number sector dims at jmax=1/2, N = 0,2,4,6,8:
EXPECTED_SECTOR_DIMS = {0: 2, 2: 20, 4: 38, 6: 20, 8: 2}

# ---------------------------------------------------------------- couplings
def coupling_electric(g2: float) -> float:
    """Coefficient of sum_l E_l^2."""
    return g2 / 2.0

def coupling_magnetic(g2: float) -> float:
    """Coefficient of -Tr(U_box + U_box^dag) (i.e. H_B = -c * Tr(...))."""
    return 1.0 / (2.0 * g2)

HOPPING_PREFACTOR = 0.5   # (1/2) sum_l ( eta_l psi^dag_s U psi_t + h.c. )

# Tree-level resonance (a=1): removing one j=1/2 link releases (g^2/2)(3/4);
# equals pair cost 2m at m* = 3 g^2 / 16.
def tree_level_resonance(g2: float) -> float:
    return 3.0 * g2 / 16.0

# ---------------------------------------------------------------- bit orders
# Qiskit strings and displayed bitstrings use q_(N-1)...q_0 (repo-wide rule).
QISKIT_BIT_ORDER = "q_(N-1)...q_0"

# Canonical basis-label form shared by both routes and compare.py:
# a state is labeled ((j1,j2,j3,j4), (n1,n2,n3,n4), intertwiner_tag) where
# j are half-integers as floats, n in {0,1,2}; intertwiner_tag disambiguates
# nothing at 2-valent vertices (always 0) but is kept for forward compat.
LABEL_DOC = "((j_l1..j_l4), (n_v1..n_v4), tag)"
