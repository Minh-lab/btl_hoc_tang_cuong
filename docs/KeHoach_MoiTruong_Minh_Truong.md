# KẾ HOẠCH TRIỂN KHAI MÔI TRƯỜNG — MINH × TRƯỞNG

> **Phạm vi:** cài đặt `AgriWaterEnv` (7 chiều, `Discrete(6)`, 30 bước/episode) + reward 6 thành phần + bộ test, theo đặc tả tại `03_04_PhanTich_ThietKe_MoiTruong.md` và `HocTangCuongN10_HoanChinh.md`.
> **Nhân sự:** 2 người — **Nguyễn Thế Trưởng** (chủ sở hữu môi trường) và **Nguyễn Minh** (reward, test, tích hợp agent).
> **Thời lượng:** 3 tuần (10 ngày làm việc thực tế) với 5 cổng kiểm soát.
> **Nguyên tắc số 1:** *chốt hợp đồng giao diện trước, viết code song song sau* — đây là thứ duy nhất giúp 2 người không chờ nhau.

---

## 1. Cổng kiểm soát (gate)

| Gate | Thời điểm | Điều kiện qua cổng | Người xác nhận |
|---|---|---|---|
| **G0** | Cuối ngày 1 | Hợp đồng giao diện (mục 2) được chốt thành file `env/contract.py`, cả 2 ký nhận | Cả 2 |
| **G1** | Cuối ngày 2 | `calculate_reward()` chạy đúng 5 tình huống ($+6$, $+10$, $-124$, $-4$, $-10$) | Minh code, Trưởng review |
| **G2** | Cuối ngày 5 | `env.step()` chạy được 1 episode 30 bước, không lỗi | Trưởng code, Minh review |
| **G3** | Cuối ngày 8 | Toàn bộ `pytest` xanh (T1–T7) | Cả 2 |
| **G4** | Cuối ngày 10 | Smoke pipeline: 4 chiến lược chạy được 5 episode trên env thật, xuất CSV | Cả 2 |

> Quy tắc: **không qua cổng thì không bắt đầu việc của cổng sau**. Nếu trễ quá 1 ngày so với kế hoạch, báo nhóm trưởng ngay trong ngày.

---

## 2. Hợp đồng giao diện (chốt ở G0, không tự ý đổi)

Đây là "hợp đồng" để Trưởng code môi trường và Minh code reward/test **song song**. Mọi thay đổi phải được cả 2 đồng ý và ghi vào changelog cuối file.

### 2.1. Chỉ số trạng thái

| Index | Tên | Miền | Chuẩn hóa |
|---|---|---|---|
| 0 | `crop_type` | int $[0, K-1]$, $K=4$ | $x/(K-1)$ |
| 1 | `crop_growth_stage` | int $[0,3]$ | $g/3$ |
| 2 | `soil_moisture` | float $[0,1]$ | giữ nguyên |
| 3 | `temperature` | float $[15,45]$ °C | $(x-15)/30$ |
| 4 | `rain_probability` | float $[0,1]$ | giữ nguyên |
| 5 | `rain_forecast_mm` | float $[0,50]$ mm | $x/50$ (ngưỡng 0.30 ≡ 15 mm) |
| 6 | `last_irrigation` | float $[0,25]$ L | $x/25$ (ngưỡng 0.50 ≡ 12,5 L) |

### 2.2. Hành động và hằng số

```python
WATER_LEVELS = (0, 5, 10, 15, 20, 25)   # lít, index = action
EPISODE_LENGTH = 30                      # 1 bước = 1 ngày
STRESS_PATIENCE = 3                      # K: stress liên tiếp ⇒ terminated
WILT_POINT, IDEAL_LO, IDEAL_HI, FIELD_CAP = 0.20, 0.40, 0.70, 0.85
IDEAL_HI_FLOWER = 0.75                   # giai đoạn g = 2: dải [0.50, 0.75]
R_MAX_MM = 50.0
```

### 2.3. Hợp đồng `step()`

```python
obs: np.float32[7]        # đã chuẩn hóa [0,1]
reward: float             # 6 thành phần, từ calculate_reward()
terminated: bool          # stress ≥ STRESS_PATIENCE ngày
truncated: bool           # day ≥ EPISODE_LENGTH
info = {
    "water_L": float,       # 0,5,...,25
    "crop_stress": bool,    # m_next < 0.20 hoặc > 0.85
    "moisture": float,      # m_next (thô, chưa chuẩn hóa)
    "growth_stage": int,
    "ideal": bool,          # 0.40 ≤ m_next ≤ 0.70
    "stress_days": int,     # bộ đếm nội bộ, phục vụ gỡ lỗi
}
```

