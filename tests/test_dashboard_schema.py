"""Canh schema giữa dashboard và ``MetricsLogger`` — hai nơi không được lệch cột.

Dashboard cố ý **không** import lõi (xem ``app/data_access.py``), nên schema được
copy. Test này là chốt chặn: đổi ``metrics.FIELDS`` mà quên dashboard sẽ đỏ ngay.
"""

from __future__ import annotations

import pytest

pd = pytest.importorskip("pandas")

from agriwater.utils.metrics import FIELDS as LOGGER_FIELDS  # noqa: E402
from app.data_access import FIELDS as APP_FIELDS  # noqa: E402
from app.data_access import SAMPLE_DIR  # noqa: E402


def test_dashboard_schema_matches_logger() -> None:
    assert APP_FIELDS == LOGGER_FIELDS


@pytest.mark.parametrize("path", sorted(SAMPLE_DIR.glob("*.csv")), ids=lambda p: p.name)
def test_fixture_matches_logger_schema(path) -> None:
    frame = pd.read_csv(path)
    assert list(frame.columns) == list(LOGGER_FIELDS)
    assert not frame.empty
    assert set(frame["agent"]) == {path.stem.split("_", 1)[0]}
