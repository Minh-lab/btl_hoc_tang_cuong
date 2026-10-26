# TÓM TẮT SESSION — 26/10/2026

> Phạm vi: trao đổi về thiết lập môi trường AgriWater-RL, cách sử dụng, luồng hoạt
> động tổng quát, và quyết định dựng sớm phần giao diện (dashboard) ở chế độ
> chỉ hiển thị. Ghi lại để người khác trong nhóm đọc được mà không cần xem lại
> toàn bộ hội thoại.

## 1. Câu hỏi đã đặt ra

| # | Câu hỏi | Kết luận |
|---|---|---|
| 1 | Thiết lập môi trường cần làm gì? | 3 tầng: môi trường phát triển (venv + deps + package), môi trường RL `AgriWaterEnv` theo 5 cổng G0–G4, điều kiện hoàn thành (≥20 test xanh, ≥10.000 bước/giây, …) |
| 2 | Cấu trúc thư mục hiện tại? | Đã giải thích cây `N10_RF/`, vai trò từng module, trạng thái code thật/chưa code |
| 3 | Sau khi thiết lập thì dùng thế nào, có cần GUI/API? | Không cần GUI, không cần REST. Dùng như thư viện Python theo chuẩn Gymnasium (`reset/step`). GUI là tầng tùy chọn phía trên |
| 4 | Luồng hoạt động tổng quát? | 4 lớp: Presentation → Application → RL & Simulation → Data; một bước `step()`, một episode 30 ngày, 4 chiến lược chạy chung một env |
| 5 | Làm phần nhìn thấy được trước (chỉ hiển thị, chưa kết nối) có được không? | **Được và nên làm**, với điều kiện mock nằm ở tầng dữ liệu, schema khớp logger, `app/` không import lõi |

## 2. Quyết định đã chốt

- **Dashboard dùng Streamlit** (đúng lựa chọn UC-06 trong tài liệu thiết kế), kèm CSV mẫu.
- **4 trang**: Tổng quan · Learning curve · So sánh 4 chiến lược · Diễn biến độ ẩm 30 ngày.
- **Read-only**: chưa có nút huấn luyện, chưa chạy env trong web, chưa upload kịch bản.
- **Mock ở tầng dữ liệu**: UI chỉ đọc qua `CsvRunRepository`; chuyển sang log thật bằng cách đặt log vào `logs/` hoặc đặt `AGRIWATER_LOGS=<thư mục>`.
- **Không thêm `streamlit` vào `requirements.txt` của lõi** — chỉ để trong extra `dashboard` của `pyproject.toml`.
- **Sinh CSV mẫu bằng script có seed**, gắn nhãn "DỮ LIỆU MẪU (synthetic)"; không gõ tay số liệu, không đưa số mẫu vào báo cáo như kết quả thật.
- Dashboard là **prototype giao diện**, timebox ≤ 4 giờ, không được chặn E-03/E-05/E-07/E-11.

## 3. Hiện trạng repo (đầu session → hiện tại)

- Dự án thật nằm ở `N10_RF/`, **có git repo riêng**; repo cha `reinforcement-learning/` chỉ còn tham chiếu cũ.
- Mã nguồn đã có khung: `agriwater/env/{contract,config,weather_model,physics,reward,agriwater_env}.py`, `agriwater/agents/*`, `agriwater/utils/metrics.py`, `configs/scenarios/*.json`, `tests/` (8 file).
- Đã cài đặt: `contract`, `config`, khung agent/registry/discretizer/logger.
- **Chưa cài đặt** (đang `NotImplementedError`): `WeatherModel.reset/sample`, toàn bộ `physics`, `reward`, `AgriWaterEnv.reset/step/render`.
- Kết quả test tại thời điểm chụp: **28 passed, 19 xfailed** (`xfail(strict=True)` canh phần chưa code).
- Môi trường: Python 3.14.8, venv `.venv` dùng `--system-site-packages`; có numpy 2.5.4, pandas 3.1.0, matplotlib 3.11.2, pytest 9.1.1. **Chưa có streamlit** (đã kiểm tra `pip install --dry-run streamlit` resolve được trên Python 3.14).

## 4. Việc đã làm trong session

| File | Trạng thái | Nội dung |
|---|---|---|
| `app/__init__.py` | ✅ tạo mới | Docstring nêu rõ dashboard không import `agriwater` |
| `app/data_access.py` | ✅ tạo mới | `FIELDS` (13 cột khớp `MetricsLogger`), `CsvRunRepository`, `default_repository()`, `episode_summary()`, `moving_average()`, `convergence_episode()`, `kpis()`, `load_scenarios()` |

Chưa commit. `git status`: `?? app/` và `?? docs/KeHoach_NganGon_MC_Va_MoiTruong.pdf` (PDF có từ trước, chưa track).

## 5. Việc còn dang dở (dashboard chưa chạy được)

> **Cập nhật cuối ngày 26/10:** cả 7 bước dưới đây **đã xong** (xem mục 8). Mục này giữ
> lại để đối chiếu lịch sử; việc tiếp theo quay về lõi: E-03 → E-05/E-07 → E-10/E-11.

Cần làm tiếp, theo thứ tự:

1. `scripts/make_fixtures.py` — sinh 4 agent × 3 kịch bản × 30 episode CSV mẫu, dùng hằng số từ `agriwater.env.contract`, seed cố định.
2. `app/components.py` — banner "DỮ LIỆU MẪU", KPI card, tiện ích format.
3. `app/views/{tong_quan,hoc_duong,so_sanh,mo_phong}.py` + `app/streamlit_app.py` (dùng `st.navigation`).
4. `pyproject.toml` — thêm `[project.optional-dependencies] dashboard = ["streamlit>=1.40"]`.
5. `tests/test_dashboard_schema.py` — canh `app.data_access.FIELDS == MetricsLogger.FIELDS`.
6. Cài `pip install -e ".[dashboard]"`, chạy thử `streamlit run app/streamlit_app.py --server.headless true`, kiểm tra HTTP 200.
7. README — thêm mục "Dashboard prototype" + 2 lệnh chạy.

