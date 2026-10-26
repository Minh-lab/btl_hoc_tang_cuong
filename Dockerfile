# Ảnh Docker cho AgriWater-RL — chỉ chứa những gì cần để chạy dashboard/test.
#
#   docker compose up --build            # dashboard tại http://localhost:8501
#   docker compose run --rm dashboard python -m pytest
#
# Mặc định KHÔNG cài torch (~2 GB). Cần DQN thì build:
#   docker build --build-arg INSTALL_TORCH=true -t agriwater-rl:torch .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Cài dependency trước khi copy code để tận dụng cache layer.
COPY pyproject.toml README.md ./
COPY agriwater ./agriwater
RUN python -m pip install --upgrade pip \
    && python -m pip install ".[dashboard,viz,dev]"

ARG INSTALL_TORCH=false
RUN if [ "$INSTALL_TORCH" = "true" ]; then \
        python -m pip install "torch>=2.0"; \
    fi

COPY configs ./configs
COPY app ./app
COPY scripts ./scripts
COPY tests ./tests

RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "app/streamlit_app.py", \
     "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
