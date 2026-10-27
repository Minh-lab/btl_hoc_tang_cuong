# KẾ HOẠCH THIẾT LẬP MÔI TRƯỜNG — MINH × TRƯỞNG

> **Không có timeline trong tài liệu này** (theo yêu cầu). Tài liệu chỉ trả lời: **làm gì · vì sao phải làm · đầu vào/đầu ra · thế nào là xong · cạm bẫy**. Thứ tự thực hiện theo **phụ thuộc kỹ thuật** (mục 4); tiến độ theo trạng thái `todo → doing → review → done`, không theo lịch.
>
> **Người đọc chính:** Nguyễn Minh, Nguyễn Thế Trưởng. Người khác đọc để review.
> **Hiệu lực:** đợt thiết lập môi trường của AgriWater-RL, bắt đầu từ hiện trạng đã ghi trong `CONTEXT.md`: **41 passed / 19 xfailed**, lõi môi trường chưa chạy được.
> **Không thay thế:** `agriwater/env/contract.py` (hợp đồng G0, nguồn sự thật) và `docs/KeHoach_MoiTruong_Minh_Truong.md` (kế hoạch tổng với cổng G0–G4). Tài liệu này chi tiết hóa **đúng đợt đang làm** và bỏ toàn bộ mốc thời gian.

---

## 1. “Thiết lập môi trường” ở đây gồm hai tầng

| Tầng | Là gì | Vì sao phải có |
|---|---|---|
| **A. Môi trường phát triển** | `.venv`, thư viện, package cài editable, pytest, dashboard chạy được trên máy từng người | Không có tầng này thì không ai chạy được test/code; hai người sẽ báo kết quả khác nhau trên cùng một commit |
| **B. Môi trường RL (`AgriWaterEnv`)** | `WeatherModel` + `physics` + `reward` + `reset/step` + cờ kết thúc, chạy được một episode 30 ngày | Không có tầng này thì **không có một episode thật nào**, nên 4 thuật toán, dashboard với log thật và mọi số liệu báo cáo đều không thể tồn tại |

Hai tầng độc lập: tầng A làm được ngay trên máy mỗi người; tầng B phải làm chung vì phụ thuộc hợp đồng.

---

## 2. Vì sao phải làm đợt này (không phải “dọn dẹp cho gọn”)

1. **19 test đang `xfail(strict=True)`** — đây không phải test hỏng, mà là **đặc tả đã viết sẵn cho phần chưa code**: reward (10), vật lý (3), `reset/step` (3), tất định (2), tốc độ (1). Chúng chỉ chuyển xanh khi môi trường thật sự chạy.
2. **Chưa có episode thật nào.** `reward`, `WeatherModel.reset/sample`, toàn bộ `physics`, `AgriWaterEnv.reset/step` đang `NotImplementedError`.
3. **4 thuật toán không thể bắt đầu.** Q-Learning, MC, DQN, Baseline đều cần `reset/step` trả `(obs, reward, terminated, truncated, info)`. Viết agent trước khi có env = viết trên cát.
4. **Dashboard đang đọc dữ liệu tổng hợp.** 12 CSV trong `app/sample_data/` do `scripts/make_fixtures.py` sinh ra để dựng giao diện; nếu không có log thật, mọi biểu đồ chỉ là hình minh họa và **không được** dùng trong báo cáo.
5. **Cổng G2/G3/G4 đang treo.** G2 = `step()` chạy 1 episode 30 bước; G3 = toàn bộ pytest xanh; G4 = smoke pipeline xuất CSV. Không qua G2/G3 thì không được chuyển sang giai đoạn thuật toán theo đúng kế hoạch nhóm.

> Nếu bỏ qua đợt này và viết agent ngay: agent sẽ được tinh chỉnh để hợp với một môi trường tưởng tượng, rồi phải làm lại toàn bộ khi env thật xuất hiện. Đây là lý do kế hoạch nhóm đặt môi trường là **điểm nghẽn số 1**.

---

## 3. Định nghĩa “môi trường đã thiết lập xong”

Chỉ được coi là xong khi **tất cả** điều sau đúng:

