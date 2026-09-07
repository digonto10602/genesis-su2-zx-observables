"""Route 2: redundant Kogut-Susskind space followed by Gauss-law projection.

Construction:
  * Each link is a truncated rigid rotor |j, mL, mR> (dim 5 at jmax=1/2).
  * Matter: 8 Jordan-Wigner fermionic modes in the frozen order (v-major).
  * The physical basis is built from vertex-local Gauss singlets (codex-built,
    verified: dims 82/152, sector dims 2,20,38,20,2, electric clusters).
  * H is built on the FULL redundant space (electric, mass, 4 hoppings with JW
    strings, plaquette trace) and projected: H_phys = P^dag H_red P.
  * The U matrix-element convention (which color index is conjugated) is
    selected NUMERICALLY as the unique variant that makes [G^a_v, H_hop] = 0;
    the choice is recorded in U_CONVENTION after first build.

Limitation (recorded in run/DECISIONS.md): at jmax=1 only the kernel dimension
(152) is computed by this route; the projected H_1 matrix is route-1-only
(redundant dim 14^4*256 ~ 9.8M exceeds the night's memory/time budget).
Route agreement is gated at jmax=1/2 per the run prompt (G1 criterion 3).
"""
from __future__ import annotations

import itertools

import numpy as np
from scipy.linalg import eigh
from scipy.sparse import csr_matrix, diags, hstack, identity, kron

from ..conventions import (ETA, LINKS, N_VAC, PARITY, casimir,
                           coupling_electric, coupling_magnetic,
                           HOPPING_PREFACTOR)

# ------------------------------------------------------------------ helpers

def _spins(jmax):
    return tuple(k / 2 for k in range(int(2 * jmax) + 1))


def _link_states(jmax):
    return [(j, ml, mr) for j in _spins(jmax)
            for ml in np.arange(-j, j + 1, 1.0)
            for mr in np.arange(-j, j + 1, 1.0)]


def _spin(j):
    m = np.arange(-j, j + 1, 1.0)
    z = np.diag(m).astype(complex)
    p = np.zeros((len(m), len(m)), complex)
    for i, x in enumerate(m[:-1]):
        p[i + 1, i] = np.sqrt(j * (j + 1) - x * (x + 1))
    return ((p + p.T.conj()) / 2, -1j * (p - p.T.conj()) / 2, z)


def _cg(j, m, a, jp):
    """CG(j,m;1/2,a|jp,m+a), a = +-1/2, closed forms."""
    d = 2 * j + 1
    if abs(jp - j - .5) < 1e-10:
        return np.sqrt((j + m + 1) / d) if a > 0 else np.sqrt((j - m + 1) / d)
    if abs(jp - j + .5) < 1e-10:
        return -np.sqrt((j - m) / d) if a > 0 else np.sqrt((j + m) / d)
    return 0.0


# ------------------------------------------- vertex singlets (codex, verified)

def _local_fermions():
    aa = []
    for c in range(2):
        x = np.zeros((4, 4), complex)
        for b in range(4):
            if b & (1 << c):
                x[b ^ (1 << c), b] = (-1) ** sum((b >> k) & 1 for k in range(c))
        aa.append(x)
    out = []
    for T in (np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2,
              np.diag([.5, -.5])):
        out.append(sum(T[a, b] * aa[a].conj().T @ aa[b]
                       for a in range(2) for b in range(2)))
    return out


# vertex v -> ((link_a, link_b), (sign_a, sign_b)); end m-index mapping below.
_ENDS = (((0, 3), (1, 1)), ((0, 1), (1, 1)), ((1, 2), (1, 1)), ((2, 3), (1, 1)))


