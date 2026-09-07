"""Run the full G2 production sequence and print a summary (OPS lane).

Operating point: g2 = 4.0, m = 3 g2/16 = 0.75 (tree-level resonance).
Rationale (physics/DISCREPANCIES.md): the W_bar-argmax estimator is
dominated by the BB-bar channel at small m and does not localize the
tree-level resonance; the breaking-time estimator argmin t_b does, at g2 >= 4
where the electric scale dominates hopping and the resonance is sharp.
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, "src")
from su2qc.dynamics import scan  # noqa: E402

G2_OP, M_OP = 4.0, 0.75

t0 = time.time()
res = scan.mass_scan()
print("mass_scan", json.dumps(res), f"{time.time()-t0:.0f}s", flush=True)

ts = scan.timeseries_at(G2_OP, M_OP, 0.5, np.linspace(0, 12, 121))
print("timeseries at op", G2_OP, M_OP, "min P_surv", float(ts["P_surv"].min()),
      "max P_meson", float(ts["P_meson"].max()),
      "max P_BBbar", float(ts["P_BBbar"].max()),
      "min dC", float(ts["E2"].sum(axis=1).min() - 2.25), flush=True)

tr = scan.truncation(G2_OP, M_OP)
print("truncation", tr, flush=True)

w = scan.select_window(G2_OP, M_OP)
print("window", json.dumps(w), flush=True)
print("verify", scan.verify_window(w), flush=True)
print("total", f"{time.time()-t0:.0f}s")
