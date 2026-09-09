"""Fallback: measure the V10 twin row at a reduced shot count, outside the gate.

Used only if the gate's r=1 measurement cannot complete inside the session's
time budget. It does NOT touch the committed gate test, which keeps R8's shot
counts; the reduction lives here and is named in the output so the ledger row
can carry the deviation instead of hiding it.

Usage: python twin_row_reduced.py <shots_r1> [shots_r0]
"""
import json, sys, time
from pathlib import Path

sys.path.insert(0, "runs/section8_v0.5.0_20260907T0628Z/src")
from qiskit import transpile  # noqa: E402
from su2qc.circuits.strang_l12 import full_circuit  # noqa: E402
from su2qc.twin import twin  # noqa: E402

SESSION = Path("runs/campaign_v060/sessions/c060_p0_20260909_5")
REPEATS = 5
BASE_SEED = {0: 500, 1: 510}
R8_SHOTS = {0: 4000, 1: 1024}


def measure(r, shots):
    t0 = time.time()
    sim = twin.twin_backend(seed=101)
    meas = twin.add_measurements(
        transpile(full_circuit(r), sim, optimization_level=0, seed_transpiler=101))
    counts = twin.run_counts([meas] * REPEATS, shots, BASE_SEED[r], sim)
    kept = [twin.postselect(c) for c in counts]
    mean, two_sigma, y = twin.bootstrap(counts, n_boot=2000, seed=77)
    return {
        "r": r, "shots": shots, "r8_shots": R8_SHOTS[r],
        "shots_reduced": shots != R8_SHOTS[r],
        "seeds": list(twin.LAST_SEEDS),
        "distinct_dictionaries": len({tuple(sorted(c.items())) for c in counts}),
        "N_kept_mean": sum(sum(k.values()) for k, _ in kept) / REPEATS,
        "yield_mean": y,
        "two_sigma": two_sigma,
        "mean": mean,
        "seconds": round(time.time() - t0, 1),
    }


def main():
    shots1 = int(sys.argv[1]) if len(sys.argv) > 1 else 256
    shots0 = int(sys.argv[2]) if len(sys.argv) > 2 else R8_SHOTS[0]
    out = {
        "note": "Fallback measurement outside the gate. The committed gate test still "
                "carries R8's shot counts; this file exists only because the r=1 "
                "measurement at 1024 shots did not complete inside the time budget.",
        "deviation_from_R8": f"r=1 measured at {shots1} shots instead of {R8_SHOTS[1]}",
        "0": measure(0, shots0),
        "1": measure(1, shots1),
    }
    (SESSION / "twin-row-reduced.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: (v if k in ("note", "deviation_from_R8")
                          else {kk: v[kk] for kk in ("shots", "distinct_dictionaries",
                                                     "N_kept_mean", "seconds")})
                      for k, v in out.items()}, indent=2))


if __name__ == "__main__":
    main()
