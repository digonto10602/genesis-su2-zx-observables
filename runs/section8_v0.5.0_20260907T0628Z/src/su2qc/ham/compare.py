"""Verifier-owned comparison of the two independent Hamiltonian routes (G1).

Basis-independent checks:
  * sorted spectra at >= 5 coupling points (incl. m = 0),
  * observable time series from the stretched string on t in [0, 10].
Owned by the VERIFY lane; neither route builder edits this file.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, expm

SRC = Path(__file__).resolve().parents[2]
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

COUPLING_POINTS = [  # (g2, m), includes m = 0
    (1.0, 0.0),
    (1.0, 0.1875),   # tree-level resonance at g2=1
    (1.0, 0.5),
    (2.0, 0.375),
    (0.5, 0.2),
    (1.5, 1.0),
]

STRETCHED = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)
TIMES = np.linspace(0.0, 10.0, 21)


def _get_routes():
    from su2qc.ham import route_spinnet as r1
    from su2qc.ham import route_gausskernel as r2
    return r1, r2


def _norm_label(label):
    (js, ns) = label[0], label[1]
    return (tuple(float(j) for j in js), tuple(int(n) for n in ns))


def spectra_comparison(jmax=0.5, points=COUPLING_POINTS):
    """Max relative deviation of sorted spectra between routes per point."""
    r1, r2 = _get_routes()
    rows = []
    for g2, m in points:
        out1 = r1.build_hamiltonian(g2, m, jmax)
        out2 = r2.build_hamiltonian(g2, m, jmax)
        H1 = out1[0].toarray()
        H2 = out2[0].toarray()
        e1 = np.sort(eigh(H1, eigvals_only=True))
        e2 = np.sort(eigh(H2, eigvals_only=True))
        scale = max(1.0, float(np.max(np.abs(e1))))
        dev = float(np.max(np.abs(e1 - e2)) / scale)
        rows.append({"g2": g2, "m": m, "max_rel_dev": dev,
                     "dim1": H1.shape[0], "dim2": H2.shape[0]})
    return rows


def _observables(route_mod, H, basis, psi0_index, times):
    """Time series of P_surv, n_v, E2_l from basis state psi0_index."""
    from su2qc import conventions as cv
    dim = H.shape[0]
    psi = np.zeros(dim, dtype=complex)
    psi[psi0_index] = 1.0
    # channel masks from labels (basis-independent definition)
    q = np.array([[cv.charge(v, int(lab[1][v])) for v in range(4)] for lab in basis])
    surv_mask = np.all(q == np.array([1, -1, 0, 0]), axis=1)
    e2 = np.array([[cv.casimir(float(lab[0][l])) for l in range(4)] for lab in basis])
    nmat = np.array([[int(lab[1][v]) for v in range(4)] for lab in basis])
    dt = times[1] - times[0]
    U = expm(-1j * H * dt)
    series = []
    for i, t in enumerate(times):
        p = np.abs(psi) ** 2
        series.append(
            {"t": float(t),
             "P_surv": float(p @ surv_mask),
             "n": (p @ nmat).tolist(),
             "E2": (p @ e2).tolist()})
        psi = U @ psi
    return series


def time_series_comparison(g2=1.0, m=0.1875, jmax=0.5, times=TIMES):
    """Max abs deviation of stretched-string observables between routes."""
    r1, r2 = _get_routes()
    out1 = r1.build_hamiltonian(g2, m, jmax)
    out2 = r2.build_hamiltonian(g2, m, jmax)
    H1, b1 = out1[0].toarray(), out1[1]
    H2, b2 = out2[0].toarray(), out2[1]
    tgt = _norm_label(STRETCHED)
    i1 = [k for k, lab in enumerate(b1) if _norm_label(lab) == tgt]
    i2 = [k for k, lab in enumerate(b2) if _norm_label(lab) == tgt]
    assert len(i1) == 1 and len(i2) == 1, (len(i1), len(i2))
    s1 = _observables(r1, H1, b1, i1[0], times)
    s2 = _observables(r2, H2, b2, i2[0], times)
    dev = 0.0
    for a, b in zip(s1, s2):
        dev = max(dev, abs(a["P_surv"] - b["P_surv"]))
        dev = max(dev, float(np.max(np.abs(np.array(a["n"]) - np.array(b["n"])))))
        dev = max(dev, float(np.max(np.abs(np.array(a["E2"]) - np.array(b["E2"])))))
    return dev, s1


if __name__ == "__main__":
    rows = spectra_comparison()
    for r in rows:
        print(r)
    dev, _ = time_series_comparison()
    print("time_series_max_abs_dev", dev)
