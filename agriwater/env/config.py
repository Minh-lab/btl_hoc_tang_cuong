"""Cấu hình môi trường — mọi tham số điều chỉnh được, không hard-code trong lõi.

Chủ sở hữu: Trưởng (task E-02). Người khác đọc và góp ý qua review.
Mặc định lấy trực tiếp từ ``contract`` để chỉ có một nguồn số liệu.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from agriwater.env import contract as C


@dataclass(frozen=True)
class EnvConfig:
    """Tham số của một lần chạy ``AgriWaterEnv``.

    Mọi ngưỡng/hệ số đều có thể ghi đè khi làm thực nghiệm, nhưng giá trị mặc
    định phải khớp ``contract`` (báo cáo V2). Sửa mặc định ⇒ sửa báo cáo.
    """

    # Kịch bản
    scenario: str = "randomized"
    scenario_path: str | None = None  # None ⇒ configs/scenarios/<scenario>.json
    crop_type: int | None = None  # None ⇒ lấy từ file kịch bản
    growth_stage: int | None = None
    episode_length: int = C.EPISODE_LENGTH
    stress_patience: int = C.STRESS_PATIENCE
    initial_moisture: float = 0.55

    # Vật lý
    irrigation_gain_per_l: float = C.IRRIGATION_GAIN_PER_L
    irrigation_efficiency: float = C.IRRIGATION_EFFICIENCY
    rain_gain_max: float = C.RAIN_GAIN_MAX
    evap_rate: float = C.EVAP_RATE
    evap_base: float = C.EVAP_BASE
    kc_by_stage: tuple[float, ...] = C.KC_BY_STAGE
    wilt_point: float = C.WILT_POINT
    field_capacity: float = C.FIELD_CAPACITY

    # Reward
    r_health: float = C.R_HEALTH
    r_stress: float = C.R_STRESS
    c_water: float = C.C_WATER
    c_waste: float = C.C_WASTE
    c_rain: float = C.C_RAIN
    c_delay: float = C.C_DELAY
    waste_moisture: float = C.WASTE_MOISTURE
    rain_prob_trigger: float = C.RAIN_PROB_TRIGGER
    rain_forecast_trigger: float = C.RAIN_FORECAST_TRIGGER
    delay_trigger: float = C.DELAY_TRIGGER

    # Trình bày
    render_mode: str | None = None

    def __post_init__(self) -> None:
        if self.episode_length <= 0:
            raise ValueError("episode_length phải > 0")
        if not 1 <= self.stress_patience <= self.episode_length:
            raise ValueError("stress_patience phải trong [1, episode_length]")
        if not 0.0 <= self.initial_moisture <= 1.0:
            raise ValueError("initial_moisture phải trong [0, 1]")
        if self.crop_type is not None and not 0 <= self.crop_type < C.N_CROP_TYPES:
            raise ValueError(f"crop_type phải trong [0, {C.N_CROP_TYPES})")
        if self.growth_stage is not None and not 0 <= self.growth_stage < C.N_GROWTH_STAGES:
            raise ValueError(f"growth_stage phải trong [0, {C.N_GROWTH_STAGES})")
        if len(self.kc_by_stage) != C.N_GROWTH_STAGES:
            raise ValueError("kc_by_stage phải có đúng N_GROWTH_STAGES phần tử")
        if not self.wilt_point < self.field_capacity <= 1.0:
            raise ValueError("cần wilt_point < field_capacity <= 1")
        if self.render_mode not in (None, "human", "rgb_array"):
            raise ValueError("render_mode chỉ nhận None, 'human', 'rgb_array'")

    # -- Tiện ích dùng chung với reward/physics -----------------------------
    def kc(self, growth_stage: int) -> float:
        return self.kc_by_stage[growth_stage]

    def ideal_range(self, growth_stage: int | None = None) -> tuple[float, float]:
        stage = C.FLOWER_STAGE if growth_stage is None else growth_stage
        return C.ideal_range(stage)

    def resolved_scenario_path(self, base_dir: str | Path = ".") -> Path:
        if self.scenario_path is not None:
            return Path(self.scenario_path)
        return Path(base_dir) / C.SCENARIO_DIR / f"{self.scenario}.json"

    def load_scenario(self, base_dir: str | Path = ".") -> dict[str, Any]:
        path = self.resolved_scenario_path(base_dir)
        with path.open(encoding="utf-8") as handle:
            scenario = json.load(handle)
        missing = [k for k in C.REQUIRED_SCENARIO_KEYS if k not in scenario]
        if missing:
            raise ValueError(f"{path} thiếu khóa {missing}")
        return scenario

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EnvConfig":
        known = {f for f in cls.__dataclass_fields__}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"EnvConfig không có trường {sorted(unknown)}")
        payload = dict(data)
        if "kc_by_stage" in payload:
            payload["kc_by_stage"] = tuple(payload["kc_by_stage"])
        return cls(**payload)


DEFAULT_CONFIG = EnvConfig()
