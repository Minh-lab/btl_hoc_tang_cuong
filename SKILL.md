# SKILL — Luật làm việc bắt buộc trong repo AgriWater-RL (Nhóm 10)

> **Đây là file AI PHẢI đọc và tuân theo trước MỌI lần triển khai.** Không đọc file này + `CONTEXT.md` thì không được sửa code.
> **`CONTEXT.md` (cùng thư mục cha) là la bàn của dự án.** Mọi việc làm phải truy vết được về một mục trong đó; không tự đổi hướng, không tự mở rộng phạm vi.
> **Có ý kiến bổ sung/cải thiện ⇒ đề xuất và chờ chủ dự án xác nhận; chỉ sau khi được xác nhận mới ghi vào `CONTEXT.md` rồi mới triển khai.**
> Thư mục làm việc: `/home/minh/reinforcement-learning/N10_RF`.

---

## 0. LUẬT BẮT BUỘC TRƯỚC MỖI LẦN TRIỂN KHAI

### 0.1. Bước 0 — Đọc và đối chiếu (không được bỏ qua)

```text
1. ĐỌC CONTEXT.md, tối thiểu 4 mục:
     §3  Trạng thái chạy được (cái gì đã có, cái gì NotImplemented)
     §5  Hợp đồng MDP (obs / action / reward / physics / episode)
     §11 Điểm chưa chốt & lỗi đặc tả đã biết
     §12 Việc tiếp theo (roadmap E-xx)
     +   KẾ HOẠCH ĐANG HIỆU LỰC: docs/KeHoach_ThietLap_MoiTruong_Minh_Truong.md (B.0 → B.7)
2. XÁC ĐỊNH task thuộc E-xx nào trong §12 (hoặc mục B.x của kế hoạch đang hiệu lực).
     Không khớp E-xx nào  ⇒ DỪNG, hỏi chủ dự án. Không tự nhận việc mới.
3. CHẠY BASELINE: .venv/bin/python -m pytest -q  → ghi lại số passed/xfailed.
4. ĐỐI CHIẾU vùng cấm: task có chạm mục nào ở §8 không?
     Có  ⇒ chỉ được làm sau khi được xác nhận (xem §0.2).
5. CHỈ SAU 1–4 mới được sửa code.
```

### 0.2. Có ý kiến bổ sung/cải thiện ⇒ đề xuất, KHÔNG tự làm

Áp dụng cho **mọi** thứ không nằm nguyên văn trong `CONTEXT.md` hoặc task card: đổi/ thêm hằng số, ngưỡng, công thức, thuật toán, kịch bản, cột log, trang dashboard, cấu trúc thư mục, thư viện, quy trình, cách đặt tên, phạm vi task…

```text
1. DỪNG — không sửa code, không sửa CONTEXT.md.
2. ĐỀ XUẤT cho chủ dự án theo đúng  dòng:
     mô tả
     • Vấn đề:      <cái gì đang sai/thiếu/lệch>
     • Bằng chứng:  <file:dòng, test đỏ, số đo, mâu thuẫn giữa 2 tài liệu>
     • Đề xuất:     <thay đổi cụ thể, phạm vi ảnh hưởng>
     • Ảnh hưởng:   <test nào đổi, báo cáo/số liệu nào phải sửa, ai bị ảnh hưởng>
     • Thay thế:     <phương án khác + vì sao không chọn>
     • Đề nghị:      “Chờ xác nhận: Đồng ý / Không / Sửa lại”
3. CHỜ xác nhận rõ ràng của chủ dự án. Im lặng, “ừ”, “ok” chung chung mà không nói rõ
   đồng ý thay đổi nào ⇒ coi như CHƯA xác nhận.
4. SAU KHI ĐƯỢC XÁC NHẬN:
     a. Ghi vào CONTEXT.md §15 “Nhật ký thay đổi đã xác nhận” (ngày, nội dung, người xác nhận).
     b. Cập nhật đúng mục liên quan trong CONTEXT.md (§5 nếu là hợp đồng, §12 nếu là roadmap…).
     c. Nếu chạm hợp đồng/hằng số ⇒ cập nhật contract + test + tài liệu .md liên quan.
     d. Chạy lại toàn bộ pytest, rồi mới code tiếp.
```

