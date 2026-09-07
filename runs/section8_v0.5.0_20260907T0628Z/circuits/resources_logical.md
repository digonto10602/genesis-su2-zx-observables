# Logical resources, L12 encoding (before routing)

Window: g2=4.0, m=0.75, dt=0.8333, r_max=3.
Block unitaries synthesized with qiskit UnitaryGate on the numerically
found support (isometry-exact), transpiled to {cz, rz, sx, x} at
optimization_level=1, seed 7. Counts are the transpiler's generic
synthesis; G4 compiles/routes for the real target.

| circuit | support qubits | CZ count | 2q depth |
|---|---|---|---|
| group D (theta=0.4167) | 12 | 4094 | 4085 |
| group h0 (theta=0.4167) | 6 | 1004 | 993 |
| group h1 (theta=0.4167) | 6 | 1004 | 993 |
| group h2 (theta=0.4167) | 6 | 1004 | 993 |
| group h3 (theta=0.4167) | 6 | 1004 | 993 |
| group B (theta=0.8333) | 8 | 29655 | 29314 |
| one Strang step | 12 | 45875 | 45037 |
| full circuit r=0 (prep + steps, merged D) | 12 | 0 | 0 |
| full circuit r=1 (prep + steps, merged D) | 12 | 45875 | 45037 |
| full circuit r=2 (prep + steps, merged D) | 12 | 87656 | 85989 |
| full circuit r=3 (prep + steps, merged D) | 12 | 129437 | 126941 |

Budget reference (prompt §0.1): ~250 CZ per Strang step, ~1000 per
circuit, 2q depth < ~200. Compare after routing in compile/resources_routed.md.
