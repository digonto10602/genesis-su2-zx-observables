import numpy as np

from su2qc.ham import route_gausskernel as route2
from su2qc.ham import route_spinnet as route1


def _poly_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def _predicted_generating_function():
    # For the three allowed link spins, Tr(T^4) = 3a^4 + 24a^2b^2 + 8b^4,
    # where a=1+x^2 and b=x, derived in predictions_C0.md.
    a = [1, 0, 1]
    a2 = _poly_mul(a, a)
    a4 = _poly_mul(a2, a2)
    a2b2 = _poly_mul(a2, [0, 0, 1])
    b4 = [0, 0, 0, 0, 1]
    out = [0] * 9
    for i, value in enumerate(a4): out[i] += 3 * value
    for i, value in enumerate(a2b2): out[i] += 24 * value
    for i, value in enumerate(b4): out[i] += 8 * value
    return out


def test_jmax1_sector_counts_match_independent_transfer_polynomial():
    expected = {0: 3, 2: 36, 4: 74, 6: 36, 8: 3}
    coeff = _predicted_generating_function()
    assert {n: coeff[n] for n in range(0, 9, 2)} == expected
    H1, labels1 = route1.build_hamiltonian(1.0, 0.1, 1.0)[:2]
    labels2, P2 = route2._basis(1.0)
    assert H1.shape == (152, 152)
    assert len(labels1) == len(labels2) == 152
    assert {n: sum(sum(x[1]) == n for x in labels1) for n in expected} == expected
    assert {n: sum(sum(x[1]) == n for x in labels2) for n in expected} == expected
    assert np.max(np.abs((P2.conj().T @ P2).toarray() - np.eye(152))) < 1e-12
