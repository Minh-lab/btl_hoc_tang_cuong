"""Entry point dashboard AgriWater-RL (Streamlit).

Chạy::

    .venv/bin/streamlit run app/streamlit_app.py

Đây là **prototype giao diện**: chỉ đọc CSV, không huấn luyện, không import lõi.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Streamlit đặt thư mục chứa script (app/) vào sys.path[0], không phải gốc dự án.
# Thêm gốc dự án để `import app...` chạy được dù khởi động từ thư mục nào.
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st  # noqa: E402

from app.views import hoc_duong, mo_phong, so_sanh, tong_quan  # noqa: E402

st.set_page_config(
    page_title="AgriWater-RL · Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

navigation = st.navigation(
    [
        st.Page(
            tong_quan.render,
            title="Tổng quan",
            icon=":material/space_dashboard:",
            url_path="tong-quan",
            default=True,
        ),
        st.Page(
            hoc_duong.render,
            title="Learning curve",
            icon=":material/show_chart:",
            url_path="learning-curve",
        ),
        st.Page(
            so_sanh.render,
            title="So sánh",
            icon=":material/compare_arrows:",
            url_path="so-sanh",
        ),
        st.Page(
            mo_phong.render,
            title="Mô phỏng",
            icon=":material/water_drop:",
            url_path="mo-phong",
        ),
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Prototype giao diện · dữ liệu đọc từ `app/sample_data/` hoặc `logs/`")

navigation.run()