- [ ] `pytest` chạy **0 xfailed**, không còn `NotImplementedError` trong `agriwater/env/`.
- [ ] `gymnasium.utils.env_checker.check_env(AgriWaterEnv(...))` pass.
- [ ] `reset(seed=42)` hai lần cho quỹ đạo **giống tuyệt đối** (obs và reward bằng nhau từng bit).
- [ ] Seed khác cho quỹ đạo khác (chống “tất định giả”).
- [ ] Một episode chạy đủ **30 ngày** (hoặc dừng sớm khi cây chết), `info` luôn đủ **6 khóa**.
- [ ] Tốc độ **≥ 10.000 bước/giây** trên máy phổ thông (đo bằng `tests/test_speed.py`).
- [ ] `reward` khớp **5 tình huống** `+6, +10, −124, −4, −10` và 4 biên `0.20/0.40/0.70/0.85`.
- [ ] Có **một CSV thật** trong `logs/` đúng 13 cột, dashboard tự chuyển sang đọc log thật.

---

## 4. Thứ tự phụ thuộc (thay cho timeline)

```text
B.0  Đọc & chốt phạm vi (cả 2)
      │
      ├──► B.1 Reward (Minh)  ────┐
      │                           │
      └──► B.2 Weather (Trưởng) ──┴──► B.3 Physics (Trưởng) ──► B.4 Env reset/step (Trưởng)
                                                                       │
                                                                       ├──► B.5 Kiểm chứng (Minh)
                                                                       ├──► B.6 render (Trưởng, cắt được)
                                                                       └──► B.7 Smoke + log thật (cả 2)
```

- **B.1 và B.2 làm song song được** (không chờ nhau): reward chỉ cần obs, weather chỉ cần JSON + generator.
- **B.3 cần B.2** để biết `WeatherStep` cung cấp gì; **không cần B.1**.
- **B.4 cần cả B.1, B.2, B.3** — đây là điểm hội tụ, không được bắt đầu khi ba phần trên còn `NotImplemented`.
- **B.5/B.6/B.7** chỉ có nghĩa sau B.4.

---

## 5. Phần A — Môi trường phát triển (làm trên máy từng người)

### A.1. Cài đặt chuẩn bằng script

- **Làm gì:** chạy `bash scripts/setup.sh`. Script tạo `.venv` với `--system-site-packages`, cài `requirements.txt`, cài package ở chế độ editable, rồi in phiên bản `agriwater` + `gymnasium`.
- **Vì sao:**
  - Một lệnh duy nhất ⇒ hai người có môi trường giống nhau, hết cảnh “máy tôi chạy được”.
  - `--system-site-packages` để **tái sử dụng `torch` có sẵn** của máy, không tải lại ~2 GB cho DQN sau này.
  - `pip install -e .` để `import agriwater` luôn trỏ vào code đang sửa, không phải bản copy cũ.
- **Đầu ra:** `.venv/bin/python -c "import agriwater, gymnasium, numpy"` chạy được; in `agriwater 0.1.0 | gymnasium <phiên bản>`.
- **Điều kiện xong:** lệnh trên exit 0 trên **máy của cả Minh và Trưởng**.
- **Cạm bẫy:** chạy script từ thư mục khác (script đã tự `cd` về gốc — đừng bỏ dòng đó); dùng Python < 3.10 (`requires-python = ">=3.10"`); tạo `.venv` **không** có `--system-site-packages` thì mất `torch` toàn cục.

### A.2. Chốt baseline test

- **Làm gì:** chạy `.venv/bin/python -m pytest -q`, ghi lại đúng con số `passed / xfailed`.
- **Vì sao:** cần mốc “trước” để chứng minh “sau”. Nếu hai người ra số khác nhau thì môi trường **chưa** giống nhau — dừng lại kiểm, đừng sửa test.
- **Đầu ra:** cả hai báo cùng một con số. Hiện tại: **41 passed, 19 xfailed** (60 case).
- **Điều kiện xong:** hai người khớp số; hiểu rằng 41 xanh **không** chứng minh môi trường chạy được.

### A.3. Dashboard — xác nhận tầng hiển thị độc lập với lõi

