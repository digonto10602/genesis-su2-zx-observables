"""Mass scan / resonance finder, truncation comparison, Trotter-window selector.

Rewritten by the OPS lane after the delegated builder timed out (partial file);
classification bugs fixed: P_surv is the EXACT charge pattern (+1,-1,0,0), not
a sorted-|q| match.
"""

import json
import os

import numpy as np
from scipy.linalg import expm

import su2qc.conventions as cv
from su2qc.dynamics.engine import evolve
from su2qc.ham.route_spinnet import (build_hamiltonian,
                                     build_hamiltonian_no_magnetic)

RUN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

STRETCHED = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)
SHORT = ((0.5, 0.0, 0.0, 0.0), (1, 1, 0, 2), 0)


def _idx(basis, label):
    for i, lab in enumerate(basis):
        if lab == label:
            return i
    raise KeyError(label)


def _classify(basis):
    """Per-state channel masks: surv, meson, BBbar, other (within N=4)."""
    dim = len(basis)
    surv = np.zeros(dim)
    meson = np.zeros(dim)
    bbbar = np.zeros(dim)
    other = np.zeros(dim)
    for i, (jt, nt, _) in enumerate(basis):
        q = tuple(nt[v] - cv.N_VAC[v] for v in range(4))
        if any(abs(x) == 2 for x in q):
            bbbar[i] = 1
        elif q == (1, -1, 0, 0):
            surv[i] = 1
        elif all(abs(x) == 1 for x in q):
            meson[i] = 1
        elif sum(nt) == 4:
            other[i] = 1
    return surv, meson, bbbar, other


def _diagnostics(basis):
    e2 = np.array([[cv.casimir(lab[0][l]) for l in range(4)] for lab in basis])
    nv = np.array([[lab[1][v] for v in range(4)] for lab in basis])
    return e2, nv


def channel_probs(basis, states):
    surv, meson, bbbar, other = _classify(basis)
    p = np.abs(states) ** 2
    return p @ surv, p @ meson, p @ bbbar, p @ other


# ---------------------------------------------------------------- mass scan

