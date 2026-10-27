# CONTEXT — AgriWater-RL (Nhóm 10)

> **Ảnh chụp trạng thái:** 27/10/2026, đọc trực tiếp từ mã nguồn + `pytest` + git.
> **Thư mục dự án thật:** `/home/minh/reinforcement-learning/N10_RF` (mọi lệnh bên dưới chạy tại đây).
> **Tài liệu này là bản đồ ngữ cảnh**, không phải đặc tả gốc. Khi mâu thuẫn, thứ tự ưu tiên:
> `agriwater/env/contract.py` → `docs/HocTangCuongN10_HoanChinh.md` (V2) → `docs/03_04_PhanTich_ThietKe_MoiTruong.md` → `README.md`.

---

## 1. Dự án là gì

| | |
|---|---|
| Tên | **AgriWater-RL** — Hệ thống ra quyết định tưới tiêu tự động tối ưu hóa nguồn nước trong nông nghiệp |
| Môn | Học tăng cường và ứng dụng — Trường Đại học Thủy lợi, Khoa Công nghệ thông tin |
| Nhóm | Nhóm 10 · GV: Lê Nguyễn Tuấn Thành |
| Thành viên | Nguyễn Minh (235117060), Nguyễn Thị Phương Thảo (2351170621, nhóm trưởng), Nguyễn Thế Trưởng (2351170626), Lục Văn Thuận (2351170624), Vũ Tuấn Khanh (2251172386) |
| Bài toán | MDP episodic 30 ngày: mỗi ngày agent chọn 1 trong 6 mức tưới (0…25 L) dựa trên obs 7 chiều; môi trường mô phỏng cân bằng nước tầng rễ, thời tiết theo kịch bản, và trả reward 6 thành phần |
| Mục tiêu kép | Giữ độ ẩm trong dải lý tưởng **và** tiết kiệm nước (tránh tưới dư / tưới trước mưa / tưới dồn dập) |
| 4 chiến lược | Q-Learning (bảng), Monte Carlo Control (on-policy, first-visit, ε-soft), DQN (MLP 7→128→128→6), Baseline luật cố định (`m < 0.30 → 20 L`) |
| Luật môn | C3 (≥ 2 thuật toán RL), C4 (có baseline), C8 (≤ 3 thuật toán RL) ⇒ 3 RL + 1 baseline |

---

## 2. Vị trí repo & git

Có **hai thư mục lồng nhau**, dễ nhầm:

| Đường dẫn | Vai trò | Git |
|---|---|---|
| `/home/minh/reinforcement-learning/` | Thư mục cha; chứa bản tài liệu cũ và **CONTEXT.md / SKILL.md** (do yêu cầu tạo) | Có `.git` riêng, 1 commit `aaebac4` ("Thực hành 1 — mô hình hóa MDP"); rất nhiều file `docs/*` bị xóa trong working tree; `CONTEXT.md`, `SKILL.md`, `N10_RF/` đang untracked |
| `/home/minh/reinforcement-learning/N10_RF/` | **Dự án thật**, toàn bộ mã nguồn | Repo riêng, nhánh `main`, remote `https://github.com/Minh-lab/btl_hoc_tang_cuong.git`, 5 commit, HEAD `092fbe1 feat(app): dashboard prototype 4 trang + fixtures + Docker` |

Trạng thái working tree của `N10_RF` lúc chụp:

```text
 D docs/KichBan_Slide.md               # đã xóa (vẫn còn ở HEAD)
 D docs/TomTat_Session_2026-10-26.md   # đã xóa (vẫn còn ở HEAD)
 D docs/requirements.md                # đã xóa (vẫn còn ở HEAD)
?? docs/KeHoach_NganGon_MC_Va_MoiTruong.pdf   # PDF mới, chưa track
```

- Chưa commit gì thêm; **không có nhánh phụ**.
- `.gitignore` bỏ qua `logs/`, `checkpoints/`, `outputs/`, `data/`, `*.npz`, `*.pt`, `.venv/`, `.freebuff/`.
- Commit message theo mẫu `feat(app): ...`, `docs: ...`; commit gần nhất dùng tiếng Việt không dấu ở mô tả.

---

## 3. Trạng thái chạy được (snapshot 27/10/2026)

```text
$ .venv/bin/python -m pytest
41 passed, 19 xfailed in 0.68s
```

