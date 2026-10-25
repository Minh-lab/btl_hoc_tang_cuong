# III. MÃ GIẢ CÁC THUẬT TOÁN DỰ KIẾN SỬ DỤNG

> **Dự án:** AgriWater-RL — Hệ thống ra quyết định tưới tiêu tự động tối ưu hóa nguồn nước trong nông nghiệp.
> **Hướng dẫn sử dụng:** Đây là **bố cục mẫu** để các thành viên điền nội dung. Các mục có đánh dấu `[ĐIỀN...]` là phần cần hoàn thành. Giữ nguyên thứ tự tiêu đề, không đổi tên thuật toán.
> Căn cứ: docx V2 — trạng thái **7 chiều**, **6 mức tưới** $\{0,5,10,15,20,25\}$ L, reward **6 thành phần**, episode **30 ngày**, $\gamma = 0.99$.
>
> | Phần | Thuật toán | Người điền nội dung | Deadline |
> |---|---|---|---|
> | III.1 | Tổng quan & lý do chọn bộ thuật toán | Nguyễn Thị Phương Thảo | ... |
> | III.2 | Quy ước chung | Nguyễn Thị Phương Thảo | ... |
> | III.3 | Q-Learning | Nguyễn Minh | ... |
> | III.4 | Monte Carlo Control | Nguyễn Minh | ... |
> | III.5 | DQN | Lục Văn Thuận | ... |
> | III.6 | Baseline (Rule-based) | Vũ Tuấn Khanh | ... |
> | III.7 | Bảng so sánh tổng hợp | Cả nhóm (Thảo tổng hợp) | ... |
> | III.8 | Kế hoạch triển khai | Cả nhóm (Thuận tổng hợp) | ... |

---

## III.1. Tổng quan bộ thuật toán và lý do lựa chọn

### III.1.1. Đặc điểm bài toán ảnh hưởng đến lựa chọn thuật toán

*Bảng bắt buộc: liên kết đặc điểm MDP (đã mô hình hóa) → hệ quả đối với việc chọn thuật toán.*

| Đặc điểm bài toán | Hệ quả đối với lựa chọn thuật toán |
|---|---|
| Không gian hành động rời rạc $\lvert A \rvert = 6$ ($\{0,5,\dots,25\}$ L) | `[ĐIỀN]` |
| Trạng thái 7 chiều (2 rời rạc + 5 liên tục) | `[ĐIỀN]` |
| Môi trường Model-free (không có trước ma trận $P$) | `[ĐIỀN]` |
| Bài toán episodic: `terminated` (cây chết) / `truncated` (30 ngày) | `[ĐIỀN]` |
| $\gamma = 0.99$, phần thưởng dài hạn | `[ĐIỀN]` |
| Hàm phần thưởng phạt nặng vùng nguy hiểm ($-100$) | `[ĐIỀN]` |
| Luật môn: C3 (≥ 2 RL), C4 (baseline), C8 (≤ 3 thuật toán) | `[ĐIỀN]` |

### III.1.2. Danh sách bộ thuật toán dự kiến cài đặt

| # | Thuật toán | Loại | Vai trò trong dự án | Người phụ trách code |
|---|---|---|---|---|
| 1 | Q-Learning | RL — off-policy TD(0), bảng Q | Thuật toán RL 1 | Nguyễn Minh |
| 2 | Monte Carlo Control | RL — on-policy, first-visit | Thuật toán RL 2 | Nguyễn Minh |
| 3 | DQN | RL — mạng nơ-ron | Thuật toán RL 3 | Lục Văn Thuận |
| 4 | Baseline (Rule-based) | Không học — luật cố định | Chiến lược cơ sở để so sánh | Vũ Tuấn Khanh |

**Lời dẫn chung.** Từ bảng phân tích ở III.1.1, nhóm chọn bộ trên: **Q-Learning** đại diện RL dạng bảng (minh bạch, có bảo đảm hội tụ), **Monte Carlo Control** đại diện nhóm học từ return đầy đủ (đối chiếu bias–variance với TD), **DQN** đại diện RL dùng xấp xỉ hàm (xử lý trạng thái 7 chiều liên tục), và **Baseline luật cố định** làm đường tham chiếu không học. Bộ này đáp ứng đồng thời **C3** (≥ 2 thuật toán RL), **C4** (có baseline) và **C8** (3 thuật toán RL + 1 chiến lược cơ sở).

Bốn thuật toán dưới đây cùng đi theo **một bố cục chung**, gồm 3 mục con:

