import numpy as np
import pytest

from src.su2qc.ham.route_gausskernel import (
    _basis, build_hamiltonian, gauss_commutator_norms, get_state, kernel_dimension,
)


pytestmark = pytest.mark.unit


def test_kernel_dimensions_and_number_sectors():
    H, labels, P = build_hamiltonian(1.0, 0.0, 0.5)
    counts = {n: sum(sum(x[1]) == n for x in labels) for n in range(9)}
    print("kernel dims:", len(labels))
    print("N sectors:", counts)
    assert len(labels) == 82
    assert counts == {0: 2, 1: 0, 2: 20, 3: 0, 4: 38, 5: 0, 6: 20, 7: 0, 8: 2}
    assert np.max(np.abs((P.conj().T @ P).toarray() - np.eye(82))) < 1e-12

    # Legacy D1 validates the jmax=1 kernel, not its unimplemented Hamiltonian.
    assert kernel_dimension(1.0) == 152
    labels1, P1 = _basis(1.0)
    print("jmax=1 kernel dim:", len(labels1))
    assert len(labels1) == 152
    assert np.max(np.abs((P1.conj().T @ P1).toarray() - np.eye(152))) < 1e-12


def test_hermiticity_and_gauss_diagnostics():
    H, labels, _ = build_hamiltonian(0.73, 0.19, 0.5)
    err = np.max(np.abs((H - H.getH()).data)) if (H - H.getH()).nnz else 0.0
    print("hermiticity:", err)
    assert err <= 1e-13
    norms = gauss_commutator_norms(0.5)
    print("Gauss commutator norms:", norms)
    assert max(norms.values()) <= 1e-12


def test_pure_electric_clusters_and_stretched_label():
    H, labels, _ = build_hamiltonian(1e6, 0.0, 0.5)
    vals, mult = np.unique(np.round(H.diagonal().real, 7), return_counts=True)
    print("electric clusters:", list(zip(vals, mult)))
    assert np.array_equal(mult, [16, 16, 18, 16, 16])
    stretched = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)
    assert sum(x == stretched for x in labels) == 1
    assert get_state(stretched, labels) >= 0
