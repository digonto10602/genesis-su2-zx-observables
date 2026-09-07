"""Exact gauge-invariant block unitaries and Strang circuits for L12."""
from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import Diagonal, UnitaryGate
from su2qc.ham import route_spinnet as rs
from su2qc.encodings.l12 import encode, physical_codes

N = 4096
_GROUPS = ("D", "h0", "h1", "h2", "h3", "B")

def _params(g2=None, m=None):
    vals = {"g2": 1.0, "m": .1875, "dt": .4, "r_max": 3}
    p = Path("physics/window.json")
    if p.exists():
        vals.update(json.loads(p.read_text()))
    if g2 is not None: vals["g2"] = g2
    if m is not None: vals["m"] = m
    return vals

@lru_cache(maxsize=8)
def _data(g2, m):
    Hs, basis = rs.build_hamiltonian(g2, m, .5)
    H0, _ = rs.build_hamiltonian_no_magnetic(g2, m, .5)
    H, H0 = Hs.toarray(), H0.toarray()
    D = np.diag(np.diag(H0))
    B = H - H0
    hs = []
    for l in range(4):
        a = np.zeros_like(H)
        for i, li in enumerate(basis):
            for j, lj in enumerate(basis):
                # A hopping matrix element changes exactly the link and its endpoints.
                if all((k == l or (li[0][k] == lj[0][k] and li[1][k] == lj[1][k])) for k in range(4)):
                    if li[0][l] != lj[0][l] or li[1][l] != lj[1][l]:
                        # The no-magnetic matrix has only hopping off diagonal.
                        a[i, j] = H0[i, j]
        hs.append(a)
    return basis, (D, *hs, B)

def _embed(M):
    out = np.zeros((N, N), complex)
    codes = physical_codes()
    out[np.ix_(codes, codes)] = M
    return out

def _embedded_exponential(M, theta):
    """Exponentiate an embedded matrix without an unnecessary 4096x4096 expm."""
    out = np.eye(N, dtype=complex)
    nz = np.flatnonzero(np.any(np.abs(M) > 1e-14, axis=1))
    seen = set()
    for i in nz:
        if i in seen: continue
        js = np.flatnonzero(np.abs(M[i]) > 1e-14)
        block = sorted(set([int(i), *map(int, js)]))
        if len(block) == 2:
            out[np.ix_(block, block)] = expm(-1j * theta * M[np.ix_(block, block)])
            seen.update(block)
    return out

def _local_matrix(l, A, basis):
    """Extract the endpoint-local hopping block, including wrap-link parity."""
    s, t = rs.LINK_ST[l]
    endpoint = list(range(3*s, 3*s+3)) + list(range(3*t, 3*t+3))
    extras = []
    if l == 3:
        # Their b bits become the two parities after CNOT(a,b) below.
        extras = [4, 7]
    qargs = endpoint + extras
    dim = 1 << len(endpoint)
    base = np.zeros((dim, dim), complex)
    codes = physical_codes()
    pos = {c: i for i, c in enumerate(codes)}
    for ii, ci in enumerate(codes):
        for jj, cj in enumerate(codes):
            if any(((ci >> q) & 1) != ((cj >> q) & 1) for q in range(N.bit_length()-1) if q not in endpoint):
                continue
            x = sum(((ci >> q) & 1) << k for k, q in enumerate(endpoint))
            y = sum(((cj >> q) & 1) << k for k, q in enumerate(endpoint))
            val = A[pos[ci], pos[cj]]
            if l == 3:
                p = ((ci >> 3) & 1) ^ ((ci >> 4) & 1) ^ ((ci >> 6) & 1) ^ ((ci >> 7) & 1)
                val *= (-1)**p
            if abs(val) > 1e-14:
                base[x, y] = val
    # Hermitian completion protects against numerical duplicate extraction.
    base = (base + base.conj().T) / 2
    if not extras:
        return qargs, base
    out = np.zeros((1 << len(qargs), 1 << len(qargs)), dtype=complex)
    for e in range(4):
        p = ((e >> 0)&1) ^ ((e >> 1)&1)
        out[e*dim:(e+1)*dim, e*dim:(e+1)*dim] = ((-1)**p) * base
    return qargs, out

@lru_cache(maxsize=32)
def unitary(group: str, theta: float, g2: float = 1.0, m: float = .1875):
    """Return a no-measurement 12-qubit circuit for ``exp(-i theta T)``."""
    if group not in _GROUPS: raise ValueError(group)
    basis, mats = _data(float(g2), float(m)); M = mats[_GROUPS.index(group)]
    qc = QuantumCircuit(12, name=f"U_{group}")
    if group == "D":
        diag = np.ones(N, complex)
        codes = physical_codes()
        diag[codes] = np.exp(-1j * theta * np.diag(M))
        qc.append(Diagonal(diag), range(12))
    elif group.startswith("h"):
        l = int(group[1]); qargs, local = _local_matrix(l, M, basis)
        if l == 3:
            qc.cx(3, 4); qc.cx(6, 7)
        qc.append(UnitaryGate(expm(-1j * theta * local)), qargs)
        if l == 3:
            qc.cx(6, 7); qc.cx(3, 4)
    else:
        qc.append(UnitaryGate(_embedded_exponential(_embed(M), theta)), range(12))
    return qc

def strang_step(theta_dict=None, dt=None, g2=None, m=None):
    p = _params(g2, m); dt = p["dt"] if dt is None else dt
    th = theta_dict or {"D":dt/2, "h0":dt/2, "h1":dt/2, "h2":dt/2, "h3":dt/2, "B":dt}
    qc = QuantumCircuit(12)
    for g in ("D","h0","h2","h1","h3","B","h1","h3","h0","h2","D"):
        qc.compose(unitary(g, th[g], p["g2"], p["m"]), inplace=True)
    return qc

def full_circuit(r=1, dt=None, g2=None, m=None):
    p = _params(g2, m); qc = QuantumCircuit(12)
    # Canonical stretched-string label from the run specification.
    code = encode(((0.,.5,.5,.5),(1,1,0,2),0))
    for q in range(12):
        if code >> q & 1: qc.x(q)
    for _ in range(int(r)): qc.compose(strang_step(dt=dt,g2=p["g2"],m=p["m"]), inplace=True)
    return qc

def resources(circ):
    t = transpile(circ, basis_gates=["cz","rz","sx","x","id"], optimization_level=1)
    counts = t.count_ops()
    return {"n_2q": int(counts.get("cz", 0)), "depth_2q": int(t.depth(lambda x: x.operation.num_qubits == 2))}

# Descriptive alias used by the G3 checks.
U_T = unitary
