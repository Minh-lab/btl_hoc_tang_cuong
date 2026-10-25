"""Cân bằng nước tầng rễ.

Chủ sở hữu: **Trưởng** — task E-07. Ba hàm ở đây là toàn bộ vật lý của môi
trường; ``AgriWaterEnv.step()`` chỉ gọi lại, không tự tính.

$$\nm_{t+1} = \\operatorname{clip}\\big(m_t + \\eta k_a a_t + \\Delta R - ET_t - D_t,\\ 0,\\ 1\\big)$$

$$ET_t = c_{\\text{evap}} \\cdot K_c(\\text{crop}, g) \\cdot \\frac{T_t - 15}{30} + c_{\\text{base}},
\\qquad D_t = \\max(0,\\ m_t + \\Delta I + \\Delta R - \\theta_{fc})$$
"""

from __future__ import annotations

from agriwater.env import contract as C
from agriwater.env.config import DEFAULT_CONFIG, EnvConfig


def evapotranspiration(
    temperature_c: float,
    growth_stage: int,
    config: EnvConfig = DEFAULT_CONFIG,
) -> float:
    """Lượng nước mất do bốc thoát hơi trong ngày (E-07).

    $ET_t = c_{evap} \\cdot K_c(g) \\cdot (T_t-15)/30 + c_{base}$, luôn ≥ 0.
    """
    raise NotImplementedError("E-07: cài đặt evapotranspiration()")


def drainage(
    moisture: float,
    irrigation: float,
    rainfall_gain: float,
    config: EnvConfig = DEFAULT_CONFIG,
) -> float:
    """Lượng nước thấm thoát khỏi tầng rễ khi vượt sức chứa đồng ruộng (E-07).

    $D_t = \\max(0,\\ m_t + \\Delta I + \\Delta R - \\theta_{fc})$, với
    ``irrigation`` và ``rainfall_gain`` là **phần gia tăng** đã tính (không phải lít).
    """
    raise NotImplementedError("E-07: cài đặt drainage()")


def update_moisture(
    moisture: float,
    action: int,
    temperature_c: float,
    rainfall_mm: float,
    growth_stage: int,
    config: EnvConfig = DEFAULT_CONFIG,
) -> tuple[float, float]:
    """Cập nhật độ ẩm đất sau một ngày (E-07).

    Args:
        moisture: $m_t$ thô trong [0, 1].
        action: index hành động trong ``range(6)``.
        temperature_c: $T_t$ (°C).
        rainfall_mm: lượng mưa thực tế của ngày (mm, đã lấy từ ``WeatherStep``).
        growth_stage: $g$ — quyết định $K_c$.

    Returns:
        ``(m_next, drainage_amount)``: độ ẩm mới đã ``clip`` về [0, 1] và lượng
        nước thấm thoát của bước, phục vụ debug/log.

    Gợi ý cài đặt:
        ``delta_i = cfg.irrigation_efficiency * cfg.irrigation_gain_per_l * WATER_LEVELS[action]``
        ``delta_r = min(cfg.rain_gain_max, rainfall_mm / R_MAX_MM)``
        ``d = drainage(moisture, delta_i, delta_r, cfg)``
        ``m_next = clip01(moisture + delta_i + delta_r - evapotranspiration(...) - d)``
    """
    raise NotImplementedError("E-07: cài đặt update_moisture()")


__all__ = ["evapotranspiration", "drainage", "update_moisture"]
