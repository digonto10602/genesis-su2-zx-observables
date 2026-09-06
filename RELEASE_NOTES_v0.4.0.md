# SU2ZX v0.4.0 release notes

- Fixed-calibration five-seed Basic/Teleport study: 860 outputs, 830 passing, 30 excluded, 415 valid pairs; 33 robust Basic, 29 robust Teleport, 21 ties.
- Frozen prospective rule and four leakage-controlled pairwise models. ML NULL; the grouped-selected model fails to beat the simple prospective baseline.
- Symmetry grid: 168 physics rows and 81 compiler rows. Symmetry ordering preserves reflection and lowers source depth, but TVD and energy effects are mixed.
- Full and asymptotic Strang fits; five-metric physics/compiler Pareto data.
- Direct-observable Aer MPS validated at N=5,8 and scaled through N=32 without full statevector reconstruction.
- PyZX QASM import precision fixed; explicit logical tolerance and independent layout-aware routed verification added.
- 120 synthetic hardware-ready comparison circuits, generalized raw/M3 analysis and fresh one-use submission approval binding. Zero QPU jobs.
- CUDA-Q CPU passes; GPU blocked on compute capability 6.1.
- Sixteen reproducible PNG/PDF figures, refreshed knowledge graph, provenance and exact final ZIP verification.

The Hamiltonian and conventions are unchanged. Numerical failures are retained and excluded, not relabeled as successes. No physical-QCD, continuum or quantum-advantage claim is made.
