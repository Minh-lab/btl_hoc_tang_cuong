# KỊCH BẢN SLIDE — AGRIWATER-RL (12 SLIDE)

> **Đồng bộ theo docx V2:** trạng thái 7 chiều, 6 mức tưới, reward 6 thành phần, episode 30 ngày, 3 kịch bản, bộ **4 chiến lược** (Q-Learning, Monte Carlo Control, DQN, Baseline).
> Bố cục: 1 slide mở đầu + 10 slide nội dung + 1 slide Q&A (đúng yêu cầu 10–12 slide).

### Slide 1: Trang bìa
- Trường Đại học Thủy Lợi — Khoa Công nghệ Thông tin.
- Đề tài: **AgriWater-RL — Hệ thống ra quyết định tưới tiêu tự động tối ưu hóa nguồn nước**.
- Nhóm 10 — 5 thành viên.
- Giảng viên: Lê Nguyễn Tuấn Thành.

**Ghi chú thuyết trình:** Chào thầy và các bạn. Nhóm 10 xin trình bày đề tài ứng dụng Học tăng cường vào bài toán tối ưu hóa hệ thống tưới tiêu tự động.
**Gợi ý hình ảnh:** logo trường, ảnh nông trại công nghệ cao.

---

### Slide 2: Đặt vấn đề & mục tiêu
- Nông nghiệp tiêu tốn lượng nước khổng lồ.
- Hệ thống tưới hiện tại quá cứng nhắc: hẹn giờ cố định hoặc ngưỡng cảm biến tĩnh.
- Không xét dài hạn, không linh hoạt theo thời tiết ⇒ lãng phí nước hoặc giảm năng suất.
- Mục tiêu: cân bằng **tiết kiệm nước tối đa** và **cây sinh trưởng lý tưởng**.

**Ghi chú thuyết trình:** Câu hỏi trung tâm là "tưới lúc nào và bao nhiêu?". Đây là bài toán chuỗi quyết định, phù hợp với Học tăng cường chứ không phải học có giám sát.
**Gợi ý hình ảnh:** ruộng khô hạn đối lập vòi nước xả lãng phí.

---

### Slide 3: Công nghệ & 6 tính năng
- Gymnasium (môi trường RL), Python, PyTorch, Stable Baselines3.
- Trực quan hóa: Streamlit, Matplotlib.
- 6 tính năng: (1) mô phỏng nông nghiệp, (2) tích hợp đa thuật toán, (3) thử nghiệm đa kịch bản, (4) so sánh chiến lược, (5) đánh giá hiệu suất, (6) báo cáo & dashboard.

**Ghi chú thuyết trình:** 6 tính năng phủ đủ 4 động từ của môn: tích hợp, thử nghiệm, so sánh, đánh giá.
**Gợi ý hình ảnh:** logo Python/Gymnasium/PyTorch/Streamlit + vòng tròn 6 bước.

---

### Slide 4: Kiến trúc 4 lớp
- **Presentation:** Streamlit dashboard.
- **Application:** Experiment Manager, Comparator, Report Generator.
- **RL & Simulation:** `AgriWaterEnv` (7 chiều, 6 hành động) + Agents.
- **Data & Storage:** Q-Table, Replay Buffer, Checkpoints, Logs, Configs.

**Ghi chú thuyết trình:** Ranh giới ổn định duy nhất giữa các lớp là API `reset/step` của Gymnasium; nhờ đó thêm thuật toán mới chỉ cần thêm một file trong `agents/` và một dòng đăng ký.
**Gợi ý hình ảnh:** sơ đồ 4 lớp xếp chồng + vòng lặp Agent ↔ Environment.

---

### Slide 5: MDP — Trạng thái S (7 chiều)
$$S_t = (\text{crop\_type}, \text{growth\_stage}, \text{soil\_moisture}, \text{temperature}, \text{rain\_probability}, \text{rain\_forecast\_mm}, \text{last\_irrigation})$$
- 2 biến rời rạc (loại cây, giai đoạn sinh trưởng) + 5 biến liên tục, chuẩn hóa $[0,1]$.
- `last_irrigation` là "bộ nhớ ngắn hạn" cho hiện tượng trễ thẩm thấu ⇒ giữ tính Markov.
- Quy mô: $4\times4\times5\times3\times2\times3\times3 = 4.320$ trạng thái rời rạc (cấu hình đầy đủ).

**Ghi chú thuyết trình:** Điểm khác biệt so với thiết kế ban đầu là trạng thái mở rộng từ 3 lên 7 chiều, cho phép agent phân biệt nhu cầu nước theo loại cây và giai đoạn sinh trưởng.
**Gợi ý hình ảnh:** vector 7 ô, mỗi ô một icon (cây, giai đoạn, giọt nước, nhiệt kế, mây mưa, thước đo, đồng hồ).

---

### Slide 6: MDP — Hành động A (6 mức tưới)
| Action | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Nước (L) | 0 | 5 | 10 | 15 | 20 | 25 |

- Rời rạc hữu hạn, $\lvert A \rvert = 6$ (bơm 25 L/phút).
- Chính sách: $\pi(a\mid s) = \mathbb{P}(A_t = a \mid S_t = s)$.
- Mở rộng từ 3 lên 6 mức giúp điều chỉnh liều lượng mịn hơn.

**Ghi chú thuyết trình:** Với 6 mức, agent có thể "tưới nhích" thay vì chỉ bật/tắt, giảm cả tưới thừa và tưới thiếu.
**Gợi ý hình ảnh:** 6 vòi nước với lưu lượng tăng dần.

---

