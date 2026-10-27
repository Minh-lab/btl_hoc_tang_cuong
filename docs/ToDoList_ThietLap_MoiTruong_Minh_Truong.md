# TO-DO LIST THIẾT LẬP MÔI TRƯỜNG — MINH × TRƯỞNG

> **File checklist tách riêng** khỏi `docs/KeHoach_ThietLap_MoiTruong_Minh_Truong.md`. File kế hoạch trả lời *làm gì / vì sao*; file này là **hợp đồng phân công**: đầu việc, người làm, file được ghi, phụ thuộc, điều kiện xong.
> **Không có timeline/deadline.** Mỗi dòng chỉ được chuyển `done` khi *điều kiện xong* đúng và có bằng chứng (test xanh, số đo, ảnh, CSV).
> **Nguồn:** `docs/03_04_PhanTich_ThietKe_MoiTruong.md` (FR-ENV-1…8, NFR-1…6, T1–T7) + `agriwater/env/contract.py`. Design doc khác code ⇒ theo code + `contract.py`, xem §5.
> **Cách gọi tên:** dùng ID — “M-03 done, T-08 review”. Không dùng “sắp xong”.

---

## 0. LUẬT CHỐNG TRÙNG & XUNG ĐỘT (đọc trước khi làm bất kỳ ID nào)

> Mục tiêu: hai người (mỗi người có AI agent riêng) làm song song trên **cùng một repo** mà **không làm lại việc của nhau** và **không giẫm file của nhau**.

### 0.1. Bốn câu gốc

1. **Một ID = một người = một nhánh = một PR.** Không gộp 2 ID vào 1 nhánh, không tách 1 ID ra 2 người.
2. **Chỉ được ghi vào các file ở cột “File được sửa”** của ID mình đang làm. Mọi file khác: chỉ đọc.
3. **Không sửa file của người kia.** Cần đổi ⇒ gửi yêu cầu (mục 0.5), người chủ sửa.
4. **File này không phải bảng trạng thái dùng chung:** mỗi người chỉ được sửa **cột `Trạng thái` của hàng mình**; không sửa nội dung, không đổi thứ tự, không xóa hàng, không tick hộ.

### 0.2. Trước khi bắt đầu một ID — 5 bước bắt buộc

```text
1. git status phải sạch;  git pull --rebase origin main
2. Kiểm "đã có ai nhận chưa":
     git ls-remote --heads origin | grep -i "<ID>"      # ví dụ M-02, T-08
     + xem danh sách PR đang mở
     Nếu đã có nhánh/PR cho ID  ⇒  KHÔNG làm lại. Chuyển sang review hoặc chọn ID khác.
3. Kiểm cột "Phụ thuộc": mọi ID liệt kê phải đang `done`.
     Chưa xong  ⇒  chọn một ID khác không phụ thuộc (xem 0.9), không ngồi chờ.
4. Kiểm cột "File được sửa": không file nào đang nằm trong PR của người kia.
5. Tạo nhánh feat/<minh|truong>-<ID>  và push ngay (PR draft).
     Nhánh đã push CHÍNH LÀ dấu hiệu "ID này đã có người nhận".
```

### 0.3. Trong lúc làm

- Chỉ commit file thuộc ID đang làm. Không commit `.venv/`, `__pycache__/`, `.pytest_cache/`, `app/sample_data/`.
- `logs/` chỉ được commit bởi **M-14/C-03** (Minh); người khác không tạo file trong `logs/`.
- Trước mỗi commit: `.venv/bin/python -m pytest -q` phải xanh (trừ test đỏ mà chính ID đó đang cài đặt).
- **Không** `git push --force`, **không** rebase/amend/reset nhánh của người kia, **không** merge `main` vào nhánh người kia.
- Không tạo file mới ngoài danh sách ở cột “File được sửa”. Cần file mới ⇒ dừng, hỏi chủ dự án và bổ sung vào checklist trước.

### 0.4. Khi xong một ID

```text
1. Gỡ xfail đúng file test của ID (nếu ID yêu cầu), chạy full pytest.
2. PR nhỏ, tiêu đề: [<ID>] <mô tả>   (ví dụ: [M-02] cài calculate_reward)
   Mô tả PR ghi: file đã sửa · test nào xanh · số đo (nếu có) · ID phụ thuộc đã xong.
3. Nhờ đúng người review:  M-* → Trưởng review;  T-* → Minh review.
4. CHỈ SAU KHI MERGE mới đổi cột Trạng thái của hàng mình thành done.
   Trước merge: doing (đang code) hoặc review (đã mở PR).
```

