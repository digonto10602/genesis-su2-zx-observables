"""Exact gauge-invariant block unitaries and Strang circuits for L12 (G3).

Method (structure, not generic 12-qubit synthesis):
  * Each Hamiltonian group T in {D, h0..h3, B} is an 82x82 matrix from the
    verified route-1 Hamiltonian (term split checked exact by the dynamics
    lane).  Lifted to the 4096-dim code space it is E T E^dag: zero on every
    unphysical code, so exp(-i theta E T E^dag) is the identity on the
    complement -> gauge invariance by construction, zero leakage.
  * D is diagonal: a 12-qubit Diagonal gate (phases on the 82 codes, 1 else).
  * Each h_l and B act non-trivially on a SUPPORT of s < 12 qubits (found
    numerically as the qubits whose bits ever change or on which the matrix
    element depends); the lifted operator factorizes as U_s (x) I on the rest
    when all elements depend only on the support bits.  For links whose
    Jordan-Wigner string crosses other vertices, the sign depends on the
    parity (a XOR b) of those vertices; the support then includes those
    (a,b) pairs.  U_s = expm(-i theta M_s) on 2^s dims (s <= 10), built as a
    UnitaryGate.  Exactness is verified by tests to 1e-12.
  * Strang step: D/2 . [h0,h2]/2 . [h1,h3]/2 . B . [h1,h3]/2 . [h0,h2]/2 . D/2
    (l0=(v0,v1), l2=(v3,v2) disjoint; l1=(v1,v2), l3=(v0,v3) disjoint).

Verification helpers avoid dense 4096x4096 operators: the circuit is applied
to statevectors on the 82 codes with Aer/Statevector, and compared with the
exact 82-dim propagator.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import Diagonal, UnitaryGate
from qiskit.quantum_info import Statevector
from scipy.linalg import expm

from su2qc.encodings.l12 import encode, physical_codes

N = 4096
NQ = 12
GROUPS = ("D", "h0", "h1", "h2", "h3", "B")
RUN = Path(__file__).resolve().parents[3]
STRETCHED = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)


def params(g2=None, m=None):
    vals = {"g2": 4.0, "m": 0.75, "dt": 0.8333333333333334, "r_max": 3}
    p = RUN / "physics" / "window.json"
    if p.exists():
        w = json.loads(p.read_text())
        vals.update({k: w[k] for k in ("g2", "m", "dt", "r_max") if k in w})
    if g2 is not None:
        vals["g2"] = g2
    if m is not None:
        vals["m"] = m
    return vals


@lru_cache(maxsize=8)
def terms(g2, m):
    """(basis, {group: 82x82 ndarray}) from the dynamics-lane exact split."""
    from su2qc.dynamics.scan import _term_split
    Hd, D, hs, B, basis = _term_split(float(g2), float(m))
    return basis, {"D": D, "h0": hs[0], "h1": hs[1], "h2": hs[2],
                   "h3": hs[3], "B": B, "H": Hd}


@lru_cache(maxsize=1)
def code_index():
    codes = physical_codes()
    return codes, {c: i for i, c in enumerate(codes)}


def basis_to_code(basis):
    return np.array([encode(lab) for lab in basis])


# ------------------------------------------------------------ support search

def _support(M, codes_of_basis):
    """Minimal-ish qubit set S such that M[i,j] (including zeros) is a
    function of the support bits of codes i and j only.  Greedy: start with
    the bits that flip on any nonzero element, then add the single bit that
    removes the most conflicts until none remain."""
    nz = np.argwhere(np.abs(M) > 1e-14)
    S = set()
    for i, j in nz:
        S |= {q for q in range(NQ)
              if (codes_of_basis[i] >> q) & 1 != (codes_of_basis[j] >> q) & 1}
    n = len(codes_of_basis)

    def n_conflicts(S):
        Sl = sorted(S)
        rest = [q for q in range(NQ) if q not in S]
        pat = np.array([sum(((c >> q) & 1) << k for k, q in enumerate(Sl))
                        for c in codes_of_basis])
        off = np.array([sum(((c >> q) & 1) << k for k, q in enumerate(rest))
                        for c in codes_of_basis])
        seen = {}
        bad = 0
        for i in range(n):
            for j in range(n):
                if off[i] != off[j]:
                    continue  # U_S (x) I gives 0 here, and so does M
                key = (pat[i], pat[j])
                v = complex(M[i, j])
                if key in seen:
                    if abs(seen[key] - v) > 1e-12:
                        bad += 1
                else:
                    seen[key] = v
        return bad

    while n_conflicts(S) > 0:
        best = None
        for q in range(NQ):
            if q in S:
                continue
            c = n_conflicts(S | {q})
            if best is None or c < best[0]:
                best = (c, q)
        S.add(best[1])
    return sorted(S)


def local_matrix(M, codes_of_basis, S):
    """2^|S| x 2^|S| Hermitian matrix acting on support S (sorted)."""
    d = 1 << len(S)
    L = np.zeros((d, d), complex)
    for i, j in np.argwhere(np.abs(M) > 1e-14):
        x = sum(((codes_of_basis[i] >> q) & 1) << k for k, q in enumerate(S))
        y = sum(((codes_of_basis[j] >> q) & 1) << k for k, q in enumerate(S))
        L[x, y] = M[i, j]
    assert np.max(np.abs(L - L.conj().T)) < 1e-13
    return L


@lru_cache(maxsize=8)
def supports(g2, m):
    basis, T = terms(g2, m)
    cb = basis_to_code(basis)
    return {g: _support(T[g], cb) for g in ("h0", "h1", "h2", "h3", "B")}


# ------------------------------------------------------------ circuits

@lru_cache(maxsize=64)
def unitary(group, theta, g2, m):
    """12-qubit circuit for exp(-i theta E T_group E^dag)."""
    basis, T = terms(g2, m)
    cb = basis_to_code(basis)
    qc = QuantumCircuit(NQ, name=f"U_{group}")
    if group == "D":
        diag = np.ones(N, complex)
        diag[cb] = np.exp(-1j * theta * np.real(np.diag(T["D"])))
        qc.append(Diagonal(diag), range(NQ))
        return qc
    S = supports(g2, m)[group]
    L = local_matrix(T[group], cb, S)
    U = expm(-1j * theta * L)
    qc.append(UnitaryGate(U, label=f"U_{group}"), S)
    return qc


def strang_step(dt, g2, m):
    qc = QuantumCircuit(NQ)
    seq = (("D", dt / 2), ("h0", dt / 2), ("h2", dt / 2), ("h1", dt / 2),
           ("h3", dt / 2), ("B", dt), ("h3", dt / 2), ("h1", dt / 2),
           ("h2", dt / 2), ("h0", dt / 2), ("D", dt / 2))
    for g, th in seq:
        qc.compose(unitary(g, float(th), g2, m), inplace=True)
    return qc


def prep_stretched(qc=None):
    qc = qc or QuantumCircuit(NQ)
    code = encode(STRETCHED)
    for q in range(NQ):
        if (code >> q) & 1:
            qc.x(q)
    return qc


def full_circuit(r, dt=None, g2=None, m=None, merge_D=True):
    p = params(g2, m)
    dt = p["dt"] if dt is None else dt
    qc = prep_stretched()
    if r == 0:
        return qc
    if not merge_D:
        for _ in range(r):
            qc.compose(strang_step(dt, p["g2"], p["m"]), inplace=True)
        return qc
    # merged adjacent D half-steps: D/2 [core] D [core] ... D/2
    core = (("h0", dt / 2), ("h2", dt / 2), ("h1", dt / 2), ("h3", dt / 2),
            ("B", dt), ("h3", dt / 2), ("h1", dt / 2), ("h2", dt / 2),
            ("h0", dt / 2))
    qc.compose(unitary("D", dt / 2, p["g2"], p["m"]), inplace=True)
    for k in range(r):
        for g, th in core:
            qc.compose(unitary(g, float(th), p["g2"], p["m"]), inplace=True)
        qc.compose(unitary("D", dt / 2 if k == r - 1 else dt, p["g2"], p["m"]),
                   inplace=True)
    return qc


# ------------------------------------------------------------ exact references

def exact_strang_matrix(dt, g2, m):
    """Exact matrix of ONE Strang step in the circuit's group ordering:
    D/2 . h0/2 . h2/2 . h1/2 . h3/2 . B . h3/2 . h1/2 . h2/2 . h0/2 . D/2
    (h0,h2 commute; h1,h3 commute)."""
    _, T = terms(g2, m)
    order = ["h0", "h2", "h1", "h3"]
    U = expm(-1j * T["D"] * dt / 2)
    for g in order:
        U = expm(-1j * T[g] * dt / 2) @ U
    U = expm(-1j * T["B"] * dt) @ U
    for g in reversed(order):
        U = expm(-1j * T[g] * dt / 2) @ U
    U = expm(-1j * T["D"] * dt / 2) @ U
    return U


def circuit_state(qc):
    """Statevector (4096) of a circuit from |0...0>."""
    return Statevector(qc).data


def to_basis(vec4096, basis):
    cb = basis_to_code(basis)
    return vec4096[cb]


def leakage_prob(vec4096):
    codes, _ = code_index()
    mask = np.ones(N, bool)
    mask[codes] = False
    return float(np.sum(np.abs(vec4096[mask]) ** 2))


# ------------------------------------------------------------ resources

def resources(circ):
    t = transpile(circ, basis_gates=["cz", "rz", "sx", "x", "id"],
                  optimization_level=1, seed_transpiler=7)
    n2 = sum(1 for inst in t.data if inst.operation.num_qubits == 2)
    return {"n_2q": int(n2),
            "depth_2q": int(t.depth(lambda x: x.operation.num_qubits == 2)),
            "depth": int(t.depth())}