- **Làm gì:** `.venv/bin/python -m pip install -e ".[dashboard]"` → `.venv/bin/python scripts/make_fixtures.py` → `bash scripts/run_dashboard.sh` → mở 4 trang (Tổng quan, Learning curve, So sánh, Mô phỏng).
- **Vì sao:**
  - Chứng minh `app/` chỉ đọc CSV, **không import** `agriwater` — đúng ranh giới kiến trúc một chiều.
  - Đây là công cụ duy nhất để nhìn kết quả khi có log thật ở B.7.
  - Kiểm luôn schema 13 cột (nếu lệch, `tests/test_dashboard_schema.py` đỏ ngay).
- **Đầu ra:** 4 trang render không exception; banner vàng **“DỮ LIỆU MẪU (tổng hợp)”** hiện trên mọi trang.
- **Điều kiện xong:** 4 trang chạy; không có số liệu mẫu nào bị ghi vào báo cáo.
- **Cạm bẫy:** `app/views/mo_phong.py` dùng `altair` trực tiếp nhưng extra chỉ khai báo `streamlit` (altair đi kèm streamlit) — nếu môi trường thiếu altair thì cài thêm, **không** đổi kiến trúc.

### A.4. Docker — tùy chọn, không chặn ai

- **Làm gì:** `docker compose up --build`, mở `http://localhost:8501`; `docker compose run --rm test` để chạy pytest trong container.
- **Vì sao:** dùng khi thành viên không muốn cài Python, hoặc cần môi trường giống hệt để chụp màn hình/demo.
- **Điều kiện xong:** container lên, healthcheck xanh, dashboard trả HTTP 200.
- **Cạm bẫy:** **chưa ai build lần nào** trên máy tạo — không được báo “Docker chạy được” khi chưa chạy thật; ảnh không cài torch mặc định (phải `--build-arg INSTALL_TORCH=true` nếu cần DQN); code trong image là bản copy lúc build.

---

## 6. Phần B — Môi trường RL

### B.0. Luật chung cho cả hai (làm trước khi code)

- Đọc `agriwater/env/contract.py` (7 chỉ số obs, hằng số vật lý, trọng số reward, hàm chuẩn hóa) và §5 của `CONTEXT.md`.
- **Không đổi `contract.py`** trong đợt này. Muốn đổi ⇒ đề xuất, chờ chủ dự án xác nhận, ghi vào `CONTEXT.md` §15.
- Không hard-code số: mọi ngưỡng lấy từ `contract`, mọi tham số lấy từ `EnvConfig`.
- Làm trên nhánh ngắn `feat/<phạm vi>`, mỗi nhánh một việc; review chéo theo mục 7; xong việc nào gỡ `pytestmark` của test việc đó.
- Trạng thái mỗi việc ghi theo `todo → doing → review → done` kèm 1 dòng “đã xong gì / còn gì”.

---

### B.1. [Minh] Reward 6 thành phần — `agriwater/env/reward.py` (E-03/E-04)

- **Làm gì:** cài `calculate_reward(state, action, next_state, config)` và `reward_breakdown(...)`; gỡ `pytestmark` trong `tests/test_reward.py`.
- **Vì sao phải làm:**
  - Reward là **tín hiệu học duy nhất** dùng chung cho cả 4 chiến lược. Reward sai ⇒ mọi so sánh giữa Q-Learning/MC/DQN/Baseline đều vô nghĩa, dù code agent đúng.
  - 5 tình huống `+6, +10, −124, −4, −10` là **bằng chứng reward định hình đúng hành vi**: thưởng khi giữ ẩm lý tưởng, phạt nặng khi cây chết/ngập, phạt nhẹ theo nước, phạt nặng khi tưới dư, tưới trước mưa, tưới dồn dập.
  - Đây là **cổng G1** của nhóm: chưa qua G1 thì không được viết agent.
