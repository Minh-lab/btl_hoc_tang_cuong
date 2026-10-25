"""NFR-2: môi trường phải đủ nhanh để train — mục tiêu ≥ 10.000 bước/giây."""

from __future__ import annotations

import time

import pytest

from agriwater.env.agriwater_env import AgriWaterEnv
from agriwater.env.config import EnvConfig

pytestmark = [
    pytest.mark.slow,
    pytest.mark.xfail(reason="E-15: cần step() hoạt động trước", strict=True),
]

MIN_STEPS_PER_SECOND = 10_000
N_STEPS = 100_000


def test_throughput(root) -> None:
    env = AgriWaterEnv(EnvConfig(scenario="randomized"), base_dir=str(root))
    env.reset(seed=0)
    actions = [i % 6 for i in range(N_STEPS)]

    start = time.perf_counter()
    for action in actions:
        _, _, terminated, truncated, _ = env.step(action)
        if terminated or truncated:
            env.reset(seed=0)
    elapsed = time.perf_counter() - start

    steps_per_second = N_STEPS / elapsed
    print(f"\n{N_STEPS} bước trong {elapsed:.2f}s ⇒ {steps_per_second:,.0f} bước/giây")
    assert steps_per_second >= MIN_STEPS_PER_SECOND