def _local_singlet(ja, jb, n, signs):
    da, db = int(2 * ja + 1), int(2 * jb + 1)
    Ia, Ib = np.eye(da), np.eye(db)
    q = _local_fermions()
    gs = []
    for a in range(3):
        gs.append(np.kron(np.kron(signs[0] * _spin(ja)[a], Ib), np.eye(4))
                  + np.kron(np.kron(Ia, signs[1] * _spin(jb)[a]), np.eye(4))
                  + np.kron(np.kron(Ia, Ib), q[a]))
    K = sum(x @ x for x in gs)
    inds = [(ia * db + ib) * 4 + b for ia in range(da) for ib in range(db)
            for b in range(4) if b.bit_count() == n]
    w, v = eigh(K[np.ix_(inds, inds)])
    if len(np.where(w < 2e-10)[0]):
        x = np.zeros(da * db * 4, complex)
        x[inds] = v[:, np.where(w < 2e-10)[0][0]]
        return x.reshape(da, db, 4)
    return None


def _physical_basis(jmax):
    states = _link_states(jmax)
    dl = len(states)
    dm = 256
    labels = []
    cols = []
    for js in itertools.product(_spins(jmax), repeat=4):
        for ns in itertools.product(range(3), repeat=4):
            loc = [_local_singlet(js[a], js[b], ns[v], sgn)
                   for v, ((a, b), sgn) in enumerate(_ENDS)]
            if any(x is None for x in loc):
                continue
            entries = {}
            nz = [[(tuple(ind), x[tuple(ind)])
                   for ind in np.argwhere(abs(x) > 1e-12)] for x in loc]
            for items in itertools.product(*nz):
                inds = tuple(z[0] for z in items)
                amp = np.prod([z[1] for z in items])
                if abs(amp) < 1e-11:
                    continue
                ml = [None] * 4
                mr = [None] * 4
                fb = 0
                for v, ((a, b), _) in enumerate(_ENDS):
                    ia, ib, bit = inds[v]
                    fb |= bit << (2 * v)
                    if v == 0:
                        ml[0], ml[3] = ia, ib
                    elif v == 1:
                        mr[0], ml[1] = ia, ib
                    elif v == 2:
                        mr[1], mr[2] = ia, ib
                    else:
                        ml[2], mr[3] = ia, ib
                li = []
                for l, j in enumerate(js):
                    mm = np.arange(-j, j + 1, 1.0)
                    li.append(states.index((j, mm[ml[l]], mm[mr[l]])))
                idx = (((li[0] * dl + li[1]) * dl + li[2]) * dl + li[3]) * dm + fb
                entries[idx] = entries.get(idx, 0) + amp
            rows = np.fromiter(entries, dtype=np.int64)
            data = np.fromiter(entries.values(), dtype=complex)
            col = csr_matrix((data, (rows, np.zeros(len(rows), dtype=np.int64))),
                             shape=(dl ** 4 * dm, 1), dtype=complex)
            col = col / np.sqrt(float(col.multiply(col.conj()).sum().real))
            cols.append(col)
            labels.append((tuple(float(x) for x in js),
                           tuple(int(x) for x in ns), 0))
    return labels, hstack(cols, format="csc")


_CACHE = {}


def _basis(jmax):
    jmax = float(jmax)
    if jmax not in _CACHE:
        _CACHE[jmax] = _physical_basis(jmax)
    return _CACHE[jmax]


def kernel_dimension(jmax):
    return len(_basis(jmax)[0])


# ------------------------------------------------------- full-space operators

# color index alpha in {+1/2: c=0, -1/2: c=1}
_ALPHAS = (0.5, -0.5)


def _link_JLR(jmax):
    """(JL[a], JR[a]) dl x dl sparse, a = x,y,z."""
    states = _link_states(jmax)
    dl = len(states)
    idx = {s: i for i, s in enumerate(states)}
    JL = [np.zeros((dl, dl), complex) for _ in range(3)]
    JR = [np.zeros((dl, dl), complex) for _ in range(3)]
    for j in _spins(jmax):
        mm = np.arange(-j, j + 1, 1.0)
        S = _spin(j)
        for a in range(3):
            for i1, m1 in enumerate(mm):
                for i2, m2 in enumerate(mm):
                    if abs(S[a][i1, i2]) < 1e-15:
                        continue
                    for mo in mm:  # spectator index
                        JL[a][idx[(j, m1, mo)], idx[(j, m2, mo)]] += S[a][i1, i2]
                        JR[a][idx[(j, mo, m1)], idx[(j, mo, m2)]] += S[a][i1, i2]
    return ([csr_matrix(x) for x in JL], [csr_matrix(x) for x in JR])


