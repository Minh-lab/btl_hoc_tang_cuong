"""Trang 3 — So sánh 4 chiến lược trên cùng một kịch bản."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app import components as ui
from app import data_access as da

COLUMNS = {
    "agent": "Chiến lược",
    "reward": "Reward TB",
    "best": "Tốt nhất",
    "water": "Nước/ep (L)",
    "ideal": "Ẩm lý tưởng",
    "stress": "Ngày stress",
    "survival": "Sống hết mùa",
    "converged": "Hội tụ (ep)",
}


def _table(agents: list[str], scenario: str) -> pd.DataFrame:
    rows = []
    for agent in agents:
        episodes = ui.get_episodes(agent, scenario)
        if episodes.empty:
            continue
        k = da.kpis(episodes)
        rows.append(
            {
                "agent": agent,
                "reward": k["reward"],
                "best": k["best_reward"],
                "water": k["water_L"],
                "ideal": k["ideal_ratio"],
                "stress": k["stress_days"],
                "survival": k["survival"],
                "converged": k["converged_at"],
            }
        )
    return pd.DataFrame(rows)


def render() -> None:
    runs = ui.get_runs()
    ui.page_header(
        "So sánh chiến lược",
        "Cùng một kịch bản, cùng seed: khác biệt kết quả chỉ do thuật toán.",
    )
    if runs.empty:
        st.error("Không tìm thấy CSV nào. Chạy `python scripts/make_fixtures.py` trước.")
        return

    scenario = st.sidebar.selectbox("Kịch bản", sorted(runs["scenario"].unique()), key="ss_scenario")
    agents = sorted(runs.loc[runs["scenario"] == scenario, "agent"].unique())

    table = _table(agents, scenario)
    if table.empty:
        st.warning("Kịch bản này chưa có dữ liệu.")
        return

    st.subheader(f"Bảng so sánh — {scenario}")
    display = table.rename(columns=COLUMNS)
    st.dataframe(
        display,
        hide_index=True,
        width="stretch",
        column_config={
            "Reward TB": st.column_config.NumberColumn(format="%.1f"),
            "Tốt nhất": st.column_config.NumberColumn(format="%.1f"),
            "Nước/ep (L)": st.column_config.NumberColumn(format="%.0f"),
            "Ẩm lý tưởng": st.column_config.ProgressColumn(min_value=0.0, max_value=1.0, format="%.1%"),
            "Ngày stress": st.column_config.NumberColumn(format="%.1f"),
            "Sống hết mùa": st.column_config.ProgressColumn(min_value=0.0, max_value=1.0, format="%.1%"),
            "Hội tụ (ep)": st.column_config.NumberColumn(format="%d"),
        },
    )

    bar_data = table.set_index("agent")
    left, right = st.columns(2)
    with left:
        st.subheader("Reward trung bình")
        st.bar_chart(pd.DataFrame({"reward": bar_data["reward"]}), height=280)
        st.caption("Cao hơn = chính sách tốt hơn trên cùng kịch bản.")
    with right:
        st.subheader("Nước tiêu thụ mỗi episode")
        st.bar_chart(pd.DataFrame({"nước (L)": bar_data["water"]}), height=280)
        st.caption("Thấp hơn = tiết kiệm hơn, nhưng phải đọc kèm reward để tránh 'tiết kiệm bằng cách để cây chết'.")

    st.subheader("Ma trận reward TB: chiến lược × kịch bản")
    pivot_rows = []
    all_scenarios = sorted(runs["scenario"].unique())
    for candidate in all_scenarios:
        candidate_agents = sorted(runs.loc[runs["scenario"] == candidate, "agent"].unique())
        for agent in candidate_agents:
            episodes = ui.get_episodes(agent, candidate)
            if not episodes.empty:
                pivot_rows.append(
                    {"agent": agent, "scenario": candidate, "reward": da.kpis(episodes)["reward"]}
                )
    pivot = pd.DataFrame(pivot_rows).pivot(index="agent", columns="scenario", values="reward")
    st.dataframe(
        pivot.style.format("{:.1f}").background_gradient(cmap="RdYlGn", axis=None),
        width="stretch",
    )
    st.caption("Kịch bản khô hạn thường khó hơn mưa bão; khoảng cách giữa các cột cho thấy khả năng tổng quát hoá.")

    st.download_button(
        "⬇️ Tải bảng so sánh (CSV)",
        data=table.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"so_sanh_{scenario}.csv",
        mime="text/csv",
    )

    with st.expander("Vì sao so sánh như vậy là công bằng?"):
        st.markdown(
            """
- Cùng **một môi trường**, cùng reward, cùng bộ kịch bản ⇒ khác biệt chỉ do thuật toán.
- Số liệu lấy **5 episode cuối** để tránh may mắn của một episode đơn lẻ.
- **Hội tụ** dùng trung bình trượt đạt 90% mức cuối — thước đo tốc độ học, không phải chất lượng cuối.
- Muốn kết luận chắc chắn phải chạy **nhiều seed**; bản dashboard này đọc mọi file cùng cặp (agent, scenario) nên tự gộp seed khi có.
            """
        )
