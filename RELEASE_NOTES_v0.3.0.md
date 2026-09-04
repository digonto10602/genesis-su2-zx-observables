# SU2ZX v0.3.0 release notes

v0.3.0 turns the original single-target compiler benchmark into a structurally and topologically diverse, exactly verified study.

Highlights:

- 35 parameterized circuits, 30 structural circuits, and five explicit angle-only duplicates across N=2–6 and Strang depths 1,2,4,8.
- Six exact Qiskit/PyZX pipelines, five synthetic topology classes, multiple layouts, 426/426 verified primary compiler records, and 54/54 verified seed-sensitivity records.
- Meaningful winner diversity: Basic and phase teleport each achieve at least three strict native-2Q wins after structural aggregation.
- ML status `NULL`: grouped cost prediction improves on always-Qiskit but does not beat always-Basic.
- A reflection-paired Strang ordering eliminates sampled ideal mirror asymmetry to numerical precision and reduces energy drift without changing source 2Q count.
- Fitted Trotter convergence order `p=1.8658 ± 0.06495` over r=1,2,4,8.
- CPU MPS validation passes for N=5,8; N=12 is exploratory.
- CUDA-Q CPU passes; GPU paths remain `BLOCKED_BY_HARDWARE`; IBM QPU remains `NOT_RUN`.

The model remains a severely truncated pure-SU(2) 2+1D plaquette-chain Hamiltonian benchmark. It does not establish continuum or physical-QCD claims.
