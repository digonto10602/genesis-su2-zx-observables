"""Structured synthesis of the L12 block unitaries.

The implementation deliberately keeps the code-space structure visible: the
small connected components of each local matrix are synthesized independently
and the diagonal term is a degree-three phase polynomial.
"""
from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import PhaseGate, UnitaryGate
from scipy.linalg import expm

from su2qc.circuits import strang_l12 as sl
from su2qc.encodings.l12 import encode, physical_codes

NQ = 12
GROUPS = sl.GROUPS
_LINK_REP = (1, 4, 7, 10)  # one copy of links 0,1,2,3


def _local_patterns(codes, support):
    return {sum(((c >> q) & 1) << k for k, q in enumerate(support)) for c in codes}


def _gray_map(x, y, target, n):
    """CNOT sequence making x,y differ only on target (self-inverse)."""
    return [(target, q) for q in range(n) if q != target and ((x >> q) & 1) != ((y >> q) & 1)]


def _mapped_pattern(p, cnots, target):
    for c, t in cnots:
        if (p >> c) & 1:
            p ^= 1 << t
    return p


def _minimal_controls(x, y, target, cnots, physical):
    """Smallest control set (exhaustive over subsets, |support| <= 8) such
    that no OTHER physical local pattern matches the selected pattern on
    the controls after the Gray-code CNOT conjugation."""
    from itertools import combinations
    mx = _mapped_pattern(x, cnots, target)
    n = max(max(physical).bit_length(), target + 1)
    fixed = {q: (mx >> q) & 1 for q in range(n) if q != target}
    others = [_mapped_pattern(z, cnots, target) for z in physical if z not in (x, y)]
    cand = sorted(fixed)
    for k in range(len(cand) + 1):
        for sub in combinations(cand, k):
            if not any(all(((mz >> q) & 1) == fixed[q] for q in sub) for mz in others):
                return sorted(sub), fixed
    return cand, fixed


def _mc_single_qubit(u, k):
    """Multi-controlled single-qubit unitary as a controlled UGate (ZYZ
    angles + phase), which qiskit synthesizes far more cheaply than a
    controlled generic UnitaryGate."""
    from qiskit.circuit.library import UGate
    from qiskit.synthesis.one_qubit import OneQubitEulerDecomposer
    theta, phi, lam, phase = OneQubitEulerDecomposer("U").angles_and_phase(np.asarray(u, complex))
    g = UGate(theta, phi, lam)
    if abs(phase) > 1e-14:
        # global phase of the target block becomes a controlled phase
        from qiskit.circuit.library import PhaseGate
        from qiskit import QuantumCircuit
        sub = QuantumCircuit(1, name="u_ph")
        sub.append(g, [0])
        sub.global_phase = phase
        return sub.to_gate().control(k) if k else sub.to_gate()
    return g.control(k) if k else g


def _two_level(qc, support, x, y, mat, physical):
    """Apply a 2x2 unitary on local patterns x,y using a Gray path."""
    n = len(support)
    differing = [q for q in range(n) if ((x >> q) & 1) != ((y >> q) & 1)]
    if not differing:
        raise ValueError("two-level states must differ")
    # choose the target (and Gray path) giving the fewest controls
    best = None
    for tgt in differing:
        cn = _gray_map(x, y, tgt, n)
        ctr, fx = _minimal_controls(x, y, tgt, cn, physical)
        score = (len(ctr), len(cn))
        if best is None or score < best[0]:
            best = (score, tgt, cn, ctr, fx)
    _, target, cnots, controls, fixed = best
    for c, t in cnots:
        qc.cx(support[c], support[t])
    # Transform the pair's matrix into computational target order.
    if ((x >> target) & 1) == 0:
        u = np.asarray(mat, complex)
    else:
        u = np.asarray([[mat[1, 1], mat[1, 0]], [mat[0, 1], mat[0, 0]]], complex)
    for q in controls:
        if not fixed[q]:
            qc.x(support[q])
    cq = [support[q] for q in controls]
    tq = support[target]
    # Zero-diagonal real couplings give exp(-i a X) = RX(2a): use the
    # specialised multi-controlled RX synthesis (much cheaper than a
    # generic controlled unitary).
    if (abs(u[0, 0] - u[1, 1]) < 1e-13 and abs(u[0, 1] - u[1, 0]) < 1e-13
            and abs(u[0, 0].imag) < 1e-13 and abs(u[0, 1].real) < 1e-13):
        ang = 2.0 * np.arctan2(-u[0, 1].imag, u[0, 0].real)
        if controls:
            qc.mcrx(ang, cq, tq)
        else:
            qc.rx(ang, tq)
    else:
        gate = _mc_single_qubit(u, len(controls))
        qc.append(gate, cq + [tq])
    for q in reversed(controls):
        if not fixed[q]:
            qc.x(support[q])
    for c, t in reversed(cnots):
        qc.cx(support[c], support[t])


