#!/usr/bin/env bash
# Cài đặt môi trường phát triển cho AgriWater-RL (chạy 1 lần sau khi clone).
#   bash scripts/setup.sh
# Dùng --system-site-packages để tái sử dụng torch/numpy đã cài sẵn (tránh tải lại ~2 GB).
set -euo pipefail
cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"

if [ ! -d .venv ]; then
    echo "==> Tạo .venv bằng $PYTHON"
    "$PYTHON" -m venv .venv --system-site-packages
fi

echo "==> Cài thư viện"
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/python -m pip install -q -r requirements.txt
.venv/bin/python -m pip install -q -e .

echo "==> Kiểm tra import"
.venv/bin/python -c "import agriwater, gymnasium, numpy; print('agriwater', agriwater.__version__, '| gymnasium', gymnasium.__version__)"

cat <<'EOF'

Xong. Lệnh dùng hằng ngày:
  .venv/bin/python -m pytest            # chạy test
  .venv/bin/python -m pytest -m "not slow"
  source .venv/bin/activate              # hoặc kích hoạt venv
EOF
