"""Trang 1 — Tổng quan: KPI của một cặp (chiến lược, kịch bản)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app import components as ui
from app import data_access as da


def render() -> None:
    runs = ui.get_runs()
    ui.page_header(
        "AgriWater-RL · Tổng quan",
        "Hệ thống ra quyết định tưới tiêu · 7 chiều trạng thái · 6 mức tưới · episode 30 ngày",
    )

    if runs.empty:
        st.error("Không tìm thấy CSV nào. Chạy `python scripts/make_fixtures.py` trước.")
        return

    ui.scenario_cards(ui.get_scenarios())
    st.divider()

    scenario = ui.select_scenario(runs)
    agent = ui.select_agent(runs, scenario)
    if st.sidebar.button("🔄 Làm mới dữ liệu", help="Xoá cache và đọc lại CSV"):
        ui.refresh()
        st.rerun()
    st.sidebar.caption(f"{len(runs)} cặp (chiến lược, kịch bản) trong kho dữ liệu.")

    episodes = ui.get_episodes(agent, scenario)
    if episodes.empty:
        st.warning("Cặp này chưa có dữ liệu.")
        return

    k = da.kpis(episodes)
    ui.kpi_row(
        [
            ("Reward TB · 5 ep cuối", ui.fmt_float(k["reward"]), "Tổng reward một episode, trung bình 5 episode cuối"),
            ("Tổng nước TB", f"{ui.fmt_float(k['water_L'], 0)} L", "Lượng nước tưới cộng dồn trong một episode"),
            ("Thời gian ẩm lý tưởng", ui.fmt_pct(k["ideal_ratio"]), "Tỉ lệ ngày có độ ẩm trong dải lý tưởng"),
            ("Ngày stress TB", ui.fmt_float(k["stress_days"], 1), "Số ngày độ ẩm < 0.20 hoặc > 0.85"),
            ("Sống hết mùa", ui.fmt_pct(k["survival"]), "Tỉ lệ episode không bị cây chết giữa chừng"),
            ("Hội tụ ở episode", "—" if k["converged_at"] is None else str(k["converged_at"]), "Episode đầu tiên mà trung bình trượt đạt 90% mức cuối"),
        ]
    )
    st.caption(
        f"Chiến lược **{agent}** · kịch bản **{scenario}** · "
        f"{k['episodes']} episode · tốt nhất {ui.fmt_float(k['best_reward'])}"
    )

    st.divider()
    left, right = st.columns(2)

    with left:
        st.subheader("Reward theo episode")
        curve = pd.DataFrame({"reward": episodes["reward"].to_numpy()}, index=episodes["episode"])
        curve["trung bình trượt (5)"] = da.moving_average(episodes["reward"], 5).to_numpy()
        st.line_chart(curve, height=280)
        st.caption("Đường mờ = reward từng episode; đường đậm = trung bình trượt 5 episode.")

    with right:
        st.subheader("Nước tưới theo episode")
        water = pd.DataFrame({"nước (L)": episodes["water_L"].to_numpy()}, index=episodes["episode"])
        st.bar_chart(water, height=280)
        st.caption("Tổng lượng nước tưới của mỗi episode — càng thấp càng tiết kiệm.")

    st.subheader("Thời gian giữ ẩm lý tưởng")
    ideal = pd.DataFrame({"ideal_ratio": episodes["ideal_ratio"].to_numpy()}, index=episodes["episode"])
    st.line_chart(ideal, height=220)

    with st.expander("10 episode gần nhất"):
        st.dataframe(
            episodes.tail(10).style.format(
                {
                    "reward": "{:.1f}",
                    "water_L": "{:.0f}",
                    "ideal_ratio": "{:.2f}",
                    "stress_days": "{:.0f}",
                }
            ),
            hide_index=True,
            width="stretch",
        )

    with st.expander("Cách đọc trang này"):
        st.markdown(
            """
- Mỗi **episode** là một mùa 30 ngày; kết thúc sớm nếu cây bị stress 3 ngày liên tiếp.
- **Reward** càng cao càng tốt: +10 khi độ ẩm lý tưởng, −100 khi cây stress, trừ thêm theo lượng nước.
- **Sống hết mùa** dưới 100% nghĩa là agent đã để cây chết ít nhất một lần.
- **Hội tụ** là episode đầu tiên mà trung bình trượt đạt 90% mức cuối — chỉ số tốc độ học, càng sớm càng tốt.
            """
        )
