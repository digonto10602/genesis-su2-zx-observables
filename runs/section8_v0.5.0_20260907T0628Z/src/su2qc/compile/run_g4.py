"""Phase 4 production: compile, route, PyZX comparison, twin run, decision inputs.

Writes compile/resources_routed.{md,json}, compile/layout.json,
compile/twin_check.json, analysis/tables/twin_timeseries.csv.
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, "src")
from qiskit import transpile  # noqa: E402
from su2qc.circuits import strang_l12 as sl  # noqa: E402
from su2qc.circuits import synth_l12 as sy  # noqa: E402
from su2qc.compile import route as rt  # noqa: E402
from su2qc.dynamics import scan  # noqa: E402
from su2qc.twin import twin  # noqa: E402

P = sl.params()
G2, M, DT, RMAX = P["g2"], P["m"], P["dt"], P["r_max"]
os.makedirs("compile", exist_ok=True)
t0 = time.time()
backend = rt.fake_heron()
NATIVE = ["cz", "rz", "sx", "x", "id"]


def n2(c):
    return sum(1 for i in c.data if i.operation.num_qubits == 2 and i.operation.name != "barrier")


def d2(c):
    return int(c.depth(lambda x: x.operation.num_qubits == 2))


# ---------------------------------------------------------------- pipelines
rows = []
isa_by_r = {}
layout = None
logical = {r: sy.synth_full_circuit(r) for r in range(RMAX + 1)}
step_logical = sy.synth_strang_step(DT, G2, M)

pipelines = {}
# Qiskit L3 (native synthesis + routing, seeded)
pipelines["qiskit_L3"] = lambda c: c
# PyZX passes are applied to the native-basis logical circuit before routing
def _zx(strategy):
    def f(c):
        flat = transpile(c, basis_gates=["cx", "rz", "sx", "x", "h", "s", "t", "tdg", "sdg"],
                         optimization_level=1, seed_transpiler=7)
        return rt.pyzx_pass(flat, strategy)
    return f
pipelines["pyzx_basic_TP"] = _zx("basic")
pipelines["pyzx_full_reduce"] = _zx("full_reduce")

results = {}
for name, pre in pipelines.items():
    try:
        pre_step = pre(step_logical)
        eq_step = rt.state_equivalence(sl.prep_stretched().compose(step_logical),
                                       sl.prep_stretched().compose(pre_step)) \
            if name != "qiskit_L3" else 0.0
        isa_step, lay = rt.route(pre_step, backend, opt=3, seed=7)
        per_step = {"n_2q": n2(isa_step), "depth_2q": d2(isa_step)}
        full = {}
        for r in range(RMAX + 1):
            pre_full = pre(logical[r]) if r else logical[r]
            isa, layr = rt.route(pre_full, backend, opt=3, seed=7,
                                 initial_layout=lay["initial_physical"])
            full[r] = {"n_2q": n2(isa), "depth_2q": d2(isa),
                       "layout": layr}
            if name == "qiskit_L3":
                isa_by_r[r] = isa
        eq_full = rt.routed_equivalence(logical[RMAX], isa) if name == "qiskit_L3" else None
        results[name] = {"pre_route_equiv_step": eq_step, "per_step": per_step,
                         "full": {str(r): {k: v for k, v in full[r].items() if k != "layout"}
                                  for r in full},
                         "routed_equiv_rmax": eq_full}
        if name == "qiskit_L3":
            layout = full[RMAX]["layout"]
        print(name, "step", per_step, "full r=%d" % RMAX, full[RMAX]["n_2q"], full[RMAX]["depth_2q"],
              "eq", eq_step, eq_full, f"{time.time()-t0:.0f}s", flush=True)
    except Exception as e:  # noqa: BLE001
        results[name] = {"error": repr(e)}
        print(name, "FAILED", repr(e), flush=True)

# routed equivalence of the chosen ISA circuits for every r (qiskit_L3)
eqs = {str(r): rt.routed_equivalence(logical[r], isa_by_r[r]) for r in range(RMAX + 1)}
print("routed equivalence per r:", eqs, flush=True)

best_name = "qiskit_L3"
best = results[best_name]
chosen = {"encoding": "L12", "pipeline": best_name,
          "per_step_2q": best["per_step"]["n_2q"],
          "full_rmax_2q": best["full"][str(RMAX)]["n_2q"],
          "depth_2q_full_rmax": best["full"][str(RMAX)]["depth_2q"]}
json.dump({"chosen": chosen, "pipelines": results, "equivalence_rmax": eqs[str(RMAX)],
           "equivalence_per_r": eqs, "backend": backend.name,
           "notes": "structured synthesis (Gray-path multi-controlled RX on minimal "
                    "control sets, exact 3x3 Givens blocks, phase-polynomial D)"},
          open("compile/resources_routed.json", "w"), indent=1)
json.dump({"backend": backend.name, "initial_physical": layout["initial_physical"],
           "final_index_layout": layout["final_index_layout"], "seed_transpiler": 7,
           "optimization_level": 3}, open("compile/layout.json", "w"), indent=1)

with open("compile/resources_routed.md", "w") as fh:
    fh.write("# Routed resources (FakeTorino, CZ-native), L12 structured synthesis\n\n")
    fh.write(f"Window g2={G2}, m={M}, dt={DT:.4f}, r_max={RMAX}. seed_transpiler=7, opt level 3.\n\n")
    fh.write("| pipeline | step CZ | step 2q-depth | full r=3 CZ | full r=3 2q-depth | pre-route equiv | routed equiv (r=3) |\n|---|---:|---:|---:|---:|---|---|\n")
    for nme, res in results.items():
        if "error" in res:
            fh.write(f"| {nme} | ERROR: {res['error']} |\n"); continue
        fh.write(f"| {nme} | {res['per_step']['n_2q']} | {res['per_step']['depth_2q']} | "
                 f"{res['full'][str(RMAX)]['n_2q']} | {res['full'][str(RMAX)]['depth_2q']} | "
                 f"{res['pre_route_equiv_step']:.1e} | {res['routed_equiv_rmax'] if res['routed_equiv_rmax'] is not None else 'n/a'} |\n")
    fh.write("\nBudget (prompt): ~250 CZ/step, ~1000 CZ/circuit, 2q depth < ~200 (+10% slack).\n")
    fh.write("Per-r routed CZ (qiskit_L3): " + ", ".join(
        f"r={r}: {results['qiskit_L3']['full'][str(r)]['n_2q']}" for r in range(RMAX + 1)) + "\n")

# ---------------------------------------------------------------- twin run
sim = twin.twin_backend(seed=101)
times = [r * DT for r in range(RMAX + 1)]
exact = scan.timeseries_at(G2, M, 0.5, np.array(times), tag="exact_at_window")
REPEATS, SHOTS = 5, 4000
rows_tw = []
n_within = 0
yields = {}
for r in range(RMAX + 1):
    meas = twin.add_measurements(isa_by_r[r])
    counts = twin.run_counts([meas] * REPEATS, SHOTS, 500 + 10 * r, sim)
    mean, two_sig, y = twin.bootstrap(counts, n_boot=300, seed=r)
    yields[r] = y
    ok_all = True
    for key, exv in (("P_surv", exact["P_surv"][r]), ("n_v3", exact["n"][r][2]),
                     ("E2_l1", exact["E2"][r][0])):
        within = abs(mean[key] - exv) <= max(two_sig[key], 1e-12)
        ok_all &= within
        rows_tw.append((r, times[r], key, exv, mean[key], two_sig[key], int(within), y))
    n_within += int(ok_all)
    print(f"twin r={r} t={times[r]:.3f} yield={y:.3f} P_surv twin={mean['P_surv']:.3f}±{two_sig['P_surv']:.3f} exact={exact['P_surv'][r]:.3f} within={ok_all}", flush=True)

os.makedirs("analysis/tables", exist_ok=True)
with open("analysis/tables/twin_timeseries.csv", "w") as fh:
    fh.write("r,t,observable,exact,twin_mean,twin_2sigma,within,yield\n")
    for row in rows_tw:
        fh.write(",".join(str(x) for x in row) + "\n")
json.dump({"yield_deepest": yields[RMAX], "yields": yields,
           "n_points_within_2sigma": n_within, "repeats": REPEATS, "shots": SHOTS,
           "mode": "twin", "backend": backend.name, "arm": "A0 (raw + post-selection)"},
          open("compile/twin_check.json", "w"), indent=1)
print("done", f"{time.time()-t0:.0f}s")
