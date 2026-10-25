"""Lớp thuật toán: Q-Learning, Monte Carlo Control, DQN, Baseline luật cố định.

Mọi agent tuân chung ``agriwater.agents.base.Agent`` và được tạo qua
``agriwater.agents.registry.make("<tên>")`` để pipeline cắm — chạy (FDD nhánh 2).

Import dưới đây để agent có sẵn tự đăng ký vào registry; agent mới thêm file
trong package này và import tương tự.
"""

from agriwater.agents import random_agent as _random_agent  # noqa: F401  (đăng ký "random")

__all__ = ["_random_agent"]