- **Đầu vào → đầu ra:** `state`, `next_state` là obs **đã chuẩn hóa** `float32[7]`; `action` là index `0…5`; trả `float` (tổng 6 thành phần). `reward_breakdown` trả dict 6 khóa `health, stress, water, waste, rain, delay`.
- **Điều kiện xong:**
  - 10 case trong `test_reward.py` xanh, gồm 4 biên `0.20 → −4`, `0.40 → +6`, `0.70 → +6`, `0.85 → −4`.
  - Tổng 6 khóa của `reward_breakdown` **bằng đúng** `calculate_reward` (cùng một lõi, không viết 2 bản).
  - Không đọc biến global; mọi trọng số/ngưỡng lấy từ `config`.
- **Cạm bẫy:**
  - `next_state` đã chuẩn hóa ⇒ dùng thẳng `0.20/0.40/0.70/0.85/0.60/0.30/0.50`, **không** chia lại cho 50 mm hay 25 L.
  - Biên **tính là thuộc** (`0.40` và `0.70` vẫn được `+10`).
  - Giai đoạn lấy từ `next_state` (chỉ số 1), không lấy từ `state`; quy đổi `round(g*3) == 2` là giai đoạn ra hoa.
  - `waste` dùng `m_t` (trạng thái **trước**), `rain` dùng `p_t, f_t` của `state`, `delay` dùng `last_irrigation` của `state`.
  - Thành phần `water` tính theo **index hành động** (`−2·action`), không theo số lít.

---

### B.2. [Trưởng] WeatherModel — `agriwater/env/weather_model.py` (E-05)

- **Làm gì:** cài `reset()` và `sample()`; giữ nguyên `from_config`/`from_file`; **có thể** thêm `tests/test_weather_model.py` vì hiện chưa có test nào canh phần này.
- **Vì sao phải làm:**
  - Môi trường là **model-free** với agent, nhưng **bộ mô phỏng phải tất định theo seed** (NFR-1). Thời tiết là nguồn ngẫu nhiên duy nhất của env, nên toàn bộ tính tái lập nằm ở đây.
  - `T, p, f` vừa đi vào obs (agent nhìn thấy để quyết định), vừa đi vào `physics` (mưa làm tăng ẩm), vừa đi vào `reward` (phạt tưới trước mưa). Sai một chỗ là lệch cả ba.
  - Kịch bản hóa bằng JSON (NFR-4) để đổi mùa khô/mưa bão/ngẫu nhiên **không phải sửa code env** — điều kiện để so sánh công bằng trên 3 kịch bản.
- **Đầu vào → đầu ra:** `scenario` dict + `np_random` (`numpy.random.Generator`); `sample()` trả `C.WeatherStep(temperature_c, rain_prob, rain_forecast_mm, rainfall_mm, rained)`.
- **Điều kiện xong:**
  - Hai lần chạy cùng seed cho **cùng chuỗi** `WeatherStep`; seed khác cho chuỗi khác.
  - `rain_prob` lấy đúng từ JSON: số vô hướng thì giữ nguyên, khoảng `[lo, hi]` thì lấy `uniform`.
  - `rained = False` ⇒ `rainfall_mm == 0`; `rained = True` ⇒ `rainfall_mm ≥ 0` quanh `forecast` có nhiễu.
  - Không dùng `random`/`np.random` toàn cục.
- **Cạm bẫy:**
  - **Không tạo generator mới** trong `reset()` hay `sample()` — generator đã được `AgriWaterEnv.reset(seed=...)` truyền vào.
  - **Không gọi `sample()` hai lần trong một bước** (làm lệch chuỗi tất định và lệch cả physics lẫn reward).
  - Thứ tự tiêu thụ RNG là một phần của hợp đồng tất định: đổi thứ tự gọi `uniform/random/normal` là đổi kết quả dù cùng seed.
  - `reset()` chỉ đưa bộ đếm nội bộ về đầu episode; không re-seed.

---

### B.3. [Trưởng] Vật lý cân bằng nước — `agriwater/env/physics.py` (E-07/E-08)

