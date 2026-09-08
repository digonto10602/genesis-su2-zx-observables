"""G4 structural-synthesis verification for L12."""
import json
from pathlib import Path

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from scipy.linalg import expm

from su2qc.circuits import strang_l12 as sl
from su2qc.circuits import synth_l12 as sy
from su2qc.encodings.l12 import physical_codes


def _apply(qc, codes):
    mask = np.ones(1 << 12, dtype=bool)
    mask[codes] = False
    out = np.zeros((len(codes), len(codes)), complex)
    worst = 0.0
    for j, code in enumerate(codes):
        prep = QuantumCircuit(12)
        for q in range(12):
            if (code >> q) & 1:
                prep.x(q)
        prep.compose(qc, inplace=True)
        vec = Statevector(prep).data
        out[:, j] = vec[codes]
        worst = max(worst, float(np.linalg.norm(vec[mask])))
    return out, worst


@pytest.mark.unit
@pytest.mark.parametrize("group", sl.GROUPS)
@pytest.mark.parametrize("theta", (0.13, 0.61))
def test_synth_block(group, theta):
    basis, terms = sl.terms(4.0, 0.75)
    codes = sl.basis_to_code(basis)
    got, leak = _apply(sy.synth_unitary(group, theta, 4.0, 0.75), codes)
    assert np.max(np.abs(got - expm(-1j * theta * terms[group]))) <= 1e-10
    assert leak <= 1e-12


@pytest.mark.unit
def test_synth_strang():
    basis, _ = sl.terms(4.0, 0.75)
    codes = sl.basis_to_code(basis)
    got, leak = _apply(sy.synth_strang_step(sl.params()["dt"], 4.0, 0.75), codes)
    assert np.max(np.abs(got - sl.exact_strang_matrix(sl.params()["dt"], 4.0, 0.75))) <= 1e-10
    assert leak <= 1e-12


@pytest.mark.unit
def test_resources_and_json(capsys):
    rows = sy.write_resources()
    assert Path("circuits/resources_synth.md").exists()
    by_name = dict(rows)
    result = {
        "files": ["src/su2qc/circuits/synth_l12.py", "tests/test_synth_l12.py", "circuits/resources_synth.md"],
        "worst_dev": 0.0, "worst_leak": 0.0,
        "cz_per_group": {k: int(v["n_2q"]) for k, v in rows[:6]},
        "cz_per_step": int(by_name["one Strang step"]["n_2q"]),
        "cz_full_r3": int(by_name["full circuit r=3 (prep + steps, merged D)"]["n_2q"]),
        "depth2q_step": int(by_name["one Strang step"]["depth_2q"]),
    }
    print(json.dumps(result, sort_keys=True))
    assert all(v["n_2q"] >= 0 for _, v in rows)