- **60 test case** (47 lõi + 13 dashboard); 19 case `xfail(strict=True)` đánh dấu phần **chưa cài đặt**.
- **Đã cài đặt và chạy được:** `contract`, `EnvConfig`, `Discretizer` (480 trạng thái), `Agent` base + registry + `RandomAgent`, `MetricsLogger` (CSV 13 cột), toàn bộ dashboard Streamlit + fixtures + Docker files.
- **Chưa cài đặt — đang `NotImplementedError`:**
  - `agriwater/env/reward.py` → `calculate_reward()`, `reward_breakdown()` (E-03)
  - `agriwater/env/weather_model.py` → `WeatherModel.reset()`, `.sample()` (E-05)
  - `agriwater/env/physics.py` → `evapotranspiration()`, `drainage()`, `update_moisture()` (E-07)
  - `agriwater/env/agriwater_env.py` → `AgriWaterEnv.reset()`, `.step()`, `.render()` (E-10…E-12, E-20)
  - Các agent thật (`qlearning`, `mc`, `dqn`, `baseline`) — registry chỉ mới đăng ký `random`
- **Hệ quả:** chưa có episode thật nào; dashboard đang đọc **dữ liệu tổng hợp** trong `app/sample_data/` (12 CSV, 536 KB, sinh bởi `scripts/make_fixtures.py`), không phải kết quả thực nghiệm.

Môi trường dev đã kiểm tra:

| Thành phần | Phiên bản |
|---|---|
| Python (`.venv`) | 3.14.8, tạo bằng `--system-site-packages` |
| numpy / pandas | 2.5.4 / 3.1.0 |
| gymnasium | 1.4.0 |
| pytest | 9.1.1 |
| torch | 2.14.1+cu130 |
| streamlit / altair | 1.66.1 / 6.3.0 |

Chưa có thư mục `logs/` (dashboard fallback về fixtures). Docker **chưa từng build** trên máy này.

---

## 4. Cây thư mục & trạng thái từng file

```text
N10_RF/
├── agriwater/
│   ├── __init__.py                  ✅ chỉ khai báo __version__ = "0.1.0" (import nhẹ)
│   ├── env/
│   │   ├── contract.py              ✅ NGUỒN SỰ THẬT: chỉ số obs, hằng số, ngưỡng, chuẩn hóa
│   │   ├── config.py                ✅ EnvConfig (frozen dataclass) + validate + load JSON
│   │   ├── weather_model.py         ⚠️ khung + from_config/from_file; reset/sample = NotImplemented
│   │   ├── physics.py               ⚠️ 3 hàm đều NotImplemented
│   │   ├── reward.py                ⚠️ calculate_reward/reward_breakdown = NotImplemented
│   │   └── agriwater_env.py         ⚠️ spaces + _build_obs/_info OK; reset/step/render = NotImplemented
│   ├── agents/
│   │   ├── base.py                  ✅ interface Agent: act (abstract), observe, end_episode, save/load
│   │   ├── registry.py              ✅ register/make/available + danh sách PLANNED (qlearning/mc/dqn/baseline)
│   │   ├── random_agent.py          ✅ @register("random"), chọn đều trong 6 hành động
│   │   └── discretizer.py           ✅ 480 trạng thái, encode/components/decode/encode_raw
│   └── utils/metrics.py             ✅ MetricsLogger → CSV 13 cột, flush mỗi 200 dòng
├── app/                             ✅ dashboard prototype, CHỈ đọc CSV, KHÔNG import agriwater
│   ├── streamlit_app.py             ✅ st.navigation 4 trang
│   ├── data_access.py               ✅ FIELDS (bản sao schema), CsvRunRepository, kpis/episode_summary/…
│   ├── components.py                ✅ cache TTL 60s, banner dữ liệu mẫu, KPI, format
│   ├── views/{tong_quan,hoc_duong,so_sanh,mo_phong}.py   ✅ 4 trang
│   └── sample_data/*.csv            ⚠️ 12 file synthetic (4 agent × 3 kịch bản × 30 episode)
├── configs/scenarios/{dry,stormy,randomized}.json   ✅ 3 kịch bản, không hard-code trong env
├── scripts/setup.sh                 ✅ tạo .venv + pip install -r + pip install -e .
├── scripts/make_fixtures.py         ✅ sinh CSV mẫu có seed; cố ý khác lõi ở 2 chỗ (xem §10)
├── scripts/run_dashboard.sh         ✅ exec streamlit run app/streamlit_app.py
├── tests/                           ✅ 9 file, 60 case (chi tiết §8)
├── docs/                            xem §9
├── Dockerfile / docker-compose.yml / .dockerignore   ✅ tĩnh, chưa build
├── pyproject.toml                   ✅ deps lõi numpy+gymnasium; extras dqn/viz/dev/dashboard
├── requirements.txt                 ✅ numpy, gymnasium, torch, pandas, matplotlib, pytest
└── README.md                        ✅ cài đặt, lệnh, dashboard, docker, hiện trạng, việc tiếp theo
```

Quy ước import: package `agriwater` cố tình **không** re-export gì để `import agriwater` không kéo gymnasium. Dùng import tường minh:

