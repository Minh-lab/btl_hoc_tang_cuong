# AgriWater-RL

Hệ thống ra quyết định tưới tiêu tự động tối ưu hóa nguồn nước trong nông nghiệp.
Bài tập lớn môn *Học tăng cường và ứng dụng* — Nhóm 10, Khoa Công nghệ thông tin, Trường Đại học Thủy lợi.

MDP: trạng thái **7 chiều**, **6 mức tưới** $\{0,5,10,15,20,25\}$ L, reward **6 thành phần**, episode **30 ngày**, $\gamma = 0.99$, môi trường **model-free**.

## Cài đặt (1 lần, sau khi clone/pull)

```bash
bash scripts/setup.sh        # tạo .venv, cài thư viện, cài package ở chế độ editable
```

Script dùng `--system-site-packages` để tái sử dụng `torch` có sẵn. Nếu máy chưa có, cài thủ công:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Lệnh hằng ngày

```bash
.venv/bin/python -m pytest                 # toàn bộ test
.venv/bin/python -m pytest -m "not slow"   # bỏ test hiệu năng
.venv/bin/python -m pytest tests/test_reward.py -v
```

## Dashboard prototype (chỉ hiển thị)

Giao diện 4 trang dựng **trước** khi môi trường chạy được, để cả nhóm hình dung sản phẩm.
Dashboard **chỉ đọc CSV**, không huấn luyện, không import `agriwater`.

```bash
.venv/bin/python -m pip install -e ".[dashboard]"      # cài streamlit (extra, không ảnh hưởng lõi)
.venv/bin/python scripts/make_fixtures.py               # sinh CSV mẫu (dữ liệu TỔNG HỢP)
bash scripts/run_dashboard.sh                           # mở http://localhost:8501
```

- Dữ liệu mẫu nằm ở `app/sample_data/`, do `scripts/make_fixtures.py` sinh có seed. **Không**
  trích số liệu ở đây vào báo cáo — đây không phải kết quả thực nghiệm.
- Khi lõi chạy được: đặt log thật vào `logs/` (đúng schema `MetricsLogger`) hoặc đặt
  `AGRIWATER_LOGS=<thư mục>`; dashboard tự chuyển sang log thật, không sửa code UI.
- Schema 13 cột của dashboard được canh bởi `tests/test_dashboard_schema.py`.

## Docker (tùy chọn)

Chỉ cần khi máy thành viên không muốn cài Python/venv, hoặc cần môi trường giống hệt để demo.
Cách chính vẫn là `bash scripts/setup.sh`.

```bash
docker compose up --build            # dashboard: http://localhost:8501
docker compose run --rm test         # chạy toàn bộ pytest trong container
docker compose down                  # tắt
```

- Ảnh dùng `python:3.12-slim`; **không** cài torch mặc định. Cần DQN:
  `docker build --build-arg INSTALL_TORCH=true -t agriwater-rl:torch .`
- Thư mục `./logs` được mount vào container; có CSV thì dashboard đọc log thật,
  không có thì dùng fixtures trong `app/sample_data/`.
- Code trong image là bản copy lúc build — sửa code phải `docker compose up --build` lại.

## Hiện trạng

**41 passed, 19 xfailed** (28 test lõi + 13 test dashboard). Các test `xfail(strict=True)` là phần
**chưa cài đặt** (reward, vật lý, `reset`/`step`) — chúng mang sẵn kỳ vọng đúng nên khi
code xong, test chuyển xanh và ai quên gỡ `pytestmark` sẽ thấy `XPASS(strict)` báo lỗi.

## Cấu trúc

```
agriwater/
├── env/
│   ├── contract.py        # HỢP ĐỒNG G0: chỉ số obs, hằng số, ngưỡng reward  [chung]
│   ├── config.py          # EnvConfig — mọi tham số, không hard-code            [Trưởng]
│   ├── weather_model.py   # sinh thời tiết theo kịch bản JSON                    [Trưởng]
│   ├── physics.py         # cân bằng nước: ET, mưa, thấm thoát                   [Trưởng]
│   ├── reward.py          # R = 6 thành phần                                     [Minh]
│   └── agriwater_env.py   # AgriWaterEnv: Box(7), Discrete(6), reset/step/render [Trưởng]
├── agents/
│   ├── base.py            # interface Agent dùng chung                           [Minh]
│   ├── registry.py        # make("qlearning" | "mc" | "dqn" | "baseline"...)
│   ├── random_agent.py    # agent ngẫu nhiên, chạy được ngay
│   └── discretizer.py     # obs → 480 trạng thái (dùng chung Q-Learning & MC)    [Minh]
└── utils/metrics.py       # MetricsLogger → CSV (UC-05)                          [Minh]

configs/scenarios/{dry,stormy,randomized}.json    # kịch bản, KHÔNG hard-code
tests/                                            # 60 test, chia theo task
docs/                                             # báo cáo, thiết kế, kế hoạch
app/                                              # dashboard prototype (Streamlit, chỉ đọc CSV)
├── streamlit_app.py                              # entry: st.navigation 4 trang
├── data_access.py                                # CsvRunRepository (fixtures ↔ logs)
├── components.py                                 # banner, KPI, cache
├── views/{tong_quan,hoc_duong,so_sanh,mo_phong}.py
└── sample_data/                                  # CSV tổng hợp — KHÔNG phải kết quả thật
scripts/setup.sh                                  # cài đặt
scripts/make_fixtures.py                          # sinh CSV mẫu cho dashboard
```

Tài liệu: `docs/KeHoach_MoiTruong_Minh_Truong.md` (hợp đồng + task E-01…E-23),
`docs/03_04_PhanTich_ThietKe_MoiTruong.md` (vật lý & kiến trúc),
`docs/HocTangCuongN10_HoanChinh.docx` (báo cáo V2).

## Việc tiếp theo (theo thứ tự phụ thuộc)

| Task | Nội dung | Người | Test sẽ chuyển xanh |
|---|---|---|---|
| E-03 | `reward.calculate_reward()` | Minh | `tests/test_reward.py` (10) |
| E-05/E-06 | `WeatherModel.sample()` | Trưởng | `test_contract.py` (đã xanh) + test mới của E-05 |
| E-07 | `physics.update_moisture()` | Trưởng | `tests/test_physics.py` (3) |
| E-10/E-11/E-12 | `reset()` / `step()` / cờ kết thúc | Trưởng | `test_env_api.py`, `test_determinism.py`, `test_speed.py` |

Khi xong một task: gỡ `pytestmark` xfail ở file test tương ứng, chạy `pytest`, rồi mở PR nhỏ (≤ 2 ngày, 1 nhánh = 1 task). Chi tiết quy trình ở mục 3 của tài liệu kế hoạch.
