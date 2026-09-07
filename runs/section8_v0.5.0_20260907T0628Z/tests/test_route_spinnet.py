"""Unit tests for route 1 (analytic spin-network/dressed-site) Hamiltonian.

Tests the SU(2) single-plaquette Hamiltonian with dynamical two-color staggered
fermions.  All numbers validated against the expected values from the conventions
and limit-check files.
"""

from __future__ import annotations

import numpy as np
import pytest

from su2qc.ham.route_spinnet import (
    build_hamiltonian,
    build_hamiltonian_no_magnetic,
    enumerate_basis,
    pure_electric_check,
    validate_dimensions,
    validate_hermiticity,
)


@pytest.mark.unit
class TestBasisDimensions:
    """Test basis size and sector decomposition."""

    @pytest.mark.parametrize("jmax,expected_dim", [(0.5, 82), (1.0, 152)])
    def test_basis_dimension(self, jmax, expected_dim):
        dim = len(enumerate_basis(jmax))
        assert dim == expected_dim, f"jmax={jmax}: dim={dim} != {expected_dim}"

    @pytest.mark.parametrize("jmax", [0.5])
    def test_sector_decomposition(self, jmax):
        """Sector dims at jmax=0.5: N=0,2,4,6,8 -> 2,20,38,20,2 (only even N)."""
        basis = enumerate_basis(jmax)
        sector_dims = {0: 0, 2: 0, 4: 0, 6: 0, 8: 0}
        for _, n_tuple, _ in basis:
            N = sum(n_tuple)
            if N in sector_dims:
                sector_dims[N] += 1

        expected = {0: 2, 2: 20, 4: 38, 6: 20, 8: 2}
        for N in expected:
            assert sector_dims[N] == expected[N], (
                f"jmax={jmax}: N={N} got {sector_dims[N]} expected {expected[N]}"
            )


@pytest.mark.unit
class TestHermiticity:
    """Test that H is Hermitian."""

    @pytest.mark.parametrize("g2, m, jmax", [
        (1.0, 0.0, 0.5),
        (1.0, 0.1875, 0.5),
        (0.5, 0.2, 0.5),
        (2.0, 0.375, 0.5),
    ])
    def test_H_hermitian(self, g2, m, jmax):
        H, _ = build_hamiltonian(g2, m, jmax)
        H_arr = H.toarray()
        diff = np.max(np.abs(H_arr - H_arr.T.conj()))
        assert diff <= 1e-13, f"H not Hermitian at (g2={g2}, m={m}, jmax={jmax}): max_diff={diff}"


@pytest.mark.unit
class TestCommutator:
    """Test [H, N] = 0 (fermion number conservation)."""

    @pytest.mark.parametrize("g2, m, jmax", [
        (1.0, 0.0, 0.5),
        (1.0, 0.1875, 0.5),
        (0.5, 0.2, 0.5),
    ])
    def test_H_commutes_with_N(self, g2, m, jmax):
        H, basis = build_hamiltonian(g2, m, jmax)
        dim = len(basis)

        # Build total number operator
        N_full = np.zeros((dim, dim))
        for i, (_, n_tuple, _) in enumerate(basis):
            N_full[i, i] = float(sum(n_tuple))

        H_arr = H.toarray()
        comm = H_arr @ N_full - N_full @ H_arr
        max_comm = np.max(np.abs(comm))
        assert max_comm <= 1e-13, f"[H,N] != 0 at (g2={g2}, m={m}, jmax={jmax}): max_comm={max_comm}"


