"""Interface chung cho cả 4 chiến lược (Q-Learning, MC, DQN, Baseline).

Chủ sở hữu: **Minh** (E-18). Không agent nào được sửa chữ ký ở đây; nếu cần
thêm hook thì cả 2 người thống nhất.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np


class Agent(ABC):
    """Tác tử tối giản: chọn hành động, nhận phản hồi, lưu/khôi phục."""

    name: str = "agent"

    def __init__(self, n_actions: int, seed: int | None = None) -> None:
        self.n_actions = int(n_actions)
        self.np_random = np.random.default_rng(seed)

    # -- Bắt buộc --------------------------------------------------------
    @abstractmethod
    def act(self, obs: np.ndarray, *, explore: bool = True) -> int:
        """Chọn hành động cho obs hiện tại (``explore=False`` khi đánh giá)."""

    # -- Tùy chọn, mặc định không làm gì --------------------------------
    def observe(
        self,
        obs: np.ndarray,
        action: int,
        reward: float,
        next_obs: np.ndarray,
        terminated: bool,
        truncated: bool,
    ) -> None:
        """Nhận một bước chuyển. Q-Learning cập nhật ngay; MC gom vào buffer."""

    def end_episode(self) -> None:
        """Kết thúc episode — MC tính $G_t$ và cập nhật $Q$ ở đây."""

    def save(self, path: str | Path) -> None:
        raise NotImplementedError(f"{type(self).__name__} chưa hỗ trợ save()")

    @classmethod
    def load(cls, path: str | Path, **kwargs: Any) -> "Agent":
        raise NotImplementedError(f"{cls.__name__} chưa hỗ trợ load()")

    def __repr__(self) -> str:  # pragma: no cover - chỉ để đọc log
        return f"{type(self).__name__}(n_actions={self.n_actions})"
