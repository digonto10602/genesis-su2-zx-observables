# Code map — live package vs archived package

Documentation only.

## Two packages

| | archived / published | live / gated |
|---|---|---|
| Path | `src/su2zx/` (+ `tools/`, `tests/`) | `runs/section8_v0.5.0_20260907T0628Z/src/su2qc/` |
| Version | v0.4.0 research package | Section-8 twin/gate pipeline |
| Status | shipped archive; still the repo-level package exposed at `src/` | every module under active gate (C0) |
| Documented by | `docs/CODE_FUNCTION_INVENTORY.md`, `docs/CODE_LOGIC_AND_TESTS.md` | `docs/SU2QC_FUNCTION_INVENTORY.md`, `docs/SU2QC_LOGIC_AND_TESTS.md`, `docs/SU2QC_CONTRACTS.md` (new this session) |

The scope defect closed by this session: the generated documentation covered only
the archived package, while the gated code lives in the `su2qc` package. The string
`su2qc` previously appeared in `docs/` only in a referenced review file.

## su2qc modules (23)

- `conventions.py` — frozen Hamiltonian/convention source of truth
- `encodings/l12.py` — 12-bit local encoding
- `circuits/strang_l12.py`, `circuits/synth_l12.py`, `circuits/export_l12.py` — circuit construction/export
- `ham/route_spinnet.py`, `ham/route_gausskernel.py` — the two Hamiltonian routes
- `ham/limits.py`, `ham/compare.py` — limit checks and cross-route comparison
- `compile/route.py`, `compile/run_g4.py` — routing and production twin pipeline
- `dynamics/engine.py`, `dynamics/scan.py` — exact evolution and channel/window scans
- `twin/twin.py` — the twin estimator (seed defect, channels, bootstrap)
- `replicate.py` — hashing/manifest helpers
- `__init__.py` files — package markers

## Link mapping inside the bundle

Every generated and carried document is packaged byte-identical to its committed
copy; no document was rewritten to make a link resolve. The layout carries the
links instead:

- `docs/CODE_FUNCTION_INVENTORY.md` links `../src/su2zx/*.py`, `../tests/*.py` and
  `../tools/*.py`, so the archived package is placed at `src/su2zx/`, its tests at
  `tests/` and the ten linked tools at `tools/`.
- `docs/SU2QC_FUNCTION_INVENTORY.md` links `../runs/section8_v0.5.0_20260907T0628Z/...`,
  so the live package is additionally placed at that repository-relative path.
- The live package therefore appears twice: canonically under
  `src/runs/section8_v0.5.0_20260907T0628Z/` (the R18 `src/` tree, which every
  hand-written document cites) and as a byte-identical alias tree under
  `runs/section8_v0.5.0_20260907T0628Z/`. `SELFTEST.json` check 3 hashes both
  copies against the working tree, so the two can never drift apart.
- Evidence that the hand-written documents cite by its repository path (for
  example `runs/campaign_v060/sessions/c060_p0_20260908_3/seed-diagnosis.json`)
  is packaged flat under `evidence/` with its original file name; the repository
  path is kept in the prose so the reader can find the file in the working tree.
- Backticked paths in `INDEX.md`, `ASK.md`, `CLAIMS.md` and `docs/GATE_MAP.md` are
  relative to the archive root; Markdown links are relative to their document.

## Which is source of truth

For the GI-cost campaign: `su2qc` (the live gated package). `src/su2zx/` remains the
archived v0.4.0 research package and is not the thing C0 gates.