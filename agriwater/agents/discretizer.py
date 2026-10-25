"""Rời rạc hóa obs 7 chiều thành 480 trạng thái cho Q-Learning và Monte Carlo.

Chủ sở hữu: **Minh** (E-17). Hai thuật toán bảng **bắt buộc** dùng chung lớp này
để phép so sánh MC ↔ TD là cùng một không gian trạng thái.

Số trạng thái: ``1 × 4 × 5 × 3 × 2 × 2 × 2 = 480`` ($480 \\times 6 = 2880$ ô $Q$).

``crop_type`` chỉ có 1 bin vì mỗi kịch bản cố định một loại cây — chia khoảng
cho chiều này chỉ làm bảng $Q$ loãng vô ích.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from agriwater.env import contract as C

# Biên trong (inner edges) của từng chiều sau khi giải chuẩn hóa.
MOISTURE_EDGES = (0.20, 0.40, 0.60, 0.80)  # → 5 bin
TEMPERATURE_EDGES_C = (25.0, 35.0)  # → 3 bin
RAIN_PROB_EDGES = (0.50,)  # → 2 bin
RAIN_FORECAST_EDGES_MM = (C.RAIN_FORECAST_TRIGGER_MM,)  # 15 mm → 2 bin
LAST_IRRIGATION_EDGES_L = (C.DELAY_TRIGGER_L,)  # 12,5 L → 2 bin

#: Số bin theo thứ tự (growth_stage, moisture, temperature, rain_prob, forecast, last_irr)
SIZES: tuple[int, ...] = (
    C.N_GROWTH_STAGES,
    len(MOISTURE_EDGES) + 1,
    len(TEMPERATURE_EDGES_C) + 1,
    len(RAIN_PROB_EDGES) + 1,
    len(RAIN_FORECAST_EDGES_MM) + 1,
    len(LAST_IRRIGATION_EDGES_L) + 1,
)

#: Tổng số trạng thái rời rạc.
N_STATES: int = int(np.prod(SIZES))


def _bin(value: float, edges: tuple[float, ...]) -> int:
    """Chỉ số bin của ``value``; giá trị bằng biên thuộc bin trên."""
    idx = int(np.digitize(value, edges, right=False))
    return min(idx, len(edges))  # digitize trả len(edges) khi vượt biên cuối


@dataclass(frozen=True)
class Discretizer:
    """Ánh xạ ``obs`` (đã chuẩn hóa) → ``int`` trong ``[0, 480)``."""

    n_states: int = N_STATES

    def __post_init__(self) -> None:
        if self.n_states != N_STATES:
            raise ValueError(f"Chỉ hỗ trợ {N_STATES} trạng thái, nhận {self.n_states}")

    def components(self, obs: np.ndarray) -> tuple[int, ...]:
        """Sáu chỉ số bin (chưa gộp thành một số nguyên) — phục vụ debug."""
        obs = np.asarray(obs, dtype=np.float64).ravel()
        if obs.size != C.OBS_DIM:
            raise ValueError(f"obs phải có {C.OBS_DIM} chiều, nhận {obs.size}")
        growth_stage = int(
            np.clip(round(obs[C.IDX_GROWTH_STAGE] * (C.N_GROWTH_STAGES - 1)), 0, C.N_GROWTH_STAGES - 1)
        )
        return (
            growth_stage,
            _bin(float(obs[C.IDX_SOIL_MOISTURE]), MOISTURE_EDGES),
            _bin(C.denorm_temperature(float(obs[C.IDX_TEMPERATURE])), TEMPERATURE_EDGES_C),
            _bin(float(obs[C.IDX_RAIN_PROB]), RAIN_PROB_EDGES),
            _bin(C.denorm_rain_forecast(float(obs[C.IDX_RAIN_FORECAST])), RAIN_FORECAST_EDGES_MM),
            _bin(C.denorm_irrigation(float(obs[C.IDX_LAST_IRRIGATION])), LAST_IRRIGATION_EDGES_L),
        )

    def encode(self, obs: np.ndarray) -> int:
        """Mã hóa obs thành một số nguyên duy nhất trong ``[0, n_states)``."""
        state = 0
        for size, idx in zip(SIZES, self.components(obs)):
            state = state * size + idx
        return int(state)

    def encode_raw(
        self,
        *,
        growth_stage: int,
        soil_moisture: float,
        temperature_c: float,
        rain_prob: float,
        rain_forecast_mm: float,
        last_irrigation_l: float,
        crop_type: int = 0,
    ) -> int:
        """Mã hóa từ giá trị thô — tiện cho test và cho Baseline."""
        obs = C.make_obs(
            crop_type=crop_type,
            growth_stage=growth_stage,
            soil_moisture=soil_moisture,
            temperature_c=temperature_c,
            rain_prob=rain_prob,
            rain_forecast_mm=rain_forecast_mm,
            last_irrigation_l=last_irrigation_l,
        )
        return self.encode(obs)

    def decode(self, state: int) -> tuple[int, ...]:
        """Giải mã về 6 chỉ số bin (nghịch đảo của ``components``)."""
        if not 0 <= state < self.n_states:
            raise ValueError(f"state phải trong [0, {self.n_states}), nhận {state}")
        digits = [0] * len(SIZES)
        for i in range(len(SIZES) - 1, -1, -1):
            state, digits[i] = divmod(state, SIZES[i])
        return tuple(digits)