**Tuyệt đối không:** tự đổi mục tiêu/direction dự án; tự thêm tính năng, thuật toán, kịch bản, metric; tự “dọn dẹp” hay refactor ngoài task; tự sửa `CONTEXT.md` khi chưa được xác nhận; tự nới test để hợp với ý mình.

**Được làm ngay, không cần hỏi:** cài đúng các hàm `NotImplementedError` theo docstring + `CONTEXT.md`; sửa bug trong đúng phạm vi task; thêm test cho phần mình vừa làm; sửa lỗi type/lint; cập nhật README khi lệnh chạy thay đổi trong phạm vi task.

### 0.3. Thứ tự ưu tiên khi có mâu thuẫn

```text
1. Xác nhận mới nhất của chủ dự án (đã ghi ở CONTEXT.md §15)
2. CONTEXT.md §5 (hợp đồng) + agriwater/env/contract.py
3. Báo cáo V2: docs/HocTangCuongN10_HoanChinh.md
4. Thiết kế: docs/03_04_PhanTich_ThietKe_MoiTruong.md
5. Kế hoạch: docs/KeHoach_MoiTruong_Minh_Truong.md
6. README.md
7. Docstring trong code
```

Gặp mâu thuẫn giữa các mục ⇒ **không tự chọn**; báo theo §0.2.

---

## 1. Ba câu phải nhớ trước khi sửa bất cứ thứ gì

1. **`agriwater/env/contract.py` là nguồn sự thật duy nhất về hằng số** — obs 7 chiều đã chuẩn hóa `[0,1]`, 6 mức tưới, mọi hằng số/ngưỡng. Không có "số ma thuật" trong code khác. (Chỉ thay đổi khi có xác nhận mới đã ghi ở `CONTEXT.md` §15.)
2. **Phần lớn lõi đang `NotImplementedError`** — `pytest` xanh hiện tại (41 passed / 19 xfailed) **không** chứng minh môi trường chạy được; 19 `xfail(strict=True)` là danh sách việc chưa làm.
3. **Số liệu trong `app/sample_data/` là dữ liệu tổng hợp**, không được trích vào báo cáo như kết quả thực nghiệm.

---

## 2. Quy trình chuẩn cho mỗi task (5 bước, lấy từ kế hoạch G0–G4)

```text
1. NHẬN TASK   → đọc task card E-xx trong docs/KeHoach_MoiTruong_Minh_Truong.md
                 hoặc mục B.x trong docs/KeHoach_ThietLap_MoiTruong_Minh_Truong.md
2. TEST ĐỎ     → chạy test hiện có, xác nhận nó đang fail/xfail đúng lý do
3. CODE TỐI THIỂU → chỉ làm test xanh, không thêm tính năng ngoài task
4. TỰ KIỂM     → gỡ pytestmark xfail, chạy toàn bộ pytest, soi checklist §7
5. BÀN GIAO    → nhánh feat/… ngắn (≤ 2 ngày), commit rõ, mở PR nhỏ
```

Khi cài xong một hàm:

```bash
# 1. gỡ dòng pytestmark xfail ở đúng file test
# 2. chạy lại
.venv/bin/python -m pytest tests/test_reward.py -v
.venv/bin/python -m pytest
```

Nếu **quên gỡ** `pytestmark`, test sẽ báo `XPASS(strict)` và đỏ — đó là thiết kế cố ý, đừng "sửa" bằng cách bỏ `strict=True`.

**Cấm:** hạ assert, nới ngưỡng, `skip` test, thêm `try/except` nuốt lỗi, hoặc sửa test của người khác cho qua.

---

## 3. Bất biến kỹ thuật (vi phạm là sai, kể cả khi test chưa bắt)

