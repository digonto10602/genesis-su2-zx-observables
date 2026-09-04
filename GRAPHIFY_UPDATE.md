# Graphify update — SU2ZX v0.3.0

- Timestamp: 2026-09-04T22:20:57Z
- Graphify version: 0.9.53
- Commands: `.mamba/bin/graphify update .`, semantic incremental merge, `.mamba/bin/graphify export html`, and a focused `graphify query` validation.
- Indexed root: repository root `SU2ZX/`.
- Indexed content: live Python packages, tests, scripts, JSON configuration/results, README, research report, validation report, environment record, research prompts, and references.
- Explicit exclusions in `.graphifyignore`: `zip_results/`, binary figure files under `artifacts/figures/`, and `artifacts/environment-pip-freeze.txt`.
- Nodes: 408.
- Edges/relationships: 678.
- Communities: 28.
- Validation: PASS.

The extraction diagnostic reported zero missing endpoints, dangling endpoints, self-loops, exact duplicate edges, or collapsed same-endpoint edges. A focused query connected the v0.3.0 winner-diversity, grouped-ML, symmetry-aware Trotter, CPU-MPS, CUDA-Q, and completion-gate concepts to their code, tests, prompts, and reports.

Known gaps: release-note prose is represented through the versioned code/report graph rather than a dedicated semantic node; large binary artifacts and prior archives are intentionally not indexed. The graph is an undirected navigation graph, so directional edge semantics remain edge attributes rather than a directed NetworkX graph.