def _givens_decomposition(v):
    """Return (diagonal, factors) with v=factors[0]...D."""
    a = np.array(v, complex)
    factors = []
    for i, j, col in ((0, 1, 0), (0, 2, 0), (1, 2, 1)):
        aa, bb = a[i, col], a[j, col]
        r = np.hypot(abs(aa), abs(bb))
        if r < 1e-14:
            continue
        g = np.eye(3, dtype=complex)
        g[np.ix_([i, j], [i, j])] = [[np.conj(aa) / r, np.conj(bb) / r],
                                      [-bb / r, aa / r]]
        a = g @ a
        factors.append((i, j, g[np.ix_([i, j], [i, j])]))
    # Numerical phases are retained; tiny off-diagonals are roundoff.
    if np.max(np.abs(a - np.diag(np.diag(a)))) > 2e-10:
        raise ArithmeticError("Givens elimination failed")
    return np.diag(a), factors


def _phase_on_pattern(qc, support, pattern, phase, physical):
    if abs(phase) < 1e-15:
        return
    # Use the last support bit as target and retain only controls necessary to
    # distinguish this physical local pattern.
    target = len(support) - 1
    controls = [q for q in range(len(support)) if q != target]
    for q in list(controls):
        trial = [z for z in controls if z != q]
        if not any(z != pattern and all(((z >> k) & 1) == ((pattern >> k) & 1) for k in trial + [target]) for z in physical):
            controls.remove(q)
    # X target turns the desired target value into 1; PhaseGate then phases it.
    if not ((pattern >> target) & 1):
        qc.x(support[target])
    fixed = {q: (pattern >> q) & 1 for q in controls}
    for q in controls:
        if not fixed[q]:
            qc.x(support[q])
    qc.append(PhaseGate(phase).control(len(controls)), [support[q] for q in controls] + [support[target]])
    for q in reversed(controls):
        if not fixed[q]:
            qc.x(support[q])
    if not ((pattern >> target) & 1):
        qc.x(support[target])


def _component_patterns(L):
    n = len(L)
    todo = set(range(n))
    out = []
    while todo:
        root = todo.pop(); comp = {root}; stack = [root]
        while stack:
            i = stack.pop()
            for j in np.flatnonzero(np.abs(L[i]) > 1e-13):
                j = int(j)
                if j in todo:
                    todo.remove(j); comp.add(j); stack.append(j)
        out.append(sorted(comp))
    return out


def _synth_local(group, theta, g2, m):
    basis, terms = sl.terms(float(g2), float(m))
    cb = sl.basis_to_code(basis)
    support = sl.supports(float(g2), float(m))[group]
    L = sl.local_matrix(terms[group], cb, support)
    physical = _local_patterns(physical_codes(), support)
    qc = QuantumCircuit(NQ, name=f"synth_{group}")
    for comp in _component_patterns(L):
        if len(comp) not in (2, 3):
            if len(comp) == 1:
                continue
            raise ValueError(f"unexpected component size {len(comp)}")
        if len(comp) == 2:
            _two_level(qc, support, comp[0], comp[1], expm(-1j * theta * L[np.ix_(comp, comp)]), physical)
            continue
        v = expm(-1j * theta * L[np.ix_(comp, comp)])
        diag, factors = _givens_decomposition(v)
        for k, p in enumerate(comp):
            _phase_on_pattern(qc, support, p, np.angle(diag[k]), physical)
        # v = E1^dag E2^dag E3^dag D; append in reverse elimination order.
        for i, j, g in reversed(factors):
            mat = g.conj().T
            _two_level(qc, support, comp[i], comp[j], mat, physical)
    return qc


def _bit_polynomial(g2, m):
    p = {(): 0.0}
    for q in _LINK_REP:
        p[(q,)] = p.get((q,), 0.0) + 3.0 * float(g2) / 8.0
    parity = (1, -1, 1, -1)
    for v in range(4):
        a, b, c = 3*v, 3*v+1, 3*v+2
        for key, val in [((c,), 2.0), ((a,), 1.0), ((b,), 1.0),
                         ((a,b), -2.0), ((a,c), -2.0), ((b,c), -2.0), ((a,b,c), 4.0)]:
            p[tuple(sorted(key))] = p.get(tuple(sorted(key)), 0.0) + float(m) * parity[v] * val
    return p