| # | Bất biến | Cách kiểm |
|---|---|---|
| 1 | `obs` là `np.float32[7]`, mọi chiều trong `[0,1]` | `obs.dtype == np.float32`, `((obs>=0)&(obs<=1)).all()` |
| 2 | Ngưỡng reward dùng **giá trị đã chuẩn hóa** (0.20 / 0.40 / 0.70 / 0.85 / 0.60 / 0.30 / 0.50) | không chia lại cho 50 hay 25 |
| 3 | Mọi ngẫu nhiên đi qua `self.np_random` (Gymnasium) | `grep -R "np.random\.\|import random" agriwater/` phải rỗng |
| 4 | `agriwater/env/**` **không** import `agriwater.agents` | `tests/test_scaffold.py::test_env_does_not_depend_on_agents` |
| 5 | `app/**` **không** import `agriwater` | `grep -R "agriwater" app/` (ngoài docstring) |
| 6 | Mọi giá trị độ ẩm/tưới/mưa đã `clip` về `[0,1]` trước khi trả obs | test biên |
| 7 | `info` đúng **6 khóa**: `water_L, crop_stress, moisture, growth_stage, ideal, stress_days` | `set(info) == {...}` |
| 8 | `step()` trả **5** phần tử, `reset()` trả **2**, cờ là `bool` thật (không phải `np.bool_`) | `test_env_api.py` |
| 9 | Schema CSV 13 cột khớp giữa `MetricsLogger.FIELDS` và `app.data_access.FIELDS` | `tests/test_dashboard_schema.py` |
| 10 | Không đổi chữ ký `Agent.act/observe/end_episode/save/load`, không đổi API `reset/step` | review |

---

## 4. Công thức phải cài (đừng tự phát minh lại)

### 4.1. Reward — `agriwater/env/reward.py` (E-03)

Đầu vào `state`, `next_state` là obs **đã chuẩn hóa**; `action` là index 0…5.

```text
m_t   = state[2]        m_next = next_state[2]
g     = next_state[1]   p_t = state[4]   f_t = state[5]   l_t = state[6]
ideal = [0.50, 0.75] nếu round(g*3) == 2, ngược lại [0.40, 0.70]   # biên tính là thuộc

R  = +10   nếu ideal[0] <= m_next <= ideal[1]
R += -100  nếu m_next < 0.20 hoặc m_next > 0.85
R += -2  * action
R += -10 * action   nếu m_t >= 0.60 và action > 0
R += -5  * action   nếu action > 0 và p_t >= 0.70 và f_t >= 0.30
R += -8  * action   nếu action > 0 và l_t >= 0.50
```

Kỳ vọng: `+6, +10, −124, −4, −10`; biên `0.20 → −4`, `0.40 → +6`, `0.70 → +6`, `0.85 → −4` (với `action=2`, `m_t=0.15`, `g=1`).
`reward_breakdown()` trả 6 khóa và **tổng phải khớp tuyệt đối** `calculate_reward()` — tốt nhất là một hàm lõi trả dict, hàm còn lại `sum()`.

Giai đoạn lấy từ **`next_state`** (docstring nói `g_next`), không lấy từ `state`.

### 4.2. Thời tiết — `agriwater/env/weather_model.py` (E-05)

```python
temperature_c     = np_random.uniform(*scenario["temp_range"])
rain_prob         = (np_random.uniform(*rain) if isinstance(rain, list) else float(rain))
rain_forecast_mm  = np_random.uniform(*scenario["rain_forecast_range"])
rained            = np_random.random() < rain_prob
rainfall_mm       = max(0.0, rain_forecast_mm * (1 + np_random.normal(0, 0.25))) if rained else 0.0
return C.WeatherStep(temperature_c, rain_prob, rain_forecast_mm, rainfall_mm, rained)
```

- `reset()` đưa bộ đếm nội bộ về 0 (và **không** tạo generator mới — generator đã được truyền từ env).
- Không dùng thứ tự gọi khác nhau giữa 2 lần chạy cùng seed (thứ tự tiêu thụ RNG chính là hợp đồng tất định).

### 4.3. Vật lý — `agriwater/env/physics.py` (E-07)

```python
delta_i = cfg.irrigation_efficiency * cfg.irrigation_gain_per_l * C.WATER_LEVELS[action]
delta_r = min(cfg.rain_gain_max, rainfall_mm / C.R_MAX_MM)
d       = drainage(moisture, delta_i, delta_r, cfg)      # max(0, m + ΔI + ΔR − θ_fc)
et      = evapotranspiration(temperature_c, growth_stage, cfg)  # c_evap·K_c·(T−15)/30 + c_base, ≥ 0
m_next  = C.clip01(moisture + delta_i + delta_r - et - d)
```

