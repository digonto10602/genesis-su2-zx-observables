#!/usr/bin/env python
"""Gate G3: encodings, exact block unitaries, Strang circuits, Trotter, leakage.

Runs the G3 test suite (the criteria are the tests) and re-derives the headline
numbers for the JSON. Scope note: L12 only tonight (S8/C7 not built);
recorded as a partial criterion, not hidden.
"""
import datetime
import json
import os
import subprocess
import sys

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(os.path.dirname(os.path.dirname(RUN)), ".mamba", "envs",
                  "su2zx", "bin", "python")
sys.path.insert(0, os.path.join(RUN, "src"))
crit = []


def check(name, target, value, ok):
    crit.append({"name": name, "target": target, "value": value, "pass": bool(ok)})
    print(("PASS " if ok else "FAIL "), name, "target", target, "value", value)


def main():
    r = subprocess.run([PY, "-m", "pytest", "tests/test_l12.py", "-q",
                        "--no-header", "-p", "no:cacheprovider"],
                       cwd=RUN, capture_output=True, text=True)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:]
    check("l12_test_suite", "all pass", tail, r.returncode == 0)

    import numpy as np
    from scipy.linalg import expm
    from su2qc.circuits import strang_l12 as sl
    from su2qc.encodings import l12
    p = sl.params()
    basis, T = sl.terms(p["g2"], p["m"])
    check("l12_physical_codes", 82, len(l12.physical_codes()),
          len(l12.physical_codes()) == 82)
    check("s8_encoding", "built", "NOT BUILT (scope, see DECISIONS)", False)
    check("c7_encoding", "built", "NOT BUILT (scope, see DECISIONS)", False)

    # worst unitary dev over groups at theta=0.61 (direct, matrix-level)
    from qiskit.quantum_info import Statevector
    from qiskit import QuantumCircuit
    cb = sl.basis_to_code(basis)
    worst, leak = 0.0, 0.0
    for g in sl.GROUPS:
        qc = sl.unitary(g, 0.61, p["g2"], p["m"])
        Uex = expm(-1j * 0.61 * T[g])
        for j in range(0, 82, 9):  # subsample columns; suite does all
            prep = QuantumCircuit(12)
            for q in range(12):
                if (cb[j] >> q) & 1:
                    prep.x(q)
            prep.compose(qc, inplace=True)
            v = Statevector(prep).data
            worst = max(worst, float(np.max(np.abs(v[cb] - Uex[:, j]))))
            leak = max(leak, sl.leakage_prob(v))
    check("block_unitary_dev", "<=1e-12", worst, worst <= 1e-12)
    check("block_unitary_leak_prob", "<=1e-12", leak, leak <= 1e-12)

    v = Statevector(sl.full_circuit(p["r_max"])).data
    lp = sl.leakage_prob(v)
    check("noiseless_leakage_prob", "<=1e-14", lp, lp <= 1e-14)

    tj = os.path.join(RUN, "circuits", "trotter_scaling.json")
    ok = os.path.exists(tj)
    if ok:
        t = json.load(open(tj))
        check("trotter_slope_Psurv", "[-2.3,-1.7]", t["slope_Psurv"],
              -2.3 <= t["slope_Psurv"] <= -1.7)
        check("trotter_slope_E2", "[-2.3,-1.7]", t["slope_E2"],
              -2.3 <= t["slope_E2"] <= -1.7)
    else:
        check("trotter_scaling", "json exists", False, False)

    res = os.path.join(RUN, "circuits", "resources_logical.md")
    check("resources_logical", "exists", os.path.exists(res), os.path.exists(res))
    for r_ in range(4):
        for ext in ("qpy", "qasm"):
            f = os.path.join(RUN, "circuits", f"l12_r{r_}.{ext}")
            ok = os.path.exists(f) and os.path.getsize(f) > (50 if r_ == 0 else 200)
            check(f"export_l12_r{r_}_{ext}", "exists, non-trivial", ok, ok)

    core = [c for c in crit if not c["name"].startswith(("s8_", "c7_"))]
    status = "PASS" if all(c["pass"] for c in core) else "FAIL"
    out = {"gate": "G3", "status": status,
           "attempt": int(os.environ.get("G3_ATTEMPT", "1")),
           "finished": datetime.datetime.utcnow().isoformat() + "Z",
           "mode": "n/a", "criteria": crit,
           "signoff": {"code": "reviews/p3_strang_l12_1.md"},
           "artifacts": ["circuits/", "tests/test_l12.py"],
           "notes": "L12 primary encoding fully verified; S8 and C7 not built "
                    "(§4.4 G3 fallback: drop the failing/absent encodings; "
                    "recorded as FAIL criteria, excluded from PASS logic by "
                    "documented scope decision D4)."}
    json.dump(out, open(os.path.join(RUN, "gates", "GATE_G3.json"), "w"), indent=1)
    print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
