"""Hợp đồng G0: chỉ số obs, hằng số, chuẩn hóa, EnvConfig và kịch bản.

Bộ test này **phải xanh ngay từ đầu** — nó bảo vệ phần đã chốt, không phải phần
đang chờ cài đặt.
"""

from __future__ import annotations

import pytest

from agriwater.env import contract as C
from agriwater.env.config import DEFAULT_CONFIG, EnvConfig


def test_obs_layout() -> None:
    assert C.OBS_DIM == 7
    assert len(C.OBS_NAMES) == C.OBS_DIM
    assert C.OBS_NAMES[2] == "soil_moisture"
    assert C.OBS_NAMES[6] == "last_irrigation"


def test_action_space() -> None:
    assert C.WATER_LEVELS == (0, 5, 10, 15, 20, 25)
    assert C.N_ACTIONS == 6
    assert C.action_to_litres(0) == 0
    assert C.action_to_litres(5) == 25


def test_action_out_of_range_rejected() -> None:
    for bad in (-1, 6, 99):
        with pytest.raises(ValueError):
            C.action_to_litres(bad)


def test_derived_triggers_are_normalized_values() -> None:
    """Ngưỡng reward tính trên obs đã chuẩn hóa: 15 mm ≡ 0.30, 12,5 L ≡ 0.50."""
    assert C.RAIN_FORECAST_TRIGGER == pytest.approx(0.30)
    assert C.DELAY_TRIGGER == pytest.approx(0.50)


def test_ideal_ranges() -> None:
    assert C.ideal_range(1) == (0.40, 0.70)
    assert C.ideal_range(C.FLOWER_STAGE) == (0.50, 0.75)
    assert C.is_ideal(0.40, 1) and C.is_ideal(0.70, 1)
    assert not C.is_ideal(0.45, C.FLOWER_STAGE)
    assert C.is_ideal(0.75, C.FLOWER_STAGE)


def test_stress_boundaries() -> None:
    assert C.is_stressed(0.19)
    assert not C.is_stressed(0.20)
    assert not C.is_stressed(0.85)
    assert C.is_stressed(0.86)


def test_normalization_stays_in_unit_interval() -> None:
    obs = C.make_obs(
        crop_type=3,
        growth_stage=3,
        soil_moisture=0.55,
        temperature_c=45.0,
        rain_prob=0.8,
        rain_forecast_mm=50.0,
        last_irrigation_l=25.0,
    )
    assert obs.dtype == "float32"
    assert obs.shape == (7,)
    assert ((obs >= 0.0) & (obs <= 1.0)).all()
    # Ngoài miền thô vẫn bị kẹp về [0, 1]
    wild = C.make_obs(temperature_c=99.0, rain_forecast_mm=500.0, last_irrigation_l=100.0)
    assert ((wild >= 0.0) & (wild <= 1.0)).all()


def test_normalization_matches_contract_table() -> None:
    obs = C.make_obs(
        crop_type=1,
        growth_stage=2,
        temperature_c=30.0,
        rain_forecast_mm=15.0,
        last_irrigation_l=12.5,
    )
    assert obs[C.IDX_CROP_TYPE] == pytest.approx(1 / 3)
    assert obs[C.IDX_GROWTH_STAGE] == pytest.approx(2 / 3)
    assert obs[C.IDX_TEMPERATURE] == pytest.approx(0.5)
    assert obs[C.IDX_RAIN_FORECAST] == pytest.approx(0.30)
    assert obs[C.IDX_LAST_IRRIGATION] == pytest.approx(0.50)


def test_default_config_is_valid() -> None:
    assert DEFAULT_CONFIG.episode_length == 30
    assert DEFAULT_CONFIG.stress_patience == 3
    assert DEFAULT_CONFIG.kc(C.FLOWER_STAGE) == 1.25
    assert DEFAULT_CONFIG.to_dict() == EnvConfig.from_dict(DEFAULT_CONFIG.to_dict()).to_dict()


def test_config_validation() -> None:
    with pytest.raises(ValueError):
        EnvConfig(episode_length=0)
    with pytest.raises(ValueError):
        EnvConfig(stress_patience=31)
    with pytest.raises(ValueError):
        EnvConfig(initial_moisture=1.5)
    with pytest.raises(ValueError):
        EnvConfig(growth_stage=4)
    with pytest.raises(ValueError):
        EnvConfig.from_dict({"unknown_field": 1})


def test_scenario_files_are_loadable(scenario: dict) -> None:
    for key in C.REQUIRED_SCENARIO_KEYS:
        assert key in scenario, f"kịch bản thiếu khóa {key}"
    assert scenario["episode_length"] == 30
    assert 0 <= scenario["crop_type"] < C.N_CROP_TYPES
    assert 0 <= scenario["growth_stage"] < C.N_GROWTH_STAGES


def test_scenario_loaded_from_config(root) -> None:
    cfg = EnvConfig(scenario="dry")
    loaded = cfg.load_scenario(root)
    assert loaded["name"] == "dry"
    assert cfg.resolved_scenario_path(root).exists()


def test_weather_step_dataclass() -> None:
    step = C.WeatherStep(30.0, 0.2, 10.0, 0.0, False)
    assert step.temperature_c == 30.0
    assert step.rained is False
