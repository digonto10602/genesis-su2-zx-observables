# SU2ZX v0.4.0 validation

## Completion verification — 2026-09-06

Fresh suite: **26 passed**, 47 upstream warnings, 8.57 seconds. Ruff, formatting,
mypy and saved-data audit pass. Fresh six-strategy controls (18 outputs), seed
reproduction, pairwise reanalysis, N=5..32 direct-MPS sweep and all 16 PNG/PDF
figures also pass. Logs and per-case JUnit results are under
`artifacts/logs/v040/completion/`. The original routing/symmetry experiment logs
below remain historical evidence, not newly executed trials.

Detailed test-to-function mapping and limitations:
[code and tests report](docs/CODE_LOGIC_AND_TESTS.md),
[function inventory](docs/CODE_FUNCTION_INVENTORY.md), and
[prompt completion audit](docs/V040_COMPLETION_AUDIT.md).

## Original research validation

Generated 2026-09-05T07:01:09.932665+00:00.

- Initial v0.3.0 baseline: 17 tests, Ruff, mypy PASS; fresh physics run 405 rows.
- Final tests: 26 passed, 47 warnings in 6.57s.
- Physics Hamiltonian, one/two plaquette analytics, Hermiticity, normalization, ordering and reconstruction regressions: PASS.
- Historical source hashes: 35/35 reproduce; prior 426-row data integrity PASS.
- New compiler: 830/860 pass; 30 failed outputs explicitly excluded. Logical atol=rtol=1e-10, routed phase-aligned maximum amplitude error <=1e-10 on zero plus three seeded random inputs. Ancillas and both layout permutations are checked.
- Six-strategy controls: 18 passing outputs. Fixed-seed/target/layout hash repeat PASS.
- Pairwise records: 415 complete verified pairs; delta integrity PASS.
- Feature allow-list and grouped leakage checks: PASS. No cost or routed-result inputs. Historical groups only for model selection; new r=3 families for prospective test.
- Frozen configuration SHA-256: PASS. No post-holdout rule tuning.
- Symmetry checks: 168 physics rows; maximum mirrored asymmetry 1.11e-15 for symmetry ordering. Even-N initial states are symmetric.
- Trotter fits: full r=1,2,4,8 and asymptotic r=2,4,8 recorded with standard errors; current N=5 exponents 1.865777 and 1.978062.
- Direct MPS N=5,8 maximum validated observable error 2.272e-09 (<1e-7); no-statevector scaling N=12..32 PASS.
- CUDA-Q qpp-cpu N=1,2,5 comparison <1e-8 PASS; GPU BLOCKED_BY_HARDWARE.
- Hardware-ready synthetic bundle: 120 circuits; QPU NOT_RUN.
- Ruff, format and mypy: PASS (see logs).
- Figures: 16 regenerated from CSV, PNG/PDF with source mapping.
- Graphify: final counts and validation in GRAPHIFY_UPDATE.md.
- Secret scan/archive: exact final ZIP validation and SHA256 receipt are generated after this document, under zip_results/; see RUN_MANIFEST.md for exact name. They are not inferred from a staging archive.

## Reproduction commands

```bash
bash scripts/run_v040.sh
.mamba/envs/su2zx/bin/python -m pytest
.mamba/envs/su2zx/bin/ruff check src tests tools
.mamba/envs/su2zx/bin/ruff format --check src tests tools
.mamba/envs/su2zx/bin/mypy src
.mamba/envs/su2zx/bin/python tools/validate_v040.py audit
.mamba/envs/su2zx/bin/python tools/plot_v040.py
.mamba/bin/graphify update .
```

Full stage commands appear in README.md. Logs are in artifacts/logs/v040/. PyZX emits two upstream Python-enum deprecation warnings; mthree emits 45 upstream CircuitInstruction deprecation warnings in the guard test. Scikit-learn warns when held-out true labels lack a predicted class; the confusion matrices retain all three labels. Neither warning is suppressed. Earlier execution failures are explained in RESEARCH_RESULTS.md; final logs contain the corrected reruns. The rejected compiler outputs remain in the raw dataset.
