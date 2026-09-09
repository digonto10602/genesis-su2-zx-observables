"""Pre-fix V10 baseline on the real L12 circuit, using the ORIGINAL run_counts.

Runs against the untouched sandbox copy of the v0.5.0 package so the working
tree's repaired module is not involved and no historical file is written.
This is the "would have failed on the old code" evidence R8(e) asks for.
"""
import json, sys, time
sys.path.insert(0, ".work/c060_p0_20260909_5_sandbox/section8/src")

from qiskit import transpile  # noqa: E402
from su2qc.circuits.strang_l12 import full_circuit  # noqa: E402
from su2qc.twin import twin  # noqa: E402

R_SHOTS = {0: 4000, 1: 1024}


def repeats(r, shots, seed=500):
    sim = twin.twin_backend(seed=101)          # production path, not compact
    isa = transpile(full_circuit(r), sim, optimization_level=0, seed_transpiler=101)
    measured = twin.add_measurements(isa)
    return twin.run_counts([measured] * 5, shots, seed, sim)


def main():
    out = {"code": "pre-fix (seed + k), sandbox copy", "path": "AerSimulator.from_backend"}
    for r, shots in R_SHOTS.items():
        t0 = time.time()
        counts = repeats(r, shots)
        distinct = len({tuple(sorted(c.items())) for c in counts})
        out[str(r)] = {"shots": shots, "distinct_dictionaries": distinct,
                       "repeat_sizes": [len(c) for c in counts],
                       "seconds": round(time.time() - t0, 1)}
        print(json.dumps({str(r): out[str(r)]}), flush=True)
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