### 2.4. Ranh giới sở hữu file

| File | Chủ sở hữu | Người kia được làm gì |
|---|---|---|
| `env/contract.py` | **Chung** (chỉ sửa khi cả 2 đồng ý) | Đọc |
| `env/config.py` | Trưởng | Đọc, góp ý qua review |
| `env/weather_model.py` | Trưởng | Đọc |
| `env/agriwater_env.py` | Trưởng | Đọc, viết test |
| `scenarios/*.json` | Trưởng | Thêm kịch bản test |
| `env/reward.py` | Minh | Đọc |
| `tests/*` | Minh | Chạy, bổ sung test |
| `agents/discretizer.py`, `agents/registry.py` | Minh | Đọc |

> Không sửa file của người kia. Cần sửa ⇒ mở issue/ghi chú, người sở hữu sửa (tránh xung đột merge và mất ngữ cảnh).

---

## 3. QUY TRÌNH MẪU (áp dụng cho mọi task)

### 3.1. Vòng lặp 5 bước

```text
1. NHẬN TASK  → lấy task card từ todolist (mục 4)
2. VIẾT TEST ĐỎ → test mô tả đúng hành vi mong muốn, chạy thấy FAIL
3. CODE TỐI THIỂU → làm test xanh; không thêm tính năng ngoài task
4. TỰ KIỂM → chạy pytest + task card DoD + review checklist (3.4)
5. BÀN GIAO → commit + push nhánh + mở PR, tag người review; ghi 1 dòng "đã xong gì / còn gì"
```

### 3.2. Task card mẫu (copy cho mỗi task)

```markdown
### [E-xx] <tên task ngắn>
- Người làm:            Minh | Trưởng
- Ước lượng:            <giờ>
- Phụ thuộc:            <E-yy hoặc "không">
- Input:                <hàm/dữ liệu đầu vào>
- Output:               <hàm/dữ liệu đầu ra, kèm kiểu dữ liệu>
- Test bắt buộc:        <tên test + kỳ vọng cụ thể>
- DoD:                  <điều kiện kiểm chứng được, không mơ hồ>
- Người review:         <người kia>
- Trạng thái:           todo | doing | review | done
```

**Ví dụ điền sẵn (dùng làm chuẩn):**

```markdown
### [E-04] Cập nhật độ ẩm _physics()
- Người làm:            Trưởng
- Ước lượng:            3 h
- Phụ thuộc:            E-03 (WeatherModel)
- Input:                (action: int, T: float, forecast_mm: float, state: EnvState)
- Output:               m_next: float ∈ [0,1]
- Test bắt buộc:        test_physics.py::test_no_water_dries (a=0, T=42 ⇒ m giảm)
                        test_physics.py::test_clip_upper (m=0.95, a=5 ⇒ m ≤ 1.0)
                        test_physics.py::test_drainage (vượt 0.85 ⇒ có D_t)
- DoD:                  công thức mục 3.5 của tài liệu môi trường; 3 test xanh;
                        mọi giá trị trả về đã clip [0,1]
- Người review:         Minh
- Trạng thái:           todo
```

### 3.3. Quy ước git

```bash
git checkout -b feat/env-physics        # feat/ | fix/ | test/ | docs/ + phạm vi ngắn
git commit -m "feat(env): them _physics va 3 test"   # <loại>(<phạm vi>): <việc đã làm>
git push -u origin feat/env-physics     # mở PR, tag người review
```

- Nhánh sống ngắn: **≤ 2 ngày**, mỗi nhánh ≤ 1 task card.
- Không commit thẳng vào `main`; PR phải xanh test mới merge.
- Cuối mỗi ngày: rebase lên `main` để tránh lệch.

### 3.4. Review checklist (6 điểm, ai review cũng dùng)

