"""The 12-qubit, three-bits-per-vertex L12 encoding.

Qubit ``3*v,3*v+1,3*v+2`` is respectively (first link, second link,
matter).  Integers use q0 as the least significant bit; displayed Qiskit
strings consequently read q11 ... q0.
"""
from __future__ import annotations

from functools import lru_cache
from numbers import Integral
from su2qc.ham.route_spinnet import enumerate_basis, _VLINKS

N_QUBITS = 12

def _bit(code, q):
    return (int(code) >> q) & 1

@lru_cache(maxsize=1)
def _maps():
    out = {}
    for label in enumerate_basis(.5):
        js, ns, tag = label
        bits = 0
        for v, (la, lb) in enumerate(_VLINKS):
            a, b = int(round(2*js[la])), int(round(2*js[lb]))
            # In this truncation the link bit is 0/1 == j 0/1/2.
            bits |= a << (3*v)
            bits |= b << (3*v+1)
            bits |= (1 if ns[v] == 2 else 0) << (3*v+2)
        out[bits] = label
    return out

def encode(label) -> int:
    """Encode a canonical route-spinnet basis label as a 12-bit integer."""
    for code, candidate in _maps().items():
        if candidate == label:
            return code
    raise ValueError(f"not a physical L12 label: {label!r}")

def decode(bits):
    """Decode an integer (or a q11...q0 bit string) or return ``None``."""
    if isinstance(bits, str):
        if len(bits) != 12 or any(c not in "01" for c in bits):
            return None
        bits = int(bits, 2)
    if not isinstance(bits, Integral) or not 0 <= bits < 4096:
        return None
    return _maps().get(bits)

def physical_codes() -> list[int]:
    return sorted(_maps())

def leakage_flags(bits):
    """Return vertex leakage and four endpoint-consistency flags."""
    if isinstance(bits, str):
        try: bits = int(bits, 2)
        except ValueError: return {"vertex": (True,)*4, "link": (True,)*4}
    vertex = tuple(bool(_bit(bits, 3*v) ^ _bit(bits, 3*v+1)) and bool(_bit(bits, 3*v+2))
                   for v in range(4))
    # Compare the two endpoint copies, using the fixed vertex incidence order.
    link = []
    for l in range(4):
        copies = [(3*v + k) for v, pair in enumerate(_VLINKS) for k, ll in enumerate(pair) if ll == l]
        link.append(bool(_bit(bits, copies[0]) ^ _bit(bits, copies[1])))
    return {"vertex": vertex, "link": tuple(link)}

def is_physical(bits) -> bool:
    f = leakage_flags(bits)
    return not any(f["vertex"]) and not any(f["link"])
