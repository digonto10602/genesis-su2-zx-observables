"""Unit tests for the exact-dynamics lane (gate G2 support)."""
import json
import os

import numpy as np
import pytest

from su2qc.dynamics import engine, scan
from su2qc.ham.route_spinnet import build_hamiltonian

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.unit
def test_self_check():
    r = engine.self_check(4.0, 0.75, 0.5, 10.0)
    assert r["expm_krylov_dev"] <= 1e-9
    assert r["energy_drift"] <= 1e-10
    assert r["N_drift"] <= 1e-10


@pytest.mark.unit
def test_evolve_matches_expm():
    from scipy.linalg import expm
    H, b = build_hamiltonian(1.0, 0.2, 0.5)[:2]
    psi0 = np.zeros(82, complex)
    psi0[scan._idx(b, scan.STRETCHED)] = 1.0
    s = engine.evolve(H, psi0, np.array([0.0, 7.3]))
    ref = expm(-1j * H.toarray() * 7.3) @ psi0
    assert np.max(np.abs(s[-1] - ref)) <= 1e-12


@pytest.mark.unit
def test_term_split_is_exact():
    Hd, D, hs, B, basis = scan._term_split(4.0, 0.75)
    assert np.max(np.abs(D + sum(hs) + B - Hd)) <= 1e-13
    # each hopping block is Hermitian and off-diagonal
    for h in hs:
        assert np.max(np.abs(h - h.conj().T)) <= 1e-13
        assert np.max(np.abs(np.diag(h))) == 0.0


@pytest.mark.unit
def test_channel_masks_partition_N4_sector():
    _, b = build_hamiltonian(1.0, 0.1, 0.5)[:2]
    surv, mes, bb, oth = scan._classify(b)
    n4 = np.array([sum(l[1]) == 4 for l in b])
    assert int(n4.sum()) == 38
    assert np.all((surv + mes + bb + oth)[n4] == 1)
    assert int(surv.sum()) == 2 and int(mes.sum()) == 2


@pytest.mark.unit
def test_artifacts_and_window():
    res = json.load(open(os.path.join(RUN, "physics", "resonance.json")))
    assert res["n_mass_points"] >= 21 and res["n_g2_values"] >= 2
    assert os.path.exists(os.path.join(RUN, "analysis", "tables",
                                       "exact_mass_scan.csv"))
    w = json.load(open(os.path.join(RUN, "physics", "window.json")))
    assert w["r_max"] in (2, 3)
    v = scan.verify_window(w)
    assert v["strang_err"] <= 0.05
    assert v["psurv_drop"] >= 0.3 or w.get("shortfall_flagged")
    assert v["pair_weight"] >= 0.05 or w.get("shortfall_flagged")
