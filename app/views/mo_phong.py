"""Trang 4 — Mô phỏng: diễn biến độ ẩm và lượng tưới của một episode."""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from app import components as ui
from app import data_access as da


def _moisture_chart(steps: pd.DataFrame) -> alt.LayerChart:
    band = (
        alt.Chart(pd.DataFrame({"lo": [da.IDEAL_LO], "hi": [da.IDEAL_HI]}))
        .mark_rect(color="#2e7d32", opacity=0.15)
        .encode(y=alt.Y("lo:Q", title="Độ ẩm đất"), y2="hi:Q")
    )
    rules = (
        alt.Chart(pd.DataFrame({"y": [da.WILT_POINT, da.FIELD_CAPACITY]}))
        .mark_rule(color="#c62828", strokeDash=[5, 4])
        .encode(y="y:Q")
    )
    line = (
        alt.Chart(steps)
        .mark_line(point=True, color="#1565c0")
        .encode(
            x=alt.X("day:Q", title="Ngày"),
            y=alt.Y("moisture:Q", scale=alt.Scale(domain=[0, 1]), title="Độ ẩm đất"),
            tooltip=[
                alt.Tooltip("day:Q", title="Ngày"),
                alt.Tooltip("moisture:Q", title="Độ ẩm", format=".3f"),
                alt.Tooltip("water_L:Q", title="Nước (L)"),
                alt.Tooltip("reward:Q", title="Reward", format=".1f"),
            ],
        )
    )
    stress = (
        alt.Chart(steps[steps["crop_stress"] == 1])
        .mark_point(color="#c62828", size=90, filled=True)
        .encode(x="day:Q", y="moisture:Q")
    )
    return (band + rules + line + stress).properties(height=380)


def render() -> None:
    runs = ui.get_runs()
    ui.page_header(
        "Mô phỏng một mùa",
        "Theo dõi độ ẩm đất, lượng nước tưới và phần thưởng của từng ngày trong episode.",
    )
    if runs.empty:
        st.error("Không tìm thấy CSV nào. Chạy `python scripts/make_fixtures.py` trước.")
        return

    scenario = ui.select_scenario(runs, key="mp_scenario")
    agent = ui.select_agent(runs, scenario, key="mp_agent")
    steps_all = ui.get_steps(agent, scenario)
    if steps_all.empty:
        st.warning("Cặp này chưa có dữ liệu.")
        return

    episodes = sorted(steps_all["episode"].unique())
    episode = st.sidebar.selectbox("Episode", episodes, index=len(episodes) - 1, key="mp_episode")
    steps = steps_all[steps_all["episode"] == episode].reset_index(drop=True)

    last = steps.iloc[-1]
    survived = int(last["day"]) >= 30
    ui.kpi_row(
        [
            ("Số ngày", str(int(last["day"])), "Kết thúc sớm nếu cây chết"),
            ("Tổng nước", f"{ui.fmt_float(steps['water_L'].sum(), 0)} L", None),
            ("Tổng reward", ui.fmt_float(steps["reward"].sum()), None),
            ("Ngày stress", str(int(steps["crop_stress"].sum())), "Độ ẩm < 0.20 hoặc > 0.85"),
            ("Kết thúc", "Hết mùa" if survived else "Cây chết", None),
        ]
    )

    st.divider()
    st.subheader("Độ ẩm đất theo ngày")
    st.altair_chart(_moisture_chart(steps), width="stretch")
    st.caption(
        f"Vùng xanh = dải lý tưởng [{da.IDEAL_LO}, {da.IDEAL_HI}] · "
        f"đường đỏ nét đứt = ngưỡng héo {da.WILT_POINT} và sức chứa {da.FIELD_CAPACITY} · "
        "chấm đỏ = ngày bị stress."
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Nước tưới mỗi ngày")
        st.bar_chart(steps.set_index("day")["water_L"], height=260)
    with right:
        st.subheader("Reward mỗi ngày")
        st.bar_chart(steps.set_index("day")["reward"], height=260)

    with st.expander("Bảng chi tiết từng ngày"):
        st.dataframe(
            steps[
                ["day", "moisture", "action", "water_L", "reward", "crop_stress", "ideal", "stress_days"]
            ].rename(
                columns={
                    "day": "Ngày",
                    "moisture": "Độ ẩm",
                    "action": "Hành động",
                    "water_L": "Nước (L)",
                    "reward": "Reward",
                    "crop_stress": "Stress",
                    "ideal": "Lý tưởng",
                    "stress_days": "Chuỗi stress",
                }
            ),
            hide_index=True,
            width="stretch",
        )

    st.info(
        "Một bước = một ngày. Agent thấy dự báo thời tiết trong obs rồi chọn mức tưới; "
        "môi trường cập nhật độ ẩm bằng cân bằng nước (tưới + mưa − bốc thoát − thấm thoát) "
        "và trả reward theo 6 thành phần."
    )
