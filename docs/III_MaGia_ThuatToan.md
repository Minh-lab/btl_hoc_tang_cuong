# III. MÃ GIẢ CÁC THUẬT TOÁN DỰ KIẾN SỬ DỤNG

> **Thuộc dự án:** AgriWater-RL — Hệ thống ra quyết định tưới tiêu tự động tối ưu hóa nguồn nước trong nông nghiệp.
> **Bối cảnh:** tiếp nối Mô hình hóa MDP theo bản docx V2 (trạng thái 7 chiều, 6 mức tưới, hàm phần thưởng 6 thành phần, $\gamma = 0.99$, episode 30 ngày) và đặc tả 6 Use Case (`UC-01 … UC-06`). Tài liệu cung cấp mã giả của **bộ 4 chiến lược**, lý do lựa chọn và kế hoạch triển khai.

---

## III.1. Tổng quan bộ thuật toán

### III.1.1. Đặc điểm bài toán → hệ quả lựa chọn thuật toán

| Đặc điểm bài toán | Hệ quả đối với lựa chọn thuật toán |
|---|---|
| Không gian hành động **rời rạc, nhỏ**: $A = \{0,1,2,3,4,5\}$ tương ứng $\{0,5,10,15,20,25\}$ L | Phù hợp với thuật toán tối ưu trực tiếp theo giá trị (value-based): Q-Learning, MC Control, DQN (mạng 6 đầu ra) |
| Không gian trạng thái **7 chiều** (2 biến rời rạc + 5 biến liên tục) | DQN xử lý trực tiếp vector liên tục; Q-Learning và MC cần rời rạc hóa (480 hoặc 4.320 trạng thái) |
| Môi trường **model-free**, $P$ không cho trước | Loại DP (Value/Policy Iteration) vì đòi hỏi biết $P$; chọn các thuật toán học từ trải nghiệm |
| Bài toán **episodic**: `terminated` khi cây chết, `truncated` sau 30 ngày | Monte Carlo áp dụng được (cần episode kết thúc để tính $G_t$) |
| $\gamma = 0.99$, thưởng dài hạn theo vụ | Q-Learning hội tụ về bất động điểm Bellman; DQN cần Target Network để ổn định mục tiêu dài hạn; MC có phương sai cao hơn |
| Phạt nặng vùng nguy hiểm ($-100$) | Cần đủ khám phá để chạm trạng thái hiếm ⇒ $\varepsilon$-greedy (Q-Learning, DQN) và $\varepsilon$-soft (MC) |
| Luật môn: **C3** (≥ 2 thuật toán RL), **C4** (có baseline), **C8** (≤ 3 thuật toán) | 3 thuật toán RL (Q-Learning, MC, DQN) + 1 baseline không học |

### III.1.2. Bộ 4 chiến lược và phân loại theo C8

| # | Chiến lược | Loại | Vai trò trong báo cáo | Người phụ trách |
|---|---|---|---|---|
| 1 | **Tabular Q-Learning** | RL — off-policy TD(0) — bảng | Mốc đối chứng dạng bảng, minh bạch | Nguyễn Minh |
| 2 | **Monte Carlo Control** | RL — on-policy, first-visit, $\varepsilon$-soft | Đối chiếu bias–variance: học từ return đầy đủ | Nguyễn Minh |
| 3 | **DQN** | RL — value-based + xấp xỉ hàm | Thuật toán chủ đạo cho trạng thái 7 chiều liên tục | Lục Văn Thuận |
| 4 | **Baseline luật cố định** | Không học (if-else) | Mốc so sánh bắt buộc (C4) | Vũ Tuấn Khanh |

> **Đếm theo C8:** 3 thuật toán RL (dòng 1–3) + 1 chiến lược cơ sở (dòng 4). Baseline là *mốc so sánh* theo đúng tinh thần C4 ("baseline: random, fixed-rule, hoặc thuật toán truyền thống"), không phải thuật toán RL. Nếu giảng viên đếm khác, MC là module cắm rời: gỡ 1 dòng trong `registry.py` là xong, không ảnh hưởng env/DQN/Q-Learning.