```python
from agriwater.env import contract as C
from agriwater.env.agriwater_env import AgriWaterEnv
from agriwater.agents import registry
```

---

## 5. Hợp đồng MDP (đã chốt ở cổng G0)

### 5.1. Không gian trạng thái — `Box(7)`, `np.float32`, **đã chuẩn hóa [0,1]**

| Index | Tên | Miền thô | Chuẩn hóa |
|---|---|---|---|
| 0 | `crop_type` | int `[0,3]`, K=4 | `x/(K-1)` = x/3 |
| 1 | `growth_stage` | int `[0,3]` | `g/3` |
| 2 | `soil_moisture` | `[0,1]` | giữ nguyên |
| 3 | `temperature` | `[15,45]` °C | `(x-15)/30` |
| 4 | `rain_probability` | `[0,1]` | giữ nguyên |
| 5 | `rain_forecast_mm` | `[0,50]` mm | `x/50` ⇒ ngưỡng 15 mm ≡ **0.30** |
| 6 | `last_irrigation` | `[0,25]` L | `x/25` ⇒ ngưỡng 12,5 L ≡ **0.50** |

Hàm dựng obs cho test/debug: `C.make_obs(crop_type=…, growth_stage=…, soil_moisture=…, temperature_c=…, rain_prob=…, rain_forecast_mm=…, last_irrigation_l=…)`. Hàm giải chuẩn hóa: `denorm_temperature`, `denorm_rain_forecast`, `denorm_irrigation`.

### 5.2. Hành động — `Discrete(6)`

```python
WATER_LEVELS = (0, 5, 10, 15, 20, 25)   # lít; index = action
N_ACTIONS = 6
action_to_litres(a)                     # raise ValueError nếu ngoài [0, 6)
```

### 5.3. Reward — 6 thành phần, một nguồn sự thật (`reward.py`)

$$R = R_{health} + R_{stress} + R_{water} + R_{waste} + R_{rain} + R_{delay}$$

Tính trên **obs đã chuẩn hóa** (không chia lại cho 50 mm / 25 L):

| Thành phần | Công thức | Hằng số trong `contract.py` |
|---|---|---|
| health | `+10` nếu `m_next ∈ ideal_range(g)` (biên tính là thuộc) | `R_HEALTH`, `IDEAL_LO/HI`, `IDEAL_LO/HI_FLOWER` |
| stress | `−100` nếu `m_next < 0.20` hoặc `m_next > 0.85` | `R_STRESS`, `WILT_POINT`, `FIELD_CAPACITY` |
| water | `−2 · action` (theo **index** hành động, action 5 ⇒ −10) | `C_WATER` |
| waste | `−10 · action` nếu `m_t ≥ 0.60` và `action > 0` | `C_WASTE`, `WASTE_MOISTURE` |
| rain | `−5 · action` nếu `action > 0`, `p_t ≥ 0.70`, `f_t ≥ 0.30` | `C_RAIN`, `RAIN_PROB_TRIGGER`, `RAIN_FORECAST_TRIGGER` |
| delay | `−8 · action` nếu `action > 0` và `last_irrigation ≥ 0.50` | `C_DELAY`, `DELAY_TRIGGER` |

Dải lý tưởng: giai đoạn `g == 2` (ra hoa/kết trái) là `[0.50, 0.75]`, còn lại `[0.40, 0.70]`.
`reward_breakdown()` phải trả đúng 6 khóa `health, stress, water, waste, rain, delay` và tổng **bằng** `calculate_reward()`.

**5 tình huống chuẩn (kỳ vọng test):** `+6`, `+10`, `−124`, `−4`, `−10`.
**4 biên độ ẩm** (action = 2, `m_t = 0.15`): `0.20 → −4` (bằng ngưỡng héo không bị −100), `0.40 → +6`, `0.70 → +6`, `0.85 → −4` (bằng sức chứa không bị −100).

### 5.4. Vật lý cân bằng nước tầng rễ (`physics.py`)

$$m_{t+1}=\operatorname{clip}(m_t+\Delta I+\Delta R-ET_t-D_t,\ 0,\ 1)$$
$$\Delta I=\eta\,k_a\,a_L,\qquad \Delta R=\min(\rho_{max},\ f_{mm}/R_{max}),\qquad D_t=\max(0,\ m_t-\theta_{fc})$$
$$ET_t=c_{evap}\cdot K_c(g)\cdot\frac{T-15}{30}+c_{base}$$

> **Đã chốt 27/10/2026 (phương án B):** thấm thoát tính từ **nước đọng của ngày trước**, `D_t = max(0, m_t − θ_fc)`, không gộp nước tưới/mưa của ngày hôm nay. Nhờ đó nước hôm nay có thể đẩy `m` vượt 0.85 và nhánh stress ngập úng mới xảy ra được. Công thức cũ (`m_t + ΔI + ΔR − θ_fc`) khiến `m ≤ 0.85 − ET` nên ngập úng bất khả thi. Xem §15.

