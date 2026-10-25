"""AgriWater-RL — môi trường mô phỏng tưới tiêu tối ưu nguồn nước.

Cấu trúc:
    agriwater.env     môi trường Gymnasium + vật lý + thời tiết + reward
    agriwater.agents  thuật toán (Q-Learning, Monte Carlo, DQN, Baseline)
    agriwater.utils   rời rạc hóa trạng thái, ghi log metric

Import ở đây cố tình giữ nhẹ để ``import agriwater`` không kéo theo gymnasium.
"""

__version__ = "0.1.0"