- **Làm gì:** cài `evapotranspiration()`, `drainage()`, `update_moisture()`; gỡ `pytestmark` trong `tests/test_physics.py`.
- **Vì sao phải làm:**
  - Đây là **toàn bộ động lực học** của môi trường: `m_{t+1}` quyết định obs, reward (lý tưởng/stress), `crop_stress`, `terminated`. Không có nó thì env chỉ là một hàm ngẫu nhiên.
  - Nó biến 6 mức tưới thành hậu quả thật (tưới thêm ẩm, mưa thêm ẩm, nắng bốc hơi, vượt sức chứa thì thấm thoát) — nhờ đó bài toán mới là “tưới bao nhiêu”, không phải “đoán số”.
  - Ba test hiện có chỉ là **mức tối thiểu** (khô khi không tưới, không vượt 1.0, có thấm thoát); phần lớn hành vi đúng/sai sẽ lộ ra ở reward + episode.
- **Đầu vào → đầu ra:**
  - `evapotranspiration(temperature_c, growth_stage, config) -> float ≥ 0`
  - `drainage(moisture, irrigation_gain, rainfall_gain, config) -> float ≥ 0`
  - `update_moisture(moisture, action, temperature_c, rainfall_mm, growth_stage, config) -> (m_next, drainage_amount)`, `m_next` đã clip `[0,1]`.
- **Điều kiện xong:**
  - 3 test vật lý xanh; thêm test biên cho `m_next` luôn trong `[0,1]` **và** test ngập úng theo công thức đã chốt: từ `m_t = 0.80`, tưới 25 L ⇒ `m_next > 0.85`.
  - Dùng `config` cho mọi hằng số; không hard-code 0.9/0.02/0.35/0.05/0.010/`KC`.
  - `ΔR = min(cfg.rain_gain_max, rainfall_mm / C.R_MAX_MM)` — dùng **lượng mưa thực tế**, không dùng dự báo.
  - `ET` không bao giờ âm (nhiệt độ thấp vẫn cộng `evap_base`).
- **Cạm bẫy:**
  - Nhầm `rainfall_mm` (thực tế, từ `WeatherStep`) với `rain_forecast_mm` (dự báo, chỉ dùng cho obs/reward).
  - Quên clip sau khi trừ `ET` và `D`. Với phương án B, `drainage` chỉ dùng `moisture` và `θ_fc`; hai tham số gia tăng vẫn giữ trong chữ ký để không đổi API nhưng **không** được cộng vào trước khi trừ `θ_fc`.
  - **Đã chốt 27/10/2026 (mục 9):** `D_t = max(0, m_t − θ_fc)` — thấm thoát tính từ nước đọng ngày trước, nên nước tưới/mưa hôm nay có thể đẩy `m` vượt 0.85. Phải thêm test biên ngập úng; **không** quay lại công thức cũ.

---

### B.4. [Trưởng] Vòng đời episode — `agriwater/env/agriwater_env.py` (E-09…E-12)

- **Làm gì:** cài `reset()`, `step()`, đếm `stress_days`, cờ `terminated`/`truncated`; giữ nguyên `observation_space`, `action_space`, `_build_obs()`, `_info()`. Gỡ `xfail` ở `test_env_api.py`, `test_determinism.py`, `test_speed.py`.
- **Vì sao phải làm:**
  - `reset/step` là **hợp đồng duy nhất** giữa môi trường và 4 agent (và cả DQN/SB3 sau này). Chuẩn Gymnasium ⇒ agent không cần biết bên trong env có gì.
  - Đây là nơi duy nhất nối 4 phần rời (thời tiết → vật lý → reward → cờ kết thúc). Sai **thứ tự** trong `step()` là sai reward, dù từng phần đều đúng.
  - Có `step()` mới có episode thật, mới qua được **G2/G3**, mới có log cho dashboard.
- **Đầu vào → đầu ra:**
  - `reset(seed=None, options=None) -> (obs float32[7], info 6 khóa)`
  - `step(action) -> (obs, reward: float, terminated: bool, truncated: bool, info 6 khóa)`
- **Điều kiện xong:**
  - `check_env()` pass (không cảnh báo shape/kiểu).
  - `reset(seed=42)` hai lần ⇒ quỹ đạo giống tuyệt đối; seed khác ⇒ khác.
  - 1 episode chạy 30 ngày; 3 ngày stress liên tiếp ⇒ `terminated=True`; hết 30 ngày ⇒ `truncated=True`; obs luôn trong `[0,1]`.
  - `info` đúng 6 khóa: `water_L, crop_stress, moisture, growth_stage, ideal, stress_days`.
  - ≥ 10.000 bước/giây.