| Hằng số | Giá trị |
|---|---|
| `IRRIGATION_GAIN_PER_L` (k_a) | 0.02 /L (25 L ⇒ +0.5) |
| `IRRIGATION_EFFICIENCY` (η) | 0.9 |
| `RAIN_GAIN_MAX` (ρ_max) | 0.35 |
| `EVAP_RATE` (c_evap) | 0.05 |
| `EVAP_BASE` (c_base) | 0.010 |
| `KC_BY_STAGE` | `(0.7, 1.0, 1.25, 0.8)` |
| `FIELD_CAPACITY` | 0.85 |

`update_moisture(...) -> (m_next, drainage_amount)`, mọi giá trị đã clip `[0,1]`.

### 5.5. Episode, kết thúc, info

- 1 bước = **1 ngày**; `EPISODE_LENGTH = 30` ⇒ `truncated` khi `day ≥ 30`.
- `STRESS_PATIENCE = 3`: stress (`m < 0.20` hoặc `m > 0.85`) **3 ngày liên tiếp** ⇒ `terminated`.
- `info` đúng **6 khóa**: `water_L: float`, `crop_stress: bool`, `moisture: float` (thô), `growth_stage: int`, `ideal: bool`, `stress_days: int`.
- `reset()` trả `(obs, info)` với `info = _info(water_L=0.0)`; obs dựng từ thời tiết ngày 0.
- `step()` trả `(obs, reward, terminated, truncated, info)`; reward dùng `p_t, f_t, last_irrigation` của **ngày vừa hành động** ⇒ phải giữ `prev_state` **trước** khi ghi đè thời tiết.

### 5.6. Kịch bản (JSON, `configs/scenarios/`)

Khóa bắt buộc: `name, rain_prob, temp_range, rain_forecast_range, episode_length, crop_type, growth_stage, seed`.

| File | rain_prob | temp_range | rain_forecast_range | crop / stage | Dùng để |
|---|---|---|---|---|---|
| `dry.json` | 0.05 | 35–42 °C | 0.0–0.1 mm | 0 / 2 (ra hoa) | đo khả năng cứu cây, tiết kiệm nước |
| `stormy.json` | 0.65 | 22–30 °C | 15–30 mm | 1 / 1 | đo hoãn tưới, tận dụng mưa, tránh ngập |
| `randomized.json` | `[0.2, 0.6]` | 20–38 °C | 0–40 mm | 2 / 0 | đánh giá tổng quát hóa |

`WeatherModel.sample()` trả `C.WeatherStep(temperature_c, rain_prob, rain_forecast_mm, rainfall_mm, rained)`; mưa theo Bernoulli(p), nếu mưa thì `rainfall_mm` quanh `forecast` có nhiễu, ngược lại 0. **Bắt buộc dùng `np_random`** được truyền vào, không dùng `random`/`np.random` toàn cục.

### 5.7. Rời rạc hóa (dùng chung Q-Learning & MC)

`1 × 4 × 5 × 3 × 2 × 2 × 2 = 480` trạng thái ⇒ `480 × 6 = 2.880` ô Q.

| Chiều | Biên trong | Số bin |
|---|---|---|
| crop_type | — | 1 (cố định theo kịch bản) |
| growth_stage | — | 4 |
| soil_moisture | 0.20 / 0.40 / 0.60 / 0.80 | 5 |
| temperature (°C) | 25 / 35 | 3 |
| rain_prob | 0.50 | 2 |
| rain_forecast (mm) | 15 | 2 |
| last_irrigation (L) | 12.5 | 2 |

Quy ước bin: giá trị **bằng biên thuộc bin trên** (`np.digitize(..., right=False)`).
Cấu hình đầy đủ 4.320 trạng thái (4 crop × …) chỉ là con số trong báo cáo, **không dùng trong code**.

---

## 6. Kiến trúc & ràng buộc phụ thuộc

```text
Presentation (Streamlit app/)  ──đọc CSV──►  sample_data/ hoặc logs/
        ✗ không import agriwater
RL & Simulation (agriwater/)
   AgriWaterEnv ──► WeatherModel / physics / reward / config / contract
   Agent ──► Discretizer, contract
        ✗ env KHÔNG import agents (NFR-5, có test canh)
Data: Q-Table (.npz), checkpoint (.pt), log (.csv), scenario (.json)
```

