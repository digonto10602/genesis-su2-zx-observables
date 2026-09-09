# v0.6.2 planning input
Higher-priority routing applies: this task requires a Fable planning pass before BUILD despite R6 no-replan wording. Preserve R7-R12 goals/order and thresholds; resolve executable ambiguities, do not redesign research. Codex BUILD; mechanical Python TEST-BENCH; Opus REVIEW/intermediate PHYSICS; Fable final sign-off and any physics doubt. No push, QPU, installs or CLI updates. All command/file targets inside repository. Supervised bounded subprocesses only, no unattended runner claim. Hard stop T0+12h; Phase 2 only with >=6h left and C0/C1 signed.
Potential specification contradictions to resolve explicitly: raw sim.run(seed=500/501) shift cannot change by editing run_counts; post-fix test should distinguish unchanged raw-Aer mechanism vs spawned effective-seed wrapper test, never silently relabel. channel_closure_residual currently ignores invalid codes on BOTH sides so adding an invalid key cannot cause a nonzero residual under its definition. Preregistration cannot contain its own full-file SHA256 fixed point. R11 prohibits writes to manifested state after signoff, but C1 amendments necessarily change it: each gate needs its own immutable snapshot. Do not weaken acceptance silently; identify any ruling needing human clarification as blocking.
Boot dirt: only two user archives and supplied prompt. R12 explicitly authorizes moving the named older ZIP; preserve newer user-requested ZIP in artifacts unless disposition authorized (potential cleanliness blocker). No discard/stash. Source prompt can be explicitly staged at scoped gate commit as task input. Prior artifacts are context, never new-session evidence.

# Repository tracked tree
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
STATUS_REPORT_20260907.md
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
artifacts/logs/v050/graph_validation_20260907.json
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
docs/refs/README.md
docs/refs/SU2QC_Nine_Month_Plan.pdf
docs/refs/sufian_overlap_20260907.md
docs/refs/v050_review_20260907.md
prompts/CODEX_AUTONOMOUS_SU2ZX_RESEARCH_PROMPT.md
prompts/CODEX_AUTONOMOUS_SU2ZX_RESEARCH_PROMPT_Laptop.md
prompts/SU2ZX_CODEX_AUTONOMOUS_RESEARCH_PROMPT_v0.3.0.md
prompts/SU2ZX_CODEX_AUTONOMOUS_RESEARCH_PROMPT_v0.4.0.md
prompts/gi_cost_campaign_v.0.6.0.md
prompts/gi_cost_campaign_v.0.6.1.md
prompts/v0.5.0.md
pyproject.toml
runs/2026-09-07-dryrun-one-month/api-call-evidence.txt
runs/2026-09-07-dryrun-one-month/brief.md
runs/2026-09-07-dryrun-one-month/claude-planning-metadata.json
runs/2026-09-07-dryrun-one-month/freeze-test-results.json
runs/2026-09-07-dryrun-one-month/plan-structure-check.json
runs/2026-09-07-dryrun-one-month/plan.md
runs/2026-09-07-dryrun-one-month/prompt-inventory.json
runs/2026-09-07-dryrun-one-month/quota-claude-after.txt
runs/2026-09-07-dryrun-one-month/quota-claude-before.txt
runs/2026-09-07-dryrun-one-month/quota-claude-final.txt
runs/2026-09-07-dryrun-one-month/quota-codex-after.txt
runs/2026-09-07-dryrun-one-month/quota-codex-before.txt
runs/2026-09-07-dryrun-one-month/quota-codex-final.txt
runs/2026-09-07-dryrun-one-month/routing-audit-final.json
runs/2026-09-07-dryrun-one-month/routing-audit.json
runs/2026-09-07-dryrun-one-month/verification-report.txt
runs/2026-09-07-dryrun-one-month/verification-report.txt.bak
runs/2026-09-07-dryrun-one-month/verification-sha256-final.json
runs/2026-09-07-dryrun-one-month/verification-sha256.json
runs/2026-09-07-dryrun-one-month/verified-config-redacted.yaml
runs/_reference/hermes-review-verdict-final.md
runs/_reference/hermes-review.md
runs/_reference/hermes-su2qc-commands.sh
runs/_reference/su2qc-run-protocol-SKILL.md.bak-20260907T135704
runs/campaign_v060/00_conventions.md
runs/campaign_v060/00_repair/v050_working_tree_divergent/README.md
runs/campaign_v060/00_repair/v050_working_tree_divergent/analysis/figures/exact_casimir.png
runs/campaign_v060/00_repair/v050_working_tree_divergent/analysis/figures/exact_channels.png
runs/campaign_v060/00_repair/v050_working_tree_divergent/analysis/figures/exact_density.png
runs/campaign_v060/00_repair/v050_working_tree_divergent/circuits/trotter_scaling.json
runs/campaign_v060/00_repair/v050_working_tree_divergent/manifest.json
runs/campaign_v060/00_repair/v050_working_tree_divergent/slope-conditioning.json
runs/campaign_v060/CAMPAIGN_STATE.json
runs/campaign_v060/CAMPAIGN_TODO.md
runs/campaign_v060/CLAIM_TABLE.md
runs/campaign_v060/CONFIG.resolved.yaml
runs/campaign_v060/GATE_LEDGER.jsonl
runs/campaign_v060/GATE_THRESHOLDS.yaml
runs/campaign_v060/PREREGISTRATION.md
runs/campaign_v060/sessions/c060_p0_20260907/ENV.md
runs/campaign_v060/sessions/c060_p0_20260907/PHYSICS_STATUS.md
runs/campaign_v060/sessions/c060_p0_20260907/SESSION_SUMMARY.md
runs/campaign_v060/sessions/c060_p0_20260907/TAKEOVER.md
runs/campaign_v060/sessions/c060_p0_20260907/baseline-regression.log
runs/campaign_v060/sessions/c060_p0_20260907/baseline-regression.xml
runs/campaign_v060/sessions/c060_p0_20260907/baseline-sandbox-sha256.json
runs/campaign_v060/sessions/c060_p0_20260907/baseline-status.txt
runs/campaign_v060/sessions/c060_p0_20260907/brief.md
runs/campaign_v060/sessions/c060_p0_20260907/inventory.json
runs/campaign_v060/sessions/c060_p0_20260907/legacy-input-sha256.json
runs/campaign_v060/sessions/c060_p0_20260907/plan-amendment.md.partial
runs/campaign_v060/sessions/c060_p0_20260907/plan-amendment.stderr.log
runs/campaign_v060/sessions/c060_p0_20260907/plan-retry.md.partial
runs/campaign_v060/sessions/c060_p0_20260907/plan-validation-issues.md
runs/campaign_v060/sessions/c060_p0_20260907/plan.md
runs/campaign_v060/sessions/c060_p0_20260907/plan.md.partial
runs/campaign_v060/sessions/c060_p0_20260907/planning-retry.stderr.log
runs/campaign_v060/sessions/c060_p0_20260907/planning.stderr.log
runs/campaign_v060/sessions/c060_p0_20260907/preservation-check.json
runs/campaign_v060/sessions/c060_p0_20260907/repair-G1.log
runs/campaign_v060/sessions/c060_p0_20260907/repair-G2.log
runs/campaign_v060/sessions/c060_p0_20260907/repair-G3.log
runs/campaign_v060/sessions/c060_p0_20260907/repair-regression.log
runs/campaign_v060/sessions/c060_p0_20260907/repair-regression.xml
runs/campaign_v060/sessions/c060_p0_20260907/repair-review-input.md
runs/campaign_v060/sessions/c060_p0_20260907/repair-source-sha256.json
runs/campaign_v060/sessions/c060_p0_20260907/repair.diff
runs/campaign_v060/sessions/c060_p0_20260907/review-regression-evidence.md
runs/campaign_v060/sessions/c060_p0_20260907/review-regression-evidence.stderr.log
runs/campaign_v060/sessions/c060_p0_20260907/review-repair-2.md
runs/campaign_v060/sessions/c060_p0_20260907/review-repair-2.stderr.log
runs/campaign_v060/sessions/c060_p0_20260907/review-repair.md
runs/campaign_v060/sessions/c060_p0_20260907/review-repair.stderr.log
runs/campaign_v060/sessions/c060_p0_20260907/run.log
runs/campaign_v060/sessions/c060_p0_20260907/slope-conditioning.json
runs/campaign_v060/sessions/c060_p0_20260907/takeover-input.md
runs/campaign_v060/sessions/c060_p0_20260907/value-stability.json
runs/campaign_v060/sessions/c060_p0_20260908_2/ENV.md
runs/campaign_v060/sessions/c060_p0_20260908_2/SESSION_SUMMARY.md
runs/campaign_v060/sessions/c060_p0_20260908_2/TIME_LEDGER.md
runs/campaign_v060/sessions/c060_p0_20260908_2/evidence-manifest.json
runs/campaign_v060/sessions/c060_p0_20260908_2/final-G1.log
runs/campaign_v060/sessions/c060_p0_20260908_2/final-G2.log
runs/campaign_v060/sessions/c060_p0_20260908_2/final-G3.log
runs/campaign_v060/sessions/c060_p0_20260908_2/final-manifest.json
runs/campaign_v060/sessions/c060_p0_20260908_2/final-manifest.sha256
runs/campaign_v060/sessions/c060_p0_20260908_2/final-regression.log
runs/campaign_v060/sessions/c060_p0_20260908_2/final-regression.xml
runs/campaign_v060/sessions/c060_p0_20260908_2/gate_C0.log
runs/campaign_v060/sessions/c060_p0_20260908_2/gate_C0.xml
runs/campaign_v060/sessions/c060_p0_20260908_2/gate_C0_command.txt
runs/campaign_v060/sessions/c060_p0_20260908_2/git-status-final.txt
runs/campaign_v060/sessions/c060_p0_20260908_2/jmax1-counts.log
runs/campaign_v060/sessions/c060_p0_20260908_2/mypy.log
runs/campaign_v060/sessions/c060_p0_20260908_2/predictions_C0.md
runs/campaign_v060/sessions/c060_p0_20260908_2/predictions_C0.md.partial
runs/campaign_v060/sessions/c060_p0_20260908_2/predictions_C0.stderr.log
runs/campaign_v060/sessions/c060_p0_20260908_2/prior-repair-G1.log
runs/campaign_v060/sessions/c060_p0_20260908_2/prior-repair-G2.log
runs/campaign_v060/sessions/c060_p0_20260908_2/prior-repair-G3.log
runs/campaign_v060/sessions/c060_p0_20260908_2/prior-repair-regression.xml
runs/campaign_v060/sessions/c060_p0_20260908_2/prior-slope-conditioning.json
runs/campaign_v060/sessions/c060_p0_20260908_2/review_C0.md
runs/campaign_v060/sessions/c060_p0_20260908_2/review_C0.stderr.log
runs/campaign_v060/sessions/c060_p0_20260908_2/review_C0_retry.md
runs/campaign_v060/sessions/c060_p0_20260908_2/review_C0_retry.stderr.log
runs/campaign_v060/sessions/c060_p0_20260908_2/ruff.log
runs/campaign_v060/sessions/c060_p0_20260908_2/signoff_C0.md
runs/campaign_v060/sessions/c060_p0_20260908_2/signoff_C0.stderr.log
runs/campaign_v060/sessions/c060_p0_20260908_2/tier2_ledger.md
runs/campaign_v060/sessions/c060_p0_20260908_2/twin-probe.log
runs/campaign_v060/sessions/c060_p0_20260908_2/twin_variance.json
runs/campaign_v060/tests/gate_C0/conftest.py
runs/campaign_v060/tests/gate_C0/test_estimator.py
runs/campaign_v060/tests/gate_C0/test_jmax1_counts.py
runs/campaign_v060/tests/gate_C0/test_twin_variance.py
runs/campaign_v060/tests/gate_C0/test_v1_regression.py
runs/section8_v0.5.0_20260907T0628Z/OUTPUT_CONTRACT.json
runs/section8_v0.5.0_20260907T0628Z/analysis/figures/exact_casimir.png
runs/section8_v0.5.0_20260907T0628Z/analysis/figures/exact_channels.png
runs/section8_v0.5.0_20260907T0628Z/analysis/figures/exact_density.png
runs/section8_v0.5.0_20260907T0628Z/analysis/tables/exact_at_window.csv
runs/section8_v0.5.0_20260907T0628Z/analysis/tables/exact_mass_scan.csv
runs/section8_v0.5.0_20260907T0628Z/analysis/tables/exact_timeseries.csv
runs/section8_v0.5.0_20260907T0628Z/bin_clock.sh
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r0.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r1.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r2.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/l12_r3.qasm
runs/section8_v0.5.0_20260907T0628Z/circuits/resources_logical.md
runs/section8_v0.5.0_20260907T0628Z/circuits/resources_synth.md
runs/section8_v0.5.0_20260907T0628Z/circuits/trotter_scaling.json
runs/section8_v0.5.0_20260907T0628Z/compile/layout.json
runs/section8_v0.5.0_20260907T0628Z/compile/resources_routed.json
runs/section8_v0.5.0_20260907T0628Z/compile/resources_routed.md
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
runs/section8_v0.5.0_20260907T0628Z/gates/gate_G4.py
runs/section8_v0.5.0_20260907T0628Z/logs/agents/l12_builder.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/l12_builder.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route1_fix_escalation.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route1_fix_escalation.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route2_attempt2.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/route2_attempt2.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/synth_l12.out.md
runs/section8_v0.5.0_20260907T0628Z/logs/agents/synth_l12.prompt.md
runs/section8_v0.5.0_20260907T0628Z/logs/cmd/run_g2.log
runs/section8_v0.5.0_20260907T0628Z/logs/cmd/run_g4.log
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
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/circuits/synth_l12.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/route.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/compile/run_g4.py
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
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/replicate.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/__init__.py
runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py
runs/section8_v0.5.0_20260907T0628Z/tests/conftest.py
runs/section8_v0.5.0_20260907T0628Z/tests/pytest.ini
runs/section8_v0.5.0_20260907T0628Z/tests/test_dynamics.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_l12.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_route_gausskernel.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_route_spinnet.py
runs/section8_v0.5.0_20260907T0628Z/tests/test_synth_l12.py
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
tools/refresh_graph_v040.py
tools/report_v040.py
tools/tn_sweep.py
tools/validate_v040.py


# Source: prompts/gi_cost_campaign_v.0.6.2.md
# SU2ZX · GI-Cost Campaign · v0.6.2 repair prompt — close C0 for real, amend C1, then Phase 2

**Hermes prompt v0.6.2 · path: `SU2ZX/prompts/gi_cost_campaign_v.0.6.2.md`**
**Amends v0.6.1 (which amends v0.6.0). Both remain in force; this file adds rulings R7–R12 and a repair order for the items the C0 sign-off of session `c060_p0_20260908_2` marked blocking. Where files disagree, the newest wins. Nothing here loosens a threshold.**

**Launch (human, one line, from the SU2ZX repository root):** `hermes` then
`@prompts/gi_cost_campaign_v.0.6.2.md  Repair and re-gate C0, then continue. T0 is now.`
Everything below is addressed to you, the Hermes orchestrator session.

---

## 0. State as found (commit `723d083`) and what the evidence says

