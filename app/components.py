"""Thành phần giao diện dùng chung + lớp cache dữ liệu cho Streamlit."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app import data_access as da


# ---------------------------------------------------------------------------
# Cache — bọc data_access để không đọc CSV lại mỗi lần bấm nút
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False, ttl=60)
def get_runs() -> pd.DataFrame:
    return da.default_repository().list_runs()


@st.cache_data(show_spinner=False, ttl=60)
def get_steps(agent: str, scenario: str) -> pd.DataFrame:
    return da.default_repository().steps(agent, scenario)


@st.cache_data(show_spinner=False, ttl=60)
def get_episodes(agent: str, scenario: str) -> pd.DataFrame:
    return da.episode_summary(get_steps(agent, scenario))


@st.cache_data(show_spinner=False, ttl=60)
def get_scenarios() -> pd.DataFrame:
    return da.load_scenarios()


@st.cache_data(show_spinner=False, ttl=60)
def get_is_synthetic() -> bool:
    return da.default_repository().synthetic


def refresh() -> None:
    """Xoá cache — dùng khi vừa sinh lại fixtures hoặc có log mới."""
    st.cache_data.clear()


# ---------------------------------------------------------------------------
# Hiển thị
# ---------------------------------------------------------------------------
def banner() -> None:
    """Nhãn nguồn dữ liệu — bắt buộc để không ai nhầm số mẫu là kết quả thật."""
    if get_is_synthetic():
        st.warning(
            "**DỮ LIỆU MẪU (tổng hợp)** — dashboard chưa kết nối môi trường. "
            "Số liệu do `scripts/make_fixtures.py` sinh ra để dựng giao diện; "
            "không dùng trong báo cáo như kết quả thực nghiệm.",
            icon="⚠️",
        )
    else:
        st.success("Đang đọc log thật từ `logs/`.", icon="✅")


def page_header(title: str, subtitle: str) -> None:
    st.title(title)
    st.caption(subtitle)
    banner()


def kpi_row(items: list[tuple[str, str, str | None]]) -> None:
    """Một hàng KPI: ``(nhãn, giá trị, help)``."""
    columns = st.columns(len(items))
    for column, (label, value, help_text) in zip(columns, items, strict=True):
        column.metric(label, value, help=help_text)


def fmt_int(value: float) -> str:
    return f"{value:,.0f}".replace(",", ".")


def fmt_float(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}".replace(",", ".")


def fmt_pct(value: float) -> str:
    return f"{value:.1%}"


def select_scenario(runs: pd.DataFrame, *, key: str = "scenario") -> str:
    scenarios = sorted(runs["scenario"].unique())
    return st.sidebar.selectbox("Kịch bản thời tiết", scenarios, key=key)


def select_agent(runs: pd.DataFrame, scenario: str, *, key: str = "agent") -> str:
    agents = sorted(runs.loc[runs["scenario"] == scenario, "agent"].unique())
    preferred = agents.index("qlearning") if "qlearning" in agents else 0
    return st.sidebar.selectbox("Chiến lược", agents, index=preferred, key=key)


def scenario_cards(scenarios: pd.DataFrame) -> None:
    if scenarios.empty:
        return
    columns = st.columns(len(scenarios))
    for column, row in zip(columns, scenarios.itertuples(index=False), strict=False):
        with column:
            st.markdown(f"**{row.scenario}**")
            st.caption(row.description)
            st.markdown(
                f"🌧️ mưa {row.rain} · 🌡️ {row.temperature} · "
                f"🌱 cây {row.crop_type} · giai đoạn {row.growth_stage}"
            )