@pytest.mark.unit
class TestPureElectricDegeneracy:
    """Test g2 -> infinity electric-level degeneracies at m=0."""

    def test_electric_degeneracies(self):
        """At g2 -> inf, m=0: degeneracies 16,16,18,16,16 by k=#(j=1/2 links)."""
        H, _ = build_hamiltonian(1e6, 0.0, 0.5)
        evals = np.sort(np.linalg.eigvalsh(H.toarray()))
        unit = 1e6 / 2.0 * 0.75  # (g2/2) * (3/4)
        ks = np.rint(evals / unit).astype(int)
        got = [int(np.sum(ks == k)) for k in range(5)]
        expected = [16, 16, 18, 16, 16]
        assert got == expected, f"Electric degeneracies got {got} expected {expected}"

        # Check relative deviation
        rel = np.max(np.abs(evals - ks * unit)) / unit
        assert rel <= 1e-8, f"Relative dev {rel} > 1e-8"


@pytest.mark.unit
class TestNoMagnetic:
    """Test build_hamiltonian_no_magnetic (electric + mass + hopping only)."""

    @pytest.mark.parametrize("g2, m, jmax", [
        (1.0, 0.0, 0.5),
        (1.0, 0.1875, 0.5),
        (0.5, 0.2, 0.5),
    ])
    def test_no_magnetic_shape(self, g2, m, jmax):
        H_no_mag, _ = build_hamiltonian_no_magnetic(g2, m, jmax)
        expected_dim = 82 if jmax == 0.5 else 152
        assert H_no_mag.shape == (expected_dim, expected_dim)

    @pytest.mark.parametrize("g2, m, jmax", [
        (1.0, 0.0, 0.5),
    ])
    def test_no_mag_hermitian(self, g2, m, jmax):
        H_no_mag, _ = build_hamiltonian_no_magnetic(g2, m, jmax)
        H_arr = H_no_mag.toarray()
        diff = np.max(np.abs(H_arr - H_arr.T.conj()))
        assert diff <= 1e-13

    @pytest.mark.parametrize("g2, m, jmax", [
        (1.0, 0.0, 0.5),
    ])
    def test_no_mag_commuting_N(self, g2, m, jmax):
        H_no_mag, basis = build_hamiltonian_no_magnetic(g2, m, jmax)
        dim = len(basis)
        N_full = np.zeros((dim, dim))
        for i, (_, n_tuple, _) in enumerate(basis):
            N_full[i, i] = float(sum(n_tuple))
        comm = H_no_mag.toarray() @ N_full - N_full @ H_no_mag.toarray()
        max_comm = np.max(np.abs(comm))
        assert max_comm <= 1e-13


@pytest.mark.unit
class TestCorePhysics:
    """Test core physics validations."""

    def test_basis_dimensions_match(self):
        """Basis dimensions match expected values."""
        r05 = validate_dimensions(0.5)
        assert r05["dim_match"], f"jmax=0.5 dim={r05['dim']} != 82"
        r10 = validate_dimensions(1.0)
        assert r10["dim_match"], f"jmax=1.0 dim={r10['dim']} != 152"

    def test_sector_dims(self):
        """Sector decomposition at jmax=0.5 matches expectations."""
        r = validate_dimensions(0.5)
        assert r["sector_N0_match"], f"N=0 sector wrong: {r['sector_dims'][0]}"
        assert r["sector_N2_match"], f"N=2 sector wrong: {r['sector_dims'][2]}"
        assert r["sector_N4_match"], f"N=4 sector wrong: {r['sector_dims'][4]}"
        assert r["sector_N6_match"], f"N=6 sector wrong: {r['sector_dims'][6]}"
        assert r["sector_N8_match"], f"N=8 sector wrong: {r['sector_dims'][8]}"

    def test_pure_electric_check(self):
        """Pure electric degeneracy check from limits.py."""
        pe = pure_electric_check()
        assert pe["ok"], f"Pure electric check failed: {pe}"

    def test_hermiticity_via_validator(self):
        """Hermiticity check via validator."""
        H, _ = build_hamiltonian(1.0, 0.0, 0.5)
        hcheck = validate_hermiticity(H)
        assert hcheck["hermitian"], f"H not Hermitian: max_diff={hcheck['max_diff']}"