Recorded: **C0 partial, C1 pass, C2 not started.** Final fresh regression 45/45; G1 17/17, G2 20/20, G3 PASS (S8/C7 excluded by D4); the j_max = 1 sector test passed against the independent generating function 3 + 36x² + 74x⁴ + 36x⁶ + 3x⁸; R2 restorations and four scoped commits done; R5 mapping confirmed by the sign-off from `conventions.py` alone. The sign-off (`signoff_C0.md`) lists seven blocking fixes and the retry review (`review_C0_retry.md`) agrees. They are all addressed below. Read both files at boot; they are the review of record.

**The V10 failure is diagnosed here, and the diagnosis is a hypothesis you must confirm before fixing.** Evidence: `twin_variance.json` shows 5 repeats at r = 0 (compact twin, 1,024 shots, run-time seeds 500…504) giving **3 distinct dictionaries, every one with exactly 47 keys**; `twin-probe.log` shows another configuration giving 4 distinct of 5 with 24 keys each; the v0.5.0 twin printed **2σ = 0.000** at r = 0 for five repeats of 4,000 shots (status report §3.4). One shared RNG stream would give 1 distinct dictionary; five independent draws would give 5 with fluctuating key counts. Neither fits. What fits all three observations: **Aer seeds each shot with `seed_simulator + shot_index`** in its sampled-noise path, so a run at seed s + 1 replays shots 1…N of the run at seed s and adds one new shot. Adjacent dictionaries are then identical exactly when the dropped outcome equals the added one (probability Σ_k p_k², about 0.5 at r = 0 where one codeword dominates), which predicts about 1 + 4 × 0.5 = 3 distinct of 5, equal key counts, and a bootstrap σ ≈ 0 over five near-identical repeats. `run_counts` uses `seed + k`, and `run_g4.py` uses `500 + 10·r` across time points with 4,000 shots — so every v0.5.0 twin repeat overlapped its neighbours in 3,999 of 4,000 shots. The construction-time `seed_simulator = 101` is not the cause; the run-time seed does override it, as R4 anticipated.

Consequences if confirmed: (i) the fix is in the seed derivation, not in Aer options; (ii) every v0.5.0 twin σ (the r = 0 datum P_surv 0.946 ± 0.000) is void and must be so recorded; (iii) the E2 endpoint's σ_stat definition is unaffected (bootstrap over repetitions is right once the repetitions are independent).

---

## 1. Rulings (apply, log the number, do not re-plan)

**R7 · V10 diagnosis protocol and fix.** Before any code change, on a sandbox copy carrying the HEAD version of `twin.py` (`git show HEAD:runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py`), run the following and write `sessions/<tag>/v10_diagnosis.json`:

1. **Shift test (decisive).** For the r = 0 measured ISA circuit on the production twin `twin_backend(seed=101)` (the `AerSimulator.from_backend` path `run_g4.py` uses), run `sim.run(t, shots=S, seed_simulator=s, memory=True)` at s = 500 and s = 501 with S = 1,024 and compare per-shot memories: record whether `mem_500[1:] == mem_501[:-1]` (list equality, all S − 1 entries). Repeat on the compact twin. Record true/false per path.
2. **Equal-seed control.** Two runs at the same seed must return identical dictionaries (bit-identical `get_counts()`); record.
3. **Well-separated seeds.** Five runs at seeds spaced by more than S (for example 500, 500 + 10⁶, 500 + 2·10⁶, …) must give five distinct dictionaries; record the distinct count and key counts.
4. **Pre-fix V10 on the production path**, r = 0 (S = 4,000) and r = 1 (S = 1,024; the r = 1 twin is slow, see §2 timing), 5 repeats each with the HEAD seeding: record distinct counts, key counts, bootstrap two_sigma per observable.

If the shift test is **true** on the production path: the hypothesis is confirmed; fix `run_counts` so per-repeat seeds are derived from `numpy.random.SeedSequence(seed).spawn(len(isa_meas_list))`, each converted to a 31-bit int, passed only through `sim.run(..., seed_simulator=...)` (drop the `set_options` mutation), and returned alongside the counts in a sidecar `run_counts_meta(...)` or a module-level `LAST_SEEDS` so the ledger can record the seeds used; keep the signature `run_counts(isa_meas_list, shots, seed, sim)` so `run_g4.py` is unchanged. Post-fix: steps 1–4 again; the shift test must now be **false**, equal seeds still identical, five distinct at r = 0 and r = 1. If the shift test is **false** on both paths, the hypothesis is wrong: record the four measurements, then compare `mem_500` and `mem_501` for any other structural overlap (equal multisets, equal prefixes, equal every-n-th entry), report what is found, and stop the V10 lane with row `fail: cause not located` and the raw memories saved — do not change seeds blindly.

**R8 · V10 acceptance (replaces the `any(two_sigma > 0)` clause).** On the production twin, post-fix, r = 0 and r = 1, five repeats: (a) five distinct dictionaries; (b) for every observable whose multinomial variance Var_s (computed from the pooled kept counts, values o_k per codeword as `predictions_C0.md` §2.2) is nonzero, `two_sigma/2` lies within a factor 2 of 0.894 × √(Var_s/(5·N̄_kept)); (c) observables with Var_s = 0 are listed as structurally empty, never counted as failures or as evidence of determinism; (d) the D-C0 case letter from `predictions_C0.md` §3.4 is recorded with the mechanism; (e) the negative control is a *run*, not a list comprehension: five repeats with all five run-time seeds forced equal must produce one distinct dictionary and the test must fail on it. The pre-fix run of R7 step 4 is the "would have failed on the old code" evidence. Shots: r = 0 at 4,000; r = 1 at 1,024 with N̄_kept used as measured. Budget the r = 1 twin at ≈ 10 min per 5 × 1,024 shots (v0.5.0 measured 35 min for 5 × 4,000); pre-fix plus post-fix plus control is under an hour. Predictions in `predictions_C0.md` (P4–P6) are judged, not edited; a miss goes to `DISCREPANCIES.md`.

**R9 · V11 test as specified (replaces `test_estimator.py`).** Four rows, each 1e-10, each with an **independent oracle written inside the test** from the classification rule stated in v0.6.1 §2.2 (decode labels with `l12.decode`, then classify with the test's own function — never by calling `twin.channel_weights` or `twin.channel_closure_residual` for the expected side):

1. *Synthetic observables with negative quasi-weights.* At least eight codewords across all four channels plus at least one N ≠ 4 codeword with |q_v| = 2 and one N ≠ 4 codeword with no |q_v| = 2 (which must fall in no channel); weights include at least two genuinely negative entries whose channel totals are still checked exactly (a channel total may itself be negative). Closed-form expected values written as literals.
2. *Closure.* `P_surv + P_meson + P_BBbar + P_other = W_kept(N=4) + W_kept(N≠4 ∧ ∃v |q_v|=2)`, both sides from the test's oracle; `twin.channel_closure_residual` must return 0 to 1e-10 on the same input, and must return the correct nonzero residual on an input deliberately constructed to violate the identity through an unphysical key (which `decode` must reject).
3. *Remainder identity, stated correctly.* At j_max = ½ with n = (1, 1, 0, 2), Gauss's law at v3 and v4 forces j2 = j3 = j4 and at v1, v2 forces j1 to differ by ½, so the q = (1, −1, 0, 0) sector contains **exactly two** link configurations, (0, ½, ½, ½) and (½, 0, 0, 0). The test states this derivation in its docstring and asserts `P_surv − P_stretched − P_short = 0` to 1e-10 on every synthetic input — an equality, not an inequality — and additionally asserts that `l12` has exactly two physical codes with that occupation pattern. (At j_max = 1 there would be four; that is a Phase 2 note, not a C0 row.)
4. *Matched subtraction and yield.* ΔO on synthetic pairs; yield via `twin.postselect` on synthetic counts mixing physical and unphysical bitstrings with a known physical fraction — not via a caller-supplied key set.

The ledger carries a fifth row `V11 ODR closure: deferred to Phase 5 (V12)` with status `deferred`, not `fail`.

**R10 · V1 evidence must be this session's.** `test_v1_regression.py` recomputes the three slopes from the final-snapshot G3 output, computes the propagated bound itself (centered log-r weights over r = 8…128, Σw² = 4.80, first-order propagation of the primary error-array deltas against `git show HEAD`), writes `sessions/<tag>/slope-conditioning.json`, and asserts |Δslope| ≤ 10 × bound and the G3 band. The legacy-suite row cites `sessions/<tag>/final-regression.xml` produced on the snapshot that contains the fixed `twin.py`, `replicate.py` and the new tests — never a prior session's XML.

**R11 · Evidence chain order.** At the gate: (1) run the one gate command **with** `--junitxml=sessions/<tag>/gate_C0.xml` and tee the log; (2) gatekeeper writes `GATE_LEDGER.jsonl` rows and `CAMPAIGN_STATE.json`; (3) write `sessions/<tag>/evidence-manifest.json` (SHA-256 of every file the rows cite, plus the ledger, state, thresholds, preregistration, and the test files) and its `.sha256`; (4) Opus review of the manifest's files, bounded to the listed files and ≥ 40 turns (last session's review died at 15 turns and left an empty file — a review that cannot finish is rerun with a narrower file list, never recorded as done); (5) Fable sign-off naming the manifest hash; (6) after sign-off, only `SESSION_SUMMARY.md` and the commit are written, and the manifest lists them as post-sign-off. Any write to a manifested file after step 3 invalidates the manifest and restarts at step 3.

**R12 · Cleanliness, C1 amendment, and the v0.5.0 twin note.**
- `git status` at boot must show only this session's work. `artifacts/SU2ZX_GI_cost_campaign_v060_last_run.zip` is moved (not deleted) to `zip_results/`, which is where archives live; if it is not ignored there, add `zip_results/*.zip` to `.gitignore` with a commit. C0's final criterion is `git status` empty after the gate commit `campaign: C0 pass <one line>`.
- `PREREGISTRATION.md` is amended deliberately: inline the three SHA-256 values (thresholds, preregistration-of-record is the hash *after* this amendment, conventions); resolve the conventions-hash ambiguity — `CAMPAIGN_STATE.hashes.conventions` (d7de725c…) and the preregistration line (fb3b7525…) differ; record both, labelled `conventions.py` and `00_conventions.md`, and make the state file carry both keys; add the prespecified defect classes (v0.5.0 Phase 5 list plus "KR K-scan changes after a Hamiltonian fix → rerun V8, new C3 row" plus, new, "twin seed derivation changes → rerun V10, new C0 row"); add one-line reasons to R1/R3/R4. Re-hash, write `gates.C1 = pass (amended <utc>)` with the old and new hashes in the row, commit `campaign: C1 amended`.
- Append to the v0.5.0 run's `physics/DISCREPANCIES.md` and to D6 in `run/DECISIONS.md`: "D-E: v0.5.0 twin repeats were seeded `seed + k` and overlap in N − 1 of N shots under Aer's per-shot seeding; every v0.5.0 twin σ is void; no v0.5.0 twin number was ever gated. Mechanism evidence: `runs/campaign_v060/sessions/<tag>/v10_diagnosis.json`." Also grep `src/su2zx/` (v0.4.0) for the same consecutive-seed pattern used with Aer sampling; report in the summary; do not modify v0.4.0 (archived, published) — a finding there is a note for its errata, not a repair.

---

## 2. Order of work (target 5 h to the C0 gate; hard cutoff 12 h)

1. **Boot (≤ 20 min).** Session tag `c060_p0_<YYYYMMDD>_3`. Read `CAMPAIGN_STATE.json`, `signoff_C0.md`, `review_C0_retry.md`, `predictions_C0.md`. Hash checks; codeword 3793; quota check into `ENV.md` (no CLI updates, answer update prompts "no"); `TIME_LEDGER.md`, `RESUME_LOCK`. Apply the zip move of R12.
2. **Regression (rule 12)** on a fresh sandbox: legacy 4-file suite, G1–G3, `tests/gate_C0` as it stands (expect the V10 failure reproduced — record it, it is the pre-fix baseline).
3. **V10 diagnosis (R7 steps 1–4, pre-fix)** — TEST-BENCH lane, no code change, results into `v10_diagnosis.json`. Opus reads the JSON and rules "confirmed / not confirmed" in `sessions/<tag>/v10_ruling.md` before any edit to `twin.py`.
4. **Wave 1 (parallel, disjoint files):** A0a′ fix `run_counts` per R7 and rewrite `tests/gate_C0/test_twin_variance.py` per R8 (Codex; 60-minute box); A0c′ rewrite `tests/gate_C0/test_estimator.py` per R9 (Codex; 45-minute box); A0d′ rewrite `tests/gate_C0/test_v1_regression.py` per R10 (Codex; 30-minute box). Each lane gets an Opus review with a file list of at most six files and ≥ 40 turns; blocking versus advisory.
5. **Wave 2:** post-fix R7 steps 1–4 and the R8 runs on the production twin (r = 0, r = 1, negative control); V1 rerun on the final snapshot (legacy suite + G1–G3 + slope conditioning); the R12 DISCREPANCIES/D6 appends; the v0.4.0 seed-pattern grep.
6. **Gate C0 (R11).** Command: `PYTHONPATH=runs/section8_v0.5.0_20260907T0628Z/src .mamba/envs/su2zx/bin/python -m pytest runs/campaign_v060/tests/gate_C0 -q -p no:cacheprovider --junitxml=runs/campaign_v060/sessions/<tag>/gate_C0.xml`. Rows: V1 (R1/R10), V10 (R8, with seeds used, distinct counts, σ table, D-C0 case, control outcome), V11 four rows plus the `deferred` ODR row, Tier 2 (carry the existing ledger; lint/mypy findings stay deferred to Phase 2 as already rowed), cleanliness. Commit `campaign: C0 pass <one line>` (or `partial` naming the criterion), `CAMPAIGN_STATE.json` → phase 1.
7. **C1 amendment (R12)**, commit. Phase → 2.
8. **Phase 2** per v0.6.1 §4 unchanged (package move first, then V2 → V3 → V5 → V7 counts → V4 → V7 dynamics → V6 → D-C8), with one Fable planning call, **only if ≥ 6 h remain before the cutoff**; otherwise stop after C1 with `next_action: "Run phase 2 per v0.6.1 §4"`. Gate C2 partial at the cutoff if opened.

Timing note: the r = 1 production twin is the slow item (≈ 10 min per 5 × 1,024 shots). Run its pre-fix and post-fix instances detached with `wait_for_done.sh`, not in the foreground of a review.

---

## 3. Acceptance, row by row (what "pass" means this session)

| Row | Pass requires | Evidence file |
|---|---|---|
| V10 mechanism | shift test true pre-fix and false post-fix on the production path (or the not-confirmed branch of R7 fully recorded) | `v10_diagnosis.json`, `v10_ruling.md` |
| V10 distinctness | 5 of 5 at r = 0 and r = 1 post-fix; 1 of 5 under the equal-seed control; pre-fix 3–4 of 5 recorded | `twin_variance.json` (both r keys present) |
| V10 variance | `two_sigma/2` within [0.5, 2] × 0.894·√(Var_s/(5·N̄_kept)) on every Var_s > 0 observable at both r; empty channels listed | `twin_variance.json`, ledger row |
| V11 | four rows at 1e-10 with in-test oracles; the violating-input residual test; the two-configuration equality; `deferred` ODR row | `gate_C0.xml`, ledger |
| V1 | 45/45 on the final snapshot; G1 17/17, G2 20/20, G3 core PASS; slopes within 10× bound and band, bound computed this session | `final-regression.xml`, `final-G{1,2,3}.log`, `slope-conditioning.json` |
| Evidence chain | manifest written after ledger and state, before review and sign-off; hashes match on recheck; review and sign-off non-empty and on the manifest hash | `evidence-manifest.json(.sha256)`, `review_C0.md`, `signoff_C0.md` |
| Cleanliness | `git status` empty after the gate commit | `git-status-final.txt` |
| C1 amended | inline hashes, both conventions hashes, defect classes, reasons; old and new preregistration hash in the row | `PREREGISTRATION.md`, ledger |