- `evapotranspiration` và `drainage` là hàm thuần, nhận `config` qua tham số (không đọc global).
- Trả `(m_next, d)`; test hiện có chỉ kiểm 3 tính chất: khô khi không tưới, `≤ 1.0`, `d > 0` khi `m=0.84` tưới 25 L + mưa 40 mm.
- **Lỗi đặc tả đã biết:** công thức này khiến `m ≤ 0.85 − ET`, nên ngập úng không bao giờ xảy ra. Trước khi "sửa cho đúng ý", **hỏi nhóm** (xem §8) — đừng tự đổi công thức vì sẽ lệch báo cáo và test.

### 4.4. Môi trường — `agriwater/env/agriwater_env.py` (E-10/E-11/E-12)

`reset(seed=None, options=None)`:

```text
1. super().reset(seed=seed)                  # tạo self.np_random — BẮT BUỘC
2. WeatherModel.from_config(cfg, self.np_random, base_dir) rồi .reset()
3. _day = 0; _moisture = cfg.initial_moisture; _stress_days = 0; _last_irrigation_l = 0
4. w = self._weather.sample() → lưu _temperature_c, _rain_prob, _rain_forecast_mm, _rainfall_mm
5. return self._build_obs(), self._info(water_L=0.0)
```

`step(action)` — **giữ đúng thứ tự**, sai thứ tự là sai reward:

```text
1. prev_state = self._build_obs()          # s_t TRƯỚC khi đổi bất cứ thứ gì
2. water_L = C.action_to_litres(action)
3. w = self._weather.sample(); ghi đè T, p, f, rainfall
4. m_next, drained = physics.update_moisture(m=self._moisture, action=action,
                        temperature_c=w.temperature_c, rainfall_mm=w.rainfall_mm,
                        growth_stage=self._growth_stage, config=self.cfg)
5. self._day += 1; self._last_irrigation_l = water_L; self._moisture = m_next
6. r = calculate_reward(prev_state, action, self._build_obs(), self.cfg)
7. stress: nếu C.is_stressed(m_next): _stress_days += 1 else 0
   terminated = _stress_days >= cfg.stress_patience
   truncated  = _day >= cfg.episode_length
8. return obs, reward, terminated, truncated, self._info(water_L)
```

Lưu ý:
- Reward phải dùng `p_t, f_t, l_t` của **ngày vừa hành động** ⇒ dùng `prev_state` đã dựng ở bước 1, **không** dựng lại sau bước 3.
- Không sample thời tiết 2 lần trong một bước (làm lệch chuỗi tất định).
- `_build_obs()` và `_info()` đã có sẵn — dùng lại, đừng viết bản thứ hai.
- `_info()` trả `moisture` **thô**, `crop_stress`/`ideal` tính từ `_moisture` hiện tại.

---

## 5. Việc chưa có test — tự viết khi làm

Các phần sau chưa được test canh, nên phải tự viết test mới (đừng chỉ dựa vào test cũ):

| Phần | Test tối thiểu nên thêm |
|---|---|
| `WeatherModel.sample()` | cùng seed ⇒ cùng chuỗi `WeatherStep`; `rain_prob` lấy đúng từ JSON; `rained=False ⇒ rainfall_mm == 0` |
| `AgriWaterEnv.reset` | 20 lần reset liên tiếp đều trả obs 7 chiều trong `[0,1]`; `info` đủ 6 khóa |
| `terminated`/`truncated` | 3 ngày liên tiếp `m < 0.20` ⇒ `terminated=True`; 30 ngày ⇒ `truncated=True`; hai cờ không cùng bật sai ngữ cảnh |
| `reward_breakdown` | tổng 6 khóa == `calculate_reward` |
| Agent mới | `registry.make("<tên>")` chạy được, `act()` trả `int` trong `[0,6)`, cùng seed ⇒ cùng hành động |

Test đặt trong `tests/`, dùng fixture sẵn có: `root`, `scenario_dir`, `scenario` (parametrize 3 kịch bản), `make_obs`, `rng`.

---

## 6. Dashboard & dữ liệu — quy tắc riêng

