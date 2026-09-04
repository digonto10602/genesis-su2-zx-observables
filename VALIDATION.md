# Laptop validation

Validated locally on 2026-09-04:

- Python 3.11.16 fixed Mamba environment: PASS.
- Ruff and mypy: PASS.
- Pytest: 13 passed.
- Qiskit: 2.5.2.
- PyZX: 0.10.6.
- One-plaquette matrix, spectrum, and transition probability: PASS.
- Two-plaquette matrix and ground energy: PASS.
- General Hamiltonian Hermiticity and mirror checks: PASS.
- Exact PyZX equivalence for Basic, phase teleport, and full reduce: PASS.
- Six-basis energy reconstruction maximum error: `1.2568e-13`.
- Initial five-plaquette energy: `3.0`.
- CPU observable pipeline: 405 rows generated.
- Generic linear-ECR compiler dataset: 240 rows generated.
- Median Basic native two-qubit reduction: about `20.3%`.
- Median Basic two-qubit-depth reduction: about `23.5%`.
- Selector outcome: `NULL`; always-Basic tied the learned selector on this generic target across all tested cost weights.
- CUDA-Q 0.15.1 `qpp-cpu`: PASS against Qiskit for `N=1,2,5`; maximum energy error `1.0614e-13` and maximum distribution TVD `1.0289e-15`.
- GPU: NVIDIA GeForce GTX 1060 Max-Q, 6144 MiB, driver 580.178.04, compute capability 6.1.
- CUDA-Q GPU, tensor-network, and direct cuTensorNet: `BLOCKED - UNSUPPORTED GPU ARCHITECTURE`; current documented minimum is 7.5.
- IBM QPU: `NOT RUN - AUTHORIZATION/CREDENTIALS REQUIRED`; no submission occurred.

The checked artifacts were regenerated on the target laptop. CSV/JSON integrity,
finite numeric fields, expected row counts, figure existence, and Markdown links
were validated before publication.