def _diagonal(qc, theta, g2, m):
    # Convert bit monomials to Z monomials: bit=(1-Z)/2.
    zpoly = {}
    for bits, coeff in _bit_polynomial(g2, m).items():
        k = len(bits)
        for mask in range(1 << k):
            zs = tuple(bits[i] for i in range(k) if (mask >> i) & 1)
            zpoly[zs] = zpoly.get(zs, 0.0) + coeff * (2.0 ** -k) * (-1.0) ** len(zs)
    qc.global_phase += -theta * zpoly.pop((), 0.0)
    for qs, coeff in zpoly.items():
        if abs(coeff) < 1e-14:
            continue
        if len(qs) == 1:
            qc.rz(2.0 * theta * coeff, qs[0])
        else:
            for q in qs[:-1]:
                qc.cx(q, qs[-1])
            qc.rz(2.0 * theta * coeff, qs[-1])
            for q in reversed(qs[:-1]):
                qc.cx(q, qs[-1])


@lru_cache(maxsize=64)
def synth_unitary(group, theta, g2, m):
    """Synthesize one exact L12 block using only one-qubit and controlled gates."""
    theta, g2, m = float(theta), float(g2), float(m)
    if group not in GROUPS:
        raise ValueError(group)
    qc = QuantumCircuit(NQ, name=f"synth_{group}")
    if group == "D":
        _diagonal(qc, theta, g2, m)
    else:
        qc.compose(_synth_local(group, theta, g2, m), inplace=True)
    return qc


def synth_strang_step(dt, g2, m):
    qc = QuantumCircuit(NQ)
    seq = (("D", dt/2), ("h0", dt/2), ("h2", dt/2), ("h1", dt/2), ("h3", dt/2),
           ("B", dt), ("h3", dt/2), ("h1", dt/2), ("h2", dt/2), ("h0", dt/2), ("D", dt/2))
    for group, theta in seq:
        qc.compose(synth_unitary(group, theta, g2, m), inplace=True)
    return qc


def synth_full_circuit(r, dt=None, g2=None, m=None, merge_D=True):
    p = sl.params(g2, m); dt = p["dt"] if dt is None else dt
    qc = sl.prep_stretched()
    if r == 0:
        return qc
    if not merge_D:
        for _ in range(r):
            qc.compose(synth_strang_step(dt, p["g2"], p["m"]), inplace=True)
        return qc
    core = (("h0", dt/2), ("h2", dt/2), ("h1", dt/2), ("h3", dt/2), ("B", dt),
            ("h3", dt/2), ("h1", dt/2), ("h2", dt/2), ("h0", dt/2))
    qc.compose(synth_unitary("D", dt/2, p["g2"], p["m"]), inplace=True)
    for k in range(r):
        for group, theta in core:
            qc.compose(synth_unitary(group, theta, p["g2"], p["m"]), inplace=True)
        qc.compose(synth_unitary("D", dt/2 if k == r-1 else dt, p["g2"], p["m"]), inplace=True)
    return qc


def _resources(circ):
    t = transpile(circ, basis_gates=["cz", "rz", "sx", "x", "id"], optimization_level=3, seed_transpiler=7)
    return {"n_2q": sum(x.operation.num_qubits == 2 for x in t.data),
            "depth_2q": t.depth(lambda x: x.operation.num_qubits == 2), "depth": t.depth()}


def write_resources(path="circuits/resources_synth.md"):
    p = sl.params(); rows = []
    for g in GROUPS:
        rows.append((f"group {g} (theta={p['dt']/2:.4f})", _resources(synth_unitary(g, p['dt']/2, p['g2'], p['m']))))
    rows.append(("one Strang step", _resources(synth_strang_step(p['dt'], p['g2'], p['m']))))
    for r in range(4):
        rows.append((f"full circuit r={r} (prep + steps, merged D)", _resources(synth_full_circuit(r))))
    out = ["# Synthesized resources, L12 encoding", "", f"Window: g2={p['g2']}, m={p['m']}, dt={p['dt']:.4f}.", "",
           "| circuit | 2q count | 2q depth | total depth |", "|---|---:|---:|---:|"]
    out += [f"| {name} | {r['n_2q']} | {r['depth_2q']} | {r['depth']} |" for name, r in rows]
    Path(path).write_text("\n".join(out) + "\n")
    return rows
