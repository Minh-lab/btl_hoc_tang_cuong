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

Hiện trạng: **28 passed, 19 xfailed**. Các test `xfail(strict=True)` là phần **chưa
cài đặt** (reward, vật lý, `reset`/`step`) — chúng mang sẵn kỳ vọng đúng nên khi
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
tests/                                            # 47 test, chia theo task
docs/                                             # báo cáo, thiết kế, kế hoạch
scripts/setup.sh                                  # cài đặt
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
