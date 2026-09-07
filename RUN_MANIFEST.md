# SU2ZX v0.4.0 run manifest

- UTC archive timestamp: 20260906T223709Z
- Input Git commit: 93ac4daaadaad76a0b36ae74b2c004f25e5c2603; verified published main revision; this final reports ZIP was created after push.
- Archive: `zip_results/SU2ZX_v0.4.0_20260906T223709Z.zip`
- Archive SHA256 and exact-file test receipt: `SU2ZX_v0.4.0_20260906T223709Z.zip.sha256` and `SU2ZX_v0.4.0_20260906T223709Z.zip.integrity.json` beside the archive.
- Baseline physics: PASS; final regression tests, Ruff, formatting, mypy, grouped leakage, frozen rule, seed reproducibility and data integrity: PASS.
- Compiler: 830/860 outputs pass; 30 excluded; 415 complete pairs.
- Robust families: Basic 33, Teleport 29, count ties 21; seed-sensitive 0; broader layout/topology result INCONCLUSIVE.
- ML: NULL. Prospective grouped-selected logistic regret 0.024954; strongest simple regret 0.008966.
- Symmetry: MIXED. 168 physics and 81 verified compiler records.
- Strang current-order exponent: full 1.865777, asymptotic 1.978062.
- TN: direct observables VALIDATED at N=5,8; no-statevector SCALING_DEMONSTRATED through N=32 at t=0.32,r=2.
- CUDA-Q CPU PASS; GPU BLOCKED_BY_HARDWARE; IBM metadata NOT_AVAILABLE; QPU NOT_RUN.
- Graphify: PASS, 796 nodes / 1258 relationships.
- Datasets: artifacts/data/v040/; 16 figures with PNG/PDF and source mappings: artifacts/figures/v040/.
- Provenance: artifacts/provenance/run_v0.4.0.json; validation logs: artifacts/logs/v040/.
- GitHub: existing digonto10602/genesis-su2-zx-observables remote; push PASS; remote main was independently verified before this archive.

## Archive scope and limitations

Includes current code/tests/scripts, research/configuration/prompts, reports, data, plots, provenance, relevant logs and refreshed graph. Historical v0.3.0 data/release notes remain included. Excludes environments, caches, .git, .work, credentials and prior archives. The exact ZIP is tested and hashed after creation; its external integrity receipt names this exact file, avoiding a self-referential archive checksum.

Compiler targets are synthetic, calibration seed fixed, basis ECR only, grids bounded. Historical winner selection is enriched. Routed equivalence is randomized numerical validation. Large-N MPS has no exact-Hamiltonian reference; long-time entanglement growth is not studied. No QPU or unsupported GPU execution occurred. No continuum, physical-QCD or quantum-advantage claims.

## Comprehensive final reports

See docs/V040_COMPLETION_AUDIT.md, docs/CODE_LOGIC_AND_TESTS.md and docs/CODE_FUNCTION_INVENTORY.md. Full source and test implementations, datasets, figures and fresh completion logs/JUnit are included. Publication receipt: artifacts/provenance/publication_v040.json. Final archive receipts and this manifest are post-commit additions.
