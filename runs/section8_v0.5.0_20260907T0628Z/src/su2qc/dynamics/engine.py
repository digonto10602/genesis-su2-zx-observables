"""Exact-dynamics engine for the 82-state (jmax=0.5) / 152-state (jmax=1) SU(2) plaquette.

evolve(H, psi0, times) -> array of states (dense expm on 82-dim; use scipy.linalg.expm
of -iH dt step matrix, cumulative).
self_check(g2, m, jmax, t_max) -> dict with expm_krylov_dev, energy_drift, N_drift.
"""

import numpy as np
from scipy.sparse.linalg import expm_multiply
from scipy.linalg import expm
from su2qc.ham.route_spinnet import build_hamiltonian
import su2qc.conventions as cv


def evolve(H, psi0, times):
    """Evolve psi0 under sparse H at times t (array).

    Returns array of shape (len(times), dim) with state vectors at each time.
    Uses dense expm of -i*H*dt per step (cumulative), since the Hilbert space
    is small (82 or 152 dims).
    """
    psi0 = np.asarray(psi0, dtype=complex).flatten()
    psi0 = psi0 / np.linalg.norm(psi0)  # normalize

    # Exact evolution via one eigendecomposition (H Hermitian, tiny):
    # psi(t) = V exp(-i E t) V^dag psi0.  Exact for arbitrary time grids.
    from scipy.linalg import eigh
    E, V = eigh(H.toarray())
    c0 = V.conj().T @ psi0
    times = np.asarray(times, dtype=float)
    phases = np.exp(-1j * np.outer(times, E))          # (T, dim)
    return (phases * c0[None, :]) @ V.T


def self_check(g2: float, m: float, jmax: float, t_max: float) -> dict:
    """Verify expm vs Krylov conservation.

    Returns dict with:
      expm_krylov_dev: max ||psi_dense(t) - psi_krylov(t)||_inf over ~21 times on [0, t_max]
      energy_drift: max |<H>(t) - <H>(0)|
      N_drift: max |<N>(t) - <N>(0)|
    Targets: <=1e-9, <=1e-10, <=1e-10.
    """
    H, basis = build_hamiltonian(g2, m, jmax)
    dim = H.shape[0]

    # Diagonal energy: electric + mass
    # Electric: (g2/2) * sum_l j_l(j_l+1)
    # Mass: m * sum_v parity_v n_v; parity = (+1, -1, +1, -1)
    parity = cv.PARITY  # (+1, -1, +1, -1)

    # Build per-state diagonal energy and fermion number
    H_diag = np.zeros(dim)
    N_diag = np.zeros(dim)

    for i, (j_tuple, n_tuple, _) in enumerate(basis):
        # Electric term
        el = 0.0
        for j in j_tuple:
            el += j * (j + 1.0)
        H_diag[i] = (g2 / 2.0) * el

        # Mass term + fermion number
        mass = m * sum(parity[v] * n_tuple[v] for v in range(4))
        H_diag[i] += mass
        N_diag[i] = float(sum(n_tuple))

    # Initial state: stretched string |((0.0,0.5,0.5,0.5),(1,1,0,2),0)>
    stretched_label = ((0.0, 0.5, 0.5, 0.5), (1, 1, 0, 2), 0)
    if stretched_label in set(basis):
        psi0_idx = basis.index(stretched_label)
    else:
        psi0_idx = 0

    psi0 = np.zeros(dim, dtype=complex)
    psi0[psi0_idx] = 1.0

    # Sample ~21 times
    n_times = 21
    times = np.linspace(0, t_max, n_times)

    # Dense evolution using expm per step
    psi_dense = np.zeros((n_times, dim), dtype=complex)
    psi_dense[0] = psi0

    for k in range(1, n_times):
        dt = times[k] - times[k - 1]
        if abs(dt) < 1e-15:
            psi_dense[k] = psi_dense[k - 1]
            continue
        U = expm(-1j * H.toarray() * dt)
        psi_dense[k] = U @ psi_dense[k - 1]

    # Krylov evolution (sparse expm_multiply)
    # expm_multiply(A, B, start, stop) computes expm(A * t) @ B for t in [start, stop]
    psi_krylov = np.zeros((n_times, dim), dtype=complex)
    psi_krylov[0] = psi0

    for k in range(1, n_times):
        A = -1j * H.tocsc() * float(times[k])
        psi_krylov[k] = expm_multiply(A, psi0)

    # Compute inf-norm deviation
    dev = np.max(np.abs(psi_dense - psi_krylov), axis=1)
    expm_krylov_dev = float(np.max(dev))

    # Compute energy <H>(t) = psi^dagger H psi
    H_arr = H.toarray()
    energies = np.zeros(n_times)
    for k in range(n_times):
        psi = psi_dense[k]
        exp_val = np.real(np.conj(psi) @ (H_arr @ psi))
        energies[k] = exp_val

    energy_drift = float(np.max(np.abs(energies - energies[0])))

    # Fermion number expectation
    N_expect = np.zeros(n_times)
    for k in range(n_times):
        psi = psi_dense[k]
        N_exp = np.sum(np.abs(psi) ** 2 * N_diag)
        N_expect[k] = float(N_exp)

    N_drift = float(np.max(np.abs(N_expect - N_expect[0])))

    return {
        "expm_krylov_dev": expm_krylov_dev,
        "energy_drift": energy_drift,
        "N_drift": N_drift,
    }