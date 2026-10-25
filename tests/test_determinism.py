"""NFR-1: cùng seed ⇒ cùng chuỗi trải nghiệm, tuyệt đối không sai một bit."""

from __future__ import annotations

import numpy as np
import pytest

from agriwater.env.agriwater_env import AgriWaterEnv
from agriwater.env.config import EnvConfig

pytestmark = pytest.mark.xfail(
    reason="E-14: cần reset()/step() hoạt động trước", strict=True
)


def _rollout(root, actions_cfg: EnvConfig, actions: list[int]) -> tuple[list[np.ndarray], list[float]]:
    env = AgriWaterEnv(actions_cfg, base_dir=str(root))
    obs, _ = env.reset(seed=42)
    observations: list[np.ndarray] = []
    rewards: list[float] = []
    for action in actions:
        obs, reward, terminated, truncated, _ = env.step(action)
        observations.append(obs.copy())
        rewards.append(reward)
        if terminated or truncated:
            obs, _ = env.reset(seed=42)
    return observations, rewards


def test_same_seed_same_trajectory(root) -> None:
    cfg = EnvConfig(scenario="randomized")
    actions = [i % 6 for i in range(200)]
    obs_a, rew_a = _rollout(root, cfg, actions)
    obs_b, rew_b = _rollout(root, cfg, actions)
    assert len(obs_a) == len(obs_b) == 200
    assert all(np.array_equal(a, b) for a, b in zip(obs_a, obs_b))
    assert rew_a == rew_b


def test_different_seed_differs(root) -> None:
    """Chống 'tất định giả': đổi seed phải cho quỹ đạo khác."""
    cfg = EnvConfig(scenario="randomized")
    actions = [i % 6 for i in range(200)]

    def run(seed: int) -> list[np.ndarray]:
        env = AgriWaterEnv(cfg, base_dir=str(root))
        obs, _ = env.reset(seed=seed)
        out = []
        for action in actions:
            obs, *_ = env.step(action)
            out.append(obs.copy())
        return out

    assert not all(np.array_equal(a, b) for a, b in zip(run(1), run(2)))
