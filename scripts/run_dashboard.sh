#!/usr/bin/env bash
# Mở dashboard AgriWater-RL. Chạy được từ bất kỳ thư mục nào:
#   bash scripts/run_dashboard.sh
#   bash scripts/run_dashboard.sh --server.port 8502
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -x .venv/bin/streamlit ]; then
    echo "Chưa có streamlit trong .venv. Cài trước:"
    echo "  .venv/bin/python -m pip install -e '.[dashboard]'"
    exit 1
fi

exec .venv/bin/streamlit run app/streamlit_app.py "$@"