def _link_U(jmax, conjL, conjR):
    """U[(alpha,beta)] dl x dl sparse; conjX conjugates that color index."""
    states = _link_states(jmax)
    dl = len(states)
    idx = {s: i for i, s in enumerate(states)}
    spins = _spins(jmax)
    U = {}
    for al in _ALPHAS:
        for be in _ALPHAS:
            M = np.zeros((dl, dl), complex)
            for (j, mL, mR) in states:
                for jp in (j + .5, j - .5):
                    if jp < -1e-10 or jp > max(spins) + 1e-10:
                        continue
                    jp = abs(round(jp * 2)) / 2
                    if jp not in spins:
                        continue
                    pref = np.sqrt((2 * j + 1) / (2 * jp + 1))
                    aL, sL = (al, 1.0) if not conjL else (-al, (1 if al > 0 else -1))
                    aR, sR = (be, 1.0) if not conjR else (-be, (1 if be > 0 else -1))
                    mLp, mRp = mL + aL, mR + aR
                    if abs(mLp) > jp + 1e-10 or abs(mRp) > jp + 1e-10:
                        continue
                    fL = _cg(j, mL, aL, jp)
                    fR = _cg(j, mR, aR, jp)
                    if abs(fL * fR) < 1e-15:
                        continue
                    M[idx[(jp, mLp, mRp)], idx[(j, mL, mR)]] += \
                        pref * sL * sR * fL * fR
            U[(al, be)] = csr_matrix(M)
    return U


def _fermion_ops():
    """Global JW annihilation ops a_k on the 256-dim space, k = 2v + c."""
    dm = 256
    ops = []
    for k in range(8):
        rows, cols, data = [], [], []
        for fb in range(dm):
            if fb & (1 << k):
                sign = (-1) ** bin(fb & ((1 << k) - 1)).count("1")
                rows.append(fb ^ (1 << k))
                cols.append(fb)
                data.append(sign)
        ops.append(csr_matrix((data, (rows, cols)), shape=(dm, dm), dtype=complex))
    return ops


def _embed_link(op, l, dl, dm):
    """kron: identity on links < l, op on link l, identity after, identity fermions."""
    mats = [identity(dl, format="csr", dtype=complex)] * 4
    mats[l] = op
    out = mats[0]
    for m in mats[1:]:
        out = kron(out, m, format="csr")
    return kron(out, identity(dm, format="csr", dtype=complex), format="csr")


def _embed_links_fermi(link_ops, fermi_op, dl, dm):
    """link_ops: dict l -> op (missing = identity); fermi_op on 256."""
    mats = [link_ops.get(l, identity(dl, format="csr", dtype=complex))
            for l in range(4)]
    out = mats[0]
    for m in mats[1:]:
        out = kron(out, m, format="csr")
    return kron(out, fermi_op, format="csr")


_SIGMA = (np.array([[0, 1], [1, 0]]) / 2, np.array([[0, -1j], [1j, 0]]) / 2,
          np.diag([0.5, -0.5]).astype(complex))


