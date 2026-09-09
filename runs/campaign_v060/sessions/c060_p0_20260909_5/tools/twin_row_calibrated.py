"""Measure the real per-shot cost of the r=1 twin, then run the largest
affordable V10 measurement. Prints progress as it goes.

R8 fixes r=1 at 1024 shots. That count proved unaffordable on this machine, so
this tool measures the per-shot cost instead of guessing it again, and records
the deviation rather than hiding it.
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
BUDGET_SECONDS = float(sys.argv[1]) if len(sys.argv) > 1 else 900.0


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def prepare(r):
    t0 = time.time()
    sim = twin.twin_backend(seed=101)
    isa = transpile(full_circuit(r), sim, optimization_level=0, seed_transpiler=101)
    meas = twin.add_measurements(isa)
    log(f"r={r}: prepared in {time.time()-t0:.1f}s, {isa.num_qubits} qubits, "
        f"depth {isa.depth()}, {len(isa.data)} ops")
    return sim, meas


def row(r, shots, sim, meas):
    t0 = time.time()
    counts = twin.run_counts([meas] * REPEATS, shots, BASE_SEED[r], sim)
    seconds = time.time() - t0
    kept = [twin.postselect(c) for c in counts]
    mean, two_sigma, y = twin.bootstrap(counts, n_boot=2000, seed=77)
    out = {
        "r": r, "shots": shots, "repeats": REPEATS,
        "seeds": list(twin.LAST_SEEDS),
        "distinct_dictionaries": len({tuple(sorted(c.items())) for c in counts}),
        "key_counts": [len(c) for c in counts],
        "N_kept_mean": sum(sum(k.values()) for k, _ in kept) / REPEATS,
        "yield_mean": y, "two_sigma": two_sigma, "mean": mean,
        "seconds": round(seconds, 1),
    }
    log(f"r={r}: {shots} shots x {REPEATS} in {seconds:.1f}s, "
        f"distinct={out['distinct_dictionaries']}, N_kept_mean={out['N_kept_mean']:.1f}")
    return out


def main():
    result = {"budget_seconds": BUDGET_SECONDS}
    sim0, meas0 = prepare(0)
    result["0"] = row(0, 4000, sim0, meas0)

    sim1, meas1 = prepare(1)
    log("r=1: calibrating with 1 repeat x 4 shots")
    t0 = time.time()
    twin.run_counts([meas1], 4, BASE_SEED[1], sim1)
    per_shot = (time.time() - t0) / 4
    log(f"r=1: measured {per_shot:.2f} s per shot")
    affordable = max(8, int(BUDGET_SECONDS / (per_shot * REPEATS)))
    log(f"r=1: budget {BUDGET_SECONDS:.0f}s -> {affordable} shots per repeat")
    result["r1_calibration"] = {
        "seconds_per_shot": round(per_shot, 3), "chosen_shots": affordable,
        "r8_shots": 1024,
        "r8_projected_hours": round(per_shot * 1024 * REPEATS / 3600.0, 2)}
    result["1"] = row(1, affordable, sim1, meas1)
    result["deviation_from_R8"] = (
        f"r=1 measured at {affordable} shots instead of R8's 1024; at the measured "
        f"{per_shot:.2f} s per shot, R8's count needs about "
        f"{per_shot*1024*REPEATS/3600.0:.1f} hours on this machine.")
    (SESSION / "twin-row-calibrated.json").write_text(json.dumps(result, indent=2) + "\n")
    log("written twin-row-calibrated.json")


if __name__ == "__main__":
    main()
