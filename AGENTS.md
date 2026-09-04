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