### 0.5. Khi hai người cùng cần một file

| Tình huống | Làm gì |
|---|---|
| File **có chủ** (bảng 0.6) | Người không phải chủ gửi yêu cầu cho chủ: `ID · file:dòng · thay đổi mong muốn · test đang đỏ`. Chủ sửa trong ID của chủ, hoặc mở ID mới nếu là việc riêng |
| File **không có chủ** (docs, script hạ tầng) | Không tự sửa. Dừng, báo chủ dự án, chờ bổ sung vào checklist |
| Cả hai cùng thấy một bug ngoài phạm vi | Không ai sửa. Ghi thành đề xuất (theo `SKILL.md` §0.2) và chờ duyệt |

### 0.6. Bảng chủ sở hữu file — ai là người **duy nhất** được ghi

| File / thư mục | Người được ghi | Ghi chú |
|---|---|---|
| `agriwater/env/contract.py` | **Chủ dự án** (qua duyệt) | Không ai tự sửa; đổi phải ghi `CONTEXT.md` §15 trước |
| `agriwater/env/config.py`, `weather_model.py`, `physics.py`, `agriwater_env.py` | **Trưởng** | Minh chỉ đọc + viết test |
| `configs/scenarios/*.json` | **Trưởng** | Đổi kịch bản phải xin duyệt |
| `agriwater/env/reward.py` | **Minh** | Trưởng chỉ đọc |
| `tests/**` | **Minh** | Trưởng **không** sửa test; cần test mới ⇒ yêu cầu Minh |
| `agriwater/agents/**`, `agriwater/utils/metrics.py` | **Minh** | Đợt này chỉ đọc, không mở rộng |
| `app/**`, `app/sample_data/**` | **Không ai** trong đợt này | Dashboard đã đóng băng |
| `scripts/make_fixtures.py`, `scripts/setup.sh`, `scripts/run_dashboard.sh` | **Không ai** | Lỗi ⇒ báo chủ dự án |
| `README.md` | **Trưởng** (T-01, T-13) | Minh chỉ đọc |
| `docs/KeHoach_*.md`, `docs/03_04_*.md` | **Chủ dự án / AI theo yêu cầu** | Không tự sửa khi đang làm ID |
| `docs/ToDoList_*.md` (file này) | **Mỗi người: chỉ cột Trạng thái hàng của mình** | Không sửa nội dung hàng người kia |
| `logs/` | **Minh** (M-14, C-03) | Trưởng không tạo file ở đây |
| `.venv/` | Mỗi máy | Không commit |

### 0.7. Chia việc nhóm C-xx (để không ai làm trùng)

| ID | Người duy nhất | Ghi chú |
|---|---|---|
| C-01 | **mỗi người tự làm trên máy mình** | Không sửa file; báo lại con số baseline |
| C-02 | **Minh** | Trưởng cung cấp thông tin, không sửa |
| C-03 | **Minh** | Trưởng chỉ xem dashboard |
| C-04 | **Minh** tổng hợp | Trưởng gửi số đo phần mình |
| C-05 | **Minh** đề xuất | Chỉ ghi `CONTEXT.md` sau khi chủ dự án duyệt |
| C-06 | **Cả hai tuân** | Không ai sửa gì thêm |

### 0.8. Xử lý xung đột git

- Người mở PR **sau** chịu trách nhiệm `git rebase origin/main` trước khi merge.
- Conflict trong `tests/**` ⇒ **Minh** xử lý; trong `agriwater/env/**` (trừ `reward.py`) ⇒ **Trưởng**; trong `reward.py` ⇒ **Minh**.
- Conflict ở `contract.py` ⇒ **dừng**, không tự chọn bên nào, báo chủ dự án.
- Không “resolve” bằng cách lấy nguyên một bên: sau khi resolve phải chạy lại full `pytest` và ghi kết quả vào PR.

### 0.9. Cặp việc chạy song song an toàn (không giẫm nhau)

