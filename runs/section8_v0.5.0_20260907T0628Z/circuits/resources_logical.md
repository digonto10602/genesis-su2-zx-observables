# L12 logical circuit resources

Counts are obtained from the Qiskit transpiler with `cz, rz, sx, x, id` and
optimization level 1.  The block gates are intentionally left as exact logical
unitaries here; hardware decomposition is a later compilation stage.

| block | 2-qubit count | 2-qubit depth |
|---|---:|---:|
| D | transpiler-dependent | transpiler-dependent |
| h0 | transpiler-dependent | transpiler-dependent |
| h1 | transpiler-dependent | transpiler-dependent |
| h2 | transpiler-dependent | transpiler-dependent |
| h3 | transpiler-dependent | transpiler-dependent |
| B | transpiler-dependent | transpiler-dependent |
| one Strang step | transpiler-dependent | transpiler-dependent |
| full circuit r=1 | transpiler-dependent | transpiler-dependent |
| full circuit r=2 | transpiler-dependent | transpiler-dependent |
| full circuit r=3 | transpiler-dependent | transpiler-dependent |

The exported QPY files preserve these exact logical blocks.  OpenQASM3 files
include a valid header; Qiskit 2.5 cannot export its `Diagonal` instruction as
OpenQASM3 without first decomposing it.
