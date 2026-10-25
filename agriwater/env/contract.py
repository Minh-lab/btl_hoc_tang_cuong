"""Hợp đồng giao diện dùng chung cho môi trường và agent.

Đây là **nguồn sự thật duy nhất** về chỉ số trạng thái, hằng số vật lý, trọng số
reward và quy ước chuẩn hóa của AgriWater-RL.

Quy ước (gate G0 — muốn đổi phải có chấp thuận của cả Minh và Trưởng):
  * ``obs`` là ``np.float32[7]``, **đã chuẩn hóa về [0, 1]**.
  * ``action`` là ``int`` trong ``range(6)``, index của ``WATER_LEVELS``.
  * Một bước = một ngày; episode dài ``EPISODE_LENGTH`` ngày.
"""

from __future__ import annotations

from typing import Final, NamedTuple

import numpy as np

SCHEMA_VERSION: Final[str] = "1.0.0"

# ---------------------------------------------------------------------------
# 1. Không gian trạng thái — 7 chiều, đã chuẩn hóa
# ---------------------------------------------------------------------------
IDX_CROP_TYPE: Final[int] = 0
IDX_GROWTH_STAGE: Final[int] = 1
IDX_SOIL_MOISTURE: Final[int] = 2
IDX_TEMPERATURE: Final[int] = 3
IDX_RAIN_PROB: Final[int] = 4
IDX_RAIN_FORECAST: Final[int] = 5
IDX_LAST_IRRIGATION: Final[int] = 6

OBS_DIM: Final[int] = 7
OBS_NAMES: Final[tuple[str, ...]] = (
    "crop_type",
    "growth_stage",
    "soil_moisture",
    "temperature",
    "rain_probability",
    "rain_forecast_mm",
    "last_irrigation",
)

# Miền thô trước khi chuẩn hóa
N_CROP_TYPES: Final[int] = 4
N_GROWTH_STAGES: Final[int] = 4
TEMP_MIN_C: Final[float] = 15.0
TEMP_MAX_C: Final[float] = 45.0
R_MAX_MM: Final[float] = 50.0
IRRIGATION_MAX_L: Final[float] = 25.0

# Ngưỡng độ ẩm đất
WILT_POINT: Final[float] = 0.20
IDEAL_LO: Final[float] = 0.40
IDEAL_HI: Final[float] = 0.70
IDEAL_LO_FLOWER: Final[float] = 0.50
IDEAL_HI_FLOWER: Final[float] = 0.75
FLOWER_STAGE: Final[int] = 2
FIELD_CAPACITY: Final[float] = 0.85

# Hành động và thời lượng episode
WATER_LEVELS: Final[tuple[int, ...]] = (0, 5, 10, 15, 20, 25)  # lít, index = action
N_ACTIONS: Final[int] = len(WATER_LEVELS)
EPISODE_LENGTH: Final[int] = 30  # 1 bước = 1 ngày
STRESS_PATIENCE: Final[int] = 3  # số ngày stress liên tiếp ⇒ terminated

# ---------------------------------------------------------------------------
# 2. Hằng số vật lý (cân bằng nước tầng rễ) — E-07
# ---------------------------------------------------------------------------
IRRIGATION_GAIN_PER_L: Final[float] = 0.02  # mỗi lít bổ sung 2% độ ẩm hữu dụng
IRRIGATION_EFFICIENCY: Final[float] = 0.9  # hiệu suất thấm của vòi tưới
RAIN_GAIN_MAX: Final[float] = 0.35  # trần tỷ lệ mưa chuyển thành độ ẩm
EVAP_RATE: Final[float] = 0.05  # bốc hơi cơ sở mỗi ngày
EVAP_BASE: Final[float] = 0.010  # thoát hơi nền của cây
KC_BY_STAGE: Final[tuple[float, ...]] = (0.7, 1.0, 1.25, 0.8)  # FAO-56 rút gọn

# ---------------------------------------------------------------------------
# 3. Trọng số và ngưỡng reward — E-03
#    Lưu ý: các ngưỡng dưới đây tính trên obs **đã chuẩn hóa**.
# ---------------------------------------------------------------------------
R_HEALTH: Final[float] = 10.0
R_STRESS: Final[float] = -100.0
C_WATER: Final[float] = -2.0  # theo index hành động (action 5 ⇒ -10)
C_WASTE: Final[float] = -10.0
C_RAIN: Final[float] = -5.0
C_DELAY: Final[float] = -8.0