- `app/` **chỉ đọc CSV**, không huấn luyện, không import lõi. Muốn thêm dữ liệu thật: đặt CSV đúng 13 cột vào `logs/` hoặc đặt `AGRIWATER_LOGS=<thư mục>`. **Không sửa UI** để đổi nguồn.
- Nếu đổi `agriwater/utils/metrics.FIELDS` ⇒ phải đổi **cả** `app/data_access.FIELDS` và 12 CSV fixtures, nếu không `test_dashboard_schema.py` đỏ.
- `make_fixtures.py` cố ý khác lõi (`rain/700`, `m0=0.50`). **Không** đưa các hằng số đó vào `contract.py` hay `physics.py`; chúng chỉ để biểu đồ minh họa có ý nghĩa.
- Thêm trang: tạo `app/views/<ten>.py` với `render()`, đăng ký `st.Page(...)` trong `app/streamlit_app.py`.
- Mọi trang phải gọi `ui.page_header(...)` để banner "DỮ LIỆU MẪU" luôn hiện khi đang dùng fixtures.
- Chạy thử nhanh không cần mở trình duyệt: dùng `streamlit.testing.v1.AppTest` (đã dùng trong session trước).

---

## 7. Checklist trước khi báo xong

```bash
cd /home/minh/reinforcement-learning/N10_RF
.venv/bin/python -m pytest -m "not slow" -q     # phải xanh, không XPASS
.venv/bin/python -m pytest -q                   # gồm cả test hiệu năng nếu đã cài step()
```

- [ ] Đã gỡ `pytestmark` xfail ở đúng file; không còn `XPASS`.
- [ ] Số test **tăng**, không giảm; không assert nào bị nới.
- [ ] Không hằng số mới ngoài `contract.py` (nếu buộc phải thêm, thêm vào `contract` + `EnvConfig`).
- [ ] Không `np.random`/`random` toàn cục trong `agriwater/`.
- [ ] `info` vẫn đúng 6 khóa; obs vẫn `float32[7]` trong `[0,1]`.
- [ ] `env/` không import `agents/`; `app/` không import `agriwater`.
- [ ] Docstring/comment tiếng Việt, có type hint, khớp phong cách file hiện tại.
- [ ] Nếu sửa hành vi đã ghi trong báo cáo ⇒ ghi vào nhật ký quyết định (mục 6 của `docs/KeHoach_MoiTruong_Minh_Truong.md`) và báo nhóm.

---

## 8. Khi nào phải hỏi, không được tự quyết

> Đây là danh sách **tối thiểu**; luật chung ở §0.2 áp dụng cho mọi thay đổi ngoài `CONTEXT.md`.

| Tình huống | Vì sao |
|---|---|
| Đổi bất kỳ hằng số/ngưỡng/chỉ số nào trong `contract.py` | Là hợp đồng G0 của 2 người + đã ghi trong báo cáo V2 |
| Sửa công thức `drainage` để ngập úng khả thi | Lỗi đặc tả đã biết, ảnh hưởng test, báo cáo và cân bằng reward — cần nhóm chốt |
| Đổi số trạng thái 480 → khác | Ảnh hưởng so sánh Q-Learning ↔ MC và bảng trong báo cáo |
| Thêm thuật toán thứ 4 vào danh sách tính điểm C8 | Luật môn giới hạn ≤ 3 thuật toán RL |
| Đổi ngữ nghĩa `terminated` vs `truncated` | Chỉ bootstrap khi `truncated`; gộp cờ sẽ làm agent học sai |
| Sửa file `.docx`/`.pdf` | Nhị phân, phải sửa thủ công bằng Word; bản `.md` mới là nguồn soạn thảo |

Ngược lại, **cứ làm luôn** (không cần hỏi): cài các hàm `NotImplementedError` đúng docstring, thêm test, sửa lỗi type/lint, cập nhật README khi lệnh thay đổi.

---

## 9. Bẫy đã từng gặp (đọc để không lặp lại)