| Làn | Minh | Trưởng | Vì sao an toàn |
|---|---|---|---|
| 1 | M-01, M-02 | T-01, T-02 | Khác file hoàn toàn (`reward.py` vs `config/weather_model.py`) |
| 2 | M-03, M-04, M-05, M-06 | T-03, T-04, T-05 | Test của Minh viết cho code Trưởng, không sửa code của nhau |
| 3 | M-07, M-08 | T-06, T-07 | M-07/M-08 chỉ sửa `tests/`; T-06/T-07 chỉ sửa `physics.py`/`agriwater_env.py` |
| 4 | M-09 | T-08, T-09 | M-09 chỉ gỡ `xfail`; T-08/T-09 cài vòng đời episode |
| 5 | M-10…M-15 | T-10…T-13 | Kiểm chứng/đo đạc vs `check_env`/`render`/`base_dir` |

> Quy tắc: nếu ID mình muốn làm **không** nằm trong làn an toàn hiện tại, kiểm 0.2 rồi chọn ID khác; **không** chen vào file đang có PR của người kia.

### 0.10. Bị chặn thì làm gì (không chờ, không giẫm việc)

- Ghi rõ trong PR: `chờ <ID>` và lý do; không đánh dấu `done`.
- Chọn ngay một ID khác **không phụ thuộc** và **khác file** (bảng 0.9).
- Nếu bị chặn vì hợp đồng/đặc tả mâu thuẫn ⇒ dừng, gửi đề xuất theo `SKILL.md` §0.2, chờ chủ dự án.

---

## 1. Checklist của Minh (reward, test, kiểm chứng, log)

> Chỉ Minh (và AI agent của Minh) được sửa các hàng M-xx. Trạng thái: `todo → doing → review → done`.

| ID | Đầu việc | File được sửa | Phụ thuộc | Trạng thái | Xong khi |
|---|---|---|---|---|---|
| **M-01** | Đọc `contract.py` + `CONTEXT.md` §5; phát biểu lại 7 chiều obs, 6 mức tưới, 6 thành phần reward, 5 tình huống `+6/+10/−124/−4/−10`, 4 biên `0.20/0.40/0.70/0.85` | không sửa (đọc) | — | `todo` | Giải thích được từng thành phần và ngưỡng **đã chuẩn hóa** mà không mở file |
| **M-02** | Cài `calculate_reward(state, action, next_state, config)` đúng 6 thành phần, dùng `config` cho mọi trọng số | `agriwater/env/reward.py` | M-01 | `todo` | 5 tình huống trong `test_reward.py` cho đúng giá trị |
| **M-03** | Cài `reward_breakdown(...)` cùng một lõi tính, trả 6 khóa `health, stress, water, waste, rain, delay` | `agriwater/env/reward.py` | M-02 | `todo` | Tổng 6 khóa **bằng đúng** `calculate_reward` trên 5 tình huống |
| **M-04** | Gỡ `pytestmark` trong `tests/test_reward.py` | `tests/test_reward.py` | M-03 | `todo` | 10 case xanh, không có `XPASS(strict)` |
| **M-05** | Thêm test còn thiếu: ngập úng `m_next = 0.90` bị `−100`; `reward_breakdown` khớp tổng; `action = 0` không bị phạt nước/waste/rain/delay | `tests/test_reward.py` | M-03 | `todo` | Test mới xanh, số test tăng |
| **M-06** | Viết `tests/test_weather_model.py`: cùng seed ⇒ cùng chuỗi `WeatherStep`; khác seed ⇒ khác; `rained = False ⇒ rainfall_mm == 0`; `rain_prob` đúng JSON (số và khoảng) | `tests/test_weather_model.py` (mới) | — (viết được ngay; xanh khi T-03) | `todo` | 4 nhóm assert xanh |
| **M-07** | Thêm test vật lý theo quyết định B: `m_t = 0.80`, `action = 5`, không mưa ⇒ `m_next > 0.85` và `D_t = 0`; `m_next` luôn trong `[0,1]` | `tests/test_physics.py` | — (viết được ngay; xanh khi T-06) | `todo` | Test xanh |
| **M-08** | Gỡ `pytestmark` trong `tests/test_physics.py` | `tests/test_physics.py` | M-07, T-06 | `todo` | 3 case cũ + M-07 xanh |
| **M-09** | Gỡ `xfail` ở `tests/test_env_api.py`, `tests/test_determinism.py`, `tests/test_speed.py` | 3 file test đó | T-07, T-08, T-09 | `todo` | Không còn `xfail` ở 3 file; test xanh |
| **M-10** | Chạy full `pytest`, xác nhận 0 `xfailed`, không còn `NotImplementedError` trong `agriwater/env/` | không sửa (chạy) | M-04, M-08, M-09 | `todo` | Dòng tổng kết chỉ có `passed`; ghi số vào PR |
| **M-11** | Đo tốc độ 100.000 bước, ghi lại số bước/giây | không sửa (chạy) | T-08 | `todo` | ≥ 10.000 bước/giây; số đo nằm trong PR/báo cáo |
| **M-12** | Kiểm NFR-5: `env/` không import `agents/`; `grep -R -e "np.random." -e "import random" agriwater/` rỗng | không sửa (kiểm) | T-08 | `todo` | Test subprocess xanh + grep rỗng |
| **M-13** | Review `physics.py` + `reset/step` của Trưởng theo 6 điểm | không sửa (review) | T-06, T-08 | `todo` | 1 dòng kết luận trong PR của Trưởng |
| **M-14** | Smoke: agent `random` chạy 3 kịch bản, ghi CSV vào `logs/` bằng `MetricsLogger` | `logs/*.csv` (mới); không sửa code | M-09, T-09 | `todo` | 3 CSV đúng 13 cột; dashboard báo “Đang đọc log thật từ `logs/`” |
| **M-15** | Kiểm trong episode thật: obs `float32[7]` trong `[0,1]`; `info` đủ 6 khóa; cờ là `bool` | không sửa (kiểm) | M-14 | `todo` | Log/ảnh chứng minh, không chỉ đọc code |
| **M-16** | Test cho agent registry (đợt thuật toán): `act()` trả `int` trong `[0,6)`, cùng seed ⇒ cùng hành động | `tests/` | — (đợt sau) | `todo` | Test xanh; **không làm trong đợt này** |

