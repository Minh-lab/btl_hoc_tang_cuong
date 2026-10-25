"""Đăng ký và tạo agent theo tên — điểm cắm duy nhất của pipeline.

Chủ sở hữu: **Minh** (E-18). Thêm thuật toán mới chỉ cần: viết module trong
``agriwater/agents/`` rồi trang trí ``@register("<tên>")`` — không sửa env.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from agriwater.agents.base import Agent

_REGISTRY: dict[str, type[Agent]] = {}

# Các thuật toán theo kế hoạch nhưng chưa triển khai — chỉ dùng cho thông báo lỗi.
PLANNED: dict[str, str] = {
    "qlearning": "Q-Learning (E-… của Minh)",
    "mc": "Monte Carlo Control (Minh)",
    "dqn": "DQN (Thuận)",
    "baseline": "Baseline luật cố định (Khanh)",
}


def register(name: str) -> Callable[[type[Agent]], type[Agent]]:
    """Decorator đăng ký một lớp agent dưới tên dùng ở CLI."""

    def _decorator(cls: type[Agent]) -> type[Agent]:
        key = name.lower()
        if key in _REGISTRY and _REGISTRY[key] is not cls:
            raise ValueError(f"Tên agent '{key}' đã được đăng ký")
        cls.name = key
        _REGISTRY[key] = cls
        return cls

    return _decorator


def available() -> list[str]:
    """Danh sách tên agent đã đăng ký."""
    return sorted(_REGISTRY)


def make(name: str, *args: Any, **kwargs: Any) -> Agent:
    """Khởi tạo agent theo tên; báo rõ nếu thuật toán chưa được cài đặt."""
    key = name.lower()
    if key not in _REGISTRY:
        hint = PLANNED.get(key, "chưa có trong kế hoạch")
        raise KeyError(
            f"Chưa có agent '{key}' ({hint}). Đang có: {available() or '∅'}"
        )
    return _REGISTRY[key](*args, **kwargs)