def mass_scan(g2_values=(1.0, 2.0, 4.0, 8.0), n_m=25, t_window=(0.0, 40.0),
              jmax=0.5):
    """Scan m in [0, g2/2] for each g2. Two resonance estimators are recorded:
    argmax of W_bar (prompt criterion 2) and argmin of t_b (breaking time);
    see physics/DISCREPANCIES.md for why they differ at strong coupling."""
    tables = os.path.join(RUN_DIR, "analysis", "tables")
    physics = os.path.join(RUN_DIR, "physics")
    os.makedirs(tables, exist_ok=True)
    rows = []
    mstar = {}
    mstar_tb = {}
    t_eval = np.linspace(t_window[0], t_window[1], 401)
    for g2 in g2_values:
        m_vals = np.linspace(0.0, 0.5 * g2, n_m)
        wbar = []
        tbs = []
        for m in m_vals:
            H, basis = build_hamiltonian(g2, m, jmax)[:2]
            psi0 = np.zeros(H.shape[0], complex)
            psi0[_idx(basis, STRETCHED)] = 1.0
            states = evolve(H, psi0, t_eval)
            ps, pm, pb, po = channel_probs(basis, states)
            drop = np.where(ps <= 0.5)[0]
            t_b = t_eval[drop[0]] if len(drop) else t_eval[np.argmin(ps)]
            W = np.trapezoid(pm + pb, t_eval) / (t_eval[-1] - t_eval[0])
            wbar.append(W)
            tbs.append(t_b)
            rows.append((g2, m, t_b, W,
                         np.trapezoid(pm, t_eval) / (t_eval[-1] - t_eval[0]),
                         np.trapezoid(pb, t_eval) / (t_eval[-1] - t_eval[0])))
        mstar[str(g2)] = float(m_vals[int(np.argmax(wbar))] / g2)
        mstar_tb[str(g2)] = float(m_vals[int(np.argmin(tbs))] / g2)
    with open(os.path.join(tables, "exact_mass_scan.csv"), "w") as fh:
        fh.write("g2,m,t_b,W_bar,P_meson_avg,P_BBbar_avg\n")
        for r in rows:
            fh.write(",".join(f"{x:.10g}" for x in r) + "\n")
    out = {"mstar_over_g2": mstar, "mstar_over_g2_tb": mstar_tb,
           "n_mass_points": n_m, "n_g2_values": len(g2_values),
           "t_window": list(t_window), "tree_level": 3.0 / 16.0}
    with open(os.path.join(physics, "resonance.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    return out


# ------------------------------------------------------------- time series

def timeseries_at(g2, m, jmax=0.5, times=None, tag="exact_timeseries"):
    if times is None:
        times = np.linspace(0.0, 12.0, 121)
    H, basis = build_hamiltonian(g2, m, jmax)[:2]
    psi0 = np.zeros(H.shape[0], complex)
    psi0[_idx(basis, STRETCHED)] = 1.0
    states = evolve(H, psi0, times)
    ps, pm, pb, po = channel_probs(basis, states)
    e2m, nvm = _diagnostics(basis)
    p = np.abs(states) ** 2
    e2 = p @ e2m
    nv = p @ nvm
    i_st, i_sh = _idx(basis, STRETCHED), _idx(basis, SHORT)
    p_st, p_sh = p[:, i_st], p[:, i_sh]
    Hd = H.toarray()
    en = np.real(np.einsum("ti,ij,tj->t", states.conj(), Hd, states))
    tables = os.path.join(RUN_DIR, "analysis", "tables")
    os.makedirs(tables, exist_ok=True)
    with open(os.path.join(tables, f"{tag}.csv"), "w") as fh:
        fh.write("t,P_stretched,P_short,P_surv,P_meson,P_BBbar,P_other,"
                 "E2_l1,E2_l2,E2_l3,E2_l4,n_v1,n_v2,n_v3,n_v4,energy\n")
        for k, t in enumerate(times):
            vals = [t, p_st[k], p_sh[k], ps[k], pm[k], pb[k], po[k],
                    *e2[k], *nv[k], en[k]]
            fh.write(",".join(f"{x:.10g}" for x in vals) + "\n")
    _figures(times, ps, pm, pb, po, e2, nv, tag)
    return {"t": times, "P_surv": ps, "P_meson": pm, "P_BBbar": pb,
            "P_other": po, "E2": e2, "n": nv, "energy": en,
            "P_stretched": p_st, "P_short": p_sh}


def _figures(times, ps, pm, pb, po, e2, nv, tag):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figs = os.path.join(RUN_DIR, "analysis", "figures")
    os.makedirs(figs, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for y, lab in ((ps, "P_surv"), (pm, "P_meson"), (pb, "P_BBbar"),
                   (po, "P_other")):
        ax.plot(times, y, label=lab)
    ax.set_xlabel("t [a]"); ax.set_ylabel("probability"); ax.legend()
    ax.set_title("String-breaking channels (exact)")
    fig.tight_layout(); fig.savefig(os.path.join(figs, "exact_channels.png"), dpi=140)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(times, e2.sum(axis=1) - 9.0 / 4.0, "k-", label="ΔC = ΣE² − 9/4")
    for l in range(4):
        ax.plot(times, e2[:, l], "--", alpha=0.6, label=f"E²_l{l+1}")
    ax.set_xlabel("t [a]"); ax.legend(fontsize=8)
    ax.set_title("Casimir reduction (exact)")
    fig.tight_layout(); fig.savefig(os.path.join(figs, "exact_casimir.png"), dpi=140)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for v in range(4):
        ax.plot(times, nv[:, v], label=f"n_v{v+1}")
    ax.set_xlabel("t [a]"); ax.set_ylabel("⟨n_v⟩"); ax.legend()
    ax.set_title("Site-resolved density (exact)")
    fig.tight_layout(); fig.savefig(os.path.join(figs, "exact_density.png"), dpi=140)
    plt.close(fig)


# ------------------------------------------------------------- truncation

def truncation(g2, m):
    """Max channel-probability shift jmax=1 vs jmax=1/2 over t in [0,12]."""
    times = np.linspace(0.0, 12.0, 121)
    out = {}
    for jmax in (0.5, 1.0):
        H, basis = build_hamiltonian(g2, m, jmax)[:2]
        psi0 = np.zeros(H.shape[0], complex)
        psi0[_idx(basis, STRETCHED)] = 1.0
        states = evolve(H, psi0, times)
        ps, pm, pb, po = channel_probs(basis, states)
        out[jmax] = np.stack([ps, pm, pb, po])
    d = float(np.max(np.abs(out[0.5] - out[1.0])))
    res = {"max_abs_dprob": d, "g2": g2, "m": m}
    with open(os.path.join(RUN_DIR, "physics", "truncation_error.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    with open(os.path.join(RUN_DIR, "physics", "truncation_error.md"), "w") as fh:
        fh.write("# Truncation error (jmax=1 vs jmax=1/2)\n\n"
                 f"At (g2, m) = ({g2}, {m}), stretched-string evolution on "
                 f"t ∈ [0, 12]:\n\n"
                 f"max |Δp| over channels and times = {d:.4g}\n\n")
        if d > 0.1:
            fh.write("**FLAG: exceeds 0.1 — hardcore-gluon truncation is a "
                     "leading systematic in this window.**\n")
        else:
            fh.write("Below the 0.1 threshold: hardcore-gluon truncation is "
                     "subleading in the chosen window.\n")
    return res


# ------------------------------------------------- Strang error and window

def _term_split(g2, m, jmax=0.5):
    """Split H into D (diagonal), h_l (per-link hopping), B (magnetic)."""
    H, basis = build_hamiltonian(g2, m, jmax)[:2]
    Hn = build_hamiltonian_no_magnetic(g2, m, jmax)[0]
    Hd = H.toarray()
    Hnd = Hn.toarray()
    D = np.diag(np.diag(Hnd))
    B = Hd - Hnd
    hop = Hnd - D
    hs = []
    for l in range(4):
        hl = np.zeros_like(hop)
        s, t = cv.LINKS[l][0], cv.LINKS[l][1]
        for i, (ji, ni, _) in enumerate(basis):
            for j in range(len(basis)):
                if abs(hop[i, j]) < 1e-14:
                    continue
                jj, nj = basis[j][0], basis[j][1]
                dj = [abs(ji[k] - jj[k]) > 1e-12 for k in range(4)]
                dn = [ni[k] != nj[k] for k in range(4)]
                if dj == [k == l for k in range(4)] and \
                        set(k for k in range(4) if dn[k]) == {s, t}:
                    hl[i, j] = hop[i, j]
        hs.append(hl)
    assert np.max(np.abs(D + sum(hs) + B - Hd)) <= 1e-13, "term split failed"
    return Hd, D, hs, B, basis


def strang_step_matrix(D, hs, B, dt):
    """One Strang step in the CIRCUIT layer ordering (prompt §5.5):
    D/2 · [h0,h2]/2 · [h1,h3]/2 · B · [h1,h3]/2 · [h0,h2]/2 · D/2."""
    order = [hs[0], hs[2], hs[1], hs[3]]
    U = expm(-1j * D * dt / 2.0)
    for h in order:
        U = expm(-1j * h * dt / 2.0) @ U
    U = expm(-1j * B * dt) @ U
    for h in reversed(order):
        U = expm(-1j * h * dt / 2.0) @ U
    U = expm(-1j * D * dt / 2.0) @ U
    return U


def strang_error(g2, m, dt, r, jmax=0.5):
    """Observable error of r Strang steps vs exact at t = r dt."""
    Hd, D, hs, B, basis = _term_split(g2, m, jmax)
    psi0 = np.zeros(Hd.shape[0], complex)
    psi0[_idx(basis, STRETCHED)] = 1.0
    Us = strang_step_matrix(D, hs, B, dt)
    psi_s = psi0.copy()
    for _ in range(r):
        psi_s = Us @ psi_s
    psi_e = expm(-1j * Hd * (r * dt)) @ psi0
    e2m, nvm = _diagnostics(basis)
    surv = _classify(basis)[0]
    pe, ps_ = np.abs(psi_e) ** 2, np.abs(psi_s) ** 2
    devs = [abs(pe @ surv - ps_ @ surv),
            float(np.max(np.abs(pe @ nvm - ps_ @ nvm))),
            float(np.max(np.abs(pe @ e2m - ps_ @ e2m)))]
    return max(devs)


def select_window(g2=1.0, m=None, jmax=0.5):
    """Choose (g2, m, dt, r_max) per prompt Phase-2 criterion 5."""
    physics = os.path.join(RUN_DIR, "physics")
    if m is None:
        res = json.load(open(os.path.join(physics, "resonance.json")))
        m = res["mstar_over_g2"][str(g2)] * g2
    H, basis = build_hamiltonian(g2, m, jmax)[:2]
    psi0 = np.zeros(H.shape[0], complex)
    psi0[_idx(basis, STRETCHED)] = 1.0
    best = None
    for r_max in (3, 2):
        for t_tot in (3.0, 2.5, 3.5, 4.0, 2.0, 5.0, 6.0, 1.5):
            dt = t_tot / r_max
            times = np.array([0.0, t_tot])
            states = evolve(H, psi0, times)
            ps, pm, pb, po = channel_probs(basis, states)
            drop = ps[0] - ps[1]
            pair = pm[1] + pb[1]
            serr = strang_error(g2, m, dt, r_max, jmax)
            cand = {"g2": g2, "m": m, "dt": dt, "r_max": r_max,
                    "expected": {"psurv_drop": float(drop),
                                 "pair_weight": float(pair),
                                 "strang_err": float(serr)},
                    "shortfall_flagged": False}
            if serr <= 0.05:
                if drop >= 0.3 and pair >= 0.05:
                    with open(os.path.join(physics, "window.json"), "w") as fh:
                        json.dump(cand, fh, indent=1)
                    return cand
                if best is None or (drop > best["expected"]["psurv_drop"]):
                    best = cand
    best["shortfall_flagged"] = True
    with open(os.path.join(physics, "window.json"), "w") as fh:
        json.dump(best, fh, indent=1)
    return best


def verify_window(w):
    """Recompute the window criteria (gate G2 calls this)."""
    g2, m, dt, r = w["g2"], w["m"], w["dt"], w["r_max"]
    H, basis = build_hamiltonian(g2, m, 0.5)[:2]
    psi0 = np.zeros(H.shape[0], complex)
    psi0[_idx(basis, STRETCHED)] = 1.0
    states = evolve(H, psi0, np.array([0.0, r * dt]))
    ps, pm, pb, po = channel_probs(basis, states)
    return {"psurv_drop": float(ps[0] - ps[1]),
            "pair_weight": float(pm[1] + pb[1]),
            "strang_err": float(strang_error(g2, m, dt, r))}
