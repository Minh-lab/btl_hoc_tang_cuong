"""Hạ tầng phải dùng được ngay: registry, agent ngẫu nhiên, logger, NFR-5."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from agriwater.agents import registry
from agriwater.agents.base import Agent
from agriwater.env import contract as C
from agriwater.utils.metrics import FIELDS, MetricsLogger


def test_random_agent_is_registered() -> None:
    assert "random" in registry.available()


def test_random_agent_acts_inside_action_space() -> None:
    agent = registry.make("random", C.N_ACTIONS, seed=0)
    assert isinstance(agent, Agent)
    actions = {agent.act(np.zeros(C.OBS_DIM, dtype=np.float32)) for _ in range(200)}
    assert actions <= set(range(C.N_ACTIONS))
    assert len(actions) > 1, "agent ngẫu nhiên phải thật sự ngẫu nhiên"


def test_unimplemented_algorithm_has_clear_error() -> None:
    with pytest.raises(KeyError) as exc:
        registry.make("qlearning", C.N_ACTIONS)
    assert "Q-Learning" in str(exc.value)


def test_metrics_logger_writes_contract_columns(tmp_path: Path) -> None:
    path = tmp_path / "logs" / "run.csv"
    obs = C.make_obs(growth_stage=2, soil_moisture=0.55, last_irrigation_l=10.0)
    info = {
        "water_L": 10.0,
        "crop_stress": False,
        "moisture": 0.55,
        "growth_stage": 2,
        "ideal": True,
        "stress_days": 0,
    }
    with MetricsLogger(path, agent_name="random", scenario="dry") as logger:
        for day in range(5):
            logger.log(episode=0, day=day, obs=obs, action=2, reward=6.0, info=info)

    with path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 5
    assert tuple(rows[0].keys()) == FIELDS
    assert rows[0]["agent"] == "random"
    assert float(rows[0]["reward"]) == pytest.approx(6.0)


def test_env_does_not_depend_on_agents(root: Path) -> None:
    """NFR-5: ``agriwater.env`` không được import ``agriwater.agents``."""
    code = (
        "import sys\n"
        "import agriwater.env.contract, agriwater.env.config,"
        " agriwater.env.reward, agriwater.env.physics,"
        " agriwater.env.weather_model, agriwater.env.agriwater_env\n"
        "bad = [m for m in sys.modules if m.startswith('agriwater.agents')]\n"
        "assert not bad, bad\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], cwd=root, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
