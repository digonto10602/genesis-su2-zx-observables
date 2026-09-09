"""Fast targeted verification of the R7 fix in su2qc.twin.twin (BUILD lane A).

Not the gate. Reduced shots on purpose; the committed gate test carries the
R8 shot counts (r=0 at 4000, r=1 at 1024).

Run:
  PYTHONPATH=runs/section8_v0.5.0_20260907T0628Z/src \
    .mamba/envs/su2zx/bin/python \
    runs/campaign_v060/sessions/c060_p0_20260909_5/tools/verify_twin_fix.py
"""
from __future__ import annotations

import json
import sys
import time

from qiskit import transpile

from su2qc.circuits.strang_l12 import full_circuit
from su2qc.twin import twin

SHOTS = 512
REPEATS = 5


def sig(counts):
    return tuple(sorted(counts.items()))


def main():
    t0 = time.time()
    out = {}
    ok = True

    # 1. seed derivation is deterministic and 31-bit
    a = twin.spawn_seeds(500, 5)
    b = twin.spawn_seeds(500, 5)
    c = twin.spawn_seeds(510, 5)
    out["spawn_seeds"] = {
        "seed500": a, "seed500_again": b, "seed510": c,
        "deterministic": a == b,
        "distinct_within": len(set(a)) == 5,
        "distinct_across_bases": not (set(a) & set(c)),
        "all_31_bit": all(0 <= s < 2 ** 31 for s in a + c),
        "no_adjacent_pairs": all(abs(a[i + 1] - a[i]) > SHOTS for i in range(4)),
    }
    ok &= all(v is True for k, v in out["spawn_seeds"].items()
              if isinstance(v, bool))

    # 2. physical_yield on empty input matches postselect
    py = twin.physical_yield({}, set())
    ps = twin.postselect({})
    out["empty_input"] = {"physical_yield": py, "postselect": [ps[0], ps[1]],
                          "agree": py == ps[1] == 0.0}
    ok &= out["empty_input"]["agree"]

    # 3. production twin, r = 0: caller state, distinctness, shift test
    sim = twin.twin_backend(seed=101)          # production path, not compact
    before = sim.options.seed_simulator
    isa = transpile(full_circuit(0), sim, optimization_level=0, seed_transpiler=101)
    meas = twin.add_measurements(isa)

    counts = twin.run_counts([meas] * REPEATS, SHOTS, 500, sim)
    meta = twin.run_counts_meta()
    after = sim.options.seed_simulator
    out["r0"] = {
        "shots": SHOTS,
        "distinct": len({sig(x) for x in counts}),
        "key_counts": [len(x) for x in counts],
        "meta": meta,
        "LAST_SEEDS": list(twin.LAST_SEEDS),
        "caller_seed_simulator_before": before,
        "caller_seed_simulator_after": after,
        "caller_unmutated": before == after,
    }
    ok &= out["r0"]["distinct"] == REPEATS
    ok &= out["r0"]["caller_unmutated"]
    ok &= meta["seeds"] == list(twin.LAST_SEEDS) == twin.spawn_seeds(500, REPEATS)

    # 4. reproducibility: same base seed -> same counts
    counts2 = twin.run_counts([meas] * REPEATS, SHOTS, 500, sim)
    out["reproducible"] = [sig(x) for x in counts] == [sig(y) for y in counts2]
    ok &= out["reproducible"]

    # 5. post-fix shift test on the spawned seeds (must be false)
    s0, s1 = twin.spawn_seeds(500, REPEATS)[:2]
    m0 = sim.run(meas, shots=SHOTS, seed_simulator=s0, memory=True).result().get_memory()
    m1 = sim.run(meas, shots=SHOTS, seed_simulator=s1, memory=True).result().get_memory()
    shift = sum(1 for i in range(SHOTS - 1) if m0[i + 1] == m1[i])
    same = sum(1 for i in range(SHOTS) if m0[i] == m1[i])
    out["shift_test_post_fix"] = {
        "seeds": [s0, s1], "shift_matches": shift, "same_index_matches": same,
        "shifted": m0[1:] == m1[:-1],
    }
    ok &= out["shift_test_post_fix"]["shifted"] is False
    # sanity: the old scheme's adjacent seeds still shift (mechanism intact)
    ma = sim.run(meas, shots=SHOTS, seed_simulator=500, memory=True).result().get_memory()
    mb = sim.run(meas, shots=SHOTS, seed_simulator=501, memory=True).result().get_memory()
    out["shift_test_old_scheme"] = {
        "seeds": [500, 501],
        "shift_matches": sum(1 for i in range(SHOTS - 1) if ma[i + 1] == mb[i]),
        "shifted": ma[1:] == mb[:-1],
    }

    # 6. equal-seed control through the real code path
    eq = [sim.run(meas, shots=SHOTS, seed_simulator=s0).result().get_counts()
          for _ in range(REPEATS)]
    out["equal_seed_control_distinct"] = len({sig(dict(x)) for x in eq})
    ok &= out["equal_seed_control_distinct"] == 1

    out["ok"] = bool(ok)
    out["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(out, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