| Mục con | Nội dung |
|---|---|
| `.1. Mã giả (Pseudocode)` | Mã giả dạng thuật toán đánh số bước (không phải code Python thật) |
| `.2. Giải thích mã giả` | Giải thích các bước/thành phần quan trọng |
| `.3. Lý do lựa chọn` | Lý do chọn thuật toán cho bài toán tưới tiêu, gắn với MDP và luật môn học |

Thứ tự trình bày: **Q-Learning → Monte Carlo → DQN → Baseline** (từ bảng đơn giản đến mạng nơ-ron, khép lại bằng thước đo đối chiếu).

---

## III.2. Quy ước chung cho cả 4 mã giả

*Điền các quy ước mà cả 4 thuật toán phải tuân thủ.*

- Vector trạng thái 7 chiều, mọi chiều chuẩn hóa $[0,1]$; `soil_moisture = S[2]`: `[ĐIỀN...]`
- Episode 30 bước (1 bước = 1 ngày); `terminated` khi stress $K=3$ ngày liên tiếp, `truncated` khi hết 30 ngày: `[ĐIỀN...]`
- Rời rạc hóa dùng chung cho Q-Learning và MC: `1×4×5×3×2×2×2 = 480` trạng thái × 6 hành động: `[ĐIỀN...]`
- $\gamma = 0.99$, dùng chung `calculate_reward()`: `[ĐIỀN...]`
- Ngữ nghĩa bootstrap: chỉ bootstrap khi `truncated`, không bootstrap khi `terminated`: `[ĐIỀN...]`

---

## III.3. Thuật toán 1 — Q-Learning (Nguyễn Minh)

### III.3.1. Mã giả (Pseudocode)

*Điền mã giả Q-Learning dạng thuật toán đánh số bước.*

```text
[ĐIỀN: mã giả Q-Learning]
```

### III.3.2. Giải thích mã giả

*Giải thích: cập nhật TD(0), $\varepsilon$-greedy + decay, cách rời rạc hóa 7 chiều về 480 trạng thái, vì sao không bootstrap khi cây chết.*

- `[ĐIỀN...]`

### III.3.3. Lý do lựa chọn cho bài toán của nhóm

1. `[ĐIỀN: model-free, không cần P]`
2. `[ĐIỀN: có bảo đảm hội tụ (Watkins & Dayan 1992)]`
3. `[ĐIỀN: minh bạch — in được bảng Q 480×6 để giải thích quyết định]`
4. `[ĐIỀN: chi phí thấp, làm mốc đối chứng cho DQN]`

---

## III.4. Thuật toán 2 — Monte Carlo Control (Nguyễn Minh)

### III.4.1. Mã giả (Pseudocode)

*Điền mã giả MC Control: chạy trọn episode, tính $G_t$ ngược, cập nhật first-visit, $\varepsilon$-soft.*

```text
[ĐIỀN: mã giả MC Control]
```

### III.4.2. Giải thích mã giả

*Giải thích: vì sao cần episode kết thúc, vì sao dùng $\varepsilon$-soft thay exploring starts, phân biệt first-visit và last-visit.*

- `[ĐIỀN...]`

### III.4.3. Lý do lựa chọn cho bài toán của nhóm

1. `[ĐIỀN: lấp nhánh kiến thức Monte Carlo của môn]`
2. `[ĐIỀN: giữ giả định model-free, dùng lại bộ rời rạc hóa của Q-Learning]`
3. `[ĐIỀN: đối chiếu bias–variance với TD(0) — tiêu chí C5]`
4. `[ĐIỀN: chi phí thấp, 1 file + 1 dòng đăng ký]`

---

## III.5. Thuật toán 3 — DQN (Lục Văn Thuận)

### III.5.1. Mã giả (Pseudocode)

*Điền mã giả DQN: mạng 7→128→128→6, Replay Buffer, Target Network, hàm loss.*

```text
[ĐIỀN: mã giả DQN]
```

### III.5.2. Giải thích mã giả

*Giải thích vai trò: (1) Replay Buffer, (2) Target Network, (3) loss MSE, (4) vì sao DQN xử lý được trạng thái 7 chiều liên tục.*

- `[ĐIỀN...]`

### III.5.3. Lý do lựa chọn cho bài toán của nhóm

1. `[ĐIỀN: trạng thái 7 chiều liên tục — bảng Q bùng nổ (4.320 trạng thái)]`
2. `[ĐIỀN: giữ nguyên độ phân giải cảm biến ở các ngưỡng 0.20/0.40/0.70/0.85]`
3. `[ĐIỀN: so sánh công bằng với Q-Learning/MC (cùng env, reward, γ)]`
4. `[ĐIỀN: khả năng khái quát sang seed/kịch bản mới]`

---

## III.6. Baseline — Luật ngưỡng cố định (Vũ Tuấn Khanh)