## 2. Checklist của Trưởng (config, weather, physics, vòng đời episode)

> Chỉ Trưởng (và AI agent của Trưởng) được sửa các hàng T-xx. Trạng thái: `todo → doing → review → done`.

| ID | Đầu việc | File được sửa | Phụ thuộc | Trạng thái | Xong khi |
|---|---|---|---|---|---|
| **T-01** | Đối chiếu `EnvConfig` với design §3.4: trường nào thực tế nằm trong JSON (`temp_range`, `rain_prob`, `rain_forecast_range`, `seed`); ghi rõ trong docstring/README, không thêm trường thừa | `agriwater/env/config.py`, `README.md` | — | `todo` | Có kết luận bằng văn bản; `EnvConfig.from_dict` vẫn validate đúng |
| **T-02** | Cài `WeatherModel.reset()`: đưa bộ đếm về đầu episode, **không** tạo generator mới, không re-seed | `agriwater/env/weather_model.py` | T-01 | `todo` | `reset()` 2 lần rồi sample vẫn cho chuỗi như lần đầu |
| **T-03** | Cài `WeatherModel.sample()`: `T`, `p`, `f` từ JSON; `rained` theo Bernoulli; `rainfall_mm` có nhiễu khi mưa, `0` khi không mưa | `agriwater/env/weather_model.py` | T-02 | `todo` | Test M-06 xanh; hai lần cùng seed giống tuyệt đối |
| **T-04** | Cài `evapotranspiration()`: `c_evap·K_c(g)·(T−15)/30 + c_base`, luôn ≥ 0 | `agriwater/env/physics.py` | T-01 | `todo` | Test khô khi không tưới xanh; `ET ≥ 0` ở `T = 15` và `T = 45` |
| **T-05** | Cài `drainage()` theo **quyết định B**: `max(0, m_t − θ_fc)`; hai tham số gia tăng giữ trong chữ ký nhưng không cộng vào | `agriwater/env/physics.py` | T-01 | `todo` | `m = 0.84` ⇒ `D > 0`; `m = 0.80` ⇒ `D = 0` |
| **T-06** | Cài `update_moisture()`: `ΔI`, `ΔR = min(ρ_max, rainfall_mm/R_max)`, trừ `ET` và `D`, clip `[0,1]`, trả `(m_next, D)` | `agriwater/env/physics.py` | T-04, T-05 | `todo` | M-07 + 3 test cũ xanh; không hard-code hằng số |
| **T-07** | Cài `reset(seed, options)`: `super().reset(seed)`, `WeatherModel.from_config(...)` rồi `.reset()`, đặt `_day/_moisture/_stress_days/_last_irrigation_l`, sample thời tiết ngày 0, trả `(obs, info)` | `agriwater/env/agriwater_env.py` | T-03, T-06 | `todo` | `test_reset_contract` xanh; 20 lần reset đều ra obs 7 chiều |
| **T-08** | Cài `step(action)` đúng 8 bước: giữ `prev_state` → `action_to_litres` → sample **một lần** → `update_moisture` → cập nhật `_day/_last_irrigation_l/_moisture` → reward bằng `prev_state` → cờ → trả 5 phần tử | `agriwater/env/agriwater_env.py` | T-07, **M-02** | `todo` | `test_step_contract_and_bounds` xanh; có phạt `R_rain` khi tưới trước mưa |
| **T-09** | Cài `stress_days` + `terminated` (`K = 3`) + `truncated` (`day ≥ 30`), cờ là `bool` Python | `agriwater/env/agriwater_env.py` | T-08 | `todo` | 3 ngày liên tiếp `m < 0.20` ⇒ `terminated`; 30 ngày ⇒ `truncated`; hai cờ không lẫn |
| **T-10** | Chạy `check_env(...)` và sửa mọi cảnh báo kiểu/shape | `agriwater/env/agriwater_env.py` | T-09 | `todo` | Pass, không cảnh báo |
| **T-11** | Xác nhận 3 kịch bản `dry/stormy/randomized` cho hành vi khác nhau **mà không sửa code env** | không sửa (chạy) | T-03 | `todo` | 3 episode cùng seed có chuỗi thời tiết khác rõ rệt |
| **T-12** | Cài `render()` vẽ chuỗi độ ẩm một episode (matplotlib) | `agriwater/env/agriwater_env.py` | T-09 | `todo` | Sinh được 1 ảnh/biểu đồ; `check_env` vẫn pass |
| **T-13** | Xử lý `base_dir`: chạy được từ thư mục khác **hoặc** tài liệu hóa rõ trong docstring + README | `agriwater/env/agriwater_env.py`, `README.md` | T-07 | `todo` | Có test hoặc ghi chú rõ; không còn lỗi “không tìm thấy JSON” khi làm đúng hướng dẫn |
| **T-14** | Review `reward.py` + test của Minh theo 6 điểm | không sửa (review) | M-03 | `todo` | 1 dòng kết luận trong PR của Minh |
| **T-15** | Chỉ sau khi chủ dự án chốt: thống nhất ngữ nghĩa obs sau `step` (thời tiết vừa sample theo docstring vs dự báo ngày kế tiếp theo design §4.3) | không sửa (chờ chốt) | chủ dự án | `todo` | Quyết định được ghi `CONTEXT.md` §15 trước khi sửa code |

