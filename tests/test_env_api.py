"""API môi trường: spaces, check_env, hợp đồng reset/step (E-13)."""

from __future__ import annotations

import numpy as np
import pytest
from gymnasium.utils.env_checker import check_env

from agriwater.env import contract as C
from agriwater.env.agriwater_env import AgriWaterEnv
from agriwater.env.config import EnvConfig

# Test không cần reset()/step() thì phải xanh ngay; test cần tới chúng thì xfail.
_needs_env_loop = pytest.mark.xfail(
    reason="E-10..E-12: reset()/step() chưa cài đặt (Trưởng)", strict=True
)


def test_spaces(root) -> None:
    env = AgriWaterEnv(EnvConfig(scenario="dry"), base_dir=str(root))
    assert env.observation_space.shape == (C.OBS_DIM,)
    assert env.action_space.n == C.N_ACTIONS
    assert env.observation_space.dtype == np.float32


@_needs_env_loop
def test_passes_gymnasium_check_env(root) -> None:
    check_env(AgriWaterEnv(EnvConfig(scenario="randomized"), base_dir=str(root)))


@_needs_env_loop
def test_reset_contract(root) -> None:
    env = AgriWaterEnv(EnvConfig(scenario="dry"), base_dir=str(root))
    obs, info = env.reset(seed=42)
    assert obs.shape == (C.OBS_DIM,) and obs.dtype == np.float32
    assert ((obs >= 0.0) & (obs <= 1.0)).all()
    assert set(info) == {"water_L", "crop_stress", "moisture", "growth_stage", "ideal", "stress_days"}


@_needs_env_loop
def test_step_contract_and_bounds(root) -> None:
    env = AgriWaterEnv(EnvConfig(scenario="stormy"), base_dir=str(root))
    env.reset(seed=7)
    for step in range(60):
        obs, reward, terminated, truncated, info = env.step(step % C.N_ACTIONS)
        assert obs.shape == (C.OBS_DIM,)
        assert ((obs >= 0.0) & (obs <= 1.0)).all(), "obs ra khỏi [0, 1]"
        assert isinstance(reward, float)
        assert isinstance(terminated, bool) and isinstance(truncated, bool)
        assert {"water_L", "crop_stress", "moisture", "growth_stage", "ideal", "stress_days"} <= set(info)
        if terminated or truncated:
            env.reset(seed=step)