### III.6.1. Mã giả (Pseudocode)

*Điền mã giả dạng if-else: $m<0.30$ ⇒ tưới 20 L (action 4); ngược lại không tưới.*

```text
[ĐIỀN: mã giả Baseline]
```

### III.6.2. Giải thích mã giả

*Giải thích ngưỡng 0.30 và mức 20 L được chọn từ thực tế hệ thống tưới cảm biến; baseline chỉ dùng 1/7 thành phần trạng thái.*

- `[ĐIỀN...]`

### III.6.3. Lý do lựa chọn Baseline

1. `[ĐIỀN: bắt buộc theo C4 — mốc so sánh]`
2. `[ĐIỀN: sanity check cho hàm reward và siêu tham số]`
3. `[ĐIỀN: chi phí bằng không, dùng kiểm thử env/logger từ tuần đầu]`
4. `[ĐIỀN: phản ánh thực tế canh tác]`

---

## III.7. Bảng so sánh tổng hợp 4 chiến lược

*Các thành viên điền cột của mình; Thảo tổng hợp cuối cùng.*

| Tiêu chí | Q-Learning | MC Control | DQN | Baseline |
|---|---|---|---|---|
| Đại diện chính sách | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |
| Xử lý trạng thái đầu vào | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |
| Cập nhật (theo bước / theo episode) | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |
| Tốc độ hội tụ | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |
| Sample efficiency | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |
| Ưu điểm chính | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |
| Nhược điểm chính | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |
| Vai trò trong báo cáo | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` | `[ĐIỀN]` |

---

## III.8. Kế hoạch triển khai nội dung mã giả

### III.8.1. Ánh xạ mã giả → Use Case → Người phụ trách

| Mã giả | Use Case liên quan | Người phụ trách |
|---|---|---|
| Q-Learning | UC-02 (Huấn luyện) | Nguyễn Minh |
| MC Control | UC-02 (Huấn luyện) | Nguyễn Minh |
| DQN | UC-02 (Huấn luyện) | Lục Văn Thuận |
| Baseline | UC-03 (Thử nghiệm, luồng con A-1) | Vũ Tuấn Khanh |
| Môi trường `AgriWaterEnv` (7D/6A, dùng chung) | UC-01, UC-05 | Nguyễn Thế Trưởng |
| Reward 6 thành phần | FR-ENV-5 | Nguyễn Thị Phương Thảo (review) |

### III.8.2. Tiêu chí nghiệm thu cho từng thuật toán

*Điền tiêu chí đo lường được (đúng luật C5: reward, convergence, stability, sample efficiency, thời gian train).*

- **Q-Learning:** `[ĐIỀN — ví dụ: reward > baseline ≥ 10%; stress giảm ≥ 50%]`
- **MC Control:** `[ĐIỀN — ví dụ: reward > baseline ≥ 10%; stress giảm ≥ 30%; ε → 0.05 đúng lịch]`
- **DQN:** `[ĐIỀN — ví dụ: vượt Q-Learning trên seed mới; loss hội tụ]`
- **Baseline:** `[ĐIỀN — không huấn luyện, là mốc 0 trong mọi biểu đồ]`

### III.8.3. Lộ trình theo tuần

| Tuần | Công việc | Người phụ trách |
|---|---|---|
| 1–2 | Reward + môi trường 7D/6A + 3 kịch bản JSON | Trưởng, Thảo |
| 3 | `Discretizer` 480 trạng thái + Baseline + logger | Minh, Khanh |
| 4 | Q-Learning + MC Control | Minh |
| 5–6 | DQN + tinh chỉnh siêu tham số | Thuận |
| 7 | 3 kịch bản × 10 seed × 4 chiến lược | Thuận, Minh |
| 8 | Biểu đồ, báo cáo, slide | Cả nhóm |

---

## Checklist tự kiểm tra trước khi nộp (Mục 10 — requirements.md)

- [ ] Đủ 4 chiến lược: Q-Learning, Monte Carlo Control, DQN, Baseline (C3, C4, C8)
- [ ] Mỗi thuật toán có đủ 3 mục: Mã giả → Giải thích → Lý do lựa chọn
- [ ] Mã giả không phải code Python thật (viết dạng thuật toán đánh số bước)
- [ ] Công thức toán viết bằng LaTeX ($...$)
- [ ] Bảng dùng Markdown table
- [ ] Gắn với MDP đã mô hình hóa (S 7 chiều, A 6 mức, $\gamma=0.99$, R 6 thành phần) — không mâu thuẫn
- [ ] Tên thành viên viết đúng chính tả, thống nhất với danh sách nhóm
