"""Môi trường mô phỏng tưới tiêu — lớp lõi của hệ thống.

Chủ sở hữu: **Trưởng** — E-09 (spaces), E-10 (reset), E-11 (step), E-12 (cờ kết
thúc), E-20 (render). Các task này là điều kiện của gate G2/G3.

Trạng thái nội bộ giữ **giá trị thô**; chỉ obs trả ra ngoài mới chuẩn hóa.
"""

from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from agriwater.env import contract as C
from agriwater.env.config import DEFAULT_CONFIG, EnvConfig
from agriwater.env.reward import calculate_reward
from agriwater.env.weather_model import WeatherModel


class AgriWaterEnv(gym.Env):
    """MDP 7 chiều trạng thái, 6 mức tưới, episode 30 ngày."""

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, config: EnvConfig | None = None, *, base_dir: str = ".") -> None:
        super().__init__()
        self.cfg = config or DEFAULT_CONFIG
        self.base_dir = base_dir
        self.scenario = self.cfg.load_scenario(base_dir)

        # Không gian chuẩn hóa: obs luôn trong [0, 1] (NFR-3).
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(C.OBS_DIM,), dtype=np.float32
        )
        self.action_space = spaces.Discrete(C.N_ACTIONS)

        self._crop_type = (
            self.cfg.crop_type if self.cfg.crop_type is not None else self.scenario["crop_type"]
        )
        self._growth_stage = (
            self.cfg.growth_stage
            if self.cfg.growth_stage is not None
            else self.scenario["growth_stage"]
        )

        self._weather: WeatherModel | None = None
        self._day = 0
        self._moisture = float(self.cfg.initial_moisture)
        self._stress_days = 0
        self._last_irrigation_l = 0.0
        self._temperature_c = C.TEMP_MIN_C
        self._rain_prob = 0.0
        self._rain_forecast_mm = 0.0
        self._rainfall_mm = 0.0

    # ------------------------------------------------------------------
    # Vòng đời episode
    # ------------------------------------------------------------------
    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        """Bắt đầu episode mới (E-10).

        Thứ tự bắt buộc:
          1. ``super().reset(seed=seed)`` để có ``self.np_random`` (NFR-1).
          2. Tạo ``WeatherModel.from_config(self.cfg, self.np_random, self.base_dir)``
             rồi ``.reset()``.
          3. ``_day = 0``; ``_moisture = cfg.initial_moisture``;
             ``_stress_days = 0``; ``_last_irrigation_l = 0.0``.
          4. Lấy thời tiết ngày 0 (``self._weather.sample()``) để obs có $T$, $p$, $f$.
          5. ``return self._build_obs(), self._info(water_L=0.0)``.
        """
        super().reset(seed=seed)
        raise NotImplementedError("E-10: cài đặt AgriWaterEnv.reset()")

    def step(
        self, action: int
    ) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        """Một ngày mô phỏng (E-11, E-12).

        Thứ tự bắt buộc — sai thứ tự là sai kết quả reward:
          1. ``prev_state = self._build_obs()`` (env phải giữ $s_t$ **trước** cập nhật).
          2. ``water_L = C.action_to_litres(action)``.
          3. Thời tiết ngày mới: ``w = self._weather.sample()``; lưu $T, p, f$,
             lượng mưa thực tế.
          4. Vật lý: ``self._moisture, drained = physics.update_moisture(...)``.
          5. ``self._day += 1``; ``self._last_irrigation_l = water_L``.
          6. Reward: ``r = calculate_reward(prev_state, action, self._build_obs(), self.cfg)``.
             Lưu ý: reward dùng $p_t$, $f_t$ của **ngày vừa hành động** (trước khi
             thời tiết ngày mới ghi đè).
          7. Cờ: ``stress_days`` cộng/giảm theo ``C.is_stressed(m_next)``;
             ``terminated = stress_days >= cfg.stress_patience``;
             ``truncated = self._day >= cfg.episode_length``.
          8. ``return obs, r, terminated, truncated, self._info(water_L)``.
        """
        raise NotImplementedError("E-11: cài đặt AgriWaterEnv.step()")

    # ------------------------------------------------------------------
    # Tiện ích đã có sẵn — dùng chung cho reset/step
    # ------------------------------------------------------------------
    def _build_obs(self) -> np.ndarray:
        """Ghép obs 7 chiều (đã chuẩn hóa) từ trạng thái nội bộ."""
        return C.make_obs(
            crop_type=int(self._crop_type),
            growth_stage=int(self._growth_stage),
            soil_moisture=self._moisture,
            temperature_c=self._temperature_c,
            rain_prob=self._rain_prob,
            rain_forecast_mm=self._rain_forecast_mm,
            last_irrigation_l=self._last_irrigation_l,
        )

    def _info(self, water_L: float) -> dict[str, Any]:
        """``info`` đúng 6 khóa theo hợp đồng 2.3 — MetricsLogger đọc trực tiếp."""
        return {
            "water_L": float(water_L),
            "crop_stress": bool(C.is_stressed(self._moisture)),
            "moisture": float(self._moisture),
            "growth_stage": int(self._growth_stage),
            "ideal": bool(C.is_ideal(self._moisture, int(self._growth_stage))),
            "stress_days": int(self._stress_days),
        }

    def render(self) -> np.ndarray | None:
        """Vẽ/ghi lại diễn biến độ ẩm của episode (E-20, cắt được nếu trễ gate)."""
        raise NotImplementedError("E-20: cài đặt AgriWaterEnv.render()")