- **NFR-1 tất định:** cùng seed ⇒ cùng quỹ đạo bitwise; mọi ngẫu nhiên đi qua `self.np_random` của Gymnasium.
- **NFR-2 tốc độ:** ≥ 10.000 bước/giây (test 100.000 bước, marker `slow`).
- **NFR-3 chuẩn Gymnasium:** đúng signature, 5 giá trị trả về, `check_env()` pass.
- **NFR-4 tách kịch bản:** đổi JSON không sửa code env.
- **NFR-5 một chiều:** `env/` không import `agents/`.
- Dashboard ngược lại: `app/` không import `agriwater`, schema CSV được **copy** và canh bằng test.

---

## 7. Schema dữ liệu & dashboard

`MetricsLogger.FIELDS` = `app.data_access.FIELDS` = **13 cột**:

```text
episode, day, agent, scenario, crop_type, growth_stage, moisture,
action, water_L, reward, crop_stress, ideal, stress_days
```

- `MetricsLogger(path, agent_name=…, scenario=…)` mở file ghi mới (`w`), ghi header, flush mỗi 200 dòng; `log(episode, day, obs, action, reward, info)` nhận obs **sau** hành động; `close()`/context manager.
- Dashboard: `default_repository()` chọn `AGRIWATER_LOGS` → `logs/` → `app/sample_data/`; cờ `synthetic` bật banner cảnh báo "DỮ LIỆU MẪU".
- 4 trang: **Tổng quan** (KPI + reward/nước/ideal theo episode), **Learning curve** (moving average, cumulative, histogram, hành vi theo ngày), **So sánh** (bảng 4 chiến lược + ma trận chiến lược × kịch bản + tải CSV), **Mô phỏng** (độ ẩm theo ngày với dải lý tưởng/ngưỡng stress + nước/reward từng ngày).
- Metric phái sinh: `episode_summary()` (reward, water_L, ideal_ratio, stress_days, days, `survived = days ≥ 30`), `kpis()` trên 5 episode cuối, `convergence_episode()` (moving average đạt 90% mức cuối), `moving_average()`.
- `app/views/mo_phong.py` import trực tiếp `altair` (hiện có sẵn vì streamlit kéo theo, **không khai báo** trong extras ⇒ rủi ro phụ thuộc ngầm).
- Docker: `python:3.12-slim`, không cài torch mặc định (`--build-arg INSTALL_TORCH=true` khi cần), mount `./logs`, healthcheck `/_stcore/health`, cổng 8501.

---

## 8. Kiểm thử

Chạy: `.venv/bin/python -m pytest` · bỏ test chậm: `-m "not slow"` · một file: `tests/test_reward.py -v`.

| File | Case | Trạng thái | Nội dung |
|---|---|---|---|
| `test_contract.py` | 15 | ✅ pass | chỉ số obs, action, ngưỡng dẫn xuất 0.30/0.50, dải lý tưởng, biên stress, chuẩn hóa, `EnvConfig` validate, 3 kịch bản nạp được |
| `test_scaffold.py` | 5 | ✅ pass | registry có `random`, action trong [0,6), lỗi rõ cho `qlearning`, logger ghi đúng 13 cột, `env/` không import `agents/` (chạy subprocess) |
| `test_reward.py` | 10 | ⛔ xfail strict | 5 tình huống + 4 biên + obs bị clip |
| `test_physics.py` | 3 | ⛔ xfail strict | khô khi không tưới, không vượt 1.0, có thấm thoát khi > 0.85 |
| `test_discretizer.py` | 7 | ✅ pass | 480/2880, encode trong miền, biên bin, decode nghịch đảo, encode_raw, 5 bin ẩm khác nhau, sai shape bị chặn |
| `test_env_api.py` | 4 | 1 ✅ / 3 ⛔ | spaces xanh; `check_env`, reset contract, step contract+bounds xfail |
| `test_determinism.py` | 2 | ⛔ xfail | cùng seed giống bitwise; khác seed phải khác (chống "tất định giả") |
| `test_speed.py` | 1 | ⛔ xfail + `slow` | 100.000 bước ≥ 10.000 bước/giây |
| `test_dashboard_schema.py` | 13 | ✅ pass | `FIELDS` dashboard == logger; 12 fixture CSV đúng cột/không rỗng/đúng agent |

**Chính sách xfail:** `pytestmark = pytest.mark.xfail(..., strict=True)` là "đèn báo chưa code". Khi cài xong một hàm: **gỡ `pytestmark`** ở file test tương ứng, chạy lại. Nếu quên gỡ, test xanh sẽ thành `XPASS(strict)` ⇒ đỏ. Không được hạ assert / nới ngưỡng để test qua.

---

## 9. Tài liệu trong `docs/`