Sau đó quay lại lõi: **E-03 reward → E-05/E-07 weather+physics → E-10/E-11 reset/step**, rồi mới nối `logs/` thật vào dashboard.

## 6. Ghi chú kỹ thuật đáng nhớ

- Schema CSV của dashboard **phải** khớp `agriwater/utils/metrics.py::FIELDS`: `episode, day, agent, scenario, crop_type, growth_stage, moisture, action, water_L, reward, crop_stress, ideal, stress_days`.
- Metric trên dashboard: cumulative reward, tổng nước/episode, `ideal_ratio`, số ngày stress, tỉ lệ sống hết mùa, episode hội tụ (moving average đạt 90% mức cuối).
- Một episode = 30 ngày; `terminated` khi stress 3 ngày liên tiếp, `truncated` khi hết 30 ngày — dashboard suy ra "sống hết mùa" từ `days >= 30`.
- Rủi ro đã ghi nhận: dashboard đẹp dễ làm trễ phần lõi; số liệu mẫu dễ bị nhầm là kết quả thật; hard-code số trong page sẽ phải viết lại khi nối log thật.

## 7. Bước kế tiếp đề xuất

Hoàn tất 7 mục ở phần 5 (khoảng 2–3 giờ), chụp màn hình 4 trang cho slide, rồi **dừng phần UI** và quay lại cài `calculate_reward()` (E-03) để có episode thật đầu tiên.

## 8. Kết quả thực hiện 7 bước (cuối ngày 26/10)

| Bước | Kết quả |
|---|---|
| 1. Fixtures | `scripts/make_fixtures.py` — 12 CSV (4 agent × 3 kịch bản × 30 episode), 536 KB, seed cố định |
| 2. Components | `app/components.py` — banner nguồn dữ liệu, KPI, cache có TTL, chọn kịch bản/chiến lược |
| 3. Views + entry | `app/views/{tong_quan,hoc_duong,so_sanh,mo_phong}.py` + `app/streamlit_app.py` (`st.navigation`) |
| 4. Extra | `pyproject.toml` thêm `dashboard = ["streamlit>=1.40"]`; đã cài streamlit 1.66.1 |
| 5. Test canh schema | `tests/test_dashboard_schema.py` (1 test schema + 12 test fixtures) |
| 6. Chạy thử | `AppTest` 4 trang: 0 exception · server thật: HTTP 200, `/health` = ok |
| 7. README | thêm mục "Dashboard prototype" + 3 lệnh chạy + cách chuyển sang `logs/` |

Kiểm thử toàn bộ: **41 passed, 19 xfailed** (28 test lõi + 13 test dashboard).

### Phát hiện cần báo nhóm (Trưởng — physics)

Với đúng công thức trong `docs/03_04_PhanTich_ThietKe_MoiTruong.md`:

```
D_t     = max(0, m_t + ΔI + ΔR − θ_fc)
m_{t+1} = clip(m_t + ΔI + ΔR − ET − D_t)
```

suy ra `m_{t+1} ≤ θ_fc − ET < 0.85`, nên **ngưỡng stress ngập úng `m > 0.85` không bao giờ xảy ra**. Cần chốt lại: hoặc bỏ nhánh stress trên, hoặc tính `D_t` từ nước đọng của ngày trước (`max(0, m_t − θ_fc)`) để nước tưới/mưa hôm nay có thể đẩy `m` vượt 0.85. Đây là lỗi đặc tả, **chưa sửa** trong lõi.

### Khác biệt có chủ ý của fixtures (không đưa vào lõi)

- hệ số mưa `rainfall_mm / 700` (trần 0.10) thay vì `/50` (trần 0.35), để kịch bản mưa bão không bão hoà độ ẩm cả mùa;
- độ ẩm ban đầu 0.50 thay vì 0.55.

Ghi rõ trong docstring `scripts/make_fixtures.py`; env thật vẫn dùng `contract.py`.

### Việc tiếp theo

1. Chụp màn hình 4 trang cho slide (dùng fixtures, ghi chú "prototype").
2. Dừng phần UI.
3. Quay lại lõi: **E-03 reward → E-05/E-07 weather + physics → E-10/E-11 reset/step**.
4. Khi có log thật: chạy lại `streamlit run app/streamlit_app.py` với `logs/` — không sửa UI.

## 9. Docker & chia sẻ cho nhóm

- Thêm `Dockerfile`, `.dockerignore`, `docker-compose.yml`, `scripts/run_dashboard.sh`.
- Ảnh dùng `python:3.12-slim`, **không** cài torch mặc định; build arg `INSTALL_TORCH=true` khi cần DQN.
- `docker compose up --build` → dashboard cổng 8501; `docker compose run --rm test` → pytest.
- Mount `./logs` để dashboard tự đọc log thật khi có.
- **Chưa build thử** trên máy tạo vì máy không có Docker; cần một thành viên có Docker chạy
  `docker compose up --build` lần đầu và báo log nếu lỗi. Kiểm tra tĩnh đã làm: YAML hợp lệ,
  `pytest` 41 passed / 19 xfailed, dashboard chạy bằng venv.
- Docker là **tùy chọn**; cách chính vẫn là `bash scripts/setup.sh` (nhẹ hơn, có thể sửa code ngay).


