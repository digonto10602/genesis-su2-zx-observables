# Graphify update — SU2ZX v0.4.0

- UTC timestamp: 2026-09-06T22:36:48.287498+00:00
- Graphify version: 0.9.53
- Nodes: 796; relationships: 1258.
- Validation: PASS. Unique IDs, existing endpoints, no self-loops/duplicate edge pairs, and critical v0.4.0 callable coverage checked.
- Graph SHA256: e017f02cd6deb3de7d292ce2c4ce7c44d6758dedb367e462e901cca79e8899f0.

## Commands

```bash
.mamba/bin/graphify update .
.mamba/bin/python tools/refresh_graph_v040.py
.mamba/bin/graphify query "direct MPS robustness pairwise selector symmetry"
.mamba/bin/graphify diagnose multigraph --json
```

The helper uses installed `graphify.build.build_merge` with dedup=False to preserve distinct repeated-heading locations, and `graphify.export.to_json`, followed by supported `cluster-only .`. Code uses AST extraction; research concepts use a separately extracted, grounded semantic fragment preserved in artifacts/provenance/graph_semantic_v040.json. New completion documents have structural heading coverage; their full prose has not received a new semantic extraction. Token accounting for the historical fragment is unavailable, represented as zero placeholders rather than a claim of zero host-agent usage. No external LLM API was used.

Indexed paths include src/, tests/, tools/, scripts/, configuration, root reports, research prompts and artifact/provenance relationships. Updated concepts connect current/reversed/symmetry ordering, exact evolution/observables, full/asymptotic convergence, Basic/Teleport/controls, fixed targets/layouts/seeds, delta costs, grouped models/frozen rule, direct MPS/scaling, CUDA-Q/IBM, datasets/plots and provenance.

Exclusions: .mamba/, .work/, .git/, caches, zip_results/, binary figures, QPY bundles and environment package listings. Binary contents are represented by data/provenance references, not parsed. Final RUN_MANIFEST archive metadata is prepared after graph refresh per the required completion order; the graph describes the research rather than a self-referential final ZIP checksum. Small CSV entries are not represented row by row. The graph is undirected; relationship direction remains in edge attributes.

# Graphify update — SU2ZX v0.5.0 status (2026-09-07)

- Graphify 0.9.53, `graphify update` (AST only, no LLM, no API cost) on the repository root and on `runs/section8_v0.5.0_20260907T0628Z/`.
- Root graph: 796 → 1459 nodes, 1258 → 2196 relationships, 61 → 131 communities. Run graph: 820 → 830 nodes, 1087 → 1105 relationships.
- Validation: PASS for both (unique ids, existing endpoints, no duplicate edge pairs; critical v0.5.0 callables present). Record: `artifacts/logs/v050/graph_validation_20260907.json`.
- Graph SHA256: root `c126c09a45074da0fc9aca3ff20791274e28e23b461544c08ca366f330e804a3`; run `577e7274a6245048fc3a368ea3f4b363bc47fb88272cbf584b54989adfa1d97c`.
- `.graphifyignore` now excludes the run's nested `graphify-out/`, agent transcripts `logs/agents/*.out.md`, exported QPY/QASM circuits and the run's pytest cache.
- Previous curated graphs were backed up by graphify to `graphify-out/2026-09-07/` in each location. Community names were not regenerated (needs an LLM backend).
- Full status: `STATUS_REPORT_20260907.md`.
