"""Hàm phần thưởng 6 thành phần — nguồn sự thật duy nhất cho $R(s, a)$.

Chủ sở hữu: **Minh** — task E-03 (cài đặt) và E-04 (9 test: 5 tình huống mẫu +
4 test biên). Báo cáo V2, mục 5.3.

$$R = R_{health} + R_{stress} + R_{water} + R_{waste} + R_{rain} + R_{delay}$$

Quy ước bắt buộc: ``state`` và ``next_state`` là obs **đã chuẩn hóa** (7 chiều,
``float32``) đúng như ``contract`` quy định, nên mọi ngưỡng dùng trực tiếp
``contract.RAIN_FORECAST_TRIGGER`` (0.30 ≡ 15 mm) và ``contract.DELAY_TRIGGER``
(0.50 ≡ 12,5 L). Không tự chia lại cho $R_{max}$ hay 25 L.
"""

from __future__ import annotations

import numpy as np

from agriwater.env import contract as C
from agriwater.env.config import DEFAULT_CONFIG, EnvConfig


def calculate_reward(
    state: np.ndarray,
    action: int,
    next_state: np.ndarray,
    config: EnvConfig = DEFAULT_CONFIG,
) -> float:
    """Phần thưởng của bước chuyển $(s_t, a_t, s_{t+1})$ (E-03).

    Args:
        state: obs trước khi hành động, ``np.float32[7]`` đã chuẩn hóa.
        action: index hành động trong ``range(6)``.
        next_state: obs sau khi hành động, ``np.float32[7]`` đã chuẩn hóa.
        config: trọng số/ngưỡng (mặc định lấy từ ``contract``).

    Returns:
        Tổng 6 thành phần.

    Đặc tả từng thành phần (giá trị đã chuẩn hóa):
        1. ``+10`` nếu ``m_next`` thuộc dải lý tưởng theo giai đoạn
           (g=2: [0.50, 0.75]; còn lại [0.40, 0.70], biên tính là **thuộc**).
        2. ``-100`` nếu ``m_next < 0.20`` hoặc ``m_next > 0.85``.
        3. ``-2 * action`` luôn trừ theo mức tưới.
        4. ``-10 * action`` nếu ``m_t >= 0.60`` và ``action > 0``.
        5. ``-5 * action`` nếu ``action > 0``, ``p_t >= 0.70``, ``f_t >= 0.30``.
        6. ``-8 * action`` nếu ``action > 0`` và ``last_irrigation >= 0.50``.

    5 tình huống chuẩn phải cho: ``+6, +10, -124, -4, -10``.
    """
    raise NotImplementedError("E-03: cài đặt calculate_reward()")


def reward_breakdown(
    state: np.ndarray,
    action: int,
    next_state: np.ndarray,
    config: EnvConfig = DEFAULT_CONFIG,
) -> dict[str, float]:
    """Phân rã 6 thành phần, dùng cho log/CSV và debug (E-19).

    Trả về dict với 6 khóa: ``health``, ``stress``, ``water``, ``waste``,
    ``rain``, ``delay``. Tổng các giá trị **phải bằng** ``calculate_reward()``.
    """
    raise NotImplementedError("E-03: cài đặt reward_breakdown()")


__all__ = ["calculate_reward", "reward_breakdown", "C"]