1. **Chuẩn hóa hai lần.** `rain_forecast_mm` trong obs đã là `mm/50`; đừng chia thêm. Ngưỡng 0.30 chính là 15 mm.
2. **Quên `super().reset(seed=seed)`** ⇒ không có `np_random` ⇒ `check_env` fail hoặc mất tất định.
3. **Reward lấy nhầm thời tiết ngày mới** ⇒ mất phạt `R_rain`, đường học lệch hẳn.
4. **Tạo `WeatherModel` mới mỗi `sample()`** ⇒ cùng seed nhưng quỹ đạo khác; phải tạo một lần trong `reset()`.
5. **Dùng `np.bool_`** cho `terminated`/`truncated` ⇒ Gymnasium `check_env` báo lỗi kiểu.
6. **`EnvConfig.ideal_range()` không truyền `growth_stage`** ⇒ trả dải ra hoa `[0.50,0.75]` thay vì `[0.40,0.70]`.
7. **Chạy từ thư mục khác** ⇒ không tìm thấy `configs/scenarios/*.json` (`base_dir` mặc định `"."`); luôn `cd` về gốc dự án.
8. **Sửa schema CSV** mà quên bản copy trong `app/data_access.py` ⇒ test đỏ (đúng như thiết kế).
9. **Nhầm fixtures là kết quả** ⇒ mọi kết luận trong báo cáo phải đến từ log thật trong `logs/`.
10. **Docker chưa build lần nào** — đừng tuyên bố "Docker chạy được" khi chưa chạy `docker compose up --build`.

---

## 10. Bản đồ nhanh: muốn X thì sửa ở đâu

| Muốn | File |
|---|---|
| Đổi ngưỡng/trọng số/hằng số vật lý | `agriwater/env/contract.py` (+ `EnvConfig` nếu cần ghi đè) |
| Đổi tham số mặc định của một lần chạy | `agriwater/env/config.py` |
| Đổi cách sinh thời tiết | `agriwater/env/weather_model.py` + `configs/scenarios/*.json` |
| Đổi vật lý đất | `agriwater/env/physics.py` |
| Đổi phần thưởng | `agriwater/env/reward.py` (một nguồn sự thật duy nhất) |
| Đổi vòng đời episode | `agriwater/env/agriwater_env.py` |
| Thêm thuật toán | file mới trong `agriwater/agents/` + `@register("tên")` + import trong `agents/__init__.py` |
| Đổi cách rời rạc hóa | `agriwater/agents/discretizer.py` (nhớ: dùng chung Q-Learning & MC) |
| Đổi cột log | `agriwater/utils/metrics.py` **và** `app/data_access.py` **và** fixtures |
| Đổi giao diện | `app/views/*.py`, `app/components.py`, `app/streamlit_app.py` |
| Đổi số liệu mẫu | `scripts/make_fixtures.py` (giữ seed, giữ nhãn synthetic) |
| Đổi cách cài/chạy | `scripts/setup.sh`, `scripts/run_dashboard.sh`, `Dockerfile` |
| Đổi đặc tả/hợp đồng | `docs/KeHoach_MoiTruong_Minh_Truong.md` §2 và §6 (nhật ký quyết định) |
| Đổi phạm vi/thứ tự đợt thiết lập môi trường | `docs/KeHoach_ThietLap_MoiTruong_Minh_Truong.md` (phải được chủ dự án xác nhận, ghi `CONTEXT.md` §15) |

---

## 11. Ngắn gọn cho agent tiếp theo

> **Trước khi code:** đọc `CONTEXT.md` §3/§5/§11/§12 → xác định E-xx → chạy pytest baseline → kiểm §8.
> **Muốn khác CONTEXT.md:** đề xuất 6 dòng, chờ chủ dự án xác nhận, ghi vào `CONTEXT.md` §15, rồi mới làm.
> Chạy `pytest` để thấy 19 `xfail` — đó là danh sách việc.
> Cài **reward trước** (test đã viết sẵn, kỳ vọng rõ), rồi **weather → physics → reset/step**.
> Mỗi lần xong: gỡ `pytestmark`, chạy full test, kiểm bất biến §3, đừng đổi `contract.py`.
> Mọi con số đưa vào báo cáo phải đến từ `logs/` thật, không phải `app/sample_data/`.

## 12. Tham khảo tài liệu mẫu /home/minh/reinforcement-learning/N10_RF/docs/tham-khao/example.docx
