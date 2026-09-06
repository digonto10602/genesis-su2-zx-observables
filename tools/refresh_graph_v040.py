"""Merge the archived semantic fragment using installed Graphify, then validate.

Run with .mamba/bin/python after .mamba/bin/graphify update .
"""

# ruff: noqa: E501
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path


def main():
    from graphify.build import build_merge
    from graphify.export import to_json

    root = Path.cwd().resolve()
    if root.name != "SU2ZX":
        raise RuntimeError("run inside SU2ZX root")
    graph = root / "graphify-out/graph.json"
    semantic = root / "artifacts/provenance/graph_semantic_v040.json"
    extraction = json.loads(semantic.read_text())
    for node in extraction["nodes"]:
        path = (root / node["source_file"]).resolve()
        assert root in path.parents and path.is_file()
    # Repeated heading labels in the function inventory are distinct locations.
    # Preserve their IDs instead of applying graph-wide label deduplication.
    merged = build_merge([extraction], graph_path=graph, root=root, directed=False, dedup=False)
    assert to_json(merged, {}, str(graph))
    subprocess.run([str(root / ".mamba/bin/graphify"), "cluster-only", "."], check=True)
    payload = json.loads(graph.read_text())
    nodes = {node["id"] for node in payload["nodes"]}
    edges = payload.get("links", payload.get("edges", []))
    assert len(nodes) == len(payload["nodes"])
    assert all(edge["source"] in nodes and edge["target"] in nodes for edge in edges)
    assert not any(edge["source"] == edge["target"] for edge in edges)
    assert len({tuple(sorted([edge["source"], edge["target"]])) for edge in edges}) == len(
        edges
    )
    for name in ["direct_mps", "verify_native", "evaluate_ml", "physics_run"]:
        assert any(name in str(node.get("label", "")) for node in payload["nodes"])
    record = dict(
        status="PASS",
        nodes=len(nodes),
        edges=len(edges),
        version=version("graphifyy"),
        graph_sha256=hashlib.sha256(graph.read_bytes()).hexdigest(),
        utc_timestamp=datetime.now(UTC).isoformat(),
        checks=[
            "unique nodes",
            "edge endpoints",
            "no self loops",
            "no duplicate pairs",
            "direct MPS, routed verification, pairwise ML and physics nodes present",
        ],
    )
    (root / "artifacts/logs/v040/graph_validation.json").write_text(
        json.dumps(record, indent=2)
    )
    text = f"""# Graphify update — SU2ZX v0.4.0

- UTC timestamp: {record["utc_timestamp"]}
- Graphify version: {record["version"]}
- Nodes: {len(nodes)}; relationships: {len(edges)}.
- Validation: PASS. Unique IDs, existing endpoints, no self-loops/duplicate edge pairs, and critical v0.4.0 callable coverage checked.
- Graph SHA256: {record["graph_sha256"]}.

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
"""
    (root / "GRAPHIFY_UPDATE.md").write_text(text)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
