"""V1 regression (R1 + R10): Trotter-slope conditioning on this session's evidence.

R10 requires that the V1 row cite evidence produced *by this session*.  The test
therefore does all of the following itself, and never reads a conditioning file
written by an earlier session:

1. Byte-identity of the committed G3 artifact `circuits/trotter_scaling.json`
   against `git show HEAD:<path>`.
2. A sandbox rerun, entirely in memory, of the primary error arrays that the G3
   suite fits (the `test_l12.py::test_trotter_scaling` computation), giving the
   primary deltas required by R1.
3. The three log-slopes refitted from both the committed and the rerun arrays.
4. The first-order propagated conditioning bound, computed here from the primary
   deltas with centered log-r weights over r = 8...128 (sum of squared weights
   4.80), per R1.
5. `sessions/<tag>/slope-conditioning.json` written under THIS session's
   directory, carrying the measured ratio |dslope| / bound per observable so the
   gatekeeper can see the remaining headroom rather than only a boolean.

Thresholds (R1, verbatim, not relaxed here):
  * primary quantities (the error arrays): 1e-12 absolute;
  * the derived log-slopes: |dslope| <= 10 x propagated bound, AND inside the
    G3 band [-2.3, -1.7].
The historical 1e-12 slope criterion is deliberately NOT asserted -- R1 records
it as ill-posed for a log-slope -- but the per-observable `ratio_to_bound` and
`stability_1e_12` fields are written to the JSON so nothing is hidden.

Everything under runs/section8_v0.5.0_20260907T0628Z/ is committed historical
evidence: this test only reads it.  The rerun is held in memory and the only
file written is under this session's directory.
"""

import json
import math
import subprocess
from pathlib import Path

import numpy as np

# --- repository-anchored paths -------------------------------------------------
# Every file access AND the git subprocess cwd go through this helper, so the
# test does not depend on the pytest process working directory.

SESSION_TAG = "c060_p0_20260909_5"
G3_RUN_REL = "runs/section8_v0.5.0_20260907T0628Z"
TROTTER_REL = f"{G3_RUN_REL}/circuits/trotter_scaling.json"
SESSION_REL = f"runs/campaign_v060/sessions/{SESSION_TAG}"

# R1: centered log-r weights over r = 8...128, sum of squared weights 4.80.
R_GRID = (8, 16, 32, 64, 128)
SUM_W2_EXPECTED = 4.80
PRIMARY_ABS = 1.0e-12
SLOPE_BAND = (-2.3, -1.7)
SLOPE_BOUND_FACTOR = 10.0


def repo_root() -> Path:
    """Repository root, derived from this file's location (never from cwd)."""
    return Path(__file__).resolve().parents[4]


def repo_path(rel: str) -> Path:
    return repo_root() / rel


def head_bytes(rel: str) -> bytes:
    """`git show HEAD:<rel>` run with cwd pinned to the repository root.

    The cwd argument is what makes this consistent with repo_path(): without it
    the subprocess would resolve HEAD from whatever directory pytest happened to
    be started in, while the file read is repository-anchored.
    """
    return subprocess.check_output(
        ["git", "show", f"HEAD:{rel}"], cwd=str(repo_root())
    )


# --- fit and propagation -------------------------------------------------------


def centered_log_weights(rs):
    """w_i = log r_i - mean(log r).  Sum of w^2 is the R1 conditioning constant."""
    lr = np.log(np.asarray(rs, dtype=float))
    return lr - lr.mean()


def log_slope(rs, errs):
    """Least-squares slope of log(err) on log(r) -- the same fit G3 uses."""
    return float(np.polyfit(np.log(np.asarray(rs, float)),
                            np.log(np.asarray(errs, float)), 1)[0])


def propagate(rs, errs, deltas):
    """First-order propagation of primary error-array deltas onto the slope.

    slope = sum_i w_i log(e_i) / sum_i w_i^2, so d slope / d e_i = w_i / (S2 e_i).
    Returns (signed predicted delta, absolute bound = sum of |contributions|).
    """
    w = centered_log_weights(rs)
    s2 = float((w ** 2).sum())
    e = np.asarray(errs, float)
    d = np.asarray(deltas, float)
    contrib = w * d / (s2 * e)
    return float(contrib.sum()), float(np.abs(contrib).sum())


# --- in-memory rerun of the primary error arrays -------------------------------


def rerun_error_arrays(rs):
    """Recompute the G3 Trotter error arrays in memory.

    This is the `test_l12.py::test_trotter_scaling` computation with the JSON
    write removed: the historical run directory must never be written to by this
    test, so the rerun result is kept in memory only.
    """
    from scipy.linalg import expm
    from su2qc.circuits import strang_l12 as sl
    from su2qc.dynamics.scan import _classify, _diagnostics

    p = sl.params()
    g2, m, dt, r_max = p["g2"], p["m"], p["dt"], p["r_max"]
    basis, T = sl.terms(g2, m)
    t_tot = r_max * dt
    i0 = basis.index(sl.STRETCHED)
    psi0 = np.zeros(len(basis), complex)
    psi0[i0] = 1.0
    surv = _classify(basis)[0]
    e2m, _ = _diagnostics(basis)
    ex = expm(-1j * T["H"] * t_tot) @ psi0
    pe = np.abs(ex) ** 2

    out = {"t": t_tot, "err_Psurv": [], "err_E2": [], "err_state": []}
    for r in rs:
        U = sl.exact_strang_matrix(t_tot / r, g2, m)
        psi = psi0.copy()
        for _ in range(r):
            psi = U @ psi
        pr = np.abs(psi) ** 2
        out["err_Psurv"].append(abs(pr @ surv - pe @ surv))
        out["err_E2"].append(float(np.max(np.abs(pr @ e2m - pe @ e2m))))
        out["err_state"].append(float(np.linalg.norm(psi - ex)))
    return out


