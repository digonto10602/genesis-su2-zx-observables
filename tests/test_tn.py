from __future__ import annotations

import numpy as np

from su2zx.core import circuit_state, strang_evolution
from su2zx.tn_study import mps_state


def test_cpu_mps_matches_statevector_for_two_plaquettes() -> None:
    circuit = strang_evolution(2, 2.0, 0.16, 2, initial_ones=(1,))
    mps, _ = mps_state(circuit, max_bond=8, tolerance=1e-14)
    np.testing.assert_allclose(mps, circuit_state(circuit), atol=1e-10)