def _gauss_ops(jmax):
    """G[a][v] on the full redundant space."""
    dl = len(_link_states(jmax))
    dm = 256
    JL, JR = _link_JLR(jmax)
    f = _fermion_ops()
    G = [[None] * 4 for _ in range(3)]
    for v in range(4):
        # link ends at v (per _ENDS / frozen conventions)
        ends = []
        for l, (s, t, _d) in enumerate(LINKS):
            if s == v:
                ends.append((l, "L"))
            if t == v:
                ends.append((l, "R"))
        for a in range(3):
            Q = csr_matrix((dm, dm), dtype=complex)
            for c1 in range(2):
                for c2 in range(2):
                    if abs(_SIGMA[a][c1, c2]) < 1e-15:
                        continue
                    Q = Q + _SIGMA[a][c1, c2] * \
                        (f[2 * v + c1].conj().T.tocsr() @ f[2 * v + c2])
            g = _embed_links_fermi({}, Q, dl, dm)
            for (l, end) in ends:
                op = JL[a] if end == "L" else JR[a]
                g = g + _embed_link(op, l, dl, dm)
            G[a][v] = g
    return G


def _c_of_alpha(al):
    return 0 if al > 0 else 1


def _build_terms(jmax, conjL, conjR):
    """All Hamiltonian term groups on the full redundant space (coefficient-free
    where possible): returns dict with electric, mass, hop_l (l=0..3, WITHOUT
    the 1/2 eta prefactor), trU (the plaquette trace, not Hermitized)."""
    states = _link_states(jmax)
    dl = len(states)
    dm = 256
    U = _link_U(jmax, conjL, conjR)
    Udag = {k: v.conj().T.tocsr() for k, v in U.items()}
    f = _fermion_ops()
    fdag = [x.conj().T.tocsr() for x in f]

    e2_link = diags([casimir(s[0]) for s in states], format="csr", dtype=complex)
    electric = sum(_embed_link(e2_link, l, dl, dm) for l in range(4))

    nmodes = [fdag[k] @ f[k] for k in range(8)]
    mass_f = sum(PARITY[v] * (nmodes[2 * v] + nmodes[2 * v + 1]) for v in range(4))
    mass = _embed_links_fermi({}, mass_f.tocsr(), dl, dm)

    hops = []
    for l, (s, t, _d) in enumerate(LINKS):
        h = None
        for al in _ALPHAS:
            for be in _ALPHAS:
                fpart = (fdag[2 * s + _c_of_alpha(al)] @ f[2 * t + _c_of_alpha(be)])
                term = _embed_links_fermi({l: U[(al, be)]}, fpart.tocsr(), dl, dm)
                h = term if h is None else h + term
        h = h + h.conj().T.tocsr()  # + h.c.
        hops.append(h)

    # plaquette trace: sum_{a,b,c,d} U0^{ab} U1^{bc} (U2^dag)^{cd} (U3^dag)^{da}
    # color-matrix dagger: (U^dag)^{cd} = adjoint of U^{dc}
    trU = None
    ident_f = identity(dm, format="csr", dtype=complex)
    for a_ in _ALPHAS:
        for b_ in _ALPHAS:
            for c_ in _ALPHAS:
                for d_ in _ALPHAS:
                    ops = {0: U[(a_, b_)], 1: U[(b_, c_)],
                           2: Udag[(d_, c_)], 3: Udag[(a_, d_)]}
                    term = _embed_links_fermi(ops, ident_f, dl, dm)
                    trU = term if trU is None else trU + term
    return {"electric": electric, "mass": mass, "hops": hops, "trU": trU}


_TERMS_CACHE = {}
U_CONVENTION = {}


def _select_convention(jmax=0.5):
    """Pick (conjL, conjR) as the variant with vanishing [G, hop] and [G, trU]."""
    key = float(jmax)
    if key in U_CONVENTION:
        return U_CONVENTION[key]
    G = _gauss_ops(jmax)
    best = None
    for conjL in (False, True):
        for conjR in (False, True):
            terms = _build_terms(jmax, conjL, conjR)
            worst = 0.0
            for op in [terms["hops"][0], terms["trU"]]:
                for a in range(3):
                    for v in range(4):
                        c = (G[a][v] @ op - op @ G[a][v])
                        if c.nnz:
                            worst = max(worst, float(np.max(np.abs(c.data))))
                if worst > 1e-10:
                    break
            if worst <= 1e-10:
                best = (conjL, conjR, terms)
                break
        if best:
            break
    assert best is not None, "no U convention makes [G,H]=0 -- construction bug"
    U_CONVENTION[key] = (best[0], best[1])
    _TERMS_CACHE[key] = best[2]
    return U_CONVENTION[key]


