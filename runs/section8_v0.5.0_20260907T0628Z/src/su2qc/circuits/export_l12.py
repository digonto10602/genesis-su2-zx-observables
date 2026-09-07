"""Write circuits/resources_logical.md and export L12 circuits (QPY + QASM3)."""
import os
import sys

sys.path.insert(0, "src")
from qiskit import qpy, transpile  # noqa: E402
from qiskit import qasm3  # noqa: E402
from su2qc.circuits import strang_l12 as sl  # noqa: E402

p = sl.params()
rows = []
for g in sl.GROUPS:
    th = p["dt"] if g == "B" else p["dt"] / 2
    r = sl.resources(sl.unitary(g, th, p["g2"], p["m"]))
    S = sl.supports(p["g2"], p["m"]).get(g, list(range(12)))
    rows.append((f"group {g} (theta={th:.4f})", len(S), r["n_2q"], r["depth_2q"]))
rs = sl.resources(sl.strang_step(p["dt"], p["g2"], p["m"]))
rows.append(("one Strang step", 12, rs["n_2q"], rs["depth_2q"]))
for r_ in range(0, p["r_max"] + 1):
    qc = sl.full_circuit(r_)
    rr = sl.resources(qc)
    rows.append((f"full circuit r={r_} (prep + steps, merged D)", 12,
                 rr["n_2q"], rr["depth_2q"]))
    t = transpile(qc, basis_gates=["cz", "rz", "sx", "x", "id"],
                  optimization_level=1, seed_transpiler=7)
    with open(f"circuits/l12_r{r_}.qpy", "wb") as fh:
        qpy.dump(t, fh)
    with open(f"circuits/l12_r{r_}.qasm", "w") as fh:
        fh.write(qasm3.dumps(t))

with open("circuits/resources_logical.md", "w") as fh:
    fh.write("# Logical resources, L12 encoding (before routing)\n\n")
    fh.write(f"Window: g2={p['g2']}, m={p['m']}, dt={p['dt']:.4f}, r_max={p['r_max']}.\n")
    fh.write("Block unitaries synthesized with qiskit UnitaryGate on the numerically\n"
             "found support (isometry-exact), transpiled to {cz, rz, sx, x} at\n"
             "optimization_level=1, seed 7. Counts are the transpiler's generic\n"
             "synthesis; G4 compiles/routes for the real target.\n\n")
    fh.write("| circuit | support qubits | CZ count | 2q depth |\n|---|---|---|---|\n")
    for name, s, n2, d2 in rows:
        fh.write(f"| {name} | {s} | {n2} | {d2} |\n")
    fh.write("\nBudget reference (prompt §0.1): ~250 CZ per Strang step, ~1000 per\n"
             "circuit, 2q depth < ~200. Compare after routing in compile/resources_routed.md.\n")
print(open("circuits/resources_logical.md").read())