No row may cite a prior session's artifact as its evidence. A row that cannot be met is `fail` or `deferred` with a reason; C0 is `pass` only when every row above is `pass` or (ODR only) `deferred`.

---

## 4. Stop conditions

- Regression not green (excluding the expected V10 pre-fix failure) within 2 h → repair session only.
- Shift test false on both twin paths and no structural overlap found → V10 `fail: cause not located`, C0 partial, no Phase 2; summary's first line says so, with the raw memories attached.
- Any post-fix variance ratio outside [0.5, 2] on an interior observable → not fixed by re-seeding; `DISCREPANCIES.md` entry, row fails, C0 partial.
- Review or sign-off unavailable → `partial: awaiting review/sign-off`; no substitute model; no phase advance.
- Cutoff → gate the open phase partial; `next_action` verbatim.

---

## 5. Session summary (v0.6.0 §9 format) — additionally state

- The V10 mechanism verdict in one sentence, with the shift-test truth values pre- and post-fix and the seeds used.
- The variance table: per observable, `two_sigma/2`, predicted SE, ratio, at r = 0 and r = 1.
- Which sign-off items 1–7 were closed and by which file.
- The v0.4.0 seed-pattern grep result (finding or none), not acted on.
- `git log --oneline -6`; the three hashes plus both conventions hashes; the exact commands that rerun C0 and (if reached) C2 from a clean shell.
- Anything a human must know before trusting a number — starting with: no hardware job has ever been submitted, and every v0.5.0 twin σ is void.

**Start now.** Diagnose before you fix, fix once, prove it on the production path, then gate. The campaign is judged on E1–E5, on the honesty of the ledger, and on whether a physicist can rebuild every number from the tree.


# Source: prompts/gi_cost_campaign_v.0.6.1.md
# SU2ZX · GI-Cost Campaign · v0.6.1 session prompt — close C0, preregister, extend the reference (Phases 0 → 2)

**Hermes prompt v0.6.1 · path: `SU2ZX/prompts/gi_cost_campaign_v.0.6.1.md`**
**Amends `prompts/gi_cost_campaign_v.0.6.0.md` (hereafter "v0.6.0"). v0.6.0 remains the campaign document: hypotheses, endpoints E1–E5, the claim table, the validation ladder V1–V14, the phase table, the thresholds, the decision rules, the deliverables tree and the summary format are all unchanged and are not repeated here. This file adds the human rulings the last session was waiting for, fixes three defects found in v0.6.0, and sets the scope of this session. Where this file and v0.6.0 disagree, this file wins; where both are silent, v0.5.0 mechanics apply as resolved in Section 1.**

**Launch (human, one line, from the SU2ZX repository root):** `hermes` then
`@prompts/gi_cost_campaign_v.0.6.1.md  Run phase 0 to C0, then continue. T0 is now.`
Everything below is addressed to you, the Hermes orchestrator session.

---

## 0. State as found, and the rulings that unblock it

The last session (`runs/campaign_v060/sessions/c060_p0_20260907/`) established: the legacy suite is 45/45 green after a test-only repair of `tests/test_route_gausskernel.py` (`kernel_dimension(1.0) == 152` plus projector orthonormality, no j_max = 1 Hamiltonian claim from route B); G1 17/17, G2 20/20 and G3 PASS in a sandbox copy; the Fable plan and its amendment (`plan.md`) are the Phase 0 plan. The session then stopped with `phase = 0`, `gates = {}`, C0 not passed, because four things needed a human. Those rulings follow. They are final for this campaign; apply them, log the ruling number in the ledger row, and do not re-plan them.

**R1 · V1 value-stability wording (replaces the 1e-12 slope criterion).** Every *primary* numeric quantity in the committed gate evidence at `eee1e162` (dimensions, sector counts, spectra, aligned matrix elements, time series, Trotter error arrays, energies, leakage probabilities, window numbers) must agree with the sandbox rerun to 1e-12 absolute. A *derived* quantity obtained by a fit — the three Trotter log-slopes in `circuits/trotter_scaling.json` — is compared at **10 × its first-order propagated conditioning bound** computed from the primary deltas by the method already recorded in `slope-conditioning.json` (centered log-r weights over r = 8…128, Σw² = 4.80), and must in addition lie inside the G3 band [−2.3, −1.7]. The bound and the measured delta are written next to every slope, every time. `GATE_THRESHOLDS.yaml` records this as `V1.primary_abs: 1.0e-12` and `V1.slope_rule: propagated_bound_x10`. Reason for the record: a 1e-12 slope stability would require the r = 128 error (3.7e-7, itself a difference of O(1) probabilities) to be stable to 1.3e-18, below double-precision epsilon; the criterion was ill-posed for a log-slope, not tight. This is the only threshold change of the campaign and it is a wording repair, not a loosening of any physics tolerance.

**R2 · Dirty working tree (the cleanliness criterion).** Dispositions by path, in this order, before the regression step:

1. `runs/section8_v0.5.0_20260907T0628Z/circuits/trotter_scaling.json` and the three modified figures under `analysis/figures/`: **the committed HEAD versions are the evidence of record** (they are what G3 signed off). Copy the working-tree versions, with SHA-256 and a copy of `slope-conditioning.json`, into `runs/campaign_v060/00_repair/v050_working_tree_divergent/` with a one-paragraph `README.md` stating the cause (log-fit conditioning, primary arrays agree to ≤ 5.4e-15), then `git checkout -- <those four paths>`. Nothing is deleted.
2. The untracked v0.5.0 Phase-4 paths under the run directory (16 paths: `synth_l12.py`, `test_synth_l12.py`, `compile/`, `twin/`, `gate_G4.py`, `resources_synth.md`, `resources_routed.*`, `layout.json`, `run_g4.log`, `synth_l12.*.md`, `exact_at_window.csv`, `compile/__init__.py`, `twin/__init__.py`): commit after an Opus read-through, message `campaign: commit phase-4 artifacts from v0.5.0`.
3. `STATUS_REPORT_20260907.md`, `.graphifyignore`, `GRAPHIFY_UPDATE.md`, `artifacts/logs/v050/`, `docs/refs/` (three files incl. the Nine-Month Plan PDF), `prompts/gi_cost_campaign_v.0.6.0.md` and this file: commit, message `repo: status report, graphify refresh, campaign references (2026-09-07)`.
4. `runs/2026-09-07-dryrun-one-month/` and `runs/_reference/`: run the repository's secret scan (`tools/` provenance/secret patterns plus: `sk-`, `hf_`, `ghp_`, `ibm`/`qiskit` token shapes, `Bearer`, `.env` contents, private-key headers) on every file. Files that pass: commit, message `ops: hermes run records 2026-09-07`. A file that fails is moved, not deleted, to `.work/quarantine/<same relative path>` and listed in the session summary. Check that `verified-config-redacted.yaml` is actually redacted before committing it.
5. After steps 1–4, `git status` must be empty except the campaign tree, which is committed at the gate. Commits are by explicit path list, never `git add -A`.

**R3 · V11 scope at C0.** The "channel closure re-reported after ODR" clause of V11 is moved to Phase 5 (it becomes a sub-row of V12, evaluated on the real estimator code path when readout mitigation and ODR exist). V11 at C0 consists of the four executable rows: synthetic quasi-distribution observables with negative entries (1e-10), channel closure identities as corrected in Section 2.2 below, matched subtraction ΔO(t) = O(t) − O(0) (1e-10), and yield. With that, V11 can PASS at C0; a `deferred to Phase 5` row is written for the ODR clause.

**R4 · The Fable amendment's rulings are adopted as written** (`plan.md`, "Superseding Fable amendment", items 2–5): the twin-seed conditional no-change path with the negative control; the bootstrap-SE (not per-repeat SD) variance criterion with multinomial variance; `pyzx_basic_TP` retired with the wording "pre-route equivalence error 1.0e+00 fails the ≥ 1 − 1e-10 hardware-eligibility requirement; root cause not diagnosed; no orthogonality claim"; the replicate skeleton at run-local `src/su2qc/replicate.py` (the module name `su2qc.replicate` is thereby satisfied; the repo-level package move is a Phase 2 deliverable, see Section 4).

**R5 · Coupling point P-A is the v0.5.0 window, not the v0.6.0 §2.2 ratio.** `physics/window.json` fixes g² = 4, m = 0.75, δt = 0.8333, r_max = 3, and `conventions.py` fixes the coefficients (g²/2, m, 1/2, 1/(2g²)) of (Σ E², staggered mass, hopping, −Tr(U□ + U□†)). In code units P-A is therefore **(cE, cM, cH, cB) = (2, 0.75, 0.5, 0.125)**, i.e. electric : hopping : magnetic = **1 : 0.25 : 0.0625** with μ = m/g_E = 3/8 and **g_E ≡ g²/2 = 2**, not the "1 : 0.5 : 0.25, our g_E = 1" printed in v0.6.0 §2.2 (that row corresponds to g² = 2, a point where no G2 visibility criterion or Trotter admissibility was ever established). Consequences: (i) time points are multiples of the frozen δt: **t = r·δt with r ∈ {1, 2}, t ∈ {0.8333, 1.6667}** in code units (τ = t·g_E ∈ {1.667, 3.333}), and t = 2.5 (r = 3) only if Phase 4 shows r = 2 → 3 admissible; the v0.6.0 "t ∈ {0.75, 1.5}/g_E" is void. (ii) P-S keeps the same electric scale so both points share g_E = 2: **(cE, cM, cH, cB) = (2, 0.75, 0.04, 0.04)**, ratio 1 : 0.02 : 0.02, μ = 3/8, Sufian time points τ ∈ {5, 12.5} → **t ∈ {2.5, 6.25}** in code units. (iii) The tree-level resonance check 2m = ¾ g_E reads 1.5 = 0.75 · 2, consistent with `tree_level_resonance(4) = 0.75`. The Phase 2 physics auditor (C2) recomputes this mapping from `conventions.py` and `window.json` alone; if the auditor's arithmetic differs from the numbers above, **`window.json` and `conventions.py` are the authority**, the corrected numbers go into the preregistration with a note, and the ledger records `R5 corrected`. The one-parameter wrapper `H(gE, mu, jmax)` of v0.6.0 §2.2 is defined with g_E = g²/2 so that `H(2, 3/8, 1/2)` reproduces the v0.5.0 Hamiltonian bit-for-bit (V2 checks this at 1e-12).

