"""Agent ngẫu nhiên — baseline hạ tầng, dùng để smoke test pipeline.

Không học gì; tồn tại để chứng minh env + registry + logger nối đúng trước khi
có thuật toán thật (E-18/E-21).
"""

from __future__ import annotations

import numpy as np

from agriwater.agents.base import Agent
from agriwater.agents.registry import register


@register("random")
class RandomAgent(Agent):
    """Chọn đều trong ``range(n_actions)``."""

    def act(self, obs: np.ndarray, *, explore: bool = True) -> int:
        return int(self.np_random.integers(0, self.n_actions))