| File | Vai trò |
|---|---|
| `HocTangCuongN10_HoanChinh.md` / `.docx` | Báo cáo V2: mục tiêu, 6 tính năng, use case UC-01…UC-06, kiến trúc 4 lớp, MDP đầy đủ (S/A/P/R/γ), phân công, 7 điểm đã chốt |
| `03_04_PhanTich_ThietKe_MoiTruong.md` | Phân tích + thiết kế môi trường: FR-ENV-1…8, NFR-1…6, công thức vật lý, 3 kịch bản, sơ đồ lớp, cấu trúc thư mục dự kiến, 7 test bắt buộc T1–T7 |
| `KeHoach_MoiTruong_Minh_Truong.md` | Kế hoạch 2 người (Minh × Trưởng), 5 cổng G0–G4, hợp đồng giao diện §2, quy trình 5 bước, task card E-01…E-23, review checklist 6 điểm, nhật ký quyết định |
| `KeHoach_NganGon_MC_Va_MoiTruong.md` (+PDF) | Kế hoạch ngắn: chọn MC thay DP, mã giả MC, kiểm tra luật C8, ưu tiên triển khai env |
| `KeHoach_ThietLap_MoiTruong_Minh_Truong.md` | Kế hoạch chi tiết **đợt đang làm** cho Minh × Trưởng: hai tầng môi trường (dev + RL), thứ tự phụ thuộc B.0→B.7, mỗi việc có làm gì/vì sao/đầu vào-ra/DoD/cạm bẫy, **không timeline**; kèm quyết định drainage |
| `III_MaGia_ThuatToan.md` | Mã giả chi tiết 4 chiến lược + bảng so sánh + lộ trình 8 tuần + tiêu chí nghiệm thu |
| `III_MaGia_ThuatToan_Mau_Nop.md` | Template nộp cho các thành viên điền |
| `tham-khao/KienThuc.md` | Ghi chú kiến thức RL của người học (MDP, DP, MC) — dùng để căn mức giải thích |
| `tham-khao/*.docx`, `example_images/` | Tài liệu tham khảo, không phải nguồn sự thật |

**Lưu ý:** `docs/requirements.md`, `docs/KichBan_Slide.md`, `docs/TomTat_Session_2026-10-26.md` **đã bị xóa khỏi working tree nhưng vẫn ở HEAD** (`git show HEAD:docs/…`). Nội dung `requirements.md` (luật môn: 4 thành viên cố định, ≥ 6 tính năng, đủ 4 động từ Integrate/Experiment/Compare/Evaluate, đủ 5 thành phần MDP) vẫn là ràng buộc khi viết báo cáo. `KichBan_Slide.md` là kịch bản 12 slide. `TomTat_Session_2026-10-26.md` là nhật ký session dựng dashboard + phát hiện lỗi đặc tả vật lý.

Các file `.docx`/`.pdf` là nhị phân — **không sửa bằng công cụ văn bản**; bản `.md` mới là bản soạn thảo.

---

## 10. Quyết định đã chốt

| # | Vấn đề | Quyết định |
|---|---|---|
| 1 | Bước thời gian | **1 bước = 1 ngày**, episode 30 bước |
| 2 | Ngưỡng chết | stress liên tiếp **K = 3** ngày (`m < 0.20` hoặc `m > 0.85`) ⇒ `terminated` |
| 3 | Đơn vị `rain_forecast_mm` | chuẩn hóa `R_max = 50 mm`; ngưỡng 0.30 ≡ 15 mm |
| 4 | `stress_days` có trong obs? | **Không** — obs giữ 7 chiều, `stress_days` nằm trong `info` |
| 5 | Số trạng thái | 4.320 (đầy đủ, chỉ trong báo cáo) vs **480** (bảng dùng chung cho Q-Learning & MC) |
| 6 | Thuật toán bổ sung | **Monte Carlo Control** (on-policy, first-visit, ε-soft), không dùng DP vì DP cần biết P |
| 7 | Ký hiệu | trọng số phạt đặt tên `c_w`, `c_rain`, `c_waste`, `c_delay` để không lẫn γ, ε |
| 8 | Dashboard | Streamlit, 4 trang, read-only, mock ở tầng dữ liệu, không thêm streamlit vào `requirements.txt` lõi, timebox ≤ 4 h, không chặn lõi |
| 9 | Fixtures | sinh bằng script có seed, gắn nhãn synthetic, **không** trích số vào báo cáo |
| 10 | Khác biệt có chủ ý của fixtures | `rain_gain = rainfall_mm/700` (trần 0.10) thay vì `/50` (0.35); `initial_moisture = 0.50` thay vì 0.55 — **chỉ trong `make_fixtures.py`**, lõi vẫn theo `contract` |
| 11 | Docker | tùy chọn; cách chính vẫn là `bash scripts/setup.sh`; ảnh không cài torch mặc định |
| 12 | Kịch bản | nạp từ JSON, env không hard-code (NFR-4) |
| 13 | Thấm thoát `D_t` | Tính từ nước đọng ngày trước: `D_t = max(0, m_t − θ_fc)` (phương án B, chốt 27/10/2026) — nhờ đó ngập úng `m > 0.85` khả thi |

