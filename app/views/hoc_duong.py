"""Trang 2 — Learning curve: quá trình học của một chiến lược."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from app import components as ui
from app import data_access as da


def render() -> None:
    runs = ui.get_runs()
    ui.page_header(
        "Learning curve",
        "Reward tăng dần theo episode = agent đang học. So sánh độ dốc và độ ổn định giữa các chiến lược.",
    )
    if runs.empty:
        st.error("Không tìm thấy CSV nào. Chạy `python scripts/make_fixtures.py` trước.")
        return

    scenario = ui.select_scenario(runs, key="lc_scenario")
    agent = ui.select_agent(runs, scenario, key="lc_agent")
    window = st.sidebar.slider("Cửa sổ trung bình trượt", 1, 15, 5)

    episodes = ui.get_episodes(agent, scenario)
    if episodes.empty:
        st.warning("Cặp này chưa có dữ liệu.")
        return

    k = da.kpis(episodes, window=max(1, window))
    ui.kpi_row(
        [
            ("Reward TB cuối", ui.fmt_float(k["reward"]), None),
            ("Reward tốt nhất", ui.fmt_float(k["best_reward"]), None),
            ("Hội tụ ở episode", "—" if k["converged_at"] is None else str(k["converged_at"]), "Trung bình trượt đạt 90% mức cuối"),
            ("Số episode", str(k["episodes"]), None),
        ]
    )

    st.divider()
    st.subheader(f"Reward theo episode — {agent} / {scenario}")
    curve = pd.DataFrame({"reward": episodes["reward"].to_numpy()}, index=episodes["episode"])
    curve[f"trung bình trượt ({window})"] = da.moving_average(episodes["reward"], window).to_numpy()
    st.line_chart(curve, height=340)

    left, right = st.columns(2)
    with left:
        st.subheader("Reward tích luỹ")
        cumulative = pd.DataFrame(
            {"cộng dồn": episodes["reward"].cumsum().to_numpy()}, index=episodes["episode"]
        )
        st.line_chart(cumulative, height=260)
        st.caption("Độ dốc càng lớn ⇒ học càng nhanh.")

    with right:
        st.subheader("Phân bố reward mỗi episode")
        counts, edges = np.histogram(episodes["reward"].to_numpy(), bins=12)
        hist = pd.DataFrame(
            {"số episode": counts},
            index=[f"{edges[i]:.0f}…{edges[i + 1]:.0f}" for i in range(len(counts))],
        )
        st.bar_chart(hist, height=260)
        st.caption("Phân bố hẹp = học ổn định; đuôi trái dài = còn episode thất bại.")

    steps = ui.get_steps(agent, scenario)
    if not steps.empty:
        st.subheader("Hành vi trung bình theo ngày trong mùa")
        by_day = steps.groupby("day", as_index=True).agg(
            reward=("reward", "mean"), water_L=("water_L", "mean")
        )
        st.line_chart(by_day, height=280)
        st.caption("Cho thấy agent tưới nhiều ở đầu mùa hay rải đều; reward/ngày phản ánh chuỗi quyết định.")

    with st.expander("Đọc learning curve thế nào?"):
        st.markdown(
            """
- **Đường gốc** dao động mạnh là bình thường (mỗi episode một chuỗi thời tiết khác nhau).
- Nhìn **đường trung bình trượt** để kết luận: đi lên rồi đi ngang = đã hội tụ.
- **Reward tích luỹ** gần như tuyến tính sau khi hội tụ ⇒ chính sách ổn định.
- Nếu reward cuối thấp hơn giữa chừng ⇒ dao động chính sách (thường gặp ở MC, ε cao).
        """
        )
