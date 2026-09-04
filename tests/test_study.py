from __future__ import annotations

import json

import numpy as np

from su2zx.study import generate_data


def test_small_data_generation(tmp_path) -> None:
    config = {
        "num_plaquettes": 5,
        "x": 2.0,
        "initial_ones": [2],
        "primary_repetitions": 2,
        "trotter_repetitions": [1, 2],
        "time_min": 0.0,
        "time_max": 0.08,
        "time_points": 3,
        "hardware_times": [0.0, 0.08],
    }
    frame, probabilities = generate_data(config, tmp_path)
    assert len(frame) == 9
    assert len(probabilities) == 2 * 2 * 32
    assert np.isfinite(frame.select_dtypes(include=[float, int]).to_numpy()).all()
    summary = json.loads((tmp_path / "data" / "physics_summary.json").read_text())
    np.testing.assert_allclose(summary["initial_energy"], 3.0, atol=1e-12)
    assert summary["max_six_basis_energy_error"] < 1e-10