WASTE_MOISTURE: Final[float] = 0.60
RAIN_PROB_TRIGGER: Final[float] = 0.70
RAIN_FORECAST_TRIGGER_MM: Final[float] = 15.0
RAIN_FORECAST_TRIGGER: Final[float] = RAIN_FORECAST_TRIGGER_MM / R_MAX_MM  # 0.30
DELAY_TRIGGER_L: Final[float] = 12.5
DELAY_TRIGGER: Final[float] = DELAY_TRIGGER_L / IRRIGATION_MAX_L  # 0.50

# Hệ số chiết khấu dùng chung cho mọi thuật toán (không nhầm với trọng số phạt).
GAMMA: Final[float] = 0.99

# ---------------------------------------------------------------------------
# 4. Kịch bản thời tiết — E-06
# ---------------------------------------------------------------------------
SCENARIO_DIR: Final[str] = "configs/scenarios"
REQUIRED_SCENARIO_KEYS: Final[tuple[str, ...]] = (
    "name",
    "rain_prob",
    "temp_range",
    "rain_forecast_range",
    "episode_length",
    "crop_type",
    "growth_stage",
    "seed",
)


# ---------------------------------------------------------------------------
# 5. Kiểu dữ liệu dùng chung giữa WeatherModel và AgriWaterEnv
# ---------------------------------------------------------------------------
class WeatherStep(NamedTuple):
    """Một ngày thời tiết do ``WeatherModel.sample()`` trả về."""

    temperature_c: float
    rain_prob: float
    rain_forecast_mm: float
    rainfall_mm: float
    rained: bool


# ---------------------------------------------------------------------------
# 6. Hàm chuẩn hóa / giải chuẩn hóa
# ---------------------------------------------------------------------------
def clip01(value: float) -> float:
    """Kẹp giá trị vào [0, 1]."""
    return float(min(1.0, max(0.0, value)))


def norm_crop_type(crop_type: int) -> float:
    return crop_type / (N_CROP_TYPES - 1)


def norm_growth_stage(growth_stage: int) -> float:
    return growth_stage / (N_GROWTH_STAGES - 1)


def norm_temperature(temperature_c: float) -> float:
    return clip01((temperature_c - TEMP_MIN_C) / (TEMP_MAX_C - TEMP_MIN_C))


def norm_rain_forecast(rain_forecast_mm: float) -> float:
    return clip01(rain_forecast_mm / R_MAX_MM)


def norm_irrigation(litres: float) -> float:
    return clip01(litres / IRRIGATION_MAX_L)


def denorm_rain_forecast(rain_forecast_norm: float) -> float:
    return rain_forecast_norm * R_MAX_MM


def denorm_irrigation(irrigation_norm: float) -> float:
    return irrigation_norm * IRRIGATION_MAX_L


def denorm_temperature(temperature_norm: float) -> float:
    return TEMP_MIN_C + temperature_norm * (TEMP_MAX_C - TEMP_MIN_C)


def ideal_range(growth_stage: int) -> tuple[float, float]:
    """Dải độ ẩm lý tưởng; giai đoạn ra hoa/kết trái (g=2) dùng dải riêng."""
    if growth_stage == FLOWER_STAGE:
        return (IDEAL_LO_FLOWER, IDEAL_HI_FLOWER)
    return (IDEAL_LO, IDEAL_HI)


def is_stressed(soil_moisture: float) -> bool:
    """Héo vĩnh viễn hoặc ngập úng."""
    return soil_moisture < WILT_POINT or soil_moisture > FIELD_CAPACITY


def is_ideal(soil_moisture: float, growth_stage: int) -> bool:
    lo, hi = ideal_range(growth_stage)
    return lo <= soil_moisture <= hi


def action_to_litres(action: int) -> int:
    """Đổi index hành động sang lít; chặn giá trị ngoài miền."""
    if not 0 <= action < N_ACTIONS:
        raise ValueError(f"action phải trong [0, {N_ACTIONS}), nhận {action}")
    return WATER_LEVELS[action]


def make_obs(
    *,
    crop_type: int = 0,
    growth_stage: int = 1,
    soil_moisture: float = 0.55,
    temperature_c: float = 28.0,
    rain_prob: float = 0.0,
    rain_forecast_mm: float = 0.0,
    last_irrigation_l: float = 0.0,
) -> np.ndarray:
    """Dựng obs 7 chiều đã chuẩn hóa từ giá trị thô (dùng cho test và debug)."""
    return np.array(
        [
            norm_crop_type(crop_type),
            norm_growth_stage(growth_stage),
            clip01(soil_moisture),
            norm_temperature(temperature_c),
            clip01(rain_prob),
            norm_rain_forecast(rain_forecast_mm),
            norm_irrigation(last_irrigation_l),
        ],
        dtype=np.float32,
    )