- **Cạm bẫy (thứ tự là bắt buộc):**
  1. `super().reset(seed=seed)` trước tiên — không có `np_random` là mất tất định.
  2. `prev_state = self._build_obs()` **trước** khi đổi bất cứ thứ gì.
  3. Chỉ `sample()` thời tiết **một lần** mỗi bước; ghi đè `T, p, f, rainfall` sau khi đã giữ `prev_state`.
  4. Reward tính bằng `prev_state` (thời tiết **ngày vừa hành động**) và obs mới (độ ẩm mới) — nếu dựng lại obs sau khi sample thì mất phạt `R_rain`.
  5. Cập nhật `_day`, `_last_irrigation_l`, `_moisture` đúng một lần; cờ phải là `bool` Python, không phải `np.bool_`.
  6. `base_dir` mặc định `"."` ⇒ luôn chạy từ gốc dự án, hoặc truyền `base_dir` tường minh.

---

### B.5. [Minh] Kiểm chứng & canh chất lượng (E-13…E-16)

- **Làm gì:** gỡ toàn bộ `pytestmark` còn lại; chạy full test; thêm test cho phần Trưởng vừa làm (weather, biên vật lý, `terminated`/`truncated`); đo và ghi lại số bước/giây; rà 10 bất biến trong `SKILL.md` §3.
- **Vì sao phải làm:**
  - Rủi ro lớn nhất của nhóm là **“test xanh giả”** (ai đó nới assert cho qua). Người viết reward/test phải là người canh, không phải người được canh.
  - Test là **tài liệu duy nhất** mô tả hành vi đúng; review chéo chỉ có giá trị khi có test làm chuẩn.
  - Số đo bước/giây là bằng chứng cho NFR-2 và cho báo cáo.
- **Đầu ra:** báo cáo ngắn: số test, số bước/giây, danh sách `xfail` đã gỡ, lỗi phát hiện thêm.
- **Điều kiện xong:** 0 `xfail` (trừ khi có quyết định cắt `render`); số test **tăng**; không assert nào bị nới.

---

### B.6. [Trưởng] `render()` — `agriwater/env/agriwater_env.py` (E-20)

- **Làm gì:** vẽ chuỗi độ ẩm của một episode (matplotlib hoặc lưu ảnh), theo `metadata["render_modes"]`.
- **Vì sao:** FR-ENV-8/UC-06 cần hình cho báo cáo và slide; đây là phần **cắt được** nếu chậm, vì nó không chặn thuật toán.
- **Điều kiện xong:** gọi `render()` sinh được 1 ảnh/biểu đồ đọc được; không làm hỏng `check_env`; không thêm phụ thuộc bắt buộc (matplotlib đã có trong extras `viz`).

---

### B.7. [Cả hai] Smoke + log thật cho dashboard

- **Làm gì:** chạy agent `random` (đã đăng ký sẵn) trên 3 kịch bản, ghi CSV vào `logs/` bằng `MetricsLogger`; mở dashboard và xác nhận banner chuyển sang “Đang đọc log thật từ `logs/`”.
- **Vì sao:**
  - Chứng minh chuỗi **env → agent → logger → dashboard** nối đúng, không chỉ từng mảnh chạy riêng.
  - Đây là lần đầu tiên dashboard hiển thị **dữ liệu thật**, thay cho fixtures; từ đây mới được trích số cho báo cáo.
  - Là tiền đề của E-21/G4 (khi có agent thật chỉ cần đổi tên agent, không sửa pipeline).
- **Đầu ra:** CSV 13 cột trong `logs/`, đọc được bởi dashboard; nêu rõ đây là log của agent ngẫu nhiên, **chưa phải** kết quả so sánh thuật toán.
- **Điều kiện xong:** dashboard hiện log thật; `episode_summary` tính đúng số ngày/reward; không sửa một dòng UI nào.
- **Không làm ở bước này:** baseline/Q-Learning/MC/DQN (thuộc đợt thuật toán), tuning, chạy 10 seed.

