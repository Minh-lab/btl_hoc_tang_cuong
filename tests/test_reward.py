"""Reward 6 thành phần — 5 tình huống mẫu của MDP + 4 test biên (E-04).

Kỳ vọng lấy nguyên từ báo cáo V2, mục 5.3:
``+6, +10, -124, -4, -10``.

Bỏ ``pytestmark`` bên dưới ngay khi ``calculate_reward()`` được cài đặt xong.
"""

from __future__ import annotations

import pytest

from agriwater.env import contract as C
from agriwater.env.reward import calculate_reward

pytestmark = pytest.mark.xfail(
    reason="E-03: calculate_reward() chưa cài đặt (Minh)", strict=True
)


def test_case_1_dry_soil_irrigated_to_ideal(make_obs) -> None:
    """Đất khô 0.15, tưới 10 L → 0.50: +10 (lý tưởng) − 4 (nước) = +6."""
    state = make_obs(growth_stage=1, soil_moisture=0.15)
    next_state = make_obs(growth_stage=1, soil_moisture=0.50)
    assert calculate_reward(state, 2, next_state) == pytest.approx(+6.0)


def test_case_2_ideal_without_irrigation(make_obs) -> None:
    """Đất ẩm 0.50, không tưới → 0.65: chỉ có +10."""
    state = make_obs(growth_stage=1, soil_moisture=0.50)
    next_state = make_obs(growth_stage=1, soil_moisture=0.65)
    assert calculate_reward(state, 0, next_state) == pytest.approx(+10.0)


def test_case_3_waterlogged(make_obs) -> None:
    """Đất ẩm 0.65, tưới 10 L → 0.90: 0 − 100 − 4 − 20 = −124."""
    state = make_obs(growth_stage=1, soil_moisture=0.65)
    next_state = make_obs(growth_stage=1, soil_moisture=0.90)
    assert calculate_reward(state, 2, next_state) == pytest.approx(-124.0)


def test_case_4_irrigating_before_heavy_rain(make_obs) -> None:
    """Khô 0.35, mưa dự báo 80% / 15 mm, tưới 10 L → 0.65: +10 − 4 − 10 = −4."""
    state = make_obs(growth_stage=1, soil_moisture=0.35, rain_prob=0.80, rain_forecast_mm=15.0)
    next_state = make_obs(growth_stage=1, soil_moisture=0.65)
    assert calculate_reward(state, 2, next_state) == pytest.approx(-4.0)


def test_case_5_irrigating_too_soon(make_obs) -> None:
    """Đợt trước tưới 15 L, tưới tiếp 10 L → 0.70: +10 − 4 − 16 = −10."""
    state = make_obs(growth_stage=1, soil_moisture=0.55, last_irrigation_l=15.0)
    next_state = make_obs(growth_stage=1, soil_moisture=0.70)
    assert calculate_reward(state, 2, next_state) == pytest.approx(-10.0)


@pytest.mark.parametrize(
    ("moisture_next", "expected"),
    [
        (0.20, -4.0),  # bằng ngưỡng héo: KHÔNG bị −100, chưa lý tưởng
        (0.40, +6.0),  # biên dưới dải lý tưởng: tính là lý tưởng
        (0.70, +6.0),  # biên trên dải lý tưởng: tính là lý tưởng
        (0.85, -4.0),  # bằng sức chứa đồng ruộng: KHÔNG bị −100
    ],
)
def test_boundary_moisture(make_obs, moisture_next: float, expected: float) -> None:
    """Test biên ngưỡng 0.20 / 0.40 / 0.70 / 0.85 với hành động tưới 10 L."""
    state = make_obs(growth_stage=1, soil_moisture=0.15)
    next_state = make_obs(growth_stage=1, soil_moisture=moisture_next)
    assert calculate_reward(state, 2, next_state) == pytest.approx(expected)


def test_full_moisture_outside_contract_range_is_clipped(make_obs) -> None:
    """Hợp đồng yêu cầu mọi obs trong [0, 1] — reward không tự sinh giá trị lạ."""
    next_state = C.make_obs(growth_stage=1, soil_moisture=0.90)
    state = C.make_obs(growth_stage=1, soil_moisture=0.65)
    assert ((next_state >= 0.0) & (next_state <= 1.0)).all()
    assert calculate_reward(state, 2, next_state) == pytest.approx(-124.0)