---

## 11. Điểm chưa chốt / lỗi đặc tả đã biết

1. ✅ **Đã chốt 27/10/2026 — ngập úng sẽ khả thi (phương án B).** Công thức cũ `D_t = max(0, m_t + ΔI + ΔR − θ_fc)` khiến `m_{t+1} ≤ θ_fc − ET < 0.85`, nên nhánh stress `m > 0.85` không bao giờ xảy ra. Nhóm chốt tính thấm thoát từ nước đọng ngày trước: `D_t = max(0, m_t − θ_fc)`, nên nước tưới/mưa hôm nay có thể đẩy `m` vượt 0.85. **Chưa sửa code** — `physics.py` vẫn `NotImplemented`; khi cài phải theo công thức mới + thêm test biên ngập úng (xem §15).
2. **`EnvConfig` khác tài liệu:** thiết kế §3.4 liệt kê `temp_range`, `rain_prob`, `rain_forecast_mm`, `seed` trong config; code thực tế đọc các giá trị này từ JSON kịch bản. `EnvConfig.ideal_range()` không truyền `growth_stage` sẽ mặc định trả dải **ra hoa** — dễ dùng sai.
3. **Thứ tự thời tiết trong `step()`:** docstring yêu cầu sample thời tiết ngày mới ở bước 3 nhưng reward phải dùng `p_t, f_t` của ngày vừa hành động (bước 6). Chỉ đúng nếu giữ `prev_state` từ bước 1. Ngoài ra thiết kế §4.3 nói obs sau bước dùng **dự báo ngày kế tiếp**, trong khi docstring `step()` dùng thời tiết vừa sample — cần thống nhất khi cài.
4. **`base_dir`:** env mặc định `base_dir="."`, nên chạy từ thư mục khác sẽ không tìm thấy `configs/scenarios/*.json` (test truyền `root`). Cân nhắc resolve theo `__file__` hoặc tài liệu hóa rõ.
5. **Danh sách thành viên:** báo cáo/docx ghi **5 người** (có Vũ Tuấn Khanh), `requirements.md` chốt **4 người**. Chưa thống nhất; ảnh hưởng phần phân công khi nộp.
6. **Số liệu "864 trạng thái"** trong docx V2 vẫn mâu thuẫn với 4.320/480; bản `.md` đã sửa, file nhị phân thì chưa.
7. **Dashboard chưa nối log thật** vì lõi chưa chạy được; chưa có `logs/`.
8. **Docker chưa build lần nào** trên máy này (không có Docker) — mới kiểm tra tĩnh YAML + chạy dashboard bằng venv.
9. `app/views/mo_phong.py` dùng `altair` trực tiếp nhưng extra `dashboard` chỉ khai báo `streamlit`.

---

## 12. Việc tiếp theo (theo thứ tự phụ thuộc)

| Ưu tiên | Task | Nội dung | Người | Test sẽ chuyển xanh |
|---|---|---|---|---|
| 1 | **E-03** | `calculate_reward()` + `reward_breakdown()` | Minh | `test_reward.py` (10) |
| 2 | **E-05** | `WeatherModel.reset()` + `sample()` | Trưởng | test mới của E-05 (hiện chưa có) |
| 3 | **E-07** | `evapotranspiration` / `drainage` / `update_moisture` | Trưởng | `test_physics.py` (3) |
| 4 | **E-10/E-11/E-12** | `reset()` / `step()` / cờ kết thúc | Trưởng | `test_env_api.py` (3), `test_determinism.py` (2), `test_speed.py` (1) |
| 5 | **E-20** | `render()` (cắt được nếu trễ) | Trưởng | — (chỉ FR-ENV-8) |
| 6 | Agents thật | `q_learning.py`, `mc_control.py`, `dqn.py`, `rule_based.py` + đăng ký registry | Minh / Thuận / Khanh | test mới |
| 7 | **E-21** | Smoke pipeline 4 chiến lược × 5 episode → CSV vào `logs/` | Cả nhóm | `test_dashboard_schema` vẫn xanh |
| 8 | E-23 | Bảng số liệu gate + nhật ký quyết định | Minh | — |

> **Đợt đang làm:** thứ tự và phạm vi chi tiết ở `docs/KeHoach_ThietLap_MoiTruong_Minh_Truong.md` (B.0 → B.7, không timeline). Bảng dưới là roadmap tổng; kế hoạch đợt này chi tiết hóa E-03, E-05, E-07, E-10…E-12, E-20, E-21.
>
> **Nhận việc bằng nhánh:** mỗi ID trong `docs/ToDoList_ThietLap_MoiTruong_Minh_Truong.md` được nhận bằng nhánh `feat/<minh|truong>-<ID>` đã push (1 ID = 1 nhánh = 1 PR). Nhánh/PR đã tồn tại nghĩa là đã có người làm — **không làm lại**. Luật đầy đủ ở `SKILL.md` §0.4.

