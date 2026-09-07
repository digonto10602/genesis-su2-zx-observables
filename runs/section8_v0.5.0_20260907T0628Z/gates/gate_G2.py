#!/usr/bin/env python
"""Gate G2: exact dynamics, resonance scan, window selection.

Reads artifacts produced by the dynamics builders and re-verifies the
critical numbers directly (expm vs Krylov, conservation, window criteria).
"""
import datetime
import json
import os
import sys

import numpy as np

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RUN, "src"))

crit = []


def check(name, target, value, ok):
    crit.append({"name": name, "target": target, "value": value, "pass": bool(ok)})
    print(("PASS " if ok else "FAIL "), name, "target", target, "value", value)


def main():
    from su2qc.dynamics import engine, scan

    # 1. expm vs Krylov and conservation at a reference point
    res = engine.self_check(g2=1.0, m=0.1875, jmax=0.5, t_max=10.0)
    check("expm_vs_krylov", "<=1e-9", res["expm_krylov_dev"],
          res["expm_krylov_dev"] <= 1e-9)
    check("energy_conservation", "<=1e-10", res["energy_drift"],
          res["energy_drift"] <= 1e-10)
    check("N_conservation", "<=1e-10", res["N_drift"], res["N_drift"] <= 1e-10)

    # 2. mass scan artifacts
    scan_path = os.path.join(RUN, "analysis", "tables", "exact_mass_scan.csv")
    check("mass_scan_table", "exists", os.path.exists(scan_path),
          os.path.exists(scan_path))
    summary = json.load(open(os.path.join(RUN, "physics", "resonance.json")))
    check("resonance_reported", "m*/g2 recorded vs 3/16",
          summary.get("mstar_over_g2"), "mstar_over_g2" in summary)
    npts = summary.get("n_mass_points", 0)
    check("mass_scan_points", ">=21", npts, npts >= 21)
    ng2 = summary.get("n_g2_values", 0)
    check("g2_values", ">=2", ng2, ng2 >= 2)

    # 3. time-series tables at m*
    ts = os.path.join(RUN, "analysis", "tables", "exact_timeseries.csv")
    check("timeseries_table", "exists", os.path.exists(ts), os.path.exists(ts))

    # 4. truncation error
    tr = os.path.join(RUN, "physics", "truncation_error.md")
    check("truncation_error_doc", "exists", os.path.exists(tr), os.path.exists(tr))
    trj = json.load(open(os.path.join(RUN, "physics", "truncation_error.json")))
    check("truncation_max_dprob", "reported (<=0.1 preferred)",
          trj.get("max_abs_dprob"), "max_abs_dprob" in trj)

    # 5. window
    wpath = os.path.join(RUN, "physics", "window.json")
    ok_w = os.path.exists(wpath)
    check("window_exists", "exists", ok_w, ok_w)
    if ok_w:
        w = json.load(open(wpath))
        for key in ("g2", "m", "dt", "r_max"):
            check(f"window_{key}", "present", w.get(key), key in w)
        check("window_rmax", "in {2,3}", w.get("r_max"), w.get("r_max") in (2, 3))
        # re-verify window criteria from the exact engine
        v = scan.verify_window(w)
        check("window_Psurv_drop", ">=0.3 (or shortfall flagged)",
              v["psurv_drop"], v["psurv_drop"] >= 0.3 or w.get("shortfall_flagged", False))
        check("window_pair_weight", ">=0.05 (or shortfall flagged)",
              v["pair_weight"], v["pair_weight"] >= 0.05 or w.get("shortfall_flagged", False))
        check("window_strang_err", "<=0.05", v["strang_err"], v["strang_err"] <= 0.05)

    signoff = os.path.join(RUN, "physics", "signoff_G2.md")
    check("physics_signoff", "exists", os.path.exists(signoff), os.path.exists(signoff))

    status = "PASS" if all(c["pass"] for c in crit) else "FAIL"
    out = {"gate": "G2", "status": status,
           "attempt": int(os.environ.get("G2_ATTEMPT", "1")),
           "finished": datetime.datetime.utcnow().isoformat() + "Z",
           "mode": "n/a", "criteria": crit,
           "signoff": {"physics": "physics/signoff_G2.md"},
           "artifacts": ["analysis/tables/", "physics/window.json"], "notes": ""}
    with open(os.path.join(RUN, "gates", "GATE_G2.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