### Slide 7: MDP — Xác suất chuyển trạng thái P
- Hệ thống **model-free**: $P(s'\mid s,a)$ **không** được cấp cho agent.
- Môi trường Gymnasium là hộp đen: nhận $a$, trả $(r, s')$ theo cân bằng nước tầng rễ.
- Lý do: thực tiễn (không ai biết trước xác suất mưa chính xác) và học thuật (môn định hướng model-free).
- Hệ quả: chọn thuật toán học từ trải nghiệm; loại Dynamic Programming.

**Ghi chú thuyết trình:** Chính vì P không cho trước nên nhóm không dùng Quy hoạch động mà chọn Q-Learning, Monte Carlo và DQN.
**Gợi ý hình ảnh:** hộp đen với mũi tên vào (action) và ra (reward, state).

---

### Slide 8: MDP — Hàm phần thưởng R (6 thành phần)
$$R = \underbrace{+10}_{\text{lý tưởng}} - \underbrace{100}_{\text{stress}} - \underbrace{2a}_{\text{nước}} - \underbrace{10a}_{\text{lãng phí}} - \underbrace{5a}_{\text{mưa}} - \underbrace{8a}_{\text{dồn dập}}$$
- Lý tưởng: $[0.40, 0.70]$; giai đoạn ra hoa: $[0.50, 0.75]$.
- Stress: $m<0.20$ hoặc $m>0.85$ ⇒ $-100$ (Safe RL).
- $R_{\text{rain}}$: dự báo mưa $\ge 70\%$ và $\ge 15$ mm ⇒ phạt tưới.
- $R_{\text{delay}}$: đợt trước tưới $\ge 12{,}5$ L ⇒ phạt tưới dồn dập.

**Ghi chú thuyết trình:** Hai thành phần mới $R_{\text{rain}}$ và $R_{\text{delay}}$ biến các biến dự báo thành hành vi thực: hoãn tưới khi sắp mưa, giãn cách các lần tưới. Nhóm kiểm chứng bằng 5 tình huống mẫu (+6, +10, −124, −4, −10).
**Gợi ý hình ảnh:** bảng 6 trọng số + 5 tình huống mẫu.

---

### Slide 9: MDP — Hệ số chiết khấu & mục tiêu
- $\gamma = 0.99$; sau 10 ngày phần thưởng còn $(0.99)^{10} \approx 90.4\%$ giá trị.
- $\gamma \to 0$: agent "không tưới" để né phạt nước ⇒ cây chết, nhận $-100$.
- Mục tiêu: $\pi^* = \arg\max_\pi \mathbb{E}\big[\sum_t \gamma^t R_{t+1}\big]$.

**Ghi chú thuyết trình:** Gamma gần 1 buộc agent đánh đổi một lượng nước nhỏ hôm nay để giữ ẩm bền vững suốt 30 ngày của vụ.
**Gợi ý hình ảnh:** đồ thị $(0.99)^k$ giảm dần + công thức mục tiêu đóng khung.

---

### Slide 10: Bộ 4 chiến lược & điểm khác biệt cốt lõi
| # | Chiến lược | Loại | Vai trò |
|---|---|---|---|
| 1 | Tabular Q-Learning | Off-policy TD(0) | Mốc dạng bảng |
| 2 | **Monte Carlo Control** | On-policy, first-visit | Đối chiếu bias–variance |
| 3 | DQN | Xấp xỉ hàm (7→128→128→6) | Thuật toán chủ đạo |
| 4 | Baseline luật cố định | Không học | Mốc so sánh (C4) |

- ⇒ **3 thuật toán RL + 1 baseline** (thỏa C3, C4, C8).
- MC ↔ TD: MC đợi hết episode mới cập nhật (không bias, phương sai cao); Q-Learning cập nhật từng bước (bootstrap, hội tụ nhanh).

**Ghi chú thuyết trình:** Việc thêm Monte Carlo xuất phát từ chính câu trong báo cáo — "MC phải đợi kết thúc cả episode" — nhóm muốn chứng minh bằng thực nghiệm thay vì chỉ nêu lý thuyết.
**Gợi ý hình ảnh:** 2 cột đối lập MC (cả episode) ↔ TD (từng bước).

---

### Slide 11: Đánh giá, phân công & tiến độ
- Metric: reward tích lũy, tổng nước (L), số lần stress, ideal ratio, thời gian hội tụ, độ ổn định (10 seed).
- 3 kịch bản: khô hạn (35–42 °C, mưa 5%), mưa bão (mưa 50–80%), ngẫu nhiên.
- Phân công: Thảo (phân rã chức năng, trạng thái S, điều phối) · Minh (use case, reward R, Q-Learning + MC) · Trưởng (kiến trúc, P, môi trường) · Thuận (γ & mục tiêu, DQN, đánh giá) · Khanh (Baseline).
- Tiến độ: tuần 1–2 môi trường, tuần 3 baseline + Discretizer, tuần 4 Q-Learning & MC, tuần 5–6 DQN, tuần 7 đa seed, tuần 8 báo cáo.

**Ghi chú thuyết trình:** Mọi so sánh dùng chung môi trường, chung hàm reward, chung γ và chung 10 seed nên khác biệt chỉ do thuật toán.
**Gợi ý hình ảnh:** timeline 8 tuần + bảng metric.

---

### Slide 12: Q&A
- Cảm ơn sự lắng nghe.
- Mời thầy cô và các bạn đặt câu hỏi, góp ý.
- Nhóm 10 xin giải đáp.

**Ghi chú thuyết trình:** Cảm ơn thầy và các bạn. Nhóm sẵn sàng giải thích chi tiết mã giả, hàm reward và cách đảm bảo so sánh công bằng giữa 4 chiến lược.
**Gợi ý hình ảnh:** dòng chữ "Q&A" + thông tin liên hệ nhóm.