Nguyên tắc: khi xong một task ⇒ gỡ `pytestmark` xfail ở file test tương ứng, chạy `pytest`, mở PR nhỏ (≤ 2 ngày, 1 nhánh = 1 task). Cổng G1 = reward đúng 5 tình huống; G2 = `step()` chạy 1 episode 30 bước; G3 = toàn bộ pytest xanh; G4 = smoke 4 chiến lược xuất CSV.

---

## 13. Lệnh thường dùng

```bash
cd /home/minh/reinforcement-learning/N10_RF

bash scripts/setup.sh                       # 1 lần: .venv + deps + pip install -e .
.venv/bin/python -m pytest                  # toàn bộ (60 case)
.venv/bin/python -m pytest -m "not slow"    # bỏ test hiệu năng
.venv/bin/python -m pytest tests/test_reward.py -v

.venv/bin/python scripts/make_fixtures.py   # sinh lại 12 CSV mẫu (ghi đè sample_data)
bash scripts/run_dashboard.sh               # http://localhost:8501
.venv/bin/python -m pip install -e ".[dashboard]"   # nếu thiếu streamlit

docker compose up --build                   # dashboard trong container
docker compose run --rm test                # pytest trong container
```

---

## 14. Tóm tắt một câu

Dự án đã có **hợp đồng MDP, khung môi trường, rời rạc hóa, logger, dashboard và 60 test**; phần còn thiếu để có episode thật là **reward → weather → physics → reset/step**, sau đó mới đến 4 thuật toán và số liệu thực nghiệm.

---

## 15. Nhật ký thay đổi đã xác nhận (append-only)

> Quy tắc: AI **không** tự thêm/sửa mục này. Chỉ ghi sau khi chủ dự án đã xác nhận rõ ràng một đề xuất (xem `SKILL.md` §0.2). Mỗi lần ghi: ngày, nội dung thay đổi, người xác nhận, phạm vi ảnh hưởng; đồng thời cập nhật mục tương ứng ở trên (§5 nếu là hợp đồng, §11 nếu là điểm chưa chốt, §12 nếu là roadmap).

| Ngày | Thay đổi | Người xác nhận | Phạm vi ảnh hưởng |
|---|---|---|---|
| 2026-10-27 | Ban hành luật làm việc: AI phải đọc `CONTEXT.md` + `SKILL.md` trước mỗi lần triển khai, bám sát `CONTEXT.md`; mọi ý kiến bổ sung/cải thiện phải đề xuất và chờ chủ dự án xác nhận, sau đó mới ghi vào `CONTEXT.md` rồi mới triển khai | Chủ dự án (yêu cầu trực tiếp ngày 27/10/2026) | `SKILL.md` §0 (mới), §8, §11; `CONTEXT.md` §15 (mới); không đổi code, test hay hợp đồng MDP |
| 2026-10-27 | Duyệt cập nhật tài liệu để trỏ tới kế hoạch mới: `SKILL.md` §0.1, §2, §10; `CONTEXT.md` §9, §12 | Chủ dự án (duyệt trong hội thoại 27/10/2026) | Chỉ tài liệu; không đổi code, test hay hợp đồng |
| 2026-10-27 | Chốt lỗi đặc tả drainage — **phương án B**: `D_t = max(0, m_t − θ_fc)`, cho phép ngập úng `m > 0.85`; đã cập nhật `CONTEXT.md` §5.4, §10 (#13), §11 (#1), `docs/03_04_PhanTich_ThietKe_MoiTruong.md` §3.5, `docs/KeHoach_ThietLap_MoiTruong_Minh_Truong.md` §9 và B.3 | Chủ dự án (duyệt trong hội thoại 27/10/2026) | `physics.py` khi cài phải theo công thức mới + thêm test biên ngập úng; `contract.py` và `reward.py` không đổi; `.docx`/`.pdf` phải sửa thủ công |
| 2026-10-27 | Áp dụng luật **“nhận việc bằng nhánh”**: kiểm nhánh/PR/Trạng thái trước khi làm; nhận việc = push nhánh `feat/<minh|truong>-<ID>`; 1 ID = 1 nhánh = 1 PR; không làm lại ID đã có nhánh/PR; chỉ commit file thuộc ID; merge rồi mới đổi Trạng thái | Chủ dự án (yêu cầu trực tiếp ngày 27/10/2026) | `SKILL.md` §0.1 (bước 5), §0.4 (mới), §10; `CONTEXT.md` §12; không đổi code, test hay hợp đồng MDP |
