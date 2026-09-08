import json
import subprocess
from pathlib import Path


def _repo():
    return Path(__file__).resolve().parents[4]


def _head_bytes(path):
    return subprocess.check_output(["git", "show", f"HEAD:{path}"])


def test_v1_restored_evidence_and_conditioned_slopes():
    repo = _repo()
    rel = "runs/section8_v0.5.0_20260907T0628Z/circuits/trotter_scaling.json"
    current = (repo / rel).read_bytes()
    assert current == _head_bytes(rel)
    values = json.loads(current)
    conditioning = json.loads(
        (repo / "runs/campaign_v060/sessions/c060_p0_20260907/slope-conditioning.json").read_text()
    )
    for row in conditioning:
        name = row["observable"]
        assert abs(row["measured_slope_delta"]) <= 10 * row["propagated_abs_bound"]
        assert -2.3 <= values[f"slope_{name}"] <= -1.7
    assert values["slope_Psurv"] == values["slope_Psurv"]
