# ASK — question → file routing

Every routed answer resolves to a path inside this bundle.

| Question | Answer files | Status |
|---|---|---|
| Where is the Hamiltonian defined? | `src/runs/section8_v0.5.0_20260907T0628Z/src/su2qc/conventions.py`; `docs/PHYSICS_SPEC.md` | complete |
| What is the encoding? | `docs/PHYSICS_SPEC.md`; `src/runs/section8_v0.5.0_20260907T0628Z/src/su2qc/encodings/l12.py`; `docs/SU2QC_FUNCTION_INVENTORY.md` | complete |
| What does `run_counts` actually do? | `docs/SU2QC_CONTRACTS.md` (entry `su2qc.twin.twin.run_counts`); `src/runs/section8_v0.5.0_20260907T0628Z/src/su2qc/twin/twin.py` (lines 54-63) | complete (defect stated) |
| Why did C0 fail? | `sessions/CODE_ISSUES.md`, `sessions/EXECUTION_ISSUES.md`; `docs/GATE_MAP.md` | complete (diagnosis only) |
| Is the seed bug fixed? | `docs/SU2QC_CONTRACTS.md` (`PROPOSED, NOT IMPLEMENTED — blocked on Fable`) | not fixed |
| Are the error bars valid? | `CLAIMS.md` (yield σ VOID); `docs/SU2QC_CONTRACTS.md` (`bootstrap`) | documented void |
| What is the closure identity and does it hold? | `docs/SU2QC_CONTRACTS.md` (`channel_closure_residual`, R15 correction); `docs/PHYSICS_SPEC.md` | holds on present basis (finite oracle) |
| Why did r=1 time out? | `sessions/EXECUTION_ISSUES.md`; `evidence/seed-diagnosis.json` (partial status) | recorded |
| What is blocked and on what? | `INDEX.md`; `sessions/EXECUTION_ISSUES.md` | Fable planning/escalation + sign-off |
| How do I rerun G3? | `docs/EXECUTION_MAP.md`; `gates/gate_G3.py` | complete |
| What was measured on hardware? | `INDEX.md` (nothing); `CLAIMS.md` | none ever |

## Other likely questions

| Question | Answer files |
|---|---|
| Where are the four session-3 issue reports? | `sessions/` (verbatim copies) |
| Where is the code graph? | `graph/GRAPH_REPORT.md`, `graph/graph.json` |
| Which package is live vs archived? | `docs/CODE_MAP.md` |
| What is excluded and why? | `EXCLUSIONS.md` |
| How is the bundle integrity proven? | `MANIFEST.json`, `MANIFEST.sha256`, `SELFTEST.json` |