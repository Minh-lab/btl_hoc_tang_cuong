"""Truy cập dữ liệu cho dashboard — lớp mỏng, chỉ đọc CSV.

Quy tắc kiến trúc
-----------------
* ``app/`` **không** import ``agriwater``: dashboard không được biết lõi tồn tại
  (chiều phụ thuộc một chiều, cùng tinh thần NFR-5).
* Giao diện chỉ nói chuyện với ``CsvRunRepository``. Hiện trỏ vào
  ``app/sample_data/`` (dữ liệu **tổng hợp**), sau này trỏ vào ``logs/`` thật mà
  không phải sửa một dòng UI nào.
* Schema cột phải khớp ``agriwater.utils.metrics.FIELDS``. Có test canh việc này:
  ``tests/test_dashboard_schema.py``.

Chuyển sang dữ liệu thật: đặt log vào ``logs/`` (đúng schema) hoặc đặt biến môi
trường ``AGRIWATER_LOGS=<thư mục>``.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

#: Bản sao schema của ``MetricsLogger`` — cố ý copy để dashboard không import lõi.
FIELDS: tuple[str, ...] = (
    "episode",
    "day",
    "agent",
    "scenario",
    "crop_type",
    "growth_stage",
    "moisture",
    "action",
    "water_L",
    "reward",
    "crop_stress",
    "ideal",
    "stress_days",
)

NUMERIC_FIELDS: tuple[str, ...] = (
    "episode",
    "day",
    "crop_type",
    "growth_stage",
    "moisture",
    "action",
    "water_L",
    "reward",
    "crop_stress",
    "ideal",
    "stress_days",
)

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
SAMPLE_DIR = APP_DIR / "sample_data"
LOGS_DIR = PROJECT_DIR / "logs"
SCENARIO_DIR = PROJECT_DIR / "configs" / "scenarios"

#: Ngưỡng vật lý chỉ dùng để **vẽ** dải tham chiếu — không phải nguồn sự thật.
WILT_POINT = 0.20
IDEAL_LO = 0.40
IDEAL_HI = 0.70
FIELD_CAPACITY = 0.85


@dataclass(frozen=True)
class Run:
    """Một cặp (agent, kịch bản) có dữ liệu trong kho."""

    agent: str
    scenario: str
    files: int


class CsvRunRepository:
    """Đọc mọi ``*.csv`` dưới ``root`` theo schema của ``MetricsLogger``."""

    def __init__(self, root: str | Path, *, synthetic: bool = False) -> None:
        self.root = Path(root)
        self.synthetic = synthetic
        self._steps_cache: dict[Path, pd.DataFrame] = {}

    # -- Đọc thô --------------------------------------------------------
    def _read(self, path: Path) -> pd.DataFrame:
        cached = self._steps_cache.get(path)
        if cached is not None:
            return cached

        df = pd.read_csv(path, usecols=list(FIELDS))
        for col in NUMERIC_FIELDS:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["agent"] = df["agent"].astype(str)
        df["scenario"] = df["scenario"].astype(str)
        df = df.dropna(subset=["episode", "day"]).sort_values(["episode", "day"])

        self._steps_cache[path] = df
        return df

    def _files(self) -> list[Path]:
        if not self.root.exists():
            return []
        return sorted(self.root.rglob("*.csv"))

    # -- API cho UI -----------------------------------------------------
    def list_runs(self) -> pd.DataFrame:
        """Bảng ``agent × scenario`` kèm số file đóng góp."""
        rows: list[dict[str, object]] = []
        for path in self._files():
            try:
                df = self._read(path)
            except (ValueError, pd.errors.ParserError):
                continue  # file không đúng schema: bỏ qua, không làm sập dashboard
            for (agent, scenario), _ in df.groupby(["agent", "scenario"], sort=True):
                rows.append({"agent": agent, "scenario": scenario, "file": path.name})

        if not rows:
            return pd.DataFrame(columns=["agent", "scenario", "files"])

        runs = pd.DataFrame(rows)
        grouped = (
            runs.groupby(["agent", "scenario"], as_index=False)
            .size()
            .rename(columns={"size": "files"})
        )
        return grouped.sort_values(["scenario", "agent"]).reset_index(drop=True)

    def steps(self, agent: str, scenario: str) -> pd.DataFrame:
        """Toàn bộ bước chạy của một cặp (agent, scenario), gộp mọi file/seed."""
        frames = []
        for path in self._files():
            df = self._read(path)
            part = df[(df["agent"] == agent) & (df["scenario"] == scenario)]
            if not part.empty:
                frames.append(part)
        if not frames:
            return pd.DataFrame(columns=list(FIELDS))
        return pd.concat(frames, ignore_index=True).sort_values(["episode", "day"])

    def episodes(self, agent: str, scenario: str) -> pd.DataFrame:
        """Tóm tắt theo episode (tổng reward, tổng nước, ideal_ratio, ...)."""
        return episode_summary(self.steps(agent, scenario))


def default_repository() -> CsvRunRepository:
    """Chọn kho dữ liệu: log thật nếu có, ngược lại dùng fixtures."""
    override = os.environ.get("AGRIWATER_LOGS")
    if override:
        path = Path(override).expanduser()
        if path.exists() and any(path.rglob("*.csv")):
            return CsvRunRepository(path, synthetic=False)

    if LOGS_DIR.exists() and any(LOGS_DIR.rglob("*.csv")):
        return CsvRunRepository(LOGS_DIR, synthetic=False)

    return CsvRunRepository(SAMPLE_DIR, synthetic=True)


# ---------------------------------------------------------------------------
# Tổng hợp — thuần pandas, không phụ thuộc Streamlit
# ---------------------------------------------------------------------------
def episode_summary(steps: pd.DataFrame, *, episode_length: int = 30) -> pd.DataFrame:
    """Gộp từng bước thành một dòng/episode.

    Cột trả về: ``reward`` (tổng), ``water_L`` (tổng), ``ideal_ratio``,
    ``stress_days`` (số ngày bị stress), ``days`` (số ngày đã chạy),
    ``survived`` (True nếu đi hết mùa, tức ``truncated`` chứ không phải cây chết).
    """
    if steps.empty:
        return pd.DataFrame(
            columns=[
                "episode",
                "reward",
                "water_L",
                "ideal_ratio",
                "stress_days",
                "days",
                "survived",
            ]
        )

    grouped = steps.groupby("episode", sort=True)
    summary = pd.DataFrame(
        {
            "reward": grouped["reward"].sum(),
            "water_L": grouped["water_L"].sum(),
            "ideal_ratio": grouped["ideal"].mean(),
            "stress_days": grouped["crop_stress"].sum(),
            "days": grouped["day"].count(),
        }
    ).reset_index()
    summary["survived"] = summary["days"] >= episode_length
    return summary


def moving_average(values: pd.Series, window: int = 5) -> pd.Series:
    """Trung bình trượt; ``window=1`` trả nguyên chuỗi."""
    window = max(1, int(window))
    return values.rolling(window=window, min_periods=1).mean()


def convergence_episode(rewards: pd.Series, *, window: int = 5, frac: float = 0.9) -> int | None:
    """Episode đầu tiên mà trung bình trượt đạt ``frac`` mức cuối (thước đo tốc độ học)."""
    if len(rewards) == 0:
        return None
    smooth = moving_average(rewards, window)
    target = frac * float(rewards.tail(window).mean())
    hits = smooth[smooth >= target]
    return int(hits.index[0]) if len(hits) else None


def kpis(episodes: pd.DataFrame, *, window: int = 5, episode_length: int = 30) -> dict[str, float]:
    """Các chỉ số tóm tắt trên ``window`` episode cuối (bỏ qua nếu chưa đủ)."""
    if episodes.empty:
        return {
            "reward": 0.0,
            "best_reward": 0.0,
            "water_L": 0.0,
            "ideal_ratio": 0.0,
            "stress_days": 0.0,
            "survival": 0.0,
            "episodes": 0,
            "converged_at": None,
            "episode_length": episode_length,
        }
    tail = episodes.tail(window)
    return {
        "reward": float(tail["reward"].mean()),
        "best_reward": float(episodes["reward"].max()),
        "water_L": float(tail["water_L"].mean()),
        "ideal_ratio": float(tail["ideal_ratio"].mean()),
        "stress_days": float(tail["stress_days"].mean()),
        "survival": float(tail["survived"].mean()),
        "episodes": int(len(episodes)),
        "converged_at": convergence_episode(episodes.set_index("episode")["reward"]),
        "episode_length": episode_length,
    }


def load_scenarios(base_dir: Path = SCENARIO_DIR) -> pd.DataFrame:
    """Đọc mô tả kịch bản từ ``configs/scenarios/*.json`` để hiển thị trên UI."""
    rows: list[dict[str, object]] = []
    for path in sorted(base_dir.glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        rain = data.get("rain_prob")
        rain_text = (
            f"{rain[0]:.0%}–{rain[1]:.0%}" if isinstance(rain, list) else f"{float(rain):.0%}"
        )
        temp = data.get("temp_range", [None, None])
        rows.append(
            {
                "scenario": data.get("name", path.stem),
                "description": data.get("description", ""),
                "rain": rain_text,
                "temperature": f"{temp[0]:.0f}–{temp[1]:.0f} °C",
                "crop_type": data.get("crop_type"),
                "growth_stage": data.get("growth_stage"),
            }
        )
    return pd.DataFrame(rows)
