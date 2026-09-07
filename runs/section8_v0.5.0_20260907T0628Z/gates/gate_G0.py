#!/usr/bin/env python
"""Gate G0: bootstrap complete."""
import json, os, subprocess, sys, datetime
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(RUN))
crit = []
def check(name, ok, target, value):
    crit.append({"name": name, "target": target, "value": value, "pass": bool(ok)})
for f in ["run/T0","run/PROMPT_HASH","run/CONFIG_ENV.md","run/INVENTORY.md","run/MODELS.md",
          "run/PLAN.md","run/TASKBOARD.md","run/GATES.md","run/DECISIONS.md",
          "reports/REPORT.md","src/su2qc/conventions.py","env/requirements.lock.txt"]:
    p = os.path.join(RUN, f); check(f, os.path.exists(p) and os.path.getsize(p) > 0, "exists", os.path.exists(p))
py = os.path.join(ROOT, ".mamba/envs/su2zx/bin/python")
r = subprocess.run([py, "-c", "from qiskit_ibm_runtime.fake_provider import FakeTorino; b=FakeTorino(); print(b.num_qubits)"], capture_output=True, text=True)
check("fake_heron_loads", r.returncode == 0 and "133" in r.stdout, "FakeTorino loads", r.stdout.strip() or r.stderr[-200:])
r2 = subprocess.run([py, "-m", "pytest", "--version"], capture_output=True, text=True)
check("pytest_runs", r2.returncode == 0, "pytest available", r2.stdout.strip().splitlines()[0] if r2.stdout else "fail")
status = "PASS" if all(c["pass"] for c in crit) else "FAIL"
out = {"gate":"G0","status":status,"attempt":1,"finished":datetime.datetime.utcnow().isoformat()+"Z",
       "mode":"n/a","criteria":crit,"artifacts":["run/","env/requirements.lock.txt"],"notes":"twin mode; FakeTorino target"}
json.dump(out, open(os.path.join(RUN,"gates/GATE_G0.json"),"w"), indent=1)
print(status); sys.exit(0 if status=="PASS" else 1)
