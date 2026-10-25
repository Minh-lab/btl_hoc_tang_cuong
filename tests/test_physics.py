"""Vật lý cân bằng nước tầng rễ (E-08, thuộc phần E-07 của Trưởng)."""

from __future__ import annotations

import pytest

from agriwater.env import contract as C
from agriwater.env.physics import update_moisture

pytestmark = pytest.mark.xfail(
    reason="E-07: update_moisture() chưa cài đặt (Trưởng)", strict=True
)


def test_dries_out_without_irrigation() -> None:
    """Một ngày nắng không tưới, không mưa ⇒ độ ẩm giảm."""
    m_next, drained = update_moisture(
        moisture=0.60, action=0, temperature_c=38.0, rainfall_mm=0.0, growth_stage=2
    )
    assert m_next < 0.60
    assert drained == pytest.approx(0.0, abs=1e-9)
    assert 0.0 <= m_next <= 1.0


def test_never_exceeds_one() -> None:
    """Tưới 25 L mỗi ngày trên đất đã đầy ⇒ vẫn kẹp ở ≤ 1."""
    moisture = C.FIELD_CAPACITY
    for _ in range(10):
        moisture, _ = update_moisture(
            moisture=moisture, action=5, temperature_c=20.0, rainfall_mm=40.0, growth_stage=1
        )
        assert 0.0 <= moisture <= 1.0


def test_drainage_above_field_capacity() -> None:
    """Vượt 0.85 ⇒ có thấm thoát $D_t > 0$."""
    _, drained = update_moisture(
        moisture=0.84, action=5, temperature_c=20.0, rainfall_mm=40.0, growth_stage=1
    )
    assert drained > 0.0