def _terms(jmax):
    key = float(jmax)
    if key not in _TERMS_CACHE:
        _select_convention(key)
    return _TERMS_CACHE[key]


def gauss_commutator_norms(jmax):
    """Max over v, a of max-abs entry of [G^a_v, H_term], per term group."""
    jmax = float(jmax)
    terms = _terms(jmax)
    G = _gauss_ops(jmax)
    named = {"electric": terms["electric"], "mass": terms["mass"],
             **{f"hop_{l}": terms["hops"][l] for l in range(4)},
             "magnetic": (terms["trU"] + terms["trU"].conj().T.tocsr())}
    out = {}
    for name, op in named.items():
        worst = 0.0
        for a in range(3):
            for v in range(4):
                c = G[a][v] @ op - op @ G[a][v]
                if c.nnz:
                    worst = max(worst, float(np.max(np.abs(c.data))))
        out[name] = worst
    return out


# ------------------------------------------------------------- projected API

def _h_red(g2, m, jmax, magnetic=True):
    t = _terms(jmax)
    H = coupling_electric(g2) * t["electric"] + m * t["mass"]
    for l in range(4):
        H = H + HOPPING_PREFACTOR * ETA[l] * t["hops"][l]
    if magnetic:
        H = H - coupling_magnetic(g2) * (t["trU"] + t["trU"].conj().T.tocsr())
    return H


def build_hamiltonian(g2, m, jmax):
    jmax = float(jmax)
    if jmax > 0.75:
        raise NotImplementedError(
            "route 2 builds the projected H only at jmax=1/2 tonight; at jmax=1 "
            "use kernel_dimension(1.0) (=152). See module docstring / DECISIONS.")
    labels, P = _basis(jmax)
    H = (P.conj().T @ _h_red(g2, m, jmax) @ P).tocsr()
    H = ((H + H.conj().T) / 2).tocsr()  # kill 1e-17 asymmetry noise
    return H, labels, P


def build_hamiltonian_no_magnetic(g2, m, jmax):
    jmax = float(jmax)
    if jmax > 0.75:
        raise NotImplementedError("see build_hamiltonian")
    labels, P = _basis(jmax)
    H = (P.conj().T @ _h_red(g2, m, jmax, magnetic=False) @ P).tocsr()
    H = ((H + H.conj().T) / 2).tocsr()
    return H, labels, P


def get_state(label, basis_labels):
    return basis_labels.index(label)


# ------------------------------------------------------ diagonal observables

def _obs(labels):
    n = len(labels)
    E = [diags([casimir(x[0][l]) for x in labels], format="csr")
         for l in range(4)]
    nv = [diags([x[1][v] for x in labels], format="csr") for v in range(4)]
    N = sum(nv[1:], nv[0])
    q = [[x[1][v] - N_VAC[v] for x in labels] for v in range(4)]
    Psurv = diags([int(tuple(q[v][i] for v in range(4)) == (1, -1, 0, 0))
                   for i in range(n)], format="csr")
    Pmes = diags([int(all(abs(q[v][i]) == 1 for v in range(4)))
                  for i in range(n)], format="csr")
    Pbb = diags([int(any(abs(q[v][i]) == 2 for v in range(4)))
                 for i in range(n)], format="csr")
    return E, nv, N, Psurv, Pmes, Pbb


def E2_link(l, basis_labels):
    return _obs(basis_labels)[0][l]


def n_op(v, basis_labels):
    return _obs(basis_labels)[1][v]


def N_total(basis_labels):
    return _obs(basis_labels)[2]


def P_surv(basis_labels):
    return _obs(basis_labels)[3]


def P_meson(basis_labels):
    return _obs(basis_labels)[4]


def P_BBbar(basis_labels):
    return _obs(basis_labels)[5]
