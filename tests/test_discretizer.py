"""Rời rạc hóa 480 trạng thái dùng chung cho Q-Learning và Monte Carlo."""

from __future__ import annotations

import numpy as np
import pytest

from agriwater.agents.discretizer import N_STATES, SIZES, Discretizer
from agriwater.env import contract as C


def test_state_count_matches_report() -> None:
    assert SIZES == (4, 5, 3, 2, 2, 2)
    assert N_STATES == 480
    assert C.N_ACTIONS * N_STATES == 2880  # số ô Q


def test_encode_in_range(rng: np.random.Generator) -> None:
    disc = Discretizer()
    for _ in range(1000):
        obs = rng.random(C.OBS_DIM).astype(np.float32)
        state = disc.encode(obs)
        assert 0 <= state < N_STATES


def test_boundary_bins() -> None:
    """Giá trị bằng biên thuộc bin trên: 0.40 → bin 2 của độ ẩm."""
    disc = Discretizer()
    assert disc.components(C.make_obs(soil_moisture=0.19))[1] == 0
    assert disc.components(C.make_obs(soil_moisture=0.20))[1] == 1
    assert disc.components(C.make_obs(soil_moisture=0.40))[1] == 2
    assert disc.components(C.make_obs(soil_moisture=1.00))[1] == 4
    # Ngưỡng dự báo mưa 15 mm và đợt tưới trước 12,5 L
    assert disc.components(C.make_obs(rain_forecast_mm=14.9))[4] == 0
    assert disc.components(C.make_obs(rain_forecast_mm=15.0))[4] == 1
    assert disc.components(C.make_obs(last_irrigation_l=12.5))[5] == 1


def test_decode_is_inverse_of_encode() -> None:
    disc = Discretizer()
    for state in range(N_STATES):
        parts = disc.decode(state)
        packed = 0
        for size, idx in zip(SIZES, parts):
            assert 0 <= idx < size
            packed = packed * size + idx
        assert packed == state


def test_encode_raw_matches_encode() -> None:
    disc = Discretizer()
    obs = C.make_obs(
        growth_stage=2,
        soil_moisture=0.62,
        temperature_c=33.0,
        rain_prob=0.75,
        rain_forecast_mm=20.0,
        last_irrigation_l=15.0,
    )
    assert disc.encode(obs) == disc.encode_raw(
        growth_stage=2,
        soil_moisture=0.62,
        temperature_c=33.0,
        rain_prob=0.75,
        rain_forecast_mm=20.0,
        last_irrigation_l=15.0,
    )


def test_distinct_moisture_bins_differ() -> None:
    disc = Discretizer()
    states = {disc.encode(C.make_obs(soil_moisture=m)) for m in (0.1, 0.3, 0.5, 0.7, 0.9)}
    assert len(states) == 5


def test_rejects_wrong_shape() -> None:
    disc = Discretizer()
    with pytest.raises(ValueError):
        disc.encode(np.zeros(3, dtype=np.float32))
    with pytest.raises(ValueError):
        disc.decode(N_STATES)