## 3. Checklist chung (cả hai) — mỗi ID có **một** người chịu trách nhiệm

| ID | Đầu việc | Người | File được sửa | Phụ thuộc | Trạng thái | Xong khi |
|---|---|---|---|---|---|---|
| **C-01** | Cài môi trường bằng `bash scripts/setup.sh` trên máy từng người | mỗi người | không sửa | — | `todo` | Cả hai ra cùng baseline `41 passed / 19 xfailed` |
| **C-02** | Gỡ hết `NotImplementedError` trong `agriwater/env/` | **Minh** (kiểm) | không sửa | M-10, M-12 | `todo` | `grep -R "NotImplementedError" agriwater/env/` rỗng |
| **C-03** | Có CSV thật đầu tiên trong `logs/`; dashboard chuyển sang log thật, banner vàng biến mất | **Minh** | `logs/` | M-14 | `todo` | Ảnh dashboard + CSV 13 cột |
| **C-04** | Bảng số đo bàn giao: số test, bước/giây, `xfail` đã gỡ, lỗi phát hiện thêm | **Minh** (tổng hợp; Trưởng gửi số phần mình) | không sửa | M-10, M-11 | `todo` | Bảng nằm trong PR/báo cáo bàn giao |
| **C-05** | Cập nhật `CONTEXT.md` §3/§11/§12 theo thực tế | **Minh** đề xuất; chủ dự án duyệt | `CONTEXT.md` (sau duyệt) | C-02, C-03 | `todo` | Đúng hiện trạng; đổi hợp đồng phải ghi §15 trước |
| **C-06** | Không làm: Q-Learning/MC/DQN/Baseline, `train.py`/`evaluate.py`, tuning, sửa `.docx`/`.pdf`, đổi schema CSV | cả hai tuân | không sửa | — | `todo` | Không có file/thay đổi ngoài phạm vi |

## 4. Truy vết yêu cầu → đầu việc (để không bỏ sót)

