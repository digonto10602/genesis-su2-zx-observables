"""Phase 4: route logical L12 circuits to a Heron-class target and verify.

  route(circ, backend, opt=3, seed=7) -> (isa_circ, layout_info)
  routed_equivalence(logical, isa) -> 1 - |<psi_routed|psi_logical>| including
        the final layout permutation (statevector on the 12 logical qubits).
  routed_resources(isa) -> dict(n_2q, depth_2q, depth)
  pyzx_tp(circ) -> circuit after the monograph's topology-preserving PyZX pass
        (reused from the repo's src/su2zx/compiler_study.py if importable).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.transpiler import CouplingMap

RUN = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
REPO = os.path.dirname(os.path.dirname(RUN))
if os.path.join(REPO, "src") not in sys.path:
    sys.path.insert(0, os.path.join(REPO, "src"))

NATIVE = ["cz", "rz", "sx", "x", "id"]


def fake_heron():
    from qiskit_ibm_runtime.fake_provider import FakeTorino
    return FakeTorino()


def route(circ, backend=None, opt=3, seed=7, initial_layout=None):
    backend = backend or fake_heron()
    isa = transpile(circ, backend=backend, optimization_level=opt,
                    seed_transpiler=seed, initial_layout=initial_layout)
    lay = isa.layout
    init = [lay.initial_layout[q] for q in circ.qubits] if lay else list(range(12))
    final = None
    if lay is not None and lay.final_layout is not None:
        fl = lay.final_layout
        final = [fl[q] for q in isa.qubits]
    return isa, {"initial_physical": [int(x) for x in init],
                 "final_index_layout": [int(x) for x in isa.layout.final_index_layout()]
                 if lay else list(range(12))}


def routed_resources(isa):
    n2 = sum(1 for inst in isa.data if inst.operation.num_qubits == 2
             and inst.operation.name != "barrier")
    return {"n_2q": int(n2),
            "depth_2q": int(isa.depth(lambda x: x.operation.num_qubits == 2)),
            "depth": int(isa.depth())}


def routed_equivalence(logical, isa):
    """1 - |<routed|logical>| with the routed state pulled back through
    final_index_layout to the logical qubit order (statevector, no measure)."""
    from qiskit.quantum_info import Operator
    psi_l = Statevector(logical).data
    # reduce ISA circuit to only its active physical qubits
    fil = isa.layout.final_index_layout()
    active = sorted({isa.find_bit(q).index for inst in isa.data for q in inst.qubits}
                    | set(int(x) for x in fil))
    idx = {p: k for k, p in enumerate(active)}
    small = QuantumCircuit(len(active))
    for inst in isa.data:
        if inst.operation.name in ("barrier", "measure", "delay"):
            continue
        small.append(inst.operation, [idx[isa.find_bit(q).index] for q in inst.qubits])
    psi_r = Statevector(small).data
    # logical qubit i sits at physical fil[i]
    order = [idx[fil[i]] for i in range(logical.num_qubits)]  # small-qubit per logical
    # permute psi_r so that qubit k of result = logical k
    n = len(active)
    psi_r = psi_r.reshape([2] * n)  # axis 0 = qubit n-1 (qiskit little endian)
    # axes: qiskit bit q corresponds to axis n-1-q
    perm_axes = [n - 1 - order[i] for i in range(logical.num_qubits)][::-1]
    rest = [a for a in range(n) if a not in perm_axes]
    psi_r = np.transpose(psi_r, rest + perm_axes).reshape(-1, 2 ** logical.num_qubits)
    # idle ancilla qubits are |0>: take the row where rest-axes are all zero
    vec = psi_r[0]
    return float(1.0 - abs(np.vdot(vec, psi_l)))


def pyzx_pass(circ, strategy="basic"):
    """The monograph's PyZX pipeline (repo src/su2zx/core.py) with its dense
    12-qubit Operator equivalence check replaced by a statevector check on
    the 82 physical codes (done by the caller via routed_equivalence-style
    comparison). strategy: 'basic' (topology-preserving), 'full_reduce'."""
    from qiskit import qasm2
    import pyzx as zx
    denominator = zx.settings.float_to_fraction_max_denominator
    try:
        zx.settings.float_to_fraction_max_denominator = 2 ** 40
        zxc = zx.Circuit.from_qasm(qasm2.dumps(circ))
    finally:
        zx.settings.float_to_fraction_max_denominator = denominator
    if strategy == "basic":
        cand = zx.optimize.basic_optimization(zxc.copy(), do_swaps=False, quiet=True)
    elif strategy == "full_reduce":
        g = zxc.to_graph()
        zx.simplify.full_reduce(g, quiet=True)
        cand = zx.extract.extract_circuit(g.copy(), up_to_perm=False,
                                          quiet=True).to_basic_gates()
    else:
        raise ValueError(strategy)
    return qasm2.loads(cand.to_qasm())


def state_equivalence(a, b):
    """1 - |<a|b>| for two same-width circuits from |0>."""
    va, vb = Statevector(a).data, Statevector(b).data
    return float(1.0 - abs(np.vdot(va, vb)))


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(RUN, "src"))
    from su2qc.circuits import strang_l12 as sl
    b = fake_heron()
    qc = sl.full_circuit(1)
    isa, lay = route(qc, b)
    print(routed_resources(isa), lay)
    print("equiv", routed_equivalence(qc, isa))
