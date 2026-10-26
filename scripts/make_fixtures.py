#!/usr/bin/env python3
"""Sinh CSV mẫu cho dashboard — **DỮ LIỆU TỔNG HỢP**, không phải kết quả thật.

Mục đích duy nhất: dựng hình giao diện (4 trang) trước khi ``AgriWaterEnv`` chạy
được. Script này:

* dùng chung hằng số với lõi (``agriwater.env.contract``) để con số trông hợp lý;
* dùng chung schema cột với ``MetricsLogger.FIELDS`` để khi nối log thật không
  phải sửa dashboard;
* **sao chép** công thức reward/vật lý ở mức tối giản — nguồn sự thật vẫn là
  ``agriwater/env/reward.py`` và ``agriwater/env/physics.py``.

Vì vậy: không trích số liệu trong ``app/sample_data/`` vào báo cáo. Chỉ dùng để
xem giao diện, chụp slide, hoặc test UI.

Khác biệt có chủ ý so với đặc tả (để biểu đồ có ý nghĩa minh hoạ):

* hệ số mưa nhỏ hơn (``rainfall_mm / 700``, trần 0.10) thay vì ``rainfall_mm / 50``
  trần 0.35 — nếu không, kịch bản mưa bão bão hoà độ ẩm cả mùa, agent không còn
  lựa chọn nào để cải thiện;
* độ ẩm ban đầu 0.50 thay vì 0.55;

Hai khác biệt này **không** được đưa ngược vào lõi; env thật vẫn dùng ``contract``.

Chạy::

    .venv/bin/python scripts/make_fixtures.py
    .venv/bin/python scripts/make_fixtures.py --episodes 10 --out /tmp/fx
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from agriwater.env import contract as C
from agriwater.utils.metrics import FIELDS

PROJECT_DIR = Path(__file__).resolve().parents[1]
SCENARIO_DIR = PROJECT_DIR / "configs" / "scenarios"
DEFAULT_OUT = PROJECT_DIR / "app" / "sample_data"

AGENTS = ("baseline", "qlearning", "mc", "dqn")

#: Hồ sơ "học" giả lập: (epsilon đầu, epsilon cuối, tỉ lệ episode khởi động ngẫu nhiên)
PROFILES: dict[str, tuple[float, float, float]] = {
    "baseline": (0.0, 0.0, 0.0),  # luật cố định, không học
    "qlearning": (1.00, 0.00, 0.15),
    "mc": (1.00, 0.02, 0.22),  # học chậm hơn Q-Learning
    "dqn": (0.95, 0.00, 0.05),
}


# ---------------------------------------------------------------------------
# Chính sách
# ---------------------------------------------------------------------------
def greedy_action(
    moisture: float,
    rain_prob: float,
    forecast_mm: float,
    last_irrigation_l: float,
    stage: int,
) -> int:
    """Chính sách "khá tốt" để mô phỏng agent đã học được; index của WATER_LEVELS."""
    if last_irrigation_l >= 12.5:  # vừa tưới đợt trước ⇒ chờ nước thấm
        return 0
    if moisture >= 0.35 and rain_prob >= 0.60 and forecast_mm >= 10.0:  # sắp mưa ⇒ hoãn tưới
        return 0

    ideal_lo, ideal_hi = C.ideal_range(stage)
    if moisture >= ideal_lo:  # đã trong dải lý tưởng ⇒ không tưới
        return 0

    # Tưới vừa đủ để về giữa dải lý tưởng (mỗi bậc 5 L ≈ +0.09 độ ẩm).
    step = C.IRRIGATION_EFFICIENCY * C.IRRIGATION_GAIN_PER_L * 5
    needed = int(np.ceil(((ideal_lo + ideal_hi) / 2 - moisture) / step))
    return int(min(max(needed, 1), C.N_ACTIONS - 1))


def choose_action(
    agent: str,
    episode: int,
    n_episodes: int,
    moisture: float,
    rain_prob: float,
    forecast_mm: float,
    last_irrigation_l: float,
    stage: int,
    rng: np.random.Generator,
) -> int:
    """Hành động theo hồ sơ học của từng agent (epsilon-greedy giả lập)."""
    if agent == "baseline":
        return 4 if moisture < 0.30 else 0

    eps_start, eps_end, warmup = PROFILES[agent]
    progress = episode / max(1, n_episodes - 1)
    if progress < warmup:
        epsilon = 1.0
    else:
        span = max(1e-9, 1.0 - warmup)
        # Giảm theo bậc hai: khám phá mạnh lúc đầu, gần như tất định khi hội tụ.
        remaining = max(0.0, 1.0 - (progress - warmup) / span)
        epsilon = eps_end + (eps_start - eps_end) * remaining**2

    if rng.random() < epsilon:
        return int(rng.integers(0, C.N_ACTIONS))
    return greedy_action(moisture, rain_prob, forecast_mm, last_irrigation_l, stage)


# ---------------------------------------------------------------------------
# Thời tiết & vật lý (bản rút gọn — chỉ để vẽ biểu đồ)
# ---------------------------------------------------------------------------
def sample_weather(scenario: dict, rng: np.random.Generator) -> tuple[float, float, float, float]:
    rain = scenario["rain_prob"]
    rain_prob = float(rng.uniform(*rain)) if isinstance(rain, list) else float(rain)
    temperature = float(rng.uniform(*scenario["temp_range"]))
    forecast = float(rng.uniform(*scenario["rain_forecast_range"]))
    rained = rng.random() < rain_prob
    rainfall = max(0.0, forecast * (1.0 + rng.normal(0.0, 0.25))) if rained else 0.0
    return temperature, rain_prob, forecast, rainfall


def update_moisture(moisture: float, action: int, temperature: float, rainfall_mm: float, stage: int) -> float:
    kc = C.KC_BY_STAGE[stage]
    irrigation = C.IRRIGATION_EFFICIENCY * C.IRRIGATION_GAIN_PER_L * C.WATER_LEVELS[action]
    # Bản mô phỏng dùng hệ số thấm nhỏ hơn contract để kịch bản mưa bão không bị
    # bão hoà 100% (xem ghi chú "khác biệt có chủ ý" ở docstring module).
    rain_gain = min(0.10, rainfall_mm / 700.0)
    drainage = max(0.0, moisture + irrigation + rain_gain - C.FIELD_CAPACITY)
    evap = C.EVAP_RATE * kc * (temperature - 15.0) / 30.0 + C.EVAP_BASE
    return float(np.clip(moisture + irrigation + rain_gain - evap - drainage, 0.0, 1.0))


def mock_reward(m: float, action: int, m_next: float, stage: int, rain_prob: float, forecast_mm: float, last_l: float) -> float:
    """Bản sao rút gọn của ``calculate_reward`` — chỉ dùng cho fixtures."""
    lo, hi = C.ideal_range(stage)
    reward = 0.0
    if lo <= m_next <= hi:
        reward += 10.0
    if m_next < C.WILT_POINT or m_next > C.FIELD_CAPACITY:
        reward -= 100.0
    reward -= 2.0 * action
    if m >= 0.60 and action > 0:
        reward -= 10.0 * action
    if action > 0 and rain_prob >= 0.70 and forecast_mm >= 15.0:
        reward -= 5.0 * action
    if action > 0 and last_l >= 12.5:
        reward -= 8.0 * action
    return reward


# ---------------------------------------------------------------------------
# Sinh dữ liệu
# ---------------------------------------------------------------------------
def generate_agent_scenario(
    agent: str,
    scenario: dict,
    writer: csv.DictWriter,
    *,
    episodes: int,
    seed: int,
) -> None:
    rng = np.random.default_rng(seed)
    stage = int(scenario["growth_stage"])
    crop_type = int(scenario["crop_type"])
    episode_length = int(scenario.get("episode_length", C.EPISODE_LENGTH))

    for episode in range(episodes):
        moisture = 0.50
        stress_days = 0
        last_l = 0.0

        for day in range(1, episode_length + 1):
            temperature, rain_prob, forecast, rainfall = sample_weather(scenario, rng)
            action = choose_action(
                agent, episode, episodes, moisture, rain_prob, forecast, last_l, stage, rng
            )
            water_l = float(C.WATER_LEVELS[action])
            m_next = update_moisture(moisture, action, temperature, rainfall, stage)

            stressed = m_next < C.WILT_POINT or m_next > C.FIELD_CAPACITY
            ideal = C.ideal_range(stage)[0] <= m_next <= C.ideal_range(stage)[1]
            stress_days = stress_days + 1 if stressed else 0

            reward = mock_reward(moisture, action, m_next, stage, rain_prob, forecast, last_l)

            writer.writerow(
                {
                    "episode": episode,
                    "day": day,
                    "agent": agent,
                    "scenario": scenario["name"],
                    "crop_type": crop_type,
                    "growth_stage": stage,
                    "moisture": round(m_next, 4),
                    "action": action,
                    "water_L": water_l,
                    "reward": round(reward, 3),
                    "crop_stress": int(stressed),
                    "ideal": int(ideal),
                    "stress_days": stress_days,
                }
            )

            moisture = m_next
            last_l = water_l

            if stress_days >= C.STRESS_PATIENCE:  # terminated: cây chết
                break


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="thư mục ghi CSV")
    parser.add_argument("--episodes", type=int, default=30, help="số episode mỗi file")
    parser.add_argument("--seed", type=int, default=42, help="seed gốc")
    args = parser.parse_args()

    scenarios = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(SCENARIO_DIR.glob("*.json"))
    ]
    args.out.mkdir(parents=True, exist_ok=True)

    print(f"==> Ghi fixtures vào {args.out} ({len(AGENTS)} agent × {len(scenarios)} kịch bản × {args.episodes} episode)")
    for scenario_index, scenario in enumerate(scenarios):
        for agent_index, agent in enumerate(AGENTS):
            path = args.out / f"{agent}_{scenario['name']}.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                generate_agent_scenario(
                    agent,
                    scenario,
                    writer,
                    episodes=args.episodes,
                    seed=args.seed + 100 * scenario_index + 7 * agent_index,
                )
            print(f"    {path.relative_to(PROJECT_DIR)}")

    print("\n==> Xong. Đây là DỮ LIỆU TỔNG HỢP, không phải kết quả thực nghiệm.")


if __name__ == "__main__":
    main()
