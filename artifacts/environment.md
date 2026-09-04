# SU2ZX v0.3.0 environment

- UTC run date: 2026-09-04
- Kernel: Linux 7.1.9-arch1-2 x86_64
- CPU: 12 logical processors
- RAM: 15 GiB physical; more than 9 GiB available before expensive work
- Disk: 446 GiB filesystem; 399 GiB available before expensive work
- GPU: NVIDIA GeForce GTX 1060 with Max-Q Design, 6144 MiB, compute capability 6.1
- NVIDIA driver: 580.178.04
- Python: 3.11 in `.mamba/envs/su2zx`
- Qiskit: 2.5.2
- Qiskit Aer: 0.17.2
- PyZX: 0.10.6
- CUDA-Q: 0.15.1
- scikit-learn: see `artifacts/environment-pip-freeze.txt`
- Compiler/lint/type tools: Git 2.55.0; Ruff and mypy versions are pinned in the freeze file

CUDA-Q CPU execution passed. GPU CUDA-Q/cuTensorNet execution is `BLOCKED_BY_HARDWARE` because this GPU is below the recorded compute-capability 7.5 minimum. No system configuration, driver, or global Python installation was modified.

Full machine-readable provenance is in `artifacts/provenance/run_v0.3.0.json`.