**Vì sao bổ sung Monte Carlo mà không phải Dynamic Programming:** DP yêu cầu biết trước $P(s' \mid s,a)$, trái với mục 2.4 của báo cáo (môi trường model-free, $P$ là hộp đen); MC giữ nguyên giả định đó, dùng lại bộ rời rạc hóa của Q-Learning và trực tiếp kiểm chứng nhận định trong báo cáo *"Monte Carlo phải đợi kết thúc cả episode mới cập nhật được"* — biến nhận định lý thuyết thành thực nghiệm.

---

## III.2. Quy ước chung cho cả 4 mã giả

- **Vector trạng thái:** $S_t = (\text{crop\_type}, \text{growth\_stage}, \text{soil\_moisture}, \text{temperature}, \text{rain\_probability}, \text{rain\_forecast\_mm}, \text{last\_irrigation})$, mọi chiều chuẩn hóa $[0,1]$; `soil_moisture` là $S[2]$.
- **Hành động:** $a_t \in \{0,\dots,5\}$ ↔ thể tích $\{0,5,10,15,20,25\}$ L.
- **Episode:** 30 bước (1 bước = 1 ngày); dừng khi `terminated` (stress $K=3$ ngày liên tiếp) hoặc `truncated` (hết 30 ngày).
- **Rời rạc hóa dùng chung cho Q-Learning và MC:** `1 × 4 × 5 × 3 × 2 × 2 × 2 = 480` trạng thái ⇒ bảng $480 \times 6 = 2.880$ ô. (Cấu hình đầy đủ theo báo cáo là $4\times4\times5\times3\times2\times3\times3 = 4.320$ trạng thái, dùng khi mở rộng đa giống cây.)
- **Hàm reward:** `calculate_reward()` 6 thành phần — **một nguồn sự thật duy nhất** cho cả 4 chiến lược.
- **$\gamma = 0.99$**, không đổi giữa các thuật toán.
- **Ngữ nghĩa kết thúc:** chỉ bootstrap khi `truncated`; khi `terminated` thì mục tiêu $= r$ (Q-Learning/DQN), MC dùng return đầy đủ tới cuối episode.
- **Gọi ngầm UC-05:** mọi vòng lặp đều phát $(S, A, R, info)$ cho module Đánh giá hiệu suất.

---

## III.3. Thuật toán 1 — Tabular Q-Learning (Nguyễn Minh)

### III.3.1. Mã giả

```text
THUẬT TOÁN TABULAR Q-LEARNING
────────────────────────────────────────────────────────
Đầu vào:
  - env: AgriWaterEnv (7 chiều, Discrete(6))
  - α (learning rate) ∈ (0,1] ; γ = 0.99
  - ε_start = 1.0, ε_end = 0.05, decay = 0.995
  - n_episodes

Bước 1. KHỞI TẠO
  1.1. Q[s,a] ← 0 với 480 trạng thái rời rạc × 6 hành động
  1.2. ε ← ε_start

Bước 2. VỚI MỖI EPISODE (ep = 1 … n_episodes)
  2.1. S ← env.reset() ; s ← Discretize(S)
  2.2. LẶP đến khi terminated hoặc truncated:
       2.2.1. nếu rand() < ε: a ← ngẫu nhiên ∈ {0..5}      (khám phá)
              ngược lại:      a ← argmax_a Q[s,a]          (khai thác)
       2.2.2. S', r, terminated, truncated, info ← env.step(a)
       2.2.3. s' ← Discretize(S')
       2.2.4. Q[s,a] ← Q[s,a] + α · [ r + γ · max_a' Q[s',a'] − Q[s,a] ]
              (nếu terminated: mục tiêu = r, KHÔNG cộng γ·max Q)
       2.2.5. s ← s'
  2.3. ε ← max(ε_end, ε · decay)

Bước 3. TRẢ VỀ Q  →  π(s) = argmax_a Q[s,a]
────────────────────────────────────────────────────────
```

### III.3.2. Giải thích

- **Cập nhật TD(0)** là lõi của Q-Learning: mỗi trải nghiệm kéo $Q(s,a)$ về mục tiêu $r + \gamma \max_{a'} Q(s',a')$; sai số $\delta_t$ là tín hiệu học.
- **Off-policy:** hành vi $\varepsilon$-greedy nhưng mục tiêu luôn dùng $\max$, nên agent học giá trị của chính sách tham lam trong khi vẫn khám phá — phù hợp với mưa ngẫu nhiên trong môi trường.
- **Rời rạc hóa 480 trạng thái:** `crop_type` cố định theo kịch bản (không chia khoảng) để bảng không bùng nổ; các biến còn lại chia 2–5 nấc, khớp các ngưỡng reward (0.20 / 0.40 / 0.70 / 0.85).
- **Không bootstrap khi `terminated`:** cây chết là trạng thái hấp thụ thật; nếu bootstrap, agent sẽ tin "sau khi chết vẫn còn giá trị".

### III.3.3. Lý do lựa chọn

1. **Model-free, đúng bản chất môi trường** — không cần $P$, chỉ học từ $(S,A,R,S')$.
2. **Mốc đối chứng chuẩn mực, có bảo đảm hội tụ** (Watkins & Dayan, 1992) khi mọi cặp $(s,a)$ được thăm vô hạn và $\alpha$ thỏa điều kiện Robbins–Monro.
3. **Minh bạch:** in được toàn bộ bảng $Q$ để giải thích quyết định tưới, phục vụ dashboard và báo cáo.
4. **Chi phí thấp:** không GPU, hội tụ nhanh trên 2.880 ô.

---

## III.4. Thuật toán 2 — Monte Carlo Control (Nguyễn Minh)

### III.4.1. Mã giả

```text
THUẬT TOÁN MC CONTROL (on-policy, first-visit, ε-soft)
────────────────────────────────────────────────────────
Đầu vào:
  - env: AgriWaterEnv ; Discretizer dùng CHUNG với Q-Learning (480 trạng thái)
  - γ = 0.99 ; ε_start = 1.0, ε_end = 0.05, decay = 0.995
  - n_episodes

Bước 1. KHỞI TẠO
  1.1. Q[s,a] ← 0 ; N[s,a] ← 0  (480 × 6)
  1.2. ε ← ε_start

Bước 2. VỚI MỖI EPISODE (ep = 1 … n_episodes)
  2.1. S ← env.reset() ; trajectory ← []
  2.2. LẶP đến khi terminated hoặc truncated:
       2.2.1. s ← Discretize(S)
       2.2.2. a ← ε-soft(Q, s):  rand() < ε → ngẫu nhiên ; ngược lại argmax
       2.2.3. S', r, terminated, truncated, info ← env.step(a)
       2.2.4. trajectory.append((s, a, r)) ; S ← S'
  2.3. TÍNH RETURN NGƯỢC (một lượt, O(T)):
       G ← 0 ; VỚI t = T−1 … 0:  G ← γ·G + r_t ; G_t ← G
  2.4. CẬP NHẬT FIRST-VISIT (một lượt xuôi):
       visited ← ∅
       VỚI t = 0 … T−1:
           (s,a) ← trajectory[t]
           nếu (s,a) ∉ visited:
               visited.add((s,a))
               N[s,a] ← N[s,a] + 1
               Q[s,a] ← Q[s,a] + (G_t − Q[s,a]) / N[s,a]
  2.5. ε ← max(ε_end, ε · decay)

Bước 3. TRẢ VỀ Q  →  π(s) = argmax_a Q[s,a]  (ε = 0 khi đánh giá)
────────────────────────────────────────────────────────
```

> **Dễ sai:** nếu quét **ngược** rồi cập nhật ngay tại lần gặp đầu tiên, ta được **last-visit MC**, không phải first-visit. Vì vậy phải tách 2 lượt như bước 2.3 và 2.4.

### III.4.2. Siêu tham số

| Siêu tham số | Giá trị | Ghi chú |
|---|---|---|
| $\gamma$ | 0.99 | Kế thừa MDP |
| $\varepsilon$ | $1.0 \to 0.05$, decay 0.995/episode | Bảo đảm $\varepsilon$-soft: mọi hành động có xác suất $\ge 0.05/6$ |
| `n_episodes` | 20.000 (≈ 600k bước) | Cùng ngân sách bước với Q-Learning để so sánh công bằng |
| Ước lượng $Q$ | Trung bình cộng tăng dần theo $N(s,a)$ | Biến thể constant-$\alpha = 0.05$ làm thí nghiệm phụ |
| Kiểu cập nhật | First-visit | Every-visit chỉ dùng để đối chiếu phương sai |

### III.4.3. Giải thích

- **Vì sao MC chạy được:** bài toán episodic (30 bước, có `terminated`/`truncated`) nên $G_t$ xác định được ở cuối episode — đúng điều kiện áp dụng MC.
- **Không bootstrap:** $G_t$ là return thực quan sát được ⇒ **không bias**, nhưng **phương sai cao** vì phụ thuộc toàn bộ đuôi episode.
- **$\varepsilon$-soft thay cho exploring starts:** không thể ép môi trường bắt đầu ở trạng thái tùy ý (mưa/nhiệt độ do kịch bản quyết định), nên dùng chính sách mềm bảo đảm mọi hành động đều có xác suất dương.
- **Đối chiếu với Q-Learning:** cùng 480 trạng thái, cùng reward, cùng $\gamma$, chỉ khác **cách ước lượng giá trị** (return đầy đủ ↔ một bước TD).

### III.4.4. Lý do lựa chọn

1. **Lấp nhánh kiến thức MC của môn**, vốn chưa có thuật toán nào trong dự án.
2. **Giữ nguyên giả định model-free** — không cần dựng $\hat P$ như DP.
3. **Chi phí thấp:** 1 file, dùng lại `Discretizer` và `AgentInterface` sẵn có.
4. **Giá trị học thuật:** cho phép đo trực tiếp **bias ↔ variance**, **học theo episode ↔ học theo bước**, **sample efficiency** — đúng các tiêu chí C5.

### III.4.5. Rủi ro và biện pháp

| Rủi ro | Nguyên nhân | Biện pháp |
|---|---|---|
| Đường cong "răng cưa" | $G_t$ phụ thuộc đuôi episode | Trung bình trượt 50 episode; ≥ 10 seed |
| Hội tụ chậm hơn Q-Learning | Không bootstrap ⇒ mỗi episode chỉ cập nhật các cặp đã thăm | Ngân sách 20.000 episode; **đây là phát hiện của báo cáo, không phải lỗi** |
| Nhiều ô $Q=0$ do chưa thăm | 2.880 ô, phân bố ghé thăm lệch | Báo cáo kèm bản đồ nhiệt $N(s,a)$; $\varepsilon$-soft bảo đảm phủ dần |

---

## III.5. Thuật toán 3 — DQN (Lục Văn Thuận)

### III.5.1. Mã giả

```text
THUẬT TOÁN DQN
────────────────────────────────────────────────────────
Đầu vào:
  - env: AgriWaterEnv (đầu vào liên tục 7 chiều)
  - α (optimizer Adam) ; γ = 0.99
  - ε: 1.0 → 0.05 (decay 0.995)
  - batch_size B = 64 ; buffer N = 100.000
  - C = 1.000 (cập nhật Target Network) ; total_timesteps

Bước 1. KHỞI TẠO
  1.1. Q_net      ← MLP 7 → 128 → 128 → 6 (ReLU)
  1.2. Target_net ← bản sao của Q_net
  1.3. Replay_Buffer ← rỗng, sức chứa N
  1.4. ε ← 1.0

Bước 2. VỚI MỖI BƯỚC (t = 1 … total_timesteps)
  2.1. a ← ε-greedy trên Q_net:
       rand() < ε → ngẫu nhiên ∈ {0..5} ; ngược lại argmax_a Q_net(S)[a]
  2.2. S', r, terminated, truncated, info ← env.step(a)
  2.3. Replay_Buffer.push((S, a, r, S', terminated))
  2.4. NẾU |buffer| ≥ B:
       2.4.1. lấy ngẫu nhiên B mẫu
       2.4.2. y ← r                      nếu terminated
              y ← r + γ·max_a' Target_net(S')[a']   ngược lại
       2.4.3. Loss ← mean((Q_net(S)[a] − y)²) ; Adam.step()
  2.5. NẾU t mod C == 0: Target_net ← Q_net
  2.6. ε ← max(0.05, ε · 0.995)
  2.7. Mỗi eval_every bước: chạy 1 episode greedy (ε=0) để log reward + lượng nước
       (A-1: nếu người dùng bấm "Dừng Huấn luyện" → lưu checkpoint & thoát)

Bước 3. TRẢ VỀ Q_net đã huấn luyện (checkpoint .pt)
────────────────────────────────────────────────────────
```

### III.5.2. Giải thích

- **Replay Buffer:** trải nghiệm RL có tương quan thời gian mạnh (hôm nay khô, mai khô hơn); lấy mẫu ngẫu nhiên phá tương quan và tăng sample efficiency.
- **Target Network:** nếu dùng chính $Q_{net}$ sinh mục tiêu thì mỗi cập nhật làm mục tiêu dịch chuyển (moving target); mạng đích đóng băng $C$ bước, đưa hội tụ về gần bất động điểm Bellman.
- **Không cần rời rạc hóa:** giữ nguyên độ phân giải cảm biến ở các ngưỡng 0.20/0.40/0.70/0.85 — điều mà bảng Q 480 ô làm mất.
- **Mục tiêu học:** $\text{Loss} = \mathbb{E}\big[(Q(s,a;\theta) - (r + \gamma \max_{a'} Q_{target}(s',a';\theta^-)))^2\big]$.

### III.5.3. Lý do lựa chọn

1. **Trạng thái 7 chiều liên tục:** bảng Q bùng nổ (4.320 trạng thái ở cấu hình thô, tăng theo cấp số nhân khi chia mịn hơn) ⇒ DQN là lựa chọn chủ đạo.
2. **Tổng quát hóa:** mạng học hàm $Q(s,a)$ liên tục, hoạt động được trên seed/kịch bản chưa gặp.
3. **So sánh công bằng với bảng Q** (C3, C5): cùng env, reward, $\gamma$ ⇒ mọi khác biệt do thuật toán.
4. **Hệ sinh thái PyTorch/SB3** sẵn sàng, phù hợp tiến độ nhóm.

---

## III.6. Thuật toán 4 — Baseline luật cố định (Vũ Tuấn Khanh)

### III.6.1. Mã giả

```text
BASELINE: LUẬT NGƯỠNG CỐ ĐỊNH (Fixed-threshold Policy)
────────────────────────────────────────────────────────
Tham số:  m_threshold = 0.30 ; a_irrigate = 4 (20 L)
          WATER_LEVELS = [0, 5, 10, 15, 20, 25]

Hàm chọn hành động:
  m_t ← S[2]                       (chỉ dùng soil_moisture)
  nếu m_t < 0.30:  a ← 4           (tưới 20 L)
  ngược lại:       a ← 0           (không tưới)

Chạy một episode (UC-03, luồng con A-1):
  S ← env.reset()
  LẶP đến khi terminated hoặc truncated:
      a ← QuyTắc(S)
      S, r, terminated, truncated, info ← env.step(a)
      └─ Ghi nhận: total_reward, total_water, stress_count, ideal_count
  ideal_ratio ← ideal_count / số bước
────────────────────────────────────────────────────────
```

### III.6.2. Giải thích

- Chính sách **tất định**, không học, không khám phá: cùng độ ẩm ⇒ cùng hành động.
- Chỉ dùng **1/7** thành phần trạng thái (`soil_moisture`), bỏ qua loại cây, giai đoạn sinh trưởng, nhiệt độ, dự báo mưa và lịch sử tưới — đây chính là "khoảng trống" mà các thuật toán RL cần chứng minh khai thác được.
- Ngưỡng 0.30 và mức 20 L được chọn theo thực tế hệ thống tưới cảm biến đơn giản.

### III.6.3. Lý do lựa chọn

1. **Bắt buộc theo C4** — không có baseline thì mọi biểu đồ reward đều vô nghĩa.
2. **Sanity check cho reward:** nếu RL không thắng nổi if-else thì lỗi nằm ở reward/siêu tham số, phát hiện sớm.
3. **Chi phí bằng không:** chạy tức thì, dùng kiểm thử env và logger ngay từ tuần đầu.
4. **Phản ánh thực tế canh tác:** mô phỏng đúng hệ thống tưới ngưỡng truyền thống.

---

## III.7. Bảng so sánh tổng hợp 4 chiến lược

| Tiêu chí (C5) | Q-Learning | MC Control | DQN | Baseline |
|---|---|---|---|---|
| Loại | Off-policy TD(0) | On-policy first-visit | Value-based + xấp xỉ hàm | Không học |
| Đại diện chính sách | Bảng $480\times6$ | Bảng $480\times6$ + $N(s,a)$ | $Q(s,a;\theta)$, MLP 7→128→128→6 | 2 nhánh if-else |
| Đầu vào trạng thái | Rời rạc hóa 480 | Rời rạc hóa 480 | Liên tục 7 chiều | Chỉ $S[2]$ |
| Cập nhật | Mỗi bước (bootstrap) | Cuối episode (return đầy đủ) | Mỗi bước, học theo batch | Không |
| Hội tụ | Nhanh, ổn định | Chậm hơn, phương sai cao | Chậm, cần replay + target | Không huấn luyện |
| Sample efficiency | Cao | Thấp | Trung bình | Không dùng mẫu |
| Mở rộng không gian S | Kém | Kém | Mạnh | Trung bình |
| Chi phí tính toán | Thấp | Thấp | Cần GPU/CPU mạnh hơn | Bằng không |
| Vai trò trong báo cáo | Mốc dạng bảng | Đối chiếu bias–variance | Thuật toán chủ đạo | Mốc cần vượt qua |

---

## III.8. Kế hoạch triển khai

### III.8.1. Ánh xạ mã giả → module code & use case

| Nội dung | File code dự kiến | Use case | Người phụ trách |
|---|---|---|---|
| `AgriWaterEnv` (7D/6A/30 ngày) | `agriwater/env/agriwater_env.py` | UC-01, UC-05 | Nguyễn Thế Trưởng |
| `WeatherModel` + 3 kịch bản JSON | `agriwater/env/weather_model.py`, `scenarios/*.json` | UC-03 | Nguyễn Thế Trưởng |
| `calculate_reward()` 6 thành phần | `agriwater/env/reward.py` | FR-ENV-5 | Nguyễn Thị Phương Thảo (review) |
| `Discretizer` (480 trạng thái) | `agriwater/agents/discretizer.py` | — | Nguyễn Minh |
| Q-Learning | `agriwater/agents/q_learning.py` | UC-02 | Nguyễn Minh |
| **MC Control** | `agriwater/agents/mc_control.py` | UC-02 | Nguyễn Minh |
| DQN | `agriwater/agents/dqn.py` | UC-02 | Lục Văn Thuận |
| Baseline | `agriwater/agents/rule_based.py` | UC-03 (A-1) | Vũ Tuấn Khanh |
| Đăng ký thuật toán | `agriwater/agents/registry.py` | UC-02/UC-03 | Nguyễn Minh |
| Log $(S,A,R)$ → metric | `agriwater/eval/metrics_logger.py` | UC-05 | Lục Văn Thuận |
| Huấn luyện & checkpoint | `agriwater/train.py` | UC-02 (A-1) | Nguyễn Minh, Lục Văn Thuận |
| Chạy đa kịch bản, đa seed | `agriwater/evaluate.py` | UC-03, UC-04 | Lục Văn Thuận |

### III.8.2. Giao diện chung (pipeline cắm – chạy)

```text
class Agent:
    def act(self, state) -> action
    def learn(self, transition)      # transition = (S, a, r, S', terminated, truncated)
    def save(self, path) / load(self, path)
```

Nhờ interface này, `train.py`/`evaluate.py` không cần biết thuật toán bên trong: `agent = REGISTRY[name](...)`.

### III.8.3. Lộ trình tuần

| Tuần | Công việc | Đầu ra | Người phụ trách |
|---|---|---|---|
| 1–2 | `calculate_reward` + 5 test; `AgriWaterEnv` 7D/6A; 3 kịch bản JSON | Env vượt `check_env`, reward khớp $+6/+10/-124/-4/-10$ | Trưởng, Thảo |
| 3 | `Discretizer` 480 trạng thái; Baseline; smoke pipeline + logger | CSV đọc được, baseline chạy | Minh, Khanh |
| 4 | Q-Learning và MC Control trên cùng bộ bảng | Cả hai reward trung bình > baseline | Minh |
| 5–6 | DQN (replay, target network); tinh chỉnh $\alpha$, batch, $\varepsilon$ | DQN hội tụ, loss giảm | Thuận |
| 7 | Chạy 3 kịch bản × 10 seed × 4 chiến lược | Bảng số liệu C5 | Thuận, Minh |
| 8 | Biểu đồ, bảng so sánh, báo cáo, slide | Báo cáo + slide 12 trang | Cả nhóm |

### III.8.4. Tiêu chí nghiệm thu

- **Baseline:** chạy không huấn luyện, là mốc 0 trong mọi biểu đồ.
- **Q-Learning:** reward trung bình/episode (greedy, $\varepsilon=0$, 10 seed) **> baseline ≥ 10%**; số lần stress giảm ≥ 50% so với baseline.
- **MC Control:** reward trung bình **> baseline ≥ 10%**; stress giảm ≥ 30% (MC phương sai cao hơn nên đặt ngưỡng thấp hơn — kỳ vọng định lượng, không phải hạ tiêu chuẩn); $\varepsilon$ về 0.05 đúng lịch.
- **DQN:** vượt Q-Learning trên kịch bản/seed mới (khả năng khái quát); loss hội tụ.
- **Cả 4:** cùng `γ = 0.99`, cùng `calculate_reward`, cùng tập kịch bản ⇒ so sánh công bằng (C5, C6).

---

*Kết thúc mục III — mã giả các thuật toán dự kiến sử dụng (bộ 4 chiến lược, đồng bộ docx V2).*