---

## 7. Ranh giới file & review chéo

| File | Chủ sở hữu | Người kia được làm gì |
|---|---|---|
| `env/contract.py` | **Chung** (chỉ sửa khi cả hai + chủ dự án đồng ý) | Đọc |
| `env/config.py`, `env/weather_model.py`, `env/physics.py`, `env/agriwater_env.py` | Trưởng | Đọc, viết test, review |
| `env/reward.py`, `tests/**`, `agents/discretizer.py`, `agents/registry.py` | Minh | Đọc, review |
| `configs/scenarios/*.json` | Trưởng | Đọc, đề xuất kịch bản mới |

- **Review chéo bắt buộc:** Trưởng review reward + test của Minh; Minh review physics + `reset/step` của Trưởng.
- Checklist review 6 điểm (lấy từ kế hoạch nhóm): đúng kiểu/độ dài theo `contract`; không hằng số ma thuật; mọi trạng thái đã clip; chỉ dùng `self.np_random`; `env/` không import `agents/`; có test mới và không assert nào bị nới.
- Không sửa file của người kia. Cần sửa ⇒ gửi ghi chú kèm `file:dòng` + test đỏ + kỳ vọng; người sở hữu sửa.

---

## 8. Không làm trong đợt này (để không loãng)

- Không cài Q-Learning / MC / DQN / Baseline (kể cả file rỗng “cho có”).
- Không tuning siêu tham số, không chạy 10 seed, không làm bảng số liệu so sánh.
- Không đổi `contract.py`, không đổi schema 13 cột, không thêm/xóa kịch bản JSON.
- Không sửa `.docx`/`.pdf` (nhị phân), không viết lại báo cáo.
- Không refactor ngoài phạm vi, không thêm thư viện mới nếu thư viện hiện có làm được.
- Không “nâng cấp” dashboard (thêm nút huấn luyện, upload kịch bản…) — dashboard vẫn read-only.

---

## 9. Lỗi đặc tả drainage — ĐÃ CHỐT (27/10/2026): phương án B

**Vấn đề:** với công thức cũ `D_t = max(0, m_t + ΔI + ΔR − θ_fc)` rồi `m_{t+1} = clip(m_t + ΔI + ΔR − ET − D_t)`, suy ra `m_{t+1} ≤ θ_fc − ET < 0.85`. Nghĩa là **nhánh stress ngập úng `m > 0.85` không bao giờ xảy ra**, dù tài liệu, reward và test đều nói tới nó.

| Phương án | Nội dung | Hệ quả |
|---|---|---|
| A. Giữ công thức, bỏ nhánh ngập úng | Giữ `D_t` như đặc tả cũ; sửa tài liệu/reward: stress chỉ còn `m < 0.20` | Ít sửa code nhất, nhưng mất một nửa ý nghĩa “tránh tưới dư” và lệch báo cáo V2 |
| **B. Tính thấm thoát từ nước đọng ngày trước (ĐÃ CHỌN)** | `D_t = max(0, m_t − θ_fc)`; nước tưới/mưa hôm nay có thể đẩy `m` vượt 0.85 | Giữ được cả hai nhánh stress, khớp tài liệu và reward; phải thêm test biên + ghi nhật ký quyết định |

**Quyết định:** chủ dự án đã duyệt **phương án B** ngày 27/10/2026; đã ghi ở `CONTEXT.md` §15, cập nhật `CONTEXT.md` §5.4/§10/§11 và `docs/03_04_PhanTich_ThietKe_MoiTruong.md` §3.5.

**Hệ quả khi cài `physics.py`:**

- `drainage(moisture, irrigation_gain, rainfall_gain, cfg)` trả `max(0, moisture − cfg.field_capacity)` — **không** cộng `ΔI`/`ΔR` vào trước khi trừ `θ_fc`.
- `update_moisture` vẫn cộng `ΔI + ΔR` vào `m_t` rồi mới trừ `ET` và `D`; `m_next` có thể vượt 0.85 và phải được clip `[0,1]`.
- Thêm test: `m_t = 0.80`, `action = 5`, không mưa ⇒ `m_next > 0.85`; và `D_t = 0` trong trường hợp đó.
- `contract.py` và `reward.py` **không đổi** (nhánh `m > 0.85 ⇒ −100` giữ nguyên).

