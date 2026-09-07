#!/usr/bin/env python
"""Gate G1: 82-state Hamiltonian by two independent routes + limit tests.

Deterministic; recomputes every criterion from the route modules directly.
"""
import datetime
import json
import os
import sys

import numpy as np
from scipy.linalg import eigh

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RUN, "src"))

crit = []


def check(name, target, value, ok):
    crit.append({"name": name, "target": target, "value": value, "pass": bool(ok)})
    print(("PASS " if ok else "FAIL "), name, "target", target, "value", value)


def main():
    from su2qc import conventions as cv
    from su2qc.ham import compare, route_gausskernel as r2, route_spinnet as r1

    # -- 1. dimensions ------------------------------------------------------
    for jmax, want in ((0.5, 82), (1.0, 152)):
        for tag, mod in (("route1", r1), ("route2", r2)):
            if tag == "route2" and jmax == 1.0:
                # route 2's jmax=1 statement is its Gauss-kernel dimension
                # (projected H at jmax=1 out of scope; run/DECISIONS.md).
                d = r2.kernel_dimension(1.0)
            else:
                H, basis = mod.build_hamiltonian(1.0, 0.1, jmax)[:2]
                d = H.shape[0]
            check(f"dim_{tag}_jmax{jmax}", want, d, d == want)

    # -- 2. fermion sectors (route1 labels; route2 checked via agreement) ---
    for tag, mod in (("route1", r1), ("route2", r2)):
        H, basis = mod.build_hamiltonian(1.0, 0.1, 0.5)[:2]
        Ns = [sum(int(n) for n in lab[1]) for lab in basis]
        dims = {N: Ns.count(N) for N in sorted(set(Ns))}
        check(f"sectors_{tag}", str(cv.EXPECTED_SECTOR_DIMS), str(dims),
              dims == cv.EXPECTED_SECTOR_DIMS)
        # [H, N] = 0
        Nop = np.diag(np.array(Ns, dtype=float))
        Hd = H.toarray()
        comm = np.max(np.abs(Hd @ Nop - Nop @ Hd))
        check(f"HN_commutator_{tag}", "<=1e-13", float(comm), comm <= 1e-13)
        herm = np.max(np.abs(Hd - Hd.conj().T))
        check(f"hermiticity_{tag}", "<=1e-13", float(herm), herm <= 1e-13)

    # -- 3. route agreement -------------------------------------------------
    rows = compare.spectra_comparison(jmax=0.5)
    worst = max(r["max_rel_dev"] for r in rows)
    check("route_spectra_rel_dev", "<=1e-12", worst, worst <= 1e-12)
    dev, _ = compare.time_series_comparison()
    check("route_time_series_dev", "<=1e-10", dev, dev <= 1e-10)

    # -- 4. Gauss law on the redundant space (route 2) ----------------------
    g = r2.gauss_commutator_norms(0.5)  # dict term -> max norm over v,a
    gworst = max(g.values())
    check("gauss_commutators", "<=1e-12", float(gworst), gworst <= 1e-12)

    # -- 5. limit tests -----------------------------------------------------
    from su2qc.ham import limits
    res = limits.pure_electric_check()
    check("pure_electric_degeneracies", "16,16,18,16,16",
          str(res["degeneracies"]), res["ok"])
    res = limits.frozen_matter_check()
    check("frozen_matter_H1_match", f"<=+{res['tol']}", res["dev"], res["ok"])
    res = limits.magnetic_off_check()
    check("magnetic_off_1d_chain", "<=1e-10", res["dev"], res["ok"])

    signoff = os.path.join(RUN, "physics", "signoff_G1.md")
    check("physics_signoff", "exists", os.path.exists(signoff), os.path.exists(signoff))

    status = "PASS" if all(c["pass"] for c in crit) else "FAIL"
    out = {"gate": "G1", "status": status,
           "attempt": int(os.environ.get("G1_ATTEMPT", "1")),
           "finished": datetime.datetime.utcnow().isoformat() + "Z",
           "mode": "n/a", "criteria": crit,
           "signoff": {"physics": "physics/signoff_G1.md"},
           "artifacts": ["src/su2qc/ham/", "tests/"],
           "notes": ""}
    with open(os.path.join(RUN, "gates", "GATE_G1.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
