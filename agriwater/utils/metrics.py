"""Ghi log metric của một episode ra CSV (UC-05, task E-19).

Chỉ dùng thư viện chuẩn nên không tạo phụ thuộc mới; ``pandas`` chỉ cần khi vẽ.

Ví dụ::

    logger = MetricsLogger("logs/random.csv", agent_name="random", scenario="dry")
    obs, info = env.reset(seed=42)
    done = False
    day = 0
    while not done:
        action = agent.act(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        day += 1
        logger.log(episode=0, day=day, obs=obs, action=action, reward=reward, info=info)
        done = terminated or truncated
    logger.close()
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import numpy as np

from agriwater.env import contract as C

FIELDS: tuple[str, ...] = (
    "episode",
    "day",
    "agent",
    "scenario",
    "crop_type",
    "growth_stage",
    "moisture",
    "action",
    "water_L",
    "reward",
    "crop_stress",
    "ideal",
    "stress_days",
)


class MetricsLogger:
    """Ghi từng bước chạy ra ``csv_path`` theo đúng cột của ``FIELDS``."""

    def __init__(
        self,
        csv_path: str | Path,
        *,
        agent_name: str = "agent",
        scenario: str = "randomized",
        flush_every: int = 200,
    ) -> None:
        self.path = Path(csv_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.agent_name = agent_name
        self.scenario = scenario
        self.day = 0
        self._rows_since_flush = 0
        self._flush_every = max(1, flush_every)
        self._handle = self.path.open("w", newline="", encoding="utf-8")
        self._writer = csv.DictWriter(self._handle, fieldnames=FIELDS)
        self._writer.writeheader()

    def log(
        self,
        *,
        episode: int,
        day: int,
        obs: np.ndarray,
        action: int,
        reward: float,
        info: dict[str, Any],
    ) -> None:
        """Ghi một bước; ``obs`` là obs **sau** hành động."""
        obs = np.asarray(obs, dtype=np.float64).ravel()
        self._writer.writerow(
            {
                "episode": episode,
                "day": day,
                "agent": self.agent_name,
                "scenario": self.scenario,
                "crop_type": int(round(obs[C.IDX_CROP_TYPE] * (C.N_CROP_TYPES - 1))),
                "growth_stage": int(info.get("growth_stage", -1)),
                "moisture": float(info.get("moisture", obs[C.IDX_SOIL_MOISTURE])),
                "action": int(action),
                "water_L": float(info.get("water_L", 0.0)),
                "reward": float(reward),
                "crop_stress": int(bool(info.get("crop_stress", False))),
                "ideal": int(bool(info.get("ideal", False))),
                "stress_days": int(info.get("stress_days", 0)),
            }
        )
        self._rows_since_flush += 1
        if self._rows_since_flush >= self._flush_every:
            self._handle.flush()
            self._rows_since_flush = 0

    def close(self) -> None:
        if not self._handle.closed:
            self._handle.flush()
            self._handle.close()

    def __enter__(self) -> "MetricsLogger":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