| Yêu cầu trong design doc | Đầu việc phụ trách |
|---|---|
| FR-ENV-1 Khởi tạo theo cấu hình | T-01, T-07 |
| FR-ENV-2 Cân bằng nước | T-04, T-05, T-06, T-08 |
| FR-ENV-3 Sinh nhiệt độ theo kịch bản | T-02, T-03, T-11 |
| FR-ENV-4 Sinh mưa Bernoulli | T-02, T-03, T-11 |
| FR-ENV-5 Tính reward (tái sử dụng) | M-02, M-03, T-08 |
| FR-ENV-6 Kết thúc episode | T-09 |
| FR-ENV-7 Cung cấp log cho UC-05 | M-14, M-15, C-03 |
| FR-ENV-8 Render tối thiểu | T-12 |
| NFR-1 Tái lập theo seed | T-02, T-03, T-07, M-09 |
| NFR-2 ≥ 10.000 bước/giây | M-11 |
| NFR-3 Chuẩn Gymnasium | T-07, T-08, T-10, M-10 |
| NFR-4 Tách bạch kịch bản | T-01, T-11 |
| NFR-5 Env không phụ thuộc agent | M-12 |
| NFR-6 Vừa liên tục vừa rời rạc hóa được | T-07 (obs `float32[7]`), `Discretizer` (đã có) |
| T1 `check_env` | T-10 |
| T2 Tất định 1.000 bước | T-07/T-08 + M-09 |
| T3 Tốc độ 100.000 bước | M-11 |
| T4 Reward 5 tình huống | M-02…M-05 |
| T5 Vật lý + clip | T-04…T-06, M-07, M-08 |
| T6 `terminated`/`truncated` | T-09 |
| T7 Không import agent | M-12 |

## 5. Design doc vs code hiện tại — chỗ phải theo code, không tạo file trùng

| Design doc ghi | Thực tế trong repo | Làm theo |
|---|---|---|
| `agriwater/eval/metrics_logger.py` | `agriwater/utils/metrics.py` (`MetricsLogger`) | File hiện có; **không** tạo `eval/` |
| `agriwater/scenarios/{dry,stormy,randomized}.json` | `configs/scenarios/*.json` (`contract.SCENARIO_DIR`) | `configs/` |
| `tests/test_no_agent_import.py` | `tests/test_scaffold.py::test_env_does_not_depend_on_agents` | File hiện có |
| `train.py`, `evaluate.py` | Chưa có | **Không làm** trong đợt này |
| `info` có 5 khóa (§3.4, §4.3) | 6 khóa, thêm `stress_days` | Theo `contract` + `_info()`: **6 khóa** |
| `info` rỗng ở `reset` | `reset` trả `_info(water_L=0.0)` | Theo code: 6 khóa |
| `EnvConfig` chứa `temp_range`, `rain_prob`, `rain_forecast_mm`, `seed` | Các giá trị này nằm trong JSON kịch bản | Theo code (NFR-4); ghi rõ ở T-01 |
| `stormy` có `rain_prob` 0.50–0.80 | `stormy.json` đặt 0.65 cố định | Theo JSON hiện tại; đổi phải xin duyệt |
| `D_t = max(0, m_t + ΔI + ΔR − θ_fc)` | Đã chốt **phương án B**: `max(0, m_t − θ_fc)` | Theo quyết định B (kế hoạch §9) |
| `obs` sau `step` dùng dự báo ngày kế tiếp (§4.3) | Docstring `step()` sample thời tiết ngày mới rồi build obs | Theo docstring; muốn khác ⇒ T-15, phải chốt trước |

## 6. Cách dùng checklist

- **Một ID, một trạng thái, một người:** `todo → doing → review → done`; `review` phải ghi tên người review (chéo: Minh ↔ Trưởng).
- Chỉ **chủ ID** được đổi `Trạng thái` của hàng đó, và **chỉ sau khi merge** mới đổi `done`.
- `doing` chỉ được đặt khi đã có nhánh `feat/<minh|truong>-<ID>` đã push (theo 0.2).
- Một ID chỉ `done` khi **điều kiện xong** đúng và **có bằng chứng** (tên test xanh, số đo, ảnh, file CSV) trong PR.
- Khi bị chặn: ghi `chờ <ID>` trong PR, chọn việc khác cùng làn (0.9), không giẫm file người kia.
- Cuối đợt: đối chiếu mục 3 (định nghĩa xong) và mục 11 (checklist bàn giao) của `KeHoach_ThietLap_MoiTruong_Minh_Truong.md`; thiếu dòng nào thì chưa bàn giao.