# --- the test ------------------------------------------------------------------


def test_v1_restored_evidence_and_conditioned_slopes():
    repo = repo_root()
    current = repo_path(TROTTER_REL).read_bytes()

    # NOTE (false-failure hazard, deliberately explicit): this same file is
    # rewritten by the legacy G3 suite -- runs/section8_v0.5.0_20260907T0628Z/
    # tests/test_l12.py::test_trotter_scaling dumps it into the run directory on
    # every execution.  Running the legacy suite in this working tree before the
    # C0 gate therefore turns a routine evidence regeneration into a spurious C0
    # failure here.  The fix is `git checkout -- <path>`, not a change to this
    # assertion.
    assert current == head_bytes(TROTTER_REL), (
        f"{TROTTER_REL} differs from `git show HEAD:{TROTTER_REL}`. This file is "
        "ALSO written by the legacy suite "
        f"({G3_RUN_REL}/tests/test_l12.py::test_trotter_scaling), so running the "
        "legacy suite in this tree before the gate rewrites the committed "
        "evidence and turns an evidence regeneration into a FALSE C0 failure. "
        "Restore it with `git checkout -- " + TROTTER_REL + "` and rerun; do not "
        "weaken this assertion."
    )

    committed = json.loads(current)
    rs = tuple(committed["r"])
    assert rs == R_GRID, ("R1 conditioning is defined on r = 8...128", rs)

    w = centered_log_weights(rs)
    s2 = float((w ** 2).sum())
    assert math.isclose(s2, SUM_W2_EXPECTED, rel_tol=2e-3), (
        "centered log-r weights must reproduce the R1 constant 4.80", s2
    )

    rerun = rerun_error_arrays(rs)

    rows = []
    for name in ("Psurv", "E2", "state"):
        key = f"err_{name}"
        e_committed = [float(x) for x in committed[key]]
        e_rerun = [float(x) for x in rerun[key]]
        deltas = [b - a for a, b in zip(e_committed, e_rerun)]

        refit_committed = log_slope(rs, e_committed)
        refit_rerun = log_slope(rs, e_rerun)
        stored = float(committed[f"slope_{name}"])

        predicted, bound = propagate(rs, e_committed, deltas)
        measured = refit_rerun - refit_committed
        ratio = (abs(measured) / bound) if bound > 0.0 else 0.0

        rows.append({
            "observable": name,
            "r": list(rs),
            "sum_w_squared": s2,
            "slope_stored": stored,
            "refit_committed": refit_committed,
            "refit_rerun": refit_rerun,
            "refit_abs_delta": abs(refit_committed - stored),
            "error_array_deltas": deltas,
            "max_error_array_delta": max(abs(d) for d in deltas),
            "primary_abs_threshold": PRIMARY_ABS,
            "primary_pass": max(abs(d) for d in deltas) <= PRIMARY_ABS,
            "propagated_abs_bound": bound,
            "predicted_slope_delta": predicted,
            "measured_slope_delta": measured,
            # Headroom, shown rather than hidden: ratio_to_bound is the fraction
            # of the 1x propagated bound consumed; ratio_to_band the fraction of
            # the R1 acceptance band (10x bound).  0.0 when the bound is exactly
            # zero because the rerun reproduced the committed arrays bit for bit.
            "ratio_to_bound": ratio,
            "ratio_to_band": ratio / SLOPE_BOUND_FACTOR,
            "bound_factor": SLOPE_BOUND_FACTOR,
            "band": list(SLOPE_BAND),
            "band_pass": SLOPE_BAND[0] <= stored <= SLOPE_BAND[1],
            # Recorded for transparency only. R1 replaced this criterion for a
            # log-slope and this test does NOT assert it; see the module
            # docstring.
            "stability_1e_12": abs(measured) <= 1e-12,
        })

    out_dir = repo_path(SESSION_REL)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "slope-conditioning.json"
    out_path.write_text(json.dumps(rows, indent=2) + "\n")
    assert out_path.is_relative_to(repo)  # never outside the repository
    assert G3_RUN_REL not in str(out_path)  # never into historical evidence

    for row in rows:
        name = row["observable"]
        assert row["primary_pass"], (
            f"V1 primary quantity err_{name} drifted beyond {PRIMARY_ABS} "
            f"absolute: max delta {row['max_error_array_delta']!r}"
        )
        assert abs(row["measured_slope_delta"]) <= (
            SLOPE_BOUND_FACTOR * row["propagated_abs_bound"]
        ), (
            f"slope_{name}: |dslope| = {row['measured_slope_delta']!r} exceeds "
            f"{SLOPE_BOUND_FACTOR} x propagated bound "
            f"{row['propagated_abs_bound']!r} (ratio to 1x bound "
            f"{row['ratio_to_bound']!r}); see {out_path}"
        )
        assert row["band_pass"], (
            f"slope_{name} = {row['slope_stored']!r} is outside the G3 band "
            f"{SLOPE_BAND}"
        )
