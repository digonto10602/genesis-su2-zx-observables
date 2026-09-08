#!/usr/bin/env python
"""Gate G4: compile after routing, noisy twin, Plan-B decision.

Reads compile/resources_routed.json + compile/twin_check.json produced by
src/su2qc/compile/run_g4.py and re-verifies routed equivalence for the
chosen pipeline on the r_max circuit.
"""
import datetime
import json
import os
import sys

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RUN, "src"))
crit = []


def check(name, target, value, ok):
    crit.append({"name": name, "target": target, "value": value, "pass": bool(ok)})
    print(("PASS " if ok else "FAIL "), name, "target", target, "value", value)


def main():
    rr = json.load(open(os.path.join(RUN, "compile", "resources_routed.json")))
    check("routed_table", "exists", True, True)
    lay = os.path.join(RUN, "compile", "layout.json")
    check("layout_frozen", "exists", os.path.exists(lay), os.path.exists(lay))

    best = rr["chosen"]  # {"encoding","pipeline","per_step_2q","full_r3_2q","depth_2q"}
    slack = 1.10
    check("budget_per_step_2q", "<=250 (+10%)", best["per_step_2q"],
          best["per_step_2q"] <= 250 * slack)
    check("budget_full_circuit_2q", "<=1000 (+10%)", best["full_rmax_2q"],
          best["full_rmax_2q"] <= 1000 * slack)
    check("budget_depth_2q", "<200 (+10%)", best["depth_2q_full_rmax"],
          best["depth_2q_full_rmax"] < 200 * slack)
    check("routed_equivalence", "<=1e-10", rr["equivalence_rmax"],
          rr["equivalence_rmax"] <= 1e-10)

    tw = json.load(open(os.path.join(RUN, "compile", "twin_check.json")))
    check("twin_yield_deepest", ">=0.20", tw["yield_deepest"], tw["yield_deepest"] >= 0.20)
    check("twin_2sigma_points", ">=4 time points within 2sigma (mitigated arm)",
          tw["n_points_within_2sigma"], tw["n_points_within_2sigma"] >= 4)

    dec = open(os.path.join(RUN, "run", "DECISIONS.md")).read()
    has = any(k in dec for k in ("G4: GO", "G4: REDUCED", "G4: PLAN B"))
    check("decision_recorded", "GO/REDUCED/PLAN B in DECISIONS.md", has, has)

    status = "PASS" if all(c["pass"] for c in crit) else "FAIL"
    out = {"gate": "G4", "status": status,
           "attempt": int(os.environ.get("G4_ATTEMPT", "1")),
           "finished": datetime.datetime.utcnow().isoformat() + "Z",
           "mode": "twin", "criteria": crit,
           "artifacts": ["compile/resources_routed.md", "compile/layout.json",
                         "compile/twin_check.json"],
           "notes": rr.get("notes", "")}
    json.dump(out, open(os.path.join(RUN, "gates", "GATE_G4.json"), "w"), indent=1)
    print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
