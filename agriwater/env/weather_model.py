"""Sinh thời tiết theo kịch bản JSON.

Chủ sở hữu: **Trưởng** — task E-05 (sinh thời tiết) và E-06 (3 file kịch bản).

Hợp đồng (đã chốt ở G0):
  * Nhận ``np_random`` từ ``gym.Env`` — **không** dùng ``random`` hay
    ``np.random`` toàn cục (NFR-1: tất định theo seed).
  * ``sample()`` trả ``WeatherStep(temperature_c, rain_prob, rain_forecast_mm,
    rainfall_mm, rained)``.
  * Mưa: $z \\sim \\text{Bernoulli}(p)$; nếu $z=1$ thì ``rainfall_mm`` lấy quanh
    ``rain_forecast_mm`` (có nhiễu), ngược lại bằng 0.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from agriwater.env import contract as C
from agriwater.env.config import EnvConfig


class WeatherModel:
    """Bộ sinh thời tiết một chiều theo ngày cho một episode."""

    def __init__(self, scenario: dict[str, Any], np_random: np.random.Generator) -> None:
        self.scenario = scenario
        self.np_random = np_random

    @classmethod
    def from_config(
        cls,
        config: EnvConfig,
        np_random: np.random.Generator,
        base_dir: str | Path = ".",
    ) -> "WeatherModel":
        """Nạp kịch bản từ ``configs/scenarios/<scenario>.json`` (NFR-4)."""
        return cls(config.load_scenario(base_dir), np_random)

    @classmethod
    def from_file(cls, path: str | Path, np_random: np.random.Generator) -> "WeatherModel":
        with Path(path).open(encoding="utf-8") as handle:
            scenario = json.load(handle)
        missing = [k for k in C.REQUIRED_SCENARIO_KEYS if k not in scenario]
        if missing:
            raise ValueError(f"{path} thiếu khóa {missing}")
        return cls(scenario, np_random)

    # -- Cần cài đặt -------------------------------------------------------
    def reset(self) -> None:
        """Đưa bộ sinh về trạng thái đầu episode (E-05)."""
        raise NotImplementedError("E-05: cài đặt reset() của WeatherModel")

    def sample(self) -> C.WeatherStep:
        """Sinh thời tiết của ngày hiện tại rồi tăng bộ đếm nội bộ (E-05).

        Gợi ý cài đặt:
          1. ``temperature_c = self.np_random.uniform(*scenario["temp_range"])``
          2. ``rain_prob = scenario["rain_prob"]`` (hoặc uniform nếu là khoảng)
          3. ``rain_forecast_mm = self.np_random.uniform(*scenario["rain_forecast_range"])``
          4. ``rained = self.np_random.random() < rain_prob``
          5. ``rainfall_mm = max(0.0, forecast * (1 + noise)) if rained else 0.0``
        """
        raise NotImplementedError("E-05: cài đặt sample() của WeatherModel")
