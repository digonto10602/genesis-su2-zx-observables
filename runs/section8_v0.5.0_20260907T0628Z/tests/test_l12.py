"""G3 tests: L12 encoding, exact block unitaries, Strang circuits, leakage."""
import json
import os

import numpy as np
import pytest
from scipy.linalg import expm

from su2qc.circuits import strang_l12 as sl
from su2qc.encodings import l12

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = sl.params()
G2, M, DT, RMAX = P["g2"], P["m"], P["dt"], P["r_max"]


@pytest.mark.unit
def test_encoding_roundtrip_and_flags():
    codes = l12.physical_codes()
    assert len(codes) == 82 and len(set(codes)) == 82
    for c in codes:
        assert l12.encode(l12.decode(c)) == c
        assert l12.is_physical(c)
    n_phys = sum(l12.is_physical(b) for b in range(4096))
    assert n_phys == 82
    # known state: stretched string
    code = l12.encode(sl.STRETCHED)
    assert code == 3793
    assert l12.decode(format(code, "012b")) == sl.STRETCHED


def _apply_on_codes(qc, basis):
    """Matrix of the circuit restricted to physical codes (82x82) and the
    leakage block (unphys x phys), via 82 statevector runs."""
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    cb = sl.basis_to_code(basis)
    codes = l12.physical_codes()
    mask = np.ones(4096, bool)
    mask[codes] = False
    Uphys = np.zeros((82, 82), complex)
    leak = 0.0
    for j, c in enumerate(cb):
        prep = QuantumCircuit(12)
        for q in range(12):
            if (c >> q) & 1:
                prep.x(q)
        prep.compose(qc, inplace=True)
        v = Statevector(prep).data
        Uphys[:, j] = v[cb]
        leak = max(leak, float(np.linalg.norm(v[mask])))
    return Uphys, leak


@pytest.mark.unit
@pytest.mark.parametrize("group", sl.GROUPS)
@pytest.mark.parametrize("theta", [0.13, 0.61])
def test_block_unitary_exact_and_leak_free(group, theta):
    basis, T = sl.terms(G2, M)
    qc = sl.unitary(group, theta, G2, M)
    Uphys, leak = _apply_on_codes(qc, basis)
    Uex = expm(-1j * theta * T[group])
    assert np.linalg.norm(Uphys - Uex) <= 1e-12
    assert leak <= 1e-12


@pytest.mark.unit
def test_full_strang_step_matches_exact_product():
    basis, T = sl.terms(G2, M)
    qc = sl.strang_step(DT, G2, M)
    Uphys, leak = _apply_on_codes(qc, basis)
    Uex = sl.exact_strang_matrix(DT, G2, M)
    assert np.linalg.norm(Uphys - Uex) <= 1e-10
    assert leak <= 1e-12
    # merged-D full circuit == unmerged
    from qiskit.quantum_info import Statevector
    a = Statevector(sl.full_circuit(2, merge_D=True)).data
    b = Statevector(sl.full_circuit(2, merge_D=False)).data
    assert np.max(np.abs(a - b)) <= 1e-12


@pytest.mark.unit
def test_noiseless_leakage_zero():
    from qiskit.quantum_info import Statevector
    from qiskit_aer import AerSimulator
    from qiskit import transpile
    qc = sl.full_circuit(RMAX)
    v = Statevector(qc).data
    assert sl.leakage_prob(v) <= 1e-14
    meas = qc.copy()
    meas.measure_all()
    sim = AerSimulator(seed_simulator=11)
    t = transpile(meas, sim, optimization_level=0)
    counts = sim.run(t, shots=10000).result().get_counts()
    flagged = sum(n for s, n in counts.items() if not l12.is_physical(s))
    assert flagged == 0


@pytest.mark.unit
def test_trotter_scaling():
    """Second-order scaling: error vs r at fixed t = RMAX*DT, r in 1..16."""
    from su2qc.dynamics.scan import _classify, _diagnostics
    basis, T = sl.terms(G2, M)
    t_tot = RMAX * DT
    i0 = basis.index(sl.STRETCHED)
    psi0 = np.zeros(82, complex)
    psi0[i0] = 1.0
    surv = _classify(basis)[0]
    e2m, _ = _diagnostics(basis)
    ex = expm(-1j * T["H"] * t_tot) @ psi0
    pe = np.abs(ex) ** 2
    rs = [8, 16, 32, 64, 128]
    errs_s, errs_e, errs_psi = [], [], []
    for r in rs:
        U = sl.exact_strang_matrix(t_tot / r, G2, M)   # matrix form, exact
        psi = psi0.copy()
        for _ in range(r):
            psi = U @ psi
        p = np.abs(psi) ** 2
        errs_s.append(abs(p @ surv - pe @ surv))
        errs_e.append(np.max(np.abs(p @ e2m - pe @ e2m)))
        errs_psi.append(float(np.linalg.norm(psi - ex)))
    fit = lambda e: float(np.polyfit(np.log(rs), np.log(e), 1)[0])
    slopes = {"Psurv": fit(errs_s), "E2": fit(errs_e), "state": fit(errs_psi)}
    json.dump({"r": rs, "t": t_tot, "err_Psurv": errs_s, "err_E2": errs_e,
               "err_state": errs_psi,
               "slope_Psurv": slopes["Psurv"], "slope_E2": slopes["E2"],
               "slope_state": slopes["state"]},
              open(os.path.join(RUN, "circuits", "trotter_scaling.json"), "w"),
              indent=1)
    for k, s in slopes.items():
        assert -2.3 <= s <= -1.7, (k, s, errs_s, errs_e, errs_psi)


@pytest.mark.unit
def test_window_strang_error():
    from su2qc.dynamics.scan import strang_error
    assert strang_error(G2, M, DT, RMAX) <= 0.05