**R6 · Session scope.** `CONFIG.resolved.yaml`: `AUTOPILOT: true`, `STOP_AT: C2`, `SESSION_HARD_HOURS: 12`, `HARDWARE_MODE: disabled` (no IBM credentials are configured on this machine; Phase 6 stays twin-only until a human configures them — state this in the preregistration's hardware slot rather than leaving it blank). Run Phase 0 to gate C0, then Phase 1 to C1, then Phase 2 to C2, inside one session while the cutoff allows; gate whatever phase is open when the cutoff arrives as `partial` with artifacts and `next_action` set. Phase 0 and Phase 1 need **no** Fable planning call (the existing `plan.md` plus this file is the plan); Phase 2 gets exactly one, bounded at 600 s, retried at most once on an empty result, then the Section 4 plan is used as written. Fable sign-off: one call per gate, on the evidence manifest hash. Model routing as before: Codex for builds, Opus 5 for reviews and physics audit, NVIDIA workers (≤ 2) for test benches. Quota at the last check: Fable week 46 % used (resets Sep 12, 3 am Denver); Codex weekly 40 % left (resets Sep 11); re-check at boot and record in `ENV.md`. **Do not update, install or reconfigure any CLI or tool** (the last session accidentally accepted a Codex CLI update at a `/status` prompt; answer such prompts with an explicit "no"). Supervised bounded subprocesses only; no watchdog claim; no push; no hardware.

---

## 1. Reference resolution (adopt verbatim; do not re-derive)

v0.6.0 cites v0.5.0 section numbers that do not exist in `prompts/v0.5.0.md`. The last session resolved them; this table is now normative.

| v0.6.0 says | Use |
|---|---|
| "§5 lanes, review, independence" | v0.5.0 §2 roles, §3 lanes and iteration loop, §0.2 non-negotiables |
| "§7 ledger row format; only the gatekeeper writes pass" | v0.5.0 §0.2 "gates are scripts", Appendix D gate-JSON schema, `run/GATES.md`; campaign ledger `runs/campaign_v060/GATE_LEDGER.jsonl` (create at boot; one JSON object per line: `{gate, item, value, threshold, source, pass, utc, evidence, rule}`) |
| "§9.1 HARDWARE_MODE; §9.3–9.5" | v0.5.0 §7 hardware policy and Phase 6–7 texts |
| "§10.4–10.5 re-plan, resume, watchdog" | v0.5.0 §1.2 heartbeat, §1.4 extension, §4.2 escalation; no resume/watchdog section exists — bounded supervised subprocesses |
| "§13 D1–D2, D6–D11" | v0.5.0 §4.3–4.4 and `run/DECISIONS.md` D1–D5; D6 is the G4 closure row written this session; D7–D11 do not exist and are logged as absent |
| "Appendix A templates; Appendix C conventions" | v0.5.0 Appendix B; `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py` (hash fb3b7525…, record it in `hashes.conventions`) |
| `tests/gate_G1..G3` | `gates/gate_G{1,2,3}.py` plus `tests/test_route_spinnet.py`, `test_route_gausskernel.py`, `test_dynamics.py`, `test_l12.py` in the run directory (`test_synth_l12.py` reported separately, informational) |
| `GATE_LEDGER.jsonl`, `strang_table.md`, `resource_table.md`, `00_conventions.md` (v0.5.0 artifacts) | `run/GATES.md` + `gates/GATE_G*.json`; `circuits/resources_logical.md` + `trotter_scaling.json`; `compile/resources_routed.md`; `conventions.py` (copy it to `runs/campaign_v060/00_conventions.md` with a header, extended in Phase 2) |
| route A / route B | route 1 = `ham/route_spinnet.py` (dressed-vertex spin network); route 2 = `ham/route_gausskernel.py` (redundant KS space projected onto the Gauss kernel) |
| the "82-state package" | the run-local package `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/` (3,658 lines). There is **no** repo-level `src/su2qc/`; do not create a second `su2qc` namespace before the Phase 2 package move (Section 4) |

Sandbox rule (from the last session, now standing): every gate script and every legacy test runs on a fresh copy of the run directory under `.work/`; no Phase 0–2 process writes any historical JSON, figure or table in `runs/section8_v0.5.0_20260907T0628Z/`. Campaign tests import the run-local package through one path constant in `runs/campaign_v060/tests/conftest.py`.

---

## 2. Phase 0 · finish and gate C0 (target 3 h; box 5 h)

### 2.1 Order of work

1. **Boot (≤ 20 min).** T0, session tag `c060_p0_<YYYYMMDD>_2`. Read `CAMPAIGN_STATE.json` (phase 0). Verify the prompt hash of v0.6.0 (50c60ff…) and record this file's hash as `hashes.prompt_v061`. Live import probe (Python 3.11.16, NumPy 2.4.6, SciPy 1.17.1, Qiskit 2.5.2, Aer 0.17.2). Codeword check: `l12` encodes the stretched string ((0, ½, ½, ½), (1, 1, 0, 2)) to 3793. Quota check, `ENV.md`, `TIME_LEDGER.md`, `RESUME_LOCK`. Write the draft `GATE_THRESHOLDS.yaml` (v0.6.0 §5 verbatim plus the R1 lines; header `status: draft`).
2. **R2 dispositions** (steps 1–4 of R2) — before regression, so the sandbox compares against a tree that equals HEAD plus the campaign files.
3. **Regression (rule 12)** on a fresh sandbox copy: legacy 4-file suite (expect 45/45), G1, G2, G3 scripts, value-stability comparison against `git show eee1e162:<path>` blobs under the R1 rule. Write V1 rows. A red result here is a repair session (2 h box) and nothing else starts.
4. **P0 physics predictions (Opus, before A0a/A0d run)** → `sessions/<tag>/predictions_C0.md`: the j_max = 1 sector counts (3, 36, 74, 36, 3; total 152) derived independently by generating function / transfer matrix; the bootstrap-SE expectations for V10 per the amendment §3 (SE = √(Var_s/(R·N̄_kept)), multinomial Var_s, R = 5); which D-C0 case applies at r = 0.
5. **Wave 1 (parallel, disjoint files):** A0a twin variance (V10) per amendment §3 — pre-fix run first at r = 0 and r = 1; "override harmless" recorded if distinct and within 2× SE; negative control with all five run-time seeds forced equal must fail; only on identical dictionaries locate the cause and fix. A0d: `tests/gate_C0/test_jmax1_counts.py` (route 1 basis and route 2 kernel labels versus P0's derivation; a mismatch fails the row and is not edited away), `tests/gate_C0/test_v1_regression.py` (the R1 wrapper), `src/su2qc/replicate.py` skeleton (manifest hashing + V1 comparison). A0b lint: ruff and mypy on the run-local package, safe autofixes only, per-line ignores with a reason, 45-minute box, then V1 rerun on the post-lint snapshot.
6. **Wave 2:** A0c estimator (V11) per Section 2.2 — additive helpers in `twin.py`, legacy `observables()` output unchanged and regression-checked; `tests/gate_C0/test_estimator.py`. G4 closure: append D6 to the run's `run/DECISIONS.md` in the literal form `G4: REDUCED (campaign v0.6.0) — 2,156 logical 2q per step (D=16, h0–h3 248/248/239/241, B=174), 3,976 routed per step, 12,142 routed at r=3, gap 8.6× logical against 250; no GATE_G4.json because compile/twin_check.json was never produced (twin killed at r=1); evidence: compile/resources_routed.md, circuits/resources_synth.md, logs/cmd/run_g4.log`; one row in `run/GATES.md`; one INFO row in the campaign ledger. `pyzx_basic_TP` retired (R4 wording). Reviews (Opus) per lane, blocking versus advisory.
7. **Gate C0.** One command: `pytest runs/campaign_v060/tests/gate_C0 --junitxml=sessions/<tag>/gate_C0.xml`. Evidence manifest hashed; ledger rows written by the gatekeeper only; Fable sign-off on the manifest hash → `sessions/<tag>/signoff_C0.md`. `CAMPAIGN_STATE.json` → `phase: 1`, `gates.C0 = pass` (or `partial` with the failing criterion named). Commit `campaign: C0 <pass|partial> <one line>`. Continue to Phase 1 (R6).

### 2.2 V11 identities (corrected; from the actual `twin.py`)

`P_surv` is the full q = (1, −1, 0, 0) occupation sector; `P_stretched` (S3, j = (0, ½, ½, ½)) and `P_short` (j = (½, 0, 0, 0)) are strict subchannels of it. Branch order: any |q_v| = 2 → BB̄; q = (1, −1, 0, 0) → surv; all |q_v| = 1 → meson; Σn = 4 → other; anything else uncounted. With N_VAC = (0, 2, 0, 2), `P_BBbar` can include N ≠ 4 codewords. The test asserts, to 1e-10 on synthetic inputs including negative quasi-weights: `P_surv + P_meson + P_BBbar + P_other = W_kept(N=4) + W_kept(N≠4 ∧ ∃v |q_v|=2)`; `P_stretched + P_short ≤ P_surv` with the remainder equal to the label-computed weight of the other j-configurations in that sector; ΔO(t) on synthetic pairs; yield equals the known physical fraction. If the campaign wants "channels sum to post-selected N = 4 weight", that is an *additive* estimator helper (N = 4 filter on BB̄ plus an explicit `P_Nviol` channel) in lane A0c, never a change to legacy output.

### 2.3 C0 exit (unchanged from v0.6.0 except as ruled)

V1 (R1 rule) pass; V10 pass (either "override harmless + negative control" or "fixed + pre-fix failure"); V11 four rows pass, ODR row `deferred to Phase 5`; Tier 2 rows each `done` / `retired` / `deferred` with reason (lint, stale test, sector-count test, `pyzx_basic_TP`, replicate skeleton, estimator test, G4 closure); `git status` empty; sign-off present. Any criterion not met → `C0: partial`, phase stays 0, `next_action` names it, and the session still proceeds to write the Phase 1 documents (they do not depend on C0) but does **not** start Phase 2 builds.

---

## 3. Phase 1 · preregister (target 2 h)

As v0.6.0 Phase 1, with these contents made explicit in `PREREGISTRATION.md`:

- Section 1 of v0.6.0 verbatim (hypotheses, E1–E5, claim table → `CLAIM_TABLE.md`).
- **Coupling points per R5**, four coefficients written out in code units and in electric units, with the g_E = g²/2 = 2 identification, the time points t = r·δt, and the P-S time points t ∈ {2.5, 6.25}; the `H(coeffs=(cE, cM, cH, cB), jmax, geometry, static_charges)` API and its one-parameter wrapper.
- v0.6.0 §2.5 matched-experiment rules; the KR search budget (rule 11); the GI synthesis-sprint box (4 h); mitigation arms M0–M2; shot policy; the prespecified defect classes (v0.5.0 Phase 5 list plus "KR K-scan changes after a Hamiltonian fix → rerun V8, new C3 row").
- The R1 V1 wording, the R3 V11 deferral, the R4 twin-seed ruling, the D6 G4 closure — each with a one-line reason.
- Hardware slot: `HARDWARE_MODE: disabled — no IBM credentials configured on the Hermes machine as of <date>; Phases 5–6 run on the calibration-derived twin until a human configures credentials and flips the mode; the D7/rule-10 submission blockers then apply unchanged.` Empty slots for backend, qubit path, δ_dev table, hashes (filled at C5).
- `GATE_THRESHOLDS.yaml` header `status: frozen`, SHA-256 into `hashes.thresholds`; preregistration SHA-256 into `hashes.preregistration`; `00_conventions.md` hash into `hashes.conventions`.
- `docs/refs/README.md` listing the three reference documents (v0.5.0 review, Sufian overlap, Nine-Month Plan PDF — note that pages 19–20 of the PDF needed OCR and the extracted text is not represented as complete) and the Sufian numbers of v0.6.0 Appendix A.
- Campaign todo list: one item per phase and per V-item.

**C1 exit:** the three hashes present; claim table present; nothing else. Commit `campaign: C1 pass`. Continue to Phase 2.

---

## 4. Phase 2 · reference extension, V2–V7 (target 8 h; gate partial at the cutoff)

One Fable planning call (R6), then the lanes of v0.6.0 Phase 2 (A2a–A2e, C2 auditor). Additions and priorities:

**Package move (first, 45-minute box, one Codex lane, Opus review).** Create the repo-level `src/su2qc/` by *moving* (git mv) the run-local package, leaving a thin re-export shim at the old path so the v0.5.0 gate scripts and tests keep running unchanged; rerun the legacy suite and G1–G3 on a fresh sandbox after the move (V1 under R1). Only after that is green may A2a/A2b extend the Hamiltonian builders. If the move is not green inside the box, revert it (git checkout of the moved paths), row `deferred`, and extend the run-local package in place; the campaign does not stall on packaging.

**Priority order if time runs short** (never loosen a threshold; gate C2 partial with whatever is done):
1. **V2** four-coefficient H by both routes at P-A and P-S (spectra, aligned matrix elements 1e-12; S3 observables over [0, 20] 1e-10); the wrapper reproduces the v0.5.0 H at g² = 4, m = 0.75 to 1e-12.
2. **V3** route 2 (Gauss-kernel) j_max = 1 Hamiltonian: the 9-state link needs a 4-qubit register (codes 9–15 unphysical) or a direct 9-level sparse register; D1 estimated the redundant space at ≈ 9.8 M — build the kernel projector sparsely, sector by sector, or by the vertex-singlet product structure the last review noted; route 1 already supports j_max = 1. Agreement 1e-12; counts 152 / (3, 36, 74, 36, 3).
3. **V5** static-charge bridge counts on route 2: one plaquette with charges at v0 and v2 → 112 / (2, 27, 54, 27, 2); 2×3 with charges at the far corners → 2,417 / (4, 119, 597, 977, 597, 119, 4). Counts are convention-independent; the C2 auditor derives them independently by generating function.
4. **V7 counts** 1,727 at 2×3, j_max = ½, by both routes and by a third method (spin-network enumeration).
5. **V4** truncation table: j_max = 1 versus ½ at t ∈ {0.8333, 1.6667} (P-A) and t ∈ {2.5, 6.25} (P-S), every primary observable, one plaquette.
6. **V7 dynamics**: 2×3 stretched string defined in `00_conventions.md` (quark on an even corner, antiquark hole on the adjacent odd vertex, flux along the five-link path); expm/Krylov in the N = 6 sector at both points; P_BB̄/P_meson versus t; K_min(t) curves for 10⁻³ accuracy.
7. **V6** bridge dynamics on STATIC-112 and STATIC-2417 at P-S from the Sufian strings (v0.6.0 Appendix A); pass / near / fail, never blocking (D-C7).
8. **D-C8**: the W̄ estimator (review N6), 1 h box, else `retired` with reason.

**Physics guardrails for this phase.** j_max = 1 at 2×3 is out of scope (D-C2). Route 2 at 2×3 without static charges is 7 links × 5 states × 4⁶ = 320,000 raw states at j_max = ½ — build the kernel sparsely and never densify a 320,000² matrix. The 2×3 count 1,727 and the plaquette count 82 are prior facts from the Nine-Month Plan's spin-network count; a mismatch in either route is a route bug until three methods agree. Every table carries the rule-13 columns (`point`, `model`, `arm`, `source`). No number from the Sufian report is ever reported as ours.

**C2 gate (gatekeeper; v0.6.0 §5 thresholds):** V2 both points; V3; V5 all four counts; V7 count by three methods and route agreement; V4 table; V6 recorded; V7 dynamics and K_min files present. Failure loop as v0.5.0 G1 (diagnosis child, route-owner fix, 45-minute box); route disagreement after the box → `C2: partial`, continue on the route that passes the counts, no hardware in Phase 6 until resolved (D7). Commit `campaign: C2 <pass|partial> <one line>`. **STOP here** (`STOP_AT: C2`): write `SESSION_SUMMARY.md`, update memory, remove `RESUME_LOCK`.

---

## 5. Stop conditions (this session)

- Regression not green within 2 h of T0 → repair session only; summary's first line is the failure.
- Any lane needing access outside the repository, a tool update, hardware, or a push → that lane stops and is rowed.
- Fable planning empty twice → use Section 4 as the plan and say so. Fable sign-off unavailable → gate `partial: awaiting sign-off`, no substitute model.
- Sector counts (V3, V5, V7) disagree with the independent derivation → row fails, no test edit, `DISCREPANCIES.md` entry, C2 partial.
- 12 h hard cutoff → gate the open phase partial; `next_action` verbatim; no early turn end before that.

---

## 6. Session summary (v0.6.0 §9 format, under one page) — additionally state

- Which rulings R1–R6 were applied and whether R5's arithmetic survived the auditor.
- The final `git log --oneline -8` and the list of quarantined files, if any.
- The three hashes, the new `src/su2qc/` layout (moved or deferred), and the exact command that reruns C0, C1 and C2 tests from a clean shell.
- Quotas at end of session.
- Anything a human must know before trusting a number — starting with the fact that no hardware job has ever been submitted by this project.

**Start now.** Record T0, apply R2, run the regression, close C0, preregister, extend the reference. The campaign is judged on E1–E5, on the honesty of the ledger, and on whether a physicist can rebuild every number from the tree.


# Source: prompts/gi_cost_campaign_v.0.6.0.md
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


# Source: runs/campaign_v060/sessions/c060_p0_20260907/plan.md
# Validated Phase 0 plan with blocking-policy precedence

Fable planning and amendment both exited 0. Amendment supersedes original decisions. Higher-priority blocking policy overrides amendment permission to continue dependent BUILD after V1 PARTIAL: only independent stale-test repair and read-only diagnostics proceed; other Phase 0 lanes remain blocked pending V1 resolution. No threshold change authorized. The quasi-weight inequality in the amendment applies only to nonnegative weights, not arbitrary signed distributions; no V11 implementation is accepted under that ambiguity.

The read is complete. The proposal that blocked the earlier attempt is present, so this is not BLOCKED. Here is the Phase 0 plan.

## 1. Verdict, source resolution, and decisions

**Not blocked.** The Nine-Month Plan Section 8 is in the repository (`.work/c060_nine_month_plan.txt`, lines 571 to 713) and its objective is superseded by the campaign anyway, so Phase 0 needs it only as the wording source for the G4 closure row. C0 will end **partial by construction** because the user-preserved dirty paths keep `git status` non-empty. Every other C0 criterion can be met this session.

**Inherited references resolved by named topic** (the v0.6.0 prompt cites v0.5.0 section numbers that do not exist in `prompts/v0.5.0.md`):

| v0.6.0 reference | Actual source used |
|---|---|
| "§5 lanes, review, independence" | v0.5.0 §2 roles, §3 lanes and iteration loop, §0.2 non-negotiables |
| "§7 ledger row format, only gatekeeper writes pass" | v0.5.0 §0.2 "gates are scripts" plus Appendix D gate JSON schema and `run/GATES.md` |
| "§9.1 HARDWARE_MODE", "§9.3–9.5" | v0.5.0 §7 hardware policy, Phase 6 and 7 texts |
| "§10.4–10.5 re-plan, resume, watchdog" | v0.5.0 §1.2 heartbeat, §1.4 extension, §4.2 escalation. No resume or watchdog section exists. Supervised bounded subprocesses only, as the takeover requires. |
| "§13 D1–D2, D6–D11" | v0.5.0 §4.3 and §4.4 plus `run/DECISIONS.md` D1 to D5. D6 to D11 do not exist and are logged as absent. |
| "Appendix A templates", "Appendix C conventions" | v0.5.0 Appendix B and `src/su2qc/conventions.py` |
| `tests/gate_G1..G3` | `gates/gate_G1.py`, `gate_G2.py`, `gate_G3.py` plus `tests/test_route_spinnet.py`, `test_route_gausskernel.py`, `test_dynamics.py`, `test_l12.py` in the run directory |
| `GATE_LEDGER.jsonl`, `strang_table.md`, `resource_table.md`, `00_conventions.md` | `run/GATES.md` plus `gates/GATE_G*.json`; `circuits/resources_logical.md` plus `trotter_scaling.json`; `compile/resources_routed.md`; `conventions.py` |

**Physics and scope decisions (mine, final for this phase):**

1. **Stale test.** The failing call `build_hamiltonian(1.0, 0.0, 1.0)` is replaced by `kernel_dimension(1.0) == 152` plus orthonormality of the route 2 kernel projector at j_max = 1. That restores exactly the legacy scope of decision D1 and claims no j_max = 1 Hamiltonian validation from route 2. The sector counts (3, 36, 74, 36, 3) go into a **new** C0 test, evaluated from route 2 kernel labels and from route 1's 152-state basis, after Opus derives them independently from the transfer matrix T(x) with entries 1+x² on the diagonal and x on the off-diagonals. I checked the totals: Tr T(1)⁴ = 152 and the x⁰ and x⁸ coefficients are 3. If measured differs from derived, the test is not edited; the row fails and goes to DISCREPANCIES.
2. **Twin variance.** The test asserts three things: the five count dictionaries are pairwise distinct, the empirical standard deviation of a density and of P_S3 across repeats is within a factor 2 of √(p(1−p)/N_kept), and a repeat with the same seeds reproduces the same dictionaries. Run at r = 0 and r = 1 per rule D-C0. The fix, whatever the cause, is to drop the construction-time seed and set the simulator seed per repeat explicitly through the simulator's options before each run. The pre-fix code is already isolated in `.work/c060_p0_legacy_baseline/`, so "would have failed on the old code" is checked there without any git operation.
3. **G4 closure.** No `GATE_G4.json` is written: the gate script cannot run because `compile/twin_check.json` was never produced (the twin was killed at r = 1, see the run log), and a hand-written gate JSON would be fabrication. Instead an append-only decision D6 goes into the run's `run/DECISIONS.md` in the literal form `G4: REDUCED (campaign v0.6.0)` with the numbers 2,156 logical per step, 3,976 routed per step, 12,142 routed at r = 3, gap 8.6×, and evidence paths, plus one row in `run/GATES.md` and one INFO row in the new campaign ledger.
4. **`pyzx_basic_TP` is retired**, not fixed. Its pre-route step equivalence is 1.0e+00 in the routed table, meaning the pass produced an orthogonal state, and it is also more expensive than the Qiskit route. Ledger row `retired` with that reason.
5. **Replicate skeleton** is written as `runs/campaign_v060/replicate.py`, not as a repo-level `src/su2qc/` package. Creating a second `su2qc` namespace beside the run-local one is the duplicate backend the takeover forbids. The module name `su2qc.replicate` is assigned in Phase 2 when the reusable package is created. The skeleton implements the manifest hashing and the V1 comparison, which V14 needs anyway.
6. **V11 scope.** The existing estimator is post-selection plus decoded observables plus bootstrap in `twin.py`. No readout mitigation or ODR code exists. V11 in Phase 0 tests what exists on synthetic quasi-distributions with negative entries, channel closure, and a matched-subtraction helper added to the same module. The "after ODR" clause gets its own row `deferred to Phase 5` rather than a silent pass.
7. **Thresholds before C1.** A draft `GATE_THRESHOLDS.yaml` with the Section 5 table verbatim and a `status: draft` header is written now so C0 tests read thresholds from the file. Its hash stays null in the campaign state until C1 freezes it. C1 may not loosen any value.
8. **Dirty work.** Nothing outside the explicit path lists below is staged or discarded. The cleanliness criterion is evaluated honestly and fails.

## 2. Acceptance criteria and lanes

**Boot checks** (OPS, no LLM): prompt hash equals the recorded 50c60ff…; interpreter and package versions match ENV.md; `l12` encodes the stretched string (0, ½, ½, ½), (1, 1, 0, 2) to codeword 3793; conventions file hash fb3b7525… recorded into `hashes.conventions`; `RESUME_LOCK` and `TIME_LEDGER.md` created.

**V1 regression** (TEST-BENCH, fresh copy of the run directory under `.work/`, gate scripts write into the copy, never the run directory):

| Item | Must hold | Historical value |
|---|---|---|
| Legacy suite | 4 tracked test files all pass; `test_synth_l12.py` reported separately as Phase-4 informational | 44 passed, 1 failed |
| G1 | dims 82 and 152 both routes; sectors 2, 20, 38, 20, 2; [H,N] and Hermiticity ≤ 1e−13; spectra ≤ 1e−12; time series ≤ 1e−10; Gauss commutators ≤ 1e−12; degeneracies 16, 16, 18, 16, 16; frozen matter ≤ 1e−8 per D3; magnetic-off ≤ 1e−10 | PASS |
| G2 | expm vs Krylov ≤ 1e−9; energy and N drift ≤ 1e−10; window g² = 4, m = 0.75, δt = 0.8333, r_max = 3 with drop 0.99348, pair weight 0.81933, Strang error 0.019065 | PASS |
| G3 | block unitary deviation ≤ 1e−12; leakage 0; noiseless leakage ≤ 1e−14; slopes −2.0980 and −2.1495 | PASS with S8/C7 excluded by D4 |
| Value stability | every numeric criterion within 1e−12 absolute of the committed JSON at eee1e16, read with `git show`; timestamps and the pytest timing string excluded; `trotter_scaling.json` compared to HEAD and the divergent working-tree copy reported | |

**V10**: distinct dictionaries, σ within 2× multinomial, seeded reproducibility, at r = 0 and r = 1; the same test run on the pre-fix copy must fail on at least one assertion.

**V11**: on synthetic quasi-distributions including negative weights, observables equal the closed-form answers to 1e−10; P_S3 + P_meson + P_BB̄ + P_other equals the post-selected N = 4 weight to 1e−10; ΔO(t) = O(t) − O(0) on synthetic pairs to 1e−10; yield equals the known physical fraction.

**Tier 2 rows** each `done`, `retired`, or `deferred` with reason: ruff and mypy on the run-local package (safe autofixes only, then V1 rerun on the post-fix snapshot; per-line ignores with a reason; box 45 minutes); stale test; sector-count test; `pyzx_basic_TP` retired; replicate skeleton; V11 test; G4 closure rows.

**Lanes and ownership** (disjoint files, Codex concurrency 3, at most two NVIDIA test workers):

| Lane | Owner | Owns | Box |
|---|---|---|---|
| R0 repair | Codex | `tests/test_route_gausskernel.py` in the run dir | 20 min build, 2 h total cap |
| T-bench | execute_code, ≤ 2 NVIDIA workers | sandbox copies, junit XML, hash manifests | continuous |
| P0 physics | Opus 5 | `sessions/…/predictions_C0.md`: sector counts at j_max = 1 by generating function, multinomial σ expectations, D-C0 case | before A0a/A0d run |
| A0a twin | Codex | `src/su2qc/twin/twin.py`, `tests/gate_C0/test_twin_variance.py` | 45 min |
| A0b lint | Codex | run-local `ham/`, `dynamics/`, `encodings/`, `circuits/`, `compile/` only | 45 min |
| A0c estimator | Codex, after A0a lands | matched-subtraction helper in `twin.py`, `tests/gate_C0/test_estimator.py` | 40 min |
| A0d counts + V1 wrapper | Codex | `tests/gate_C0/test_jmax1_counts.py`, `tests/gate_C0/test_v1_regression.py`, `replicate.py`, draft thresholds | 45 min |
| REVIEW | Opus 5 | `reviews/c0_<file>_<n>.md`, blocking vs advisory, checks the pre-fix failure of the twin test | per lane |
| OPS scribe | orchestrator | ledger rows, D6 append, `GATES.md` row, `PHYSICS_STATUS.md` hourly, `TIME_LEDGER.md` | continuous |
| Sign-off | Fable 5.1, one call | `sessions/…/signoff_C0.md` on the snapshot manifest hash | end |

## 3. Schedule, gate, stop conditions, integration

| Clock from T0 | Step |
|---|---|
| 0:00–0:20 | Boot checks, draft thresholds, ledger initialised, P0 predictions dispatched |
| 0:20–1:00 | R0 repair, then full legacy suite plus G1–G3 in a fresh sandbox. No BUILD lane starts before V1 is green, per Section 7 step 2. |
| 1:00–2:15 | Wave 1: A0a, A0b, A0d in parallel; reviews start as each returns |
| 2:15–3:00 | Wave 2: A0c, lint on `twin/` and `compile/`, V1 rerun on the post-lint snapshot |
| 3:00–3:40 | Gate: one command `pytest runs/campaign_v060/tests/gate_C0 --junitxml`, evidence manifest hashed, ledger rows written by the gatekeeper only |
| 3:40–4:00 | Scoped commits, Fable sign-off on the manifest hash, `SESSION_SUMMARY.md`, state update, `RESUME_LOCK` removed |
| Latest 5:00 | Gate with whatever is done; remaining items continue next session. Hard cutoff 12 h. |

**Gate C0 row logic.** V1, V10, V11 rows pass only on deterministic evidence plus the Fable sign-off on the same manifest hash. The cleanliness criterion fails. Result: `C0: partial` with the failing criterion named, phase stays 0, `next_action` set to: "User resolves the listed dirty paths; then rerun `tests/gate_C0` and the V1 sandbox on a fresh copy and re-gate C0 to phase 1."

**Stop conditions.** Repair not green at 2 h: stop, summary first line is the failure, nothing else runs. Sector counts differ from Opus's derivation: row fails, no test edit, C0 partial, Phase 2 V3 blocked. V10 still zero-variance at r = 1 after the fix: row fails, Phase 5 twin work blocked. Any lane needing access outside the repository, hardware, or push: that lane stops. Fable sign-off unavailable: gate recorded as `partial: awaiting sign-off`, no substitute. Lint box expires: row `partial` with counts, V1 must still be green on the final snapshot.

**Commits, all by explicit path list, never by `git add -A`:**

| Commit | Contents |
|---|---|
| `campaign: commit phase-4 artifacts from v0.5.0` | the 16 untracked paths under the run directory, after Opus review |
| `campaign: C0 partial <one line>` | `runs/campaign_v060/` tree, the two `docs/refs` files, the v0.6.0 prompt, the stale-test fix, the twin fix, new tests, the D6 and GATES.md appends |

**Left untouched for the user**, listed in the summary with a recommended disposition each: modified `trotter_scaling.json` and three figures in the run directory (working tree diverges from the committed evidence), `.graphifyignore`, `GRAPHIFY_UPDATE.md`, `STATUS_REPORT_20260907.md`, `artifacts/logs/v050/`, `runs/2026-09-07-dryrun-one-month/`, `runs/_reference/`.

**Integration path.** No package move, no new runner. Campaign tests import the run-local package through one path constant in a `conftest.py`, run legacy code in fresh `.work/` copies, and compare against `git show` blobs. Historical JSON, figures, and tables in the run directory are never written by any Phase 0 process.


# Superseding Fable amendment

Approval for the Python check was denied, so I did the propagation by hand from the printed arrays. Result is unambiguous; ruling follows.

# Phase 0 plan amendment (physics escalation, Fable 5.1)

**Verdict: AMEND, not BLOCKED.** V1 is not restorable to a literal PASS, but that does not trigger the regression-repair STOP, and the stale-test repair remains permitted. Details per issue.

## 1. Value stability of `trotter_scaling.json`: amplification is established, not plausible

The slope is `polyfit(log r, log err)` over r = 8…128. Centered log-r weights are ±1.386, ±0.693, 0 with Σw² = 4.80. The first-order slope change from a relative perturbation ε in the r = 128 error alone is 1.386·ε/4.80 = 0.289·ε.

| criterion | max abs Δ in err array | rel Δ at r = 128 | predicted slope Δ | measured slope Δ |
|---|---|---|---|---|
| Psurv | 6.3e-16 | 1.7e-9 | 4.9e-10 | 4.99e-10 |
| E2 | 5.4e-15 | 4.8e-9 | 1.39e-9 | 1.398e-9 |
| state | 2.4e-15 | 3.6e-11 | 1.04e-11 | 1.047e-11 |

Prediction matches measurement to two digits in all three. The primary quantities (the error arrays) agree to ≤ 5.4e-15, inside 1e-12. A slope stability of 1e-12 would require the r = 128 error (3.7e-7, itself a difference of O(1) probabilities) to be stable to 1.3e-18 absolute, below double-precision epsilon on O(1). No non-bitwise-identical rerun can meet it. The criterion is ill-posed for the log-slope, not merely tight.

Decisions:
- **Threshold is not waived.** V1 sub-rows: G1–G3 gate scripts PASS/FAIL as they report; every primary numeric value compared at 1e-12 (expected PASS); the three slopes compared at 1e-12 and recorded **FAIL, cause established: floating-point conditioning of the log-slope fit**, with the table above in the row. V1 overall = **PARTIAL**, never PASS, until the user amends the V1 wording (e.g. 1e-12 on primary values, slopes at the propagated bound). That is a prompt change only the user may make. C0 stays partial for this reason as well as cleanliness.
- **Does this force STOP?** No. The STOP condition is "regression repair not green in 2 h", where green means the legacy suite passes after the stale-test fix and G1–G3 gate scripts PASS in the sandbox. Those establish the legacy package behaves as before, which is the only thing the Phase 0 BUILD lanes depend on. BUILD lanes proceed. Anything in later phases that cites V1 PASS is blocked until the user rules.
- **Permitted bounded diagnostic** (TEST-BENCH, mechanical, read-only on both JSON versions): refit slopes from the committed `err_*` arrays with the same `polyfit` call and confirm reproduction of the committed slopes to 1e-14 (proves the fit is deterministic and the Δ is entirely input-borne); compute the propagated bound as above for the sandbox rerun vs HEAD and vs working tree; record all three. **Not permitted:** editing the fit or thresholds in `test_l12.py`, touching the working-tree JSON or figures, or substituting the committed values for the rerun.

## 2. V11 closure identity and status

The plan's identity is wrong. From `twin.py` `observables()`: `P_surv` is the full q = (1,−1,0,0) occupation sector; `P_stretched` (S3, j = (0,½,½,½)) and `P_short` (j = (½,0,0,0)) are strict subchannels of it, and other j-configurations in that sector are counted in `P_surv` only. Channels are normalized by kept weight, and the branch order is: any |q| = 2 → BB̄; q = (1,−1,0,0) → surv; all |q| = 1 → meson; Σn = 4 → other; anything else uncounted. With N_VAC = (0,2,0,2), surv and meson imply N = 4 but **P_BBbar can include N ≠ 4 codewords** (e.g. q = (2,0,0,0)), and kept weight with N ≠ 4 and no |q| = 2 falls in no channel.

Exact identities the test must assert (all to 1e-10 on synthetic inputs, including negative quasi-weights):
- `P_surv + P_meson + P_BBbar + P_other = W_kept(N=4) + W_kept(N≠4 ∧ ∃v |q_v|=2)`, both sides computed from decoded labels.
- `P_stretched + P_short ≤ P_surv`, and `P_surv − P_stretched − P_short` equals the label-computed weight of the remaining j-configurations in the (1,−1,0,0) sector.
- If the campaign wants the cleaner "channels sum to post-selected N = 4 weight", that requires an N = 4 filter on BB̄ and an explicit `P_Nviol` channel. That is an estimator change, not a test change: allowed only in lane A0c as an additive helper, with the legacy `observables()` output unchanged and regression-checked.

Status: no readout-mitigation step and no ODR exist in the estimator; the "re-reported after ODR" clause cannot be executed in Phase 0. **V11 = PARTIAL at C0** (rows: synthetic-quasi observables, closure, matched subtraction, yield; ODR-closure row `deferred to Phase 5, V11 rerun on real code path`). Not PASS. C0 cannot exit on V11 grounds either.

## 3. Seed override: conditional no-change path is mandatory

`twin_backend(seed=101)` sets a construction-time `seed_simulator`; `run_counts` passes `seed_simulator = seed + k` per run, and Aer run options override backend options. The per-run seed should already dominate. Amended lane A0a:
1. Run the V10 test on the pre-fix isolated copy first, at r = 0 and r = 1.
2. If five dictionaries are distinct and σ is within 2× → record **"override harmless: run-time seed_simulator = seed + k supersedes construction-time 101"**, no code change, V10 PASS on that evidence. Do not manufacture RED and do not alter the seed + k semantics.
3. Reviewer's "test would fail on old code" requirement is then satisfied by a **negative control**, not history: run the same test with all five run-time seeds forced equal and show it fails (proves detection power).
4. Only if step 1 shows identical dictionaries: locate the actual cause (e.g. run option ignored by this Aer version) and fix at that point; then step 3 becomes the pre-fix run.

Variance criterion, corrected: `bootstrap()` returns 2× the bootstrap standard error **of the mean over R = 5 repeats**, so the expectation is SE = √(Var_s / (R·N̄_kept)), not the per-repeat SD √(p(1−p)/N_kept). Using the per-repeat SD would be off by √5 ≈ 2.24 and fail the 2× window spuriously. Var_s is the multinomial variance of the observable over the pooled kept weights, Var_s = Σ_s w_s O(s)² − (Σ_s w_s O(s))², valid for densities taking values 0, 1, 2 and for E2 as well as for Bernoulli channels. Compare `two_sigma/2` to SE, factor 2 both sides. Note: with 5 repeats the sample SE has ~35% intrinsic scatter (χ²₄), so the seeded test is deterministic and a single-observable miss is recorded as a discrepancy with that probability, never fixed by re-seeding.

## 4. `pyzx_basic_TP`

`state_equivalence` returns 1 − |⟨a|b⟩|; the table prints 1.0e+00 with one significant digit, so all that is established is |overlap| < 0.05. Retire with reason: **"pre-route equivalence error 1.0e+00 fails the ≥ 1 − 1e-10 hardware-eligibility requirement; root cause not diagnosed (candidate: qasm round-trip qubit or phase convention); no orthogonality claim."** Remove the word "orthogonal" from the plan and the ledger row.

## 5. Replicate skeleton path

Prompt Section on code layout puts reusable code in a repo-level `src/su2qc/` package, which does not exist; the takeover forbids a second `su2qc` namespace. Ruling: write the skeleton as run-local `src/su2qc/replicate.py` inside the existing single package, alongside the `twin.py` edits already in scope. The module name `su2qc.replicate` is then literally satisfied. Ledger row `done (skeleton; repo-level package move deferred to Phase 2 with the rest of the package)`. A campaign-local `replicate.py` would have to be rowed `partial`, not done.

## Consolidated stop conditions and gate result

- STOP only if the legacy suite plus G1–G3 gate scripts are not green in the sandbox within 2 h.
- C0 result: **partial**, failing criteria named: repository cleanliness (user-preserved paths), V1 slope stability (threshold ill-posed, user ruling required), V11 ODR clause (deferred to Phase 5). Phase stays 0.
- Independent stale-test repair (kernel dimension 152 plus projector orthonormality, no j_max = 1 Hamiltonian claim) remains permitted and required.
- No historical JSON, figure, or table is written by any Phase 0 process. Final sign-off reserved for the snapshot manifest.


# Source: runs/campaign_v060/sessions/c060_p0_20260908_2/signoff_C0.md
**PARTIAL.** C0 is correctly recorded as partial and correctly blocks C2, but the evidence chain behind the rows marked `pass` has gaps that must be closed before C0 can be re-gated. C1 meets its formal exit criteria and I sign it off with two advisories. Nothing was edited; one requested source, the session's own `plan.md`, does not exist, so I used the 20260907 `plan.md` plus the v0.6.1 prompt, which R6 designates as the Phase 0 plan.

## What checks out

- **Conventions and R5 mapping.** `conventions.py` hashes to the frozen value in ENV.md and 00_conventions.md. From its definitions, cE = g²/2 = 2, cM = m = 0.75, cH = 1/2, cB = 1/(2g²) = 0.125, so electric:hopping:magnetic = 1:0.25:0.0625, μ = m/g_E = 3/8, and the resonance check 2m = (3/4)·g_E = 1.5 holds. P-S time points τ/g_E give t = 2.5 and 6.25. The preregistration matches all of this. Casimir j(j+1), N_VAC = (0,2,0,2), and the dC baseline of 2.25 (three j = ½ links in the stretched string) are consistent in twin.py.
- **j_max = 1 sector counts.** I re-derived the transfer matrix: T = a·1 + b·A on the 3-spin path graph, eigenvalues a, a ± √2 b, so Tr T⁴ = 3a⁴ + 24a²b² + 8b⁴ = 3 + 36x² + 74x⁴ + 36x⁶ + 3x⁸. The same formula gives 2 + 20x² + 38x⁴ + 20x⁶ + 2x⁸ at j_max = ½, matching the frozen sector dims. The test asserts both route splits and projector orthonormality at 1e-12, and the log shows it passing.
- **R1 slope rule.** Measured deltas against 10× the propagated bound: Psurv 4.99e-10 vs 5.00e-9, E2 1.40e-9 vs 1.40e-8, state 1.05e-11 vs 1.05e-10. All three slopes sit in [−2.3, −1.7]. The sandbox G3 log slopes equal the "working" values in `value-stability.json`, so the deltas are genuinely sandbox-vs-committed. R2 is complete: `trotter_scaling.json` and the three figures match HEAD, and the divergent copies are preserved under `00_repair/`.
- **C2 blocking.** Phase stays 0, `gates.C0 = partial`, `next_action` names the blockers, no repo-level `src/su2qc/` exists, no Phase 2 rows or tests exist. Correct.
- **Legacy output.** The `observables()` body is untouched in the twin.py diff. The D6/D7 appends and the stale-test repair match the ruled wording.

## Required fixes (blocking re-gate of C0)

1. **Snapshot integrity is broken.** `evidence-manifest.json` was written at 11:38:00.44; `GATE_LEDGER.jsonl` (11:38:00.53) and `CAMPAIGN_STATE.json` (11:38:00.61) were written after it, and their current SHA-256 values (9016ceeb…, bf68c7ab…) differ from the manifest entries (509d2f70…, ae214cf8…). A sign-off "on the manifest hash" is impossible as it stands. Write the ledger and state first, hash last.
2. **No execution record of the gate command.** `gate_C0_command.txt` omits `--junitxml`, and no `gate_C0.xml` or log exists. Only `jmax1-counts.log` records an actual pass. The V1 and V11 `pass` rows have no captured run in this session. Rerun the one gate command with junit output into the session directory.
3. **V10 test does not implement R4.** Four defects in `test_twin_variance.py`:
   - The variance criterion is `any(two_sigma > 0)`, not the frozen "factor 2 of the multinomial SE = √(Var_s/(R·N̄_kept))" with the 0.894 bootstrap factor from predictions_C0 §2.3.
   - The "negative control" asserts that a list of one dictionary repeated five times has one unique element. It never runs the twin with equal seeds, so it proves nothing about detection power.
   - It uses `compact=True`, which bypasses `AerSimulator.from_backend(seed_simulator=101)` entirely. The construction-time override that V10 exists to test is therefore neither removed nor shown harmless on the production path used by `run_g4.py`.
   - Code was changed (`set_options`, `compact`) before a recorded pre-fix run at r = 0 and r = 1; `twin-probe.log` ("0 [24,…] 4") is an undocumented probe of yet another configuration.
4. **The V10 failure is a seed-plumbing defect, not statistics, and D-C0 was never reached.** Five 1024-shot draws over ~47 outcomes cannot coincide by chance, and five identical key counts of 47 confirm a shared RNG stream. R4's "identical dictionaries" branch applies: locate the cause (record Aer's reported `seed_simulator` per repeat from result metadata), fix, then the pre-fix run becomes the negative control. Because the assertion fails at r = 0, r = 1 never ran and `twin_variance.json` holds only r = 0. I attempted a repo-untouched probe of both backend paths, but the harness denied the scratch-file write, so the mechanism is inferred, not measured.
5. **V11 test does not meet §2.2.** No 1e-10 equality against the closed-form answers (P_stretched 0.7, P_short 0.2, P_BBbar 0.1, P_surv 0.9, meson and other 0); the "negative entries" case subtracts 0.05 from 0.7, leaving a positive weight, so no negative quasi-weight is ever exercised; the remainder identity P_surv − P_stretched − P_short is asserted only as an inequality and the synthetic input contains no third j-configuration to test it; the closure identity is computed from the same classification code on both sides. The ledger also lacks the separate `deferred to Phase 5` ODR row that R3 requires. I do not sign V11 as PASS.
6. **V1 legacy-suite row cites prior-session evidence** (`repair-regression.xml`) on a snapshot without this session's twin.py and replicate.py changes. The plan required V1 green on the final snapshot. Rerun the four-file suite plus G1–G3 in a fresh sandbox copy and record it here.
7. **Review and sign-off artifacts are empty.** `review_C0.md` contains only "Error: Reached max turns (15)"; `signoff_C0.md` is empty. No Opus review of lanes A0a/A0c exists, so the V11 row also lacks its required REVIEW step.

## C1

PASS on its exit criteria: the three hashes are present in the state file and match the files, and the claim table is present. Advisories: `PREREGISTRATION.md` still reads "Threshold SHA-256: [to be filled at C1]" although C1 is closed; the R1/R3/R4/D6 rulings are listed without the one-line reasons §3 asks for; the four-coefficient API signature and the prespecified defect classes are absent. Fixing the placeholder changes the preregistration hash, so do it deliberately and re-record the hash.

## Housekeeping

`RESUME_LOCK` is still present, no `SESSION_SUMMARY.md` exists for this session, `CAMPAIGN_TODO.md` shows C1 items unchecked, and `CONFIG.resolved.yaml` has `AUTOPILOT: false` and `STOP_AT: phase`, which differs from R6 but errs conservative. Cleanliness remains failed by design under the preserve-dirty-work rule and was not waived.


# Source: runs/campaign_v060/sessions/c060_p0_20260908_2/review_C0_retry.md
**FAIL** — C0 evidence does not support a PASS on this snapshot; it is at best partial, and two ledger rows are already `pass: false`.

- **V1 — substantively OK, procedurally short.** Slopes −2.0980 (Psurv), −2.1495 (E2), −2.0070 (state) all sit in the frozen band [−2.3, −1.7], and every measured slope delta is ~10× under its propagated bound (4.99e-10 vs 5.00e-9; 1.40e-9 vs 1.40e-8; 1.05e-11 vs 1.05e-10), so `slope_rule: propagated_bound_x10` is met even though each row's `stability_pass` is false against the raw 1e-12. But the cited `slope-conditioning.json` does not exist in `c060_p0_20260908_2` — it lives only in the 20260907 session and the `00_repair` copy — and the legacy-suite row cites prior-session `repair-regression.xml`, i.e. a snapshot without this session's `twin.py`/`replicate.py` edits.
- **V10 — hard FAIL, and the failure is real.** `twin_variance.json` holds only `{"0": {distinct_dictionaries: 3, repeat_sizes: [47,47,47,47,47]}}` against the required 5 distinct at r=0. Five identical support sizes over ~47 outcomes is a shared RNG stream, not a statistical coincidence, so this is a seed-plumbing defect. The `bootstrap_se: factor_2_of_multinomial_expectation` criterion was never exercised, and r=1 never ran because the r=0 assertion aborted.
- **V11 — `pass: true` is not supported.** The ledger value is only "focused synthetic tests 2 passed"; the threshold file requires four separate 1e-10 checks (synthetic observables, channel closure, matched subtraction, yield), and the sign-off records that no closed-form 1e-10 equality is asserted, no negative quasi-weight is ever produced, and closure is computed from the same classifier on both sides. The required `odr: deferred_to_phase_5` row is also absent from the ledger. This row should be flipped to fail or unproven.
- **Cleanliness — correctly FAIL, correctly not waived.** `repository_clean: true` is unmet; the ledger records it as false with the campaign and C0 edits uncommitted, and the sign-off explicitly notes it "was not waived." That is the right handling under the preserve-dirty-work rule — it just means C0 cannot be PASS.
- **C2 block — correctly enforced.** Phase stays 0, `gates.C0 = partial`, no repo-level `src/su2qc/` and no Phase 2 rows or tests exist. The C2 thresholds (1e-12 route agreement, 1e-10 series, exact counts) are untouched and properly gated behind C0.
- **Evidence integrity — broken.** I recomputed the manifest: `GATE_LEDGER.jsonl` is `9016ceeb…` vs manifest `509d2f70…`, and `CAMPAIGN_STATE.json` is `bf68c7ab…` vs manifest `ae214cf8…`. Both were written *after* the manifest, so no sign-off "on the manifest hash" is possible. (`GATE_THRESHOLDS.yaml` and `twin_variance.json` do match.)
- **No REVIEW artifact exists.** `review_C0.md` is 29 bytes containing only "Error: Reached max turns (15)"; `review_C0_retry.md` is 0 bytes. Neither is in the manifest. Under the routing rule the Opus REVIEW step is missing outright, so no row can carry the required review sign-off on this snapshot.
- **No captured gate execution.** `gate_C0_command.txt` omits `--junitxml` and there is no `gate_C0.xml`/run log in the session; `jmax1-counts.log` is the only recorded pass, leaving the V1 and V11 `pass` rows without deterministic evidence from this session.


# Source: runs/campaign_v060/sessions/c060_p0_20260908_2/predictions_C0.md
# predictions_C0.md

# P0 physics predictions — gate C0 (campaign v0.6.1, Phase 0)

**Written by:** Opus 5 (REVIEW/PHYSICS lane), 2026-09-08, **before** lanes A0a and A0d are run
(v0.6.1 §2.1 item 4). Preregistered: nothing below may be edited after A0a/A0d produce numbers;
a disagreement is a `DISCREPANCIES.md` entry and a failed row, never a test edit
(v0.6.1 §5, bullet 4).

**Sources used** (repository only; no other material):
`prompts/gi_cost_campaign_v.0.6.1.md` §§0–2, 5; `prompts/gi_cost_campaign_v.0.6.0.md` lines 117,
142, 242 (V10 row, Phase-0 item 2, decision rule D-C0 — v0.6.0 remains the campaign document per
v0.6.1 §0); `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py`;
`.../ham/route_spinnet.py`; `.../ham/route_gausskernel.py`; and, for §3 only,
`.../twin/twin.py`, `.../compile/run_g4.py`, `.../circuits/synth_l12.py`,
`.../circuits/strang_l12.py`, `.../encodings/l12.py` (working-tree state as of 2026-09-08;
`twin.py` is one of the modified paths in the dirty tree, so the reader should confirm the
line numbers against the snapshot the gate actually runs).

Every statement is tagged **[S]** if it is read from a source, or **[D]** if it is my derivation
from those sources. Illustrative arithmetic that depends on a quantity not present in any source
(e.g. FakeTorino readout error rates) is tagged **[illustrative]** and is not a preregistered
number.

---

## 1. The j_max = 1 sector generating function

### 1.1 Inputs (frozen conventions only — no route label lists were read for this derivation)

- **[S]** Geometry. `conventions.py:20` gives four vertices; `conventions.py:34` gives
  `LINKS = ((0,1,"x"), (1,2,"y"), (3,2,"x"), (0,3,"y"))`, i.e. l1: v1→v2, l2: v2→v3, l3: v4→v3,
  l4: v1→v4. **[D]** Vertex incidences are therefore v1:{l4,l1}, v2:{l1,l2}, v3:{l2,l3},
  v4:{l3,l4}: every vertex is 2-valent and the patch is a single 4-cycle
  l1 – v2 – l2 – v3 – l3 – v4 – l4 – v1 – l1.
- **[S]** Truncation. `conventions.py:9–15, 64–65`: j ∈ {0, ½} at `JMAX_HALF`, j ∈ {0, ½, 1} at
  `JMAX_ONE`; one spin label per link.
- **[S]** Matter. `conventions.py:50–53`: two-color staggered fermions, one doublet per vertex,
  four Fock states per site — n = 0 (color-singlet vacuum), n = 1 (doublet), n = 2 (doubly
  occupied singlet). **[D]** As SU(2)-color representations the site Fock space decomposes as
  **1 ⊕ 2 ⊕ 1**: the matter spin is j_m = 0 for n ∈ {0, 2} and j_m = ½ for n = 1.
- **[D]** Gauss law at a 2-valent vertex v with incident link spins (j_a, j_b) and matter spin
  j_m: the physical states are the SU(2) singlets of V_{j_a} ⊗ V_{j_b} ⊗ V_{j_m}. The number of
  such singlets is the multiplicity of j_m in j_a ⊗ j_b, i.e. **1** if
  |j_a − j_b| ≤ j_m ≤ j_a + j_b with j_a + j_b − j_m integral, and **0** otherwise. Link
  orientation is irrelevant because V_j ≅ V_j* for SU(2), so the same count applies whether the
  end carries U or U†.
- **[D]** Specialising: j_m = 0 ⇒ j_a = j_b, and then n ∈ {0, 2} (two states);
  j_m = ½ ⇒ |j_a − j_b| = ½, and then n = 1 (one state); |j_a − j_b| = 1 admits neither, so such
  link pairs are excluded. Multiplicity never exceeds 1, which is why a 2-valent intertwiner tag
  carries no information (`conventions.py:97–100`, `LABEL_DOC`, tag ≡ 0).

  *Consistency note (not an input):* this reproduces the rule stated in the route-1 docstring
  (`route_spinnet.py:9–12`) and the structural condition under which route 2's `_local_singlet`
  returns a vector rather than `None` (`route_gausskernel.py:84–101`). The derivation above does
  not use either.

### 1.2 Vertex weight and transfer matrix

**[D]** Grade states by the total fermion number N = Σ_v n_v (this is the sector label used by
`validate_dimensions`, `route_spinnet.py:692–698`, and by `EXPECTED_SECTOR_DIMS`,
`conventions.py:74`). Track it with a formal variable x, giving each vertex the weight

  w(j_a, j_b) = 1 + x²      if j_a = j_b        (n = 0 or n = 2)
  w(j_a, j_b) = x           if |j_a − j_b| = ½  (n = 1)
  w(j_a, j_b) = 0           otherwise.

Because the patch is a 4-cycle of links with one vertex between each consecutive pair, the full
gauge-invariant generating function factorises into a transfer matrix on the link-spin alphabet:

  Z_{j_max}(x) = Σ_{j_1 j_2 j_3 j_4} w(j_4,j_1) w(j_1,j_2) w(j_2,j_3) w(j_3,j_4) = **Tr T⁴**,

with T indexed by the allowed spins and T[j, j'] = w(j, j'). Writing a = 1 + x² and b = x:

  j_max = 1:  T = ⎡a b 0⎤   j_max = ½:  T = ⎡a b⎤
                  ⎢b a b⎥                    ⎣b a⎦
                  ⎣0 b a⎦

**[D]** T = a·1 + b·A, where A is the adjacency matrix of the path graph on d = 2 j_max + 1
spins (only Δj = ±½ neighbours are connected). Its eigenvalues are
λ_k = a + 2b cos(kπ/(d+1)), k = 1 … d, so in general

  **Z(x) = Σ_{k=1}^{d} ( a + 2b cos(kπ/(d+1)) )⁴,  a = 1 + x², b = x.**

For j_max = 1 (d = 3) the eigenvalues are a + √2 b, a, a − √2 b, hence

  Z_1(x) = (a+√2b)⁴ + a⁴ + (a−√2b)⁴ = **3a⁴ + 24a²b² + 8b⁴**.

### 1.3 Expansion and the predicted counts

**[D]** With a = 1 + x², b = x:

  3(1+x²)⁴ = 3 + 12x² + 18x⁴ + 12x⁶ + 3x⁸
  24x²(1+x²)² =     24x² + 48x⁴ + 24x⁶
  8x⁴ =                     8x⁴

  **Z_1(x) = 3 + 36x² + 74x⁴ + 36x⁶ + 3x⁸**

| N = Σ n_v | 0 | 2 | 4 | 6 | 8 | total |
|---|---:|---:|---:|---:|---:|---:|
| **predicted dim, j_max = 1** | **3** | **36** | **74** | **36** | **3** | **152** |

Checks, all **[D]**:

1. **Total.** Z_1(1) = 3·2⁴ + 24·2²·1 + 8 = 48 + 96 + 8 = **152**, matching
   `EXPECTED_DIM[JMAX_ONE] = 152` (`conventions.py:72`).
2. **Palindromy.** Particle–hole conjugation n_v ↦ 2 − n_v multiplies each vertex weight by x²
   (a ↦ x²a, b ↦ x²·x⁻¹·… more directly: x⁸ Z_1(1/x) = Z_1(x)), so the sector list must be a
   palindrome — 3, 36, 74, 36, 3 is.
3. **j_max = ½ cross-check with the same machinery.** d = 2 gives
   Z_{1/2}(x) = (a+b)⁴ + (a−b)⁴ = 2a⁴ + 12a²b² + 2b⁴
   = 2 + 20x² + 38x⁴ + 20x⁶ + 2x⁸, total 82 — reproducing
   `EXPECTED_SECTOR_DIMS = {0: 2, 2: 20, 4: 38, 6: 20, 8: 2}` and `EXPECTED_DIM[JMAX_HALF] = 82`
   (`conventions.py:72–74`) exactly. The same formula therefore predicts both truncations from
   one structure, which is the strongest available evidence that the j_max = 1 numbers are not a
   transcription of the route output.
4. **Odd sectors.** Z contains only even powers of x, so all odd-N sectors are empty **[D]** —
   a consequence of the 4-cycle having an even number of vertices and each n = 1 vertex
   contributing exactly one power of x, with the number of |Δj| = ½ edges around a cycle
   necessarily even.

### 1.4 What the C0/C2 tests must find

- **[S/D]** `tests/gate_C0/test_jmax1_counts.py` (v0.6.1 §2.1 item 5) compares route 1's
  `enumerate_basis(1.0)` and route 2's `kernel_dimension(1.0)` against the table above. Route 2
  emits exactly one basis column per (js, ns) for which all four vertices admit a local singlet
  (`route_gausskernel.py:110–152`), and route 1 enumerates the same admissibility conditions
  vertex by vertex (`route_spinnet.py:234–312`); **[D]** both must therefore reproduce Z_1(x)
  identically, including the per-N breakdown, not merely the total 152. A route that returns
  152 with a different sector split is a route bug.
- **[S]** Route 2 builds only the *kernel dimension* at j_max = 1; `build_hamiltonian` raises
  `NotImplementedError` for j_max > 0.75 (`route_gausskernel.py:422–427`). The count row is
  therefore testable at C0; the j_max = 1 *Hamiltonian* agreement is V3 at C2 (v0.6.1 §4,
  priority 2), not a C0 row.
- **[S]** A mismatch fails the row, is written to `DISCREPANCIES.md`, and is not edited away
  (v0.6.1 §2.1 item 5 and §5).

---

## 2. Bootstrap-SE expectations for V10 (R = 5, multinomial observable variance)

### 2.1 The prescribed formula

**[S]** v0.6.1 §2.1 item 4 fixes the criterion as

  **SE = √( Var_s / (R · N̄_kept) ),  Var_s multinomial,  R = 5**,

adopted from the Fable amendment §3 via ruling R4 (v0.6.1 §0: bootstrap-SE, *not* per-repeat SD,
with multinomial variance). **[S]** v0.6.0 line 117 (V10) requires five repeats at r = 0 to
produce five distinct count dictionaries with bootstrap σ > 0 and ≈ the multinomial expectation;
v0.6.0 line 142 fixes "≈" as **within a factor 2**. **[S]** v0.6.1 §2.1 item 5 additionally
requires the pre-fix and post-override runs to be *distinct and within 2 × SE* for
"override harmless" to be recorded.

### 2.2 Definitions, made explicit for the twin's estimator

**[S]** `twin.observables()` (`twin.py:66–96`) decodes each kept bitstring to a label and
accumulates weights w = n/tot, i.e. every observable is a **self-normalised** average over the
post-selected sample. **[D]** Conditional on the number of kept shots, the kept sample is a
multinomial draw over the physical codewords with probabilities {p_k}. For a diagonal observable
O taking value o_k on codeword k, with Ō = Σ_k p_k o_k:

  **Var_s = Σ_k p_k (o_k − Ō)² = Σ_k p_k o_k² − Ō².**

Special cases used by the V10 rows **[D]**:

| observable | values o_k | Var_s |
|---|---|---|
| channel probability (`P_surv`, `P_meson`, `P_BBbar`, `P_other`, `P_stretched`, `P_short`) | {0, 1} | **P(1 − P)** |
| two-valued observable (`n_v3` ∈ {0, 2} at r = 0; `E2_l1` ∈ {0, 0.75}) | {o_lo, o_hi} | **(Δo)² p(1 − p)** |
| general `E2_l`, `n_v` | multi-valued | Σ p_k o_k² − Ō² |

**[D]** N̄_kept is the mean number of post-selected shots per repeat, i.e. `shots × yield` with
the yield returned by `postselect()` (`twin.py:60–63`). **[S]** In the v0.5.0 twin run
`REPEATS, SHOTS = 5, 4000` (`run_g4.py:125`), so R · N̄_kept = 20 000 × yield unless the C0
lane changes the shot count. **[D]** The fluctuation of N_kept itself enters a self-normalised
ratio only at second order, so the formula is exact to O(1/N) conditional on N̄_kept.

### 2.3 The predicted relation between the formula and what `twin.bootstrap()` returns

**[S]** `twin.bootstrap()` (`twin.py:152–169`) resamples the **R = 5 repeats** with replacement
`n_boot` times, averages, and returns `two_sigma = 2 × std(boot means, ddof=1)`.

**[D]** Two consequences that must be stated before the run, because they change the number the
test compares against:

1. The nonparametric bootstrap SE of a mean of n values equals σ̂₀/√n, where σ̂₀ is the
   ddof = 0 sample SD. Relative to the ddof = 1 standard error of the mean — which is what
   √(Var_s/(R·N̄_kept)) estimates — this is low by a factor **√((R−1)/R) = √(4/5) = 0.894**.
   Hence the preregistered expectation is

   **`two_sigma` ≈ 2 × 0.894 × SE = 1.79 × SE**, i.e. `two_sigma/2` ≈ 0.89 × √(Var_s/(5·N̄_kept)),

   with a further ≈ 1/√(2·n_boot) ≈ 4 % Monte-Carlo jitter at n_boot = 300 (`run_g4.py:132`).
   The 11 % deficit is expected and is **not** a failure; it is well inside the factor-2 band.
2. An SD estimated from R = 5 repeats has ν = 4 degrees of freedom, so its own relative
   scatter is ≈ 1/√(2ν) = **35 % (1σ)**; a 2σ excursion spans roughly 0.5×–1.7× the true SE.
   This is the quantitative reason the V10 criterion is a factor-2 band rather than a tight
   tolerance, and the reason ruling R4 prefers the bootstrap-SE over the raw per-repeat SD.

### 2.4 Preregistered numeric expectations

**[D, parametric — the only non-illustrative form]** For a channel probability P at yield y with
S shots per repeat and R = 5:

  SE = √( P(1−P) / (5 · y · S) );  worst case (P = ½) SE = 1/(2√(5yS)).

**[illustrative]** at S = 4000 and y = 0.8 (R·N̄_kept = 16 000):

| observable / regime | Var_s | SE | expected `two_sigma` (= 1.79 SE) |
|---|---:|---:|---:|
| P = 0.50 (worst case) | 0.2500 | 3.95e-3 | 7.1e-3 |
| P = 0.97 (r = 0 `P_surv`, see §3) | 0.0291 | 1.35e-3 | 2.4e-3 |
| `n_v3` ∈ {0,2}, p(2) = 0.03 | 0.1164 | 2.70e-3 | 4.8e-3 |
| `E2_l1` ∈ {0,0.75}, p(0.75) = 0.03 | 0.0164 | 1.01e-3 | 1.8e-3 |

These four rows are illustrations of the formula, not predictions of the twin's output: the
actual P and y depend on FakeTorino error rates, which appear in no source read here. **The
preregistered claim is the formula, the 1.79 factor, the factor-2 acceptance band, and the
degenerate cases identified in §3.3 — not the table entries.**

### 2.5 Degenerate cases the V10 row must handle

**[D]** Var_s = 0 whenever the kept sample is concentrated on codewords that share the
observable's value — in particular P ∈ {0, 1} exactly. The multinomial formula then predicts
SE = 0, and an observed bootstrap σ = 0 is *agreement*, not a failure of the twin. The V10
"σ > 0" clause must therefore be evaluated on an observable whose P is interior; §3.3 predicts
which observables those are at r = 0. Reporting σ = 0 on a structurally empty channel as
evidence of a deterministic twin would be a false positive for D-C0.

---

## 3. Which D-C0 case applies at r = 0 — and whether r = 1 is required

### 3.1 The rule

**[S]** `prompts/gi_cost_campaign_v.0.6.0.md:242`, verbatim: "**D-C0 Twin fix ambiguity.** If the
twin's five repeats are distinct after removing the `seed_simulator = 101` override but σ is
still zero at r = 0, the r = 0 circuit has no two-qubit gates and the readout-noise-only twin may
be deterministic under the noise model's readout-error implementation: test at r = 1 as well;
record which case applies."

**[S]** v0.6.1 §2.1 item 5 independently orders the lane: "pre-fix run first at r = 0 **and**
r = 1; 'override harmless' recorded if distinct and within 2× SE; negative control with all five
run-time seeds forced equal must fail; only on identical dictionaries locate the cause and fix."

### 3.2 What the r = 0 circuit and the seed plumbing actually are

**[S]** Facts, with citations:

- `synth_full_circuit(0)` returns `prep_stretched()` and nothing else
  (`synth_l12.py:271–275`); `prep_stretched()` applies **X gates only**, one per set bit of the
  encoded stretched codeword (`strang_l12.py:175–181`).
- The codeword is `l12.encode(((0, ½, ½, ½), (1, 1, 0, 2)))`. **[D]** Working it out from the L12
  layout (`l12.py:18–31`: qubits 3v, 3v+1 carry the two incident link spins as 0/1, qubit 3v+2 is
  set iff n_v = 2): bits {0, 4, 6, 7, 9, 10, 11} = **3793**, i.e. **7 X gates**, confirming the
  boot codeword check of v0.6.1 §2.1 item 1.
- The twin is `AerSimulator.from_backend(FakeTorino, seed_simulator=seed)` with `seed = 101` at
  construction (`twin.py:28–34`, `run_g4.py:122`) — this is the override V10 targets.
- The five repeats are five copies of one measured circuit, run with **distinct run-time seeds**
  `seed + k` for k = 0…4, i.e. 500…504 at r = 0 and 510…514 at r = 1
  (`twin.py:50–57`, `run_g4.py:131`). The transpile inside `run_counts` is at
  `optimization_level=0` on an already-ISA circuit with a fixed `seed_transpiler`.

**[D]** Consequences:

- D-C0's premise "the r = 0 circuit has no two-qubit gates" is **true**: an X-layer routed with a
  fixed initial layout requires no SWAPs, so the r = 0 ISA circuit is 1q-only.
- The twin is nevertheless *not* noiseless at r = 0: the backend noise model attaches 1q gate
  error and idle relaxation to the X layer and readout-assignment error to all 12 measurements,
  and Aer samples readout error **per shot**. The premise "the readout-noise-only twin may be
  deterministic" is predicted **false**.
- Whether the five dictionaries differ turns on precedence: a run-time `seed_simulator` passed to
  `sim.run(...)` is expected to override the backend option set at construction. That expectation
  is exactly what V10 tests; it is not asserted here as a fact.

### 3.3 Predicted structure of the r = 0 kept sample

**[D]** From `l12.is_physical` (`l12.py:53–69`: the two endpoint copies of every link must agree,
and no vertex may have unequal link bits together with a set matter bit), the physical neighbours
of code 3793 are:

| Hamming distance from 3793 | physical? | resulting label | channel |
|---|---|---|---|
| flip bit 8 (v3 matter) | yes | n = (1,1,2,2), q₃ = +2 | **P_BBbar** |
| flip bit 11 (v4 matter) | yes | n = (1,1,0,0), q₄ = −2 | **P_BBbar** |
| any single link-copy flip | no | — | discarded by post-selection |
| distance 3 (e.g. bits 7, 9, 11) | yes | n = (1,1,1,1) | P_meson |
| distance 4 (e.g. bits 0, 7, 9, 10) | yes | N = 4, mixed q | P_other |
| the only other q = (1,−1,0,0) codeword is the short string j = (½,0,0,0), code **2058** | yes | — | P_short (**distance 8**) |

Therefore **[D]**, at r = 0:

- `P_surv` = `P_stretched` is interior — slightly below 1, with the deficit dominated by the two
  distance-1 matter-bit errors → **Var_s > 0, σ > 0**. Same for `P_BBbar`, `n_v3` (0 vs 2 on the
  v3 flip) and `E2_l1` (0 vs 0.75 on link-flip survivors), which are precisely the three
  observables the twin row checks (`run_g4.py:135–136`).
- `P_short` (distance 8), `P_meson` (distance 3, ≲ 1 expected count in 4000 shots at percent-level
  error rates **[illustrative]**) and `P_other` (distance 4) are predicted to be **identically
  zero in all five repeats**, giving σ = 0 *for a structural reason predicted in advance by the
  multinomial formula itself* (§2.5) — not because the twin is deterministic.

### 3.4 The call

**Predicted case: D-C0 case A — the escalation clause does not fire at r = 0.** **[D]**

| branch | prediction | how it is recognised |
|---|---|---|
| five dictionaries **identical** | **not expected** | any two repeats equal as dicts ⇒ construction-time seed wins ⇒ §2.1 item 5's "identical dictionaries" branch: locate the cause and fix, then re-run |
| five dictionaries **distinct, σ > 0** on `P_surv`, `P_BBbar`, `n_v3`, `E2_l1` | **expected** | bootstrap `two_sigma`/2 within a factor 2 of √(Var_s/(5·N̄_kept)) (§2.3–2.4) ⇒ record **"override harmless"**, D-C0 not triggered |
| distinct but σ = 0 on `P_short`, `P_meson`, `P_other` | **expected, benign** | the multinomial prediction is *also* zero for these channels; record as structurally empty, **do not** invoke D-C0 |
| distinct but σ = 0 on an observable with interior predicted P | **not expected** | this alone triggers D-C0 ⇒ test at r = 1 and record the mechanism |

**Answer to "must D-C0 r = 0 use r = 1?"** **[D]** No — the r = 0 point is predicted to be
self-sufficient for the seed question, so D-C0's fallback to r = 1 is predicted not to be
required. But r = 1 is run regardless, for two independent reasons: **[S]** v0.6.1 §2.1 item 5
mandates the pre-fix run at both r = 0 and r = 1 irrespective of D-C0; and **[D]** r = 1 is the
only point at which the channels that are structurally empty at r = 0 (`P_meson`, `P_other`, and
`P_short`) acquire interior probabilities, so the "bootstrap σ ≈ multinomial expectation" half of
V10 (v0.6.0 line 117) can only be tested across all channels at r ≥ 1. Treat r = 1 as the
confirmatory point for the variance comparison, not as a D-C0 remedy.

**Negative control.** **[D]** With all five run-time seeds forced equal (and the transpile seed
already common across k), Aer is expected to return bit-identical dictionaries, so the control
run must fail the distinctness assertion. If the control *passes* — distinct dictionaries under
identical seeds — the twin has an unseeded stochastic path and the V10 row fails regardless of
the r = 0 result.

**What the ledger row must record**, per D-C0's "record which case applies" **[D]**: the case
letter from the table above, the mechanism (seed precedence, structural zero variance, or genuine
determinism), the observable each σ was evaluated on, `two_sigma/2`, the predicted SE with the
0.894 bootstrap factor applied, N̄_kept and yield, and the negative-control outcome.

---

## 4. Falsification summary (what makes each prediction wrong)

| # | prediction | falsified by |
|---|---|---|
| P1 | j_max = 1 sector counts (3, 36, 74, 36, 3), total 152, by both routes | either route returning a different total or a different split |
| P2 | j_max = ½ counts (2, 20, 38, 20, 2), total 82, from the *same* generating function | disagreement with `EXPECTED_SECTOR_DIMS` |
| P3 | all odd-N sectors empty at both truncations | any odd-N basis element |
| P4 | `two_sigma` ≈ 1.79 × √(Var_s/(5·N̄_kept)), inside the factor-2 V10 band | a ratio outside [0.5, 2] on an observable with interior P |
| P5 | at r = 0: five distinct dictionaries; σ > 0 on `P_surv`, `P_BBbar`, `n_v3`, `E2_l1`; σ = 0 on `P_short`, `P_meson`, `P_other` | identical dictionaries, or σ = 0 on the first group, or σ > 0 on `P_short` |
| P6 | D-C0 case A: the r = 1 escalation is not required by D-C0 (though r = 1 is run anyway) | any σ = 0 on an interior-P observable at r = 0 |

**Out of scope for this document:** the STATIC-112 and STATIC-2417 bridge counts and the 2×3
count 1,727 (v0.6.1 §4, priorities 3–4) are C2 rows; the static-charge convention is not fixed in
`conventions.py`, so no count is predicted here. The same transfer-matrix method extends to them
and will be used by the C2 auditor.


# Source: AGENTS.md
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


# Source: README.md
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


# Proposal section 8: .work/c060_nine_month_plan.txt lines 571-713
but it does not move the program’s physics deliverable. The roadmap’s Path A, learned ZX
rewriting evaluated after routing, is where the compiler novelty actually lives; the selector is a
placeholder for it.

7.3 Verdict

Keep the scaffold, change the object, and demote the compiler comparison to a secondary
endpoint that costs nothing once the circuits exist.

                                                11

8 The rebuilt one-month project: SU(2) with dynamical matter on one plaquette

8.1 Hypothesis


   For the hardcore-gluon SU(2) single-plaquette patch with four staggered two-color
   fermion sites (82 gauge-invariant states, 12 qubits in a local gauge-invariant encoding), a
   symmetry-verified second-order product-formula evolution on a Heron-class IBM device
   reproduces the exact pair-creation and Casimir-reduction dynamics of a flux string within
   2σ over at least four time points, with leakage-flag post-selection retaining at least 20
   percent of shots, at most about 250 CZ per Strang step, two or three Strang steps per
   circuit, at most about 1,000 CZ per circuit including state preparation and basis changes,
   and two-qubit depth below about 200. This would be the first quantum-hardware time
   series for a non-Abelian gauge theory with dynamical fermions on a plaquette geometry,
   the smallest two-dimensional unit; the phrase “2+1D” is reserved for the 2 × 3 ladder
   and beyond, where an interior vertex exists.


The problem this month answers is a current one: what does it cost, in qubits and two-qubit
depth, to evolve SU(2) with fundamental matter on a plaquette on today’s hardware, and
does the hardware reproduce the non-Abelian channel structure of string breaking with a
decomposed error budget? Nothing larger is claimed. At this size the physics is exactly
diagonalizable; the hardware does not add knowledge about SU(2), it establishes the resource
frontier and the verification method that the proposal’s months 4 to 8 need. That is the honest
version of what a one-month hardware project can solve.

8.2 Model and observables

The Hamiltonian is the proposal’s Eq. (1) on one square plaquette with open bound-
                      g2
aries: electric term 2a ∑ℓ E2ℓ with E2 = j( j + 1) on each of the four links, staggered mass
                                                     1
m ∑n (−1)nx +ny ψ̂n† ψ̂n , gauge-covariant hopping 2a  ∑ η ψ̂n† Ûℓ ψ̂n′ + h.c. across the four links,
                                                                               

and the magnetic term − 2g12 a Tr Û□ + Û□ † . Each matter site holds two colors, so its four Fock
                                             

states are the color-singlet vacuum, the doublet, and the doubly occupied color singlet, which
in SU(2) is the baryon. The truncation is j ∈ {0, 12 }. The gauge-invariant basis is built two
independent ways, by spin-network coupling coefficients and by projecting the 20-qubit
redundant Kogut–Susskind Hamiltonian onto its Gauss-law kernel, and the two must agree to
10−12 . Three limits are unit tests: g → ∞ (pure electric), m → ∞ (matter frozen; the plaquette
must reduce to the monograph’s one-plaquette Hamiltonian H            e1 ), and the ring limit without
the magnetic term (a four-site periodic loop-string-hadron chain).
Staggering fixes the geometry of the initial state: a quark is a particle on an even vertex and
an antiquark a hole on an odd vertex, and adjacent vertices of the plaquette have opposite
parity, so a quark–antiquark pair sits on adjacent vertices and can be joined by the one-link
path or the three-link path. The initial state is the stretched string, the pair joined by j = 1/2
flux along the three-link path. It has two competing decay channels: coherent shortening
to the one-link path through the magnetic term, and breaking by pair creation on the two
intermediate vertices (an even and an odd one) into two mesons. The baryon channel, a
doubly occupied even vertex paired with a doubly empty odd vertex, is defined by projectors


                                                 12

and its weight is measured, as in Cataldi et al. The observables are the Casimir per link, the
site-resolved matter density, projectors onto the stretched string, the short string, the meson
channel and the baryon–antibaryon channel, string survival, the energy (conserved by the exact
evolution, not by the product formula), and the leakage-flag rate. The mass is scanned across
the finite-size resonance near m = 3g2 /(16a) in the proposal’s normalization (m = 3gE /8 in
Cataldi’s), which exact diagonalization locates on day 5; the jmax = 1 basis (152 states) gives
the truncation error at the same couplings.

8.3 Claim boundaries


Supported if the gates pass                                     Not supported by this experiment

A 12-qubit symmetry-verified evolution of SU(2) with dy-        String tension, a continuum limit, or
namical matter on a plaquette is within reach of current        hadron phenomenology
hardware at a stated depth and yield
The meson-versus-baryon channel split, the string shorten-      Any classically intractable calcula-
ing, and the Casimir reduction survive on hardware within       tion; the patch is exactly solvable
the error budget
An error budget decomposed into truncation, Trotter, com-       Baryon blockade and the full 2+1D
pile, device, and shot contributions                            claim, which need ladders (Idea 1,
                                                                months 5 and 6)
The compiler comparison of the monograph, as a secondary        Quantum advantage of any kind
endpoint on physically meaningful circuits


8.4 Thirty-day plan


Days     Work                                                                Exit evidence

1 to 3   Freeze conventions (units, staggered phases, qubit order, basis); Agreement to 10−12 ; lim-
         build the 82-state Hamiltonian by both routes; run the three      its pass; preregistration
         limit tests                                                       draft
4 to 6   Exact dynamics: string survival, shortening, Casimir reduction,   Truncation-error state-
         meson and baryon projectors versus mass; locate the finite-size   ment; time window
         resonance; jmax = 1 comparison                                    chosen where physics
                                                                           is visible
7 to 9   Encodings: 3-qubit-per-vertex local encoding with leakage         Circuit family verified;
         flags versus the 7-qubit compact encoding; Pauli decomposi-       error falls as r −2 ; noise-
         tion, gauge-invariant term grouping with each grouped term        less leakage rate exactly
         synthesized as an exact block unitary, Strang circuits with exact zero
         unitary checks (monograph code reused); Trotter error versus
         repetitions
10 to    Compile to heavy-hex targets with Qiskit level 3 and the mono- CZ and two-qubit-depth
12       graph’s PyZX pipelines, judged after routing; noisy simulation table; pipeline chosen by
         with a device noise model; Plan B decision if the per-step bud- routed count, the mono-
         get is missed                                                     graph’s finding applied
13 to    Measurement design (groupings for all observables), readout       Six-to-twenty-setting
14       mitigation plan, post-selection on leakage flags and energy;      measurement plan;
         preregistration signed                                            frozen configuration


                                                  13

Days     Work                                                                 Exit evidence

15 to    CUDA-Q statevector and tensor-network cross-checks; full             Rehearsal output repro-
17       noisy pipeline rehearsal; decide the hardware window (two            duces exact observables
         or three Strang steps, at most about 1,000 CZ per circuit, two-      within the noise model
         qubit depth below about 200)
18       Dry run: inspect every ISA circuit, resource summary, approval       Approval summary
         token                                                                archived
19 to    Pilot: three times, all groupings, 2,048 shots; stop/go review on    Pilot passes or defects
20       equivalence, mapping, bit order, symmetries                          listed
21 to    Fix only prespecified defects; re-freeze                             Change log
22
23       First full run: five times, two mitigation arms (none; decou-        Job, calibration, usage
         pling plus twirling plus decoherence renormalization), optional      records; raw immutable
         extrapolation arm; the month-4 production run repeats this           export
         with full statistics and a second calibration window
24 to    Analysis: exact comparison, bootstrap over time blocks, post-        Primary and secondary
26       selection yield, error-budget decomposition; second calibration      tables with intervals
         window if quota permits
27       Ablations: mitigation arms, encodings, compiler pipelines (the       Ablation table
Extraction may be incomplete outside this section; original docs/refs/SU2QC_Nine_Month_Plan.pdf.