"""Fixture dùng chung. Chạy: ``python -m pytest`` từ thư mục gốc dự án."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from agriwater.env import contract as C

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "configs" / "scenarios"


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def scenario_dir() -> Path:
    return SCENARIO_DIR


@pytest.fixture(params=["dry", "stormy", "randomized"])
def scenario(request: pytest.FixtureRequest, scenario_dir: Path) -> dict[str, Any]:
    with (scenario_dir / f"{request.param}.json").open(encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def make_obs() -> Any:
    """Hàm dựng obs đã chuẩn hóa từ giá trị thô."""
    return C.make_obs


@pytest.fixture
def rng() -> np.random.Generator:
    return np.random.default_rng(0)