- [ ] Hàm trả đúng kiểu/độ dài như `contract.py` (obs 7 chiều, reward float, 4 cờ bool).
- [ ] Không có hằng số "ma thuật" — lấy từ `contract.py`.
- [ ] Mọi giá trị trạng thái đã `clip()` về $[0,1]$.
- [ ] Không dùng `random`/`np.random` toàn cục — chỉ `self.np_random`.
- [ ] `env/` không import bất kỳ module `agents/` nào (NFR-5).
- [ ] Có test mới hoặc test cũ vẫn xanh; không hạ/tắt assert để test qua.

### 3.5. Xử lý khi bị chặn

| Tình huống | Làm gì |
|---|---|
| Bị chặn > 2 giờ vì thiếu phần của người kia | Nhắn ngay trong nhóm + dùng stub theo `contract.py` (ví dụ `reward` tạm trả 0.0) để tiếp tục |
| Phát hiện đặc tả mâu thuẫn | Ghi vào mục 6 (nhật ký quyết định), cả 2 chốt trong 10 phút, không tự sửa một mình |
| Test đỏ do người kia | Không sửa file người kia; gửi log + test name + kỳ vọng |
| Trễ gate | Báo nhóm trưởng trong ngày, đề xuất cắt phạm vi (thường cắt `render()` trước) |

### 3.6. Nhịp làm việc

- **10 phút đầu ngày:** chốt task hôm nay theo todolist, xác nhận không chờ nhau.
- **Cuối ngày:** cập nhật trạng thái task card (todo → doing → review → done) + 1 dòng bàn giao.
- **Cuối tuần:** chạy toàn bộ `pytest` và ghi số liệu (bước/giây, số test xanh) vào bảng gate.

---

## 4. TODOLIST TRIỂN KHAI

Ký hiệu: `[ ]` chưa xong · `[~]` đang làm · `[x]` xong · `[!]` bị chặn

### Tuần 1 — Nền tảng: hợp đồng, reward, vật lý