---

## 10. Rủi ro & cách xử lý

| # | Rủi ro | Dấu hiệu | Cách xử lý |
|---|---|---|---|
| 1 | Chờ nhau vì thiếu phần của người kia | Việc “doing” không tiến triển | B.1 và B.2 độc lập — làm song song; dùng stub theo `contract` khi bị chặn |
| 2 | “Test xanh giả” | Assert bị nới, test bị skip | Review chéo + đếm số test phải tăng; cấm sửa test của người khác |
| 3 | Lệch hợp đồng (mỗi người hiểu một kiểu) | Test đỏ vì kiểu dữ liệu/độ dài khác | `contract.py` là nguồn sự thật; mọi thay đổi phải ghi `CONTEXT.md` §15 |
| 4 | Env chậm (< 10.000 bước/giây) | `test_speed` đỏ | Tránh tạo mảng/đối tượng mỗi bước; đo lại trước khi báo xong |
| 5 | Ngập úng bất khả thi (mục 9) | Reward không bao giờ phạt `> 0.85` | Chốt với chủ dự án trước khi code; không tự sửa |
| 6 | Dashboard trông “thật” nhưng là fixtures | Banner vàng biến mất sai lúc | Chỉ tin số khi banner báo “log thật”; mọi kết luận phải từ `logs/` |
| 7 | Docker chưa từng build | Lỗi chỉ xuất hiện khi build | Không tuyên bố đã kiểm; một người có Docker chạy thử rồi báo log |

---

## 11. Checklist bàn giao đợt thiết lập môi trường

- [ ] Cả hai cài được bằng `bash scripts/setup.sh` và ra cùng baseline test.
- [ ] Reward khớp `+6, +10, −124, −4, −10` + 4 biên; `reward_breakdown` khớp tổng.
- [ ] Weather tất định theo seed; 3 kịch bản nạp được, không sửa code env.
- [ ] Physics: `m` luôn trong `[0,1]`, có thấm thoát khi vượt sức chứa, `ET ≥ 0`.
- [ ] `check_env` pass; episode 30 ngày; `terminated` sau 3 ngày stress; `truncated` khi hết mùa.
- [ ] Tất định: cùng seed giống tuyệt đối, khác seed khác quỹ đạo.
- [ ] ≥ 10.000 bước/giây, có số đo ghi lại.
- [ ] 0 `xfail`; số test tăng; `env/` không import `agents/`; `app/` không import `agriwater`.
- [ ] Có CSV thật trong `logs/`, dashboard đọc được.
- [ ] `CONTEXT.md` đã cập nhật §3 (trạng thái), §11 (điểm chưa chốt), §12 (việc tiếp theo) và §15 nếu có thay đổi được duyệt.
- [ ] Việc còn lại (nếu cắt `render`) được ghi rõ, không để “xong một nửa” mà không ai biết.

---

## 12. Cách báo tiến độ khi không có timeline

- Mỗi việc B.x có đúng 4 trạng thái: `todo → doing → review → done`; chỉ chuyển khi có bằng chứng (test xanh, số đo, ảnh).
- Báo cáo 1 dòng mỗi lần bàn giao: **đã xong gì / còn gì / ai review**.
- Không dùng “sắp xong”, “gần được”: dùng test nào còn đỏ, hàm nào còn `NotImplemented`.
- Khi bị chặn: nêu **ai đang chờ ai**, phần nào có thể làm song song, và stub tạm theo `contract` để không dừng việc khác.

> **Checklist chi tiết theo người (file riêng):** `docs/ToDoList_ThietLap_MoiTruong_Minh_Truong.md` — M-01…M-16 (Minh), T-01…T-15 (Trưởng), C-01…C-06 (chung), kèm **luật chống trùng & xung đột** (chủ sở hữu file, cách nhận việc bằng nhánh, thứ tự phụ thuộc) để hai người dùng AI agent song song mà không giẫm nhau.