| ID | Task | Người | Est | Phụ thuộc | DoD |
|---|---|---|---|---|---|
| E-01 | `[ ]` Khung dự án: `requirements.txt`, package `agriwater/`, `env/contract.py` | Minh | 1 h | — | `python -c "import agriwater"`; `pytest` exit 0 |
| E-02 | `[ ]` `EnvConfig` + hằng số (`WATER_LEVELS`, ngưỡng, `K`, `episode_length`) | Trưởng | 1 h | E-01 | Không còn số "ma thuật" trong code sau này |
| E-03 | `[ ]` `calculate_reward()` 6 thành phần | Minh | 2 h | E-02 | 5 tình huống: $+6$, $+10$, $-124$, $-4$, $-10$ |
| E-04 | `[ ]` Test reward: 5 tình huống + 4 test biên ($m'=0.20/0.40/0.70/0.85$) | Minh | 2 h | E-03 | `test_reward.py` xanh (9 test); **review bởi Trưởng** |
| E-05 | `[ ]` `WeatherModel`: sinh $T$, $p$, $f$ từ JSON, dùng `np_random` | Trưởng | 3 h | E-02 | 2 lần `reset(seed=42)` cho chuỗi thời tiết giống nhau |
| E-06 | `[ ]` 3 kịch bản `dry.json`, `stormy.json`, `randomized.json` | Trưởng | 1 h | E-05 | Đổi file ⇒ hành vi env khác, **không sửa code env** |
| E-07 | `[ ]` `_physics()`: cân bằng nước, $ET$ theo $K_c$, thấm thoát $D_t$, clip | Trưởng | 3 h | E-05 | 3 test vật lý xanh + obs luôn trong $[0,1]$ |
| E-08 | `[ ]` Test vật lý (khô khi không tưới, clip trần, có $D_t$ khi vượt 0.85) | Minh | 2 h | E-07 | `test_physics.py` xanh |
| **G0/G1** | `[ ]` Chốt hợp đồng + review reward | Cả 2 | 1 h | E-01…E-04 | Gate G0, G1 đạt |

### Tuần 2 — Lớp môi trường Gymnasium

| ID | Task | Người | Est | Phụ thuộc | DoD |
|---|---|---|---|---|---|
| E-09 | `[ ]` `observation_space = Box(7)`, `action_space = Discrete(6)` | Trưởng | 1 h | E-07 | `check_env` không báo lỗi shape |
| E-10 | `[ ]` `reset(seed, options)` → `(obs, info)`; nạp kịch bản, khởi tạo `last_irrigation` | Trưởng | 2 h | E-09 | Chạy 20 lần reset liên tiếp, obs đúng 7 chiều |
| E-11 | `[ ]` `step(action)` đủ 7 bước theo hợp đồng 2.3 | Trưởng | 4 h | E-10 | 1 episode 30 bước chạy sạch |
| E-12 | `[ ]` Đếm `stress_days` + `terminated` ($K=3$) / `truncated` (30 ngày) | Trưởng | 2 h | E-11 | Test: 3 ngày $m<0.20$ ⇒ `terminated`; hết 30 bước ⇒ `truncated` |
| E-13 | `[ ]` `test_env_api.py`: `check_env`, kiểu trả về, obs trong biên, `info` đủ 6 khóa | Minh | 2 h | E-11 | T1, T10 xanh |
| E-14 | `[ ]` `test_determinism.py`: 2 lần `reset(seed=42)` + 1.000 bước giống tuyệt đối | Minh | 2 h | E-12 | NFR-1 đạt (`np.array_equal`) |
| E-15 | `[ ]` Benchmark tốc độ: 100.000 bước, in bước/giây | Minh | 1 h | E-12 | ≥ 10.000 bước/giây (NFR-2) |
| E-16 | `[ ]` `test_no_agent_import.py`: `env/` không import `agents/` | Minh | 30' | E-11 | NFR-5 đạt |
| **G2/G3** | `[ ]` Review env + chạy toàn bộ `pytest` | Cả 2 | 1 h | E-11…E-16 | Gate G2, G3 đạt |

### Tuần 3 — Tích hợp agent & bàn giao

| ID | Task | Người | Est | Phụ thuộc | DoD |
|---|---|---|---|---|---|
| E-17 | `[ ]` `Discretizer`: 7 chiều → 480 trạng thái (dùng chung Q-Learning & MC) | Minh | 2 h | E-11 | `encode(obs)` trả int ∈ $[0,480)$; test biên bin |
| E-18 | `[ ]` `AgentInterface` + `registry.py` + agent ngẫu nhiên | Minh | 2 h | E-17 | `REGISTRY["random"]` chạy được |
| E-19 | `[ ]` `MetricsLogger`: nhận `(S,A,R,info)`, xuất CSV (water, stress, ideal, reward) | Minh | 2 h | E-18 | CSV 5 episode đọc được, có moving average |
| E-20 | `[ ]` `render()`: vẽ chuỗi độ ẩm 1 episode | Trưởng | 2 h | E-11 | Sinh 1 ảnh/biểu đồ (FR-ENV-8); **cắt được nếu trễ gate** |
| E-21 | `[ ]` Smoke pipeline 4 chiến lược (Baseline + random thay Q/MC/DQN) × 5 episode | Cả 2 | 3 h | E-18, E-19 | Bảng CSV 4 dòng chiến lược, không lỗi |
| E-22 | `[ ]` README chạy thử: 3 lệnh (`pytest`, `train.py --algorithm random`, `evaluate.py`) | Trưởng | 1 h | E-21 | Người khác clone về chạy được trong 5 phút |
| E-23 | `[ ]` Bàn giao: bảng số liệu gate (test xanh, bước/giây) + nhật ký quyết định | Minh | 1 h | E-21 | Ghi vào mục 6 của tài liệu này |
| **G4** | `[ ]` Demo cho cả nhóm + chốt mốc chuyển sang thuật toán | Cả 2 | 1 h | Tất cả | Gate G4 đạt |

### Checkpoint theo ngày (dùng khi họp nhanh)

- [ ] **Ngày 1:** G0 — hợp đồng chốt, 2 nhánh git đã mở.
- [ ] **Ngày 2:** G1 — reward + 9 test xanh.
- [ ] **Ngày 3–4:** vật lý + weather + 3 kịch bản; env reset được.
- [ ] **Ngày 5:** G2 — `step()` chạy 1 episode 30 bước.
- [ ] **Ngày 6–7:** terminated/truncated, determinism, tốc độ.
- [ ] **Ngày 8:** G3 — `pytest` toàn bộ xanh.
- [ ] **Ngày 9:** Discretizer + registry + logger.
- [ ] **Ngày 10:** G4 — smoke 4 chiến lược + README + bàn giao.

---

## 5. Phân công theo năng lực và tải

| Người | Tải chính | Vì sao hợp lý | Tải ước lượng |
|---|---|---|---|
| **Nguyễn Thế Trưởng** | Môi trường: config, weather, physics, `step/reset`, `render` (E-02, E-05…E-07, E-09…E-12, E-20, E-22) | Là người đã mô hình hóa $P$ và hành động $A$ trong báo cáo ⇒ hiểu rõ động lực học | ~19 h |
| **Nguyễn Minh** | Reward, test, tích hợp: (E-01, E-03, E-04, E-08, E-13…E-19, E-21, E-23) | Đã thiết kế hàm phần thưởng $R$ ⇒ test reward do chính tác giả viết; đồng thời chuẩn bị Discretizer cho Q-Learning/MC tuần sau | ~19 h |

**Cân bằng:** mỗi người ~19 h cho 10 ngày (≈ 2 h/ngày), chừa thời gian cho môn khác. Trưởng phụ trách phần "khó gỡ lỗi" (vật lý), Minh phụ trách phần "khó sai" (test) — hai người review chéo nhau.

---

## 6. Nhật ký quyết định (điền trong quá trình làm)

| Ngày | Vấn đề | Quyết định | Người chốt |
|---|---|---|---|
| | 1 bước = 1 ngày hay 1 phút? | **1 bước = 1 ngày**, episode 30 bước | Cả 2 |
| | Ngưỡng stress liên tiếp $K$ | $K = 3$ (thử 2 và 5 nếu kết quả bất thường) | Cả 2 |
| | `rain_forecast_mm` đơn vị | Chuẩn hóa $R_{\max}=50$ mm; ngưỡng 0.30 ≡ 15 mm | Cả 2 |
| | Có đưa `stress_days` vào obs? | Không — giữ obs 7 chiều, đưa vào `info` | Cả 2 |
| 27/10/2026 | `D_t` làm ngập úng bất khả thi (`m ≤ 0.85 − ET`) | **Phương án B**: `D_t = max(0, m_t − θ_fc)` — thấm thoát từ nước đọng ngày trước; ngập úng `m > 0.85` khả thi; thêm test biên | Chủ dự án |
| | | | |

---

## 7. Rủi ro riêng của mô hình 2 người

| # | Rủi ro | Dấu hiệu | Biện pháp |
|---|---|---|---|
| 1 | Chờ nhau vì thiếu phần của người kia | Task "doing" quá 1 ngày không tiến triển | Dùng stub theo `contract.py`; hợp đồng chốt ở G0 chính là để tránh việc này |
| 2 | Lệch đặc tả (mỗi người hiểu một kiểu) | Test của Minh đỏ vì Trưởng trả khác kiểu | `contract.py` là nguồn sự thật duy nhất; sửa hợp đồng phải cả 2 đồng ý |
| 3 | Bus factor = 1 (chỉ 1 người hiểu physics) | Trưởng nghỉ ⇒ dự án dừng | Minh review toàn bộ `_physics()`, đọc test như tài liệu |
| 4 | Env chậm (< 10.000 bước/giây) | Benchmark ngày 7 thấy thấp | Vector hóa, tránh tạo mảng mỗi bước; đo lại trước khi qua G3 |
| 5 | Test "xanh giả" | Ai đó sửa assert/ngưỡng cho qua | Review checklist 3.4: cấm hạ assert; số test phải tăng, không giảm |
| 6 | Trễ gate do `render()` | Task E-20 kéo dài | `render()` là task **cắt được** — FR-ENV-8 không chặn thuật toán |

---

## 8. Bàn giao cuối giai đoạn (định nghĩa hoàn thành)

- [ ] `pytest` xanh toàn bộ (T1–T7), số test ≥ 20.
- [ ] Tốc độ ≥ 10.000 bước/giây, có log số đo.
- [ ] Reward khớp 5 tình huống của MDP.
- [ ] 3 kịch bản JSON chạy được, không sửa code env.
- [ ] `Discretizer` 480 trạng thái + `registry.py` + `MetricsLogger` chạy được.
- [ ] Smoke pipeline 4 chiến lược (Baseline, random; Q-Learning/MC/DQN thay sau) xuất CSV.
- [ ] README 3 lệnh chạy được trên máy người khác.
- [ ] Nhật ký quyết định mục 6 đã điền đủ.

*Sau gate G4, môi trường được "đóng băng": chỉ sửa khi có bug, mọi thay đổi phải chạy lại bộ test và ghi vào changelog hợp đồng.*
