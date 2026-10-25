# KẾ HOẠCH NGẮN — THÊM 1 THUẬT TOÁN MONTE CARLO + TRIỂN KHAI MÔI TRƯỜNG

> **Căn cứ:** `docs/HocTangCuongN10_HoanChinh.docx` (bản V2), luật môn tại `docs/requirements.md`.
> **Lưu ý:** bản docx V2 đã nâng bài toán lên **trạng thái 7 chiều / 6 hành động / reward 6 thành phần**, nên kế hoạch dài trước đây (dựa trên bản 3 chiều / 3 hành động) đã được gỡ khỏi kho tài liệu; tài liệu này là bản kế hoạch duy nhất còn hiệu lực.

---

## 1. Hiện trạng và khoảng trống

| Hạng mục | Trong docx V2 | Khoảng trống |
|---|---|---|
| MDP $(S, A, P, R, \gamma)$ | Đủ: $S$ 7 chiều, $A = \{0,5,10,15,20,25\}$ L, $P$ model-free, $R$ 6 thành phần, $\gamma = 0.99$ | — |
| Thuật toán | Q-Learning, DQN, Baseline luật cố định | **Thiếu nhóm MC** (docx chỉ *nhắc* MC để so sánh với Q-Learning) |
| Môi trường | Đặc tả: `Box(7)`, `Discrete(6)`, cân bằng nước tầng rễ, 3 kịch bản (khô / mưa bão / ngẫu nhiên 30 ngày) | **Chưa có code** — đây là điểm nghẽn của toàn bộ dự án |
| Kiểm thử, tái lập | Yêu cầu có (seed, profile) | Chưa có test nào |

---

## 2. Chọn thuật toán bổ sung: **Monte Carlo Control**

| Tiêu chí | Monte Carlo | Dynamic Programming |
|---|---|---|
| Cần biết $P$? | Không | **Có** — trái với mục 2.4 docx ("P không được cho trước", model-free) |
| Dùng lại hạ tầng có sẵn | Chỉ cần thêm 1 file, dùng chung bộ rời rạc hóa của Q-Learning | Phải dựng thêm $\hat P$ + sửa lại tuyên bố model-free |
| Giá trị cho báo cáo | Docx đã viết *"Monte Carlo phải đợi kết thúc cả episode"* — thêm MC biến câu đó thành **thí nghiệm thật**: MC ↔ TD(0) ↔ DQN | Trùng ý "quy hoạch", không có đối chứng mới |
| Công sức | ~8 h | ~14 h |

**Kết luận: chọn on-policy First-Visit MC Control ($\varepsilon$-soft).** Bỏ DP vì DP đi ngược giả định model-free mà docx đã lập luận kỹ ở mục 2.4.

---

## 3. Thiết kế MC Control

Bộ rời rạc hóa **dùng chung với Q-Learning** (để so sánh công bằng, đúng tinh thần "Tabular Q-Learning với rời rạc hóa mạnh" trong docx):

$$\lvert S_{\text{tab}} \rvert = 1_{\text{crop}} \times 4_{\text{stage}} \times 5_{\text{ẩm}} \times 3_{\text{nhiệt}} \times 2_{p_{\text{mưa}}} \times 2_{\text{mm}} \times 2_{\text{tưới}} = 480,\qquad \lvert S_{\text{tab}} \rvert \times \lvert A \rvert = 2.880$$

(`crop_type` cố định trong một kịch bản nên không cần chia khoảng — nhờ đó bảng nhỏ đi 4 lần so với con số 4.320 mà docx nêu.)

```text
MC CONTROL (on-policy, first-visit, ε-soft)
────────────────────────────────────────────
1. Q[s,a] ← 0 ; N[s,a] ← 0 ; ε ← 1.0 ; γ ← 0.99
2. LẶP mỗi episode (30 ngày):
     S ← env.reset()
     trajectory ← []
     LẶP đến terminated/truncated:
         a ← ε-soft(Q, Discretize(S))          # rand<ε → ngẫu nhiên
         S', r, te, tr, info ← env.step(a)
         trajectory.append((Discretize(S), a, r)) ; S ← S'
     # tính return ngược
     G ← 0 ; VỚI t = T-1 → 0:  G ← γ·G + rₜ ; Gₜ ← G
     # cập nhật FIRST-VISIT (quét xuôi, có tập visited)
     VỚI t = 0 → T-1 nếu (s,a) chưa gặp:
         N[s,a] += 1 ; Q[s,a] += (Gₜ − Q[s,a]) / N[s,a]
     ε ← max(0.05, 0.995·ε)
3. TRẢ VỀ Q  (đánh giá bằng π(s) = argmax Q, ε = 0)
────────────────────────────────────────────
```

| Siêu tham số | Giá trị | Ghi chú |
|---|---|---|
| $\gamma$ | 0.99 | Kế thừa MDP, không đổi |
| $\varepsilon$ | $1.0 \to 0.05$, decay 0.995/episode | Bảo đảm mọi hành động có xác suất ≥ 0.05/6 |
| `n_episodes` | 20.000 (≈ 600k bước) | Cùng ngân sách bước với Q-Learning ≥ 600k để so sánh công bằng |
| Ước lượng $Q$ | Trung bình cộng tăng dần | Biến thể constant-$\alpha$=0.05 làm thí nghiệm phụ |

**Nghiệm thu:** reward trung bình (10 seed, $\varepsilon=0$) **> baseline ≥ 10%**; số lần stress giảm ≥ 30% so với baseline; đường cong (trung bình trượt 50 episode) tăng rõ; cùng seed ⇒ cùng đường cong; bảng $Q$ in được và giải thích được bằng lời.
**Rủi ro chính:** 2.880 ô $(s,a)$ ⇒ phải kèm bản đồ nhiệt số lần thăm $N(s,a)$ trong báo cáo; hội tụ chậm hơn Q-Learning là *kết quả cần báo cáo*, không phải lỗi.

---

## 4. Kiểm tra luật C8 (tối đa 3 thuật toán)

| Chiến lược | Loại | Đếm vào C8 | Người phụ trách |
|---|---|---|---|
| Monte Carlo Control | RL, tabular | Có | Nguyễn Minh |
| Q-Learning | RL, tabular | Có | Nguyễn Minh |
| DQN | RL, học sâu | Có | Lục Văn Thuận |
| Baseline luật cố định | Không học (mốc C4) | Không | Vũ Tuấn Khanh |

⇒ **3 thuật toán RL + 1 baseline** ⇒ thỏa C3, C4, C8. MC là module cắm rời: nếu bị đếm khác, gỡ 1 dòng đăng ký là xong.

---

## 5. Triển khai môi trường (ưu tiên số 1)

| Bước | Nội dung | DoD |
|---|---|---|
| E1 | Khung dự án: `requirements.txt`, package, `scenarios/{dry,stormy,random}.json` | Import chạy, 3 kịch bản nạp được |
| E2 | `env/reward.py` — 6 thành phần: $+10$ lý tưởng (hoa/kết trái: $[0.50,0.75]$), $-100$ stress ($<0.20$ hoặc $>0.85$), $-2a$ nước, $-10a$ lãng phí ($m_t\ge0.60$), $-5a$ mưa ($p\ge0.70$, mm$\ge0.30$), $-8a$ dồn dập ($last\_irr\ge0.50$) | Khớp 5 tình huống docx: $+6$, $+10$, $-124$, $-4$, $-10$ |
| E3 | `env/weather.py` — sinh $T$, $p_{mưa}$, $mm$ theo kịch bản, qua `np_random` (không dùng `random` toàn cục) | Đổi kịch bản không phải sửa code env |
| E4 | `env/agriwater_env.py` — `Box(7)` chuẩn hóa $[0,1]$, `Discrete(6)`; cân bằng nước tầng rễ: $m_{t+1} = \operatorname{clip}(m_t + \Delta I(a) + \Delta R - ET(T, K_c) - D, 0, 1)$; cập nhật `last_irrigation`; `info` = {water_L, stress, moisture, stage} | `check_env()` pass; 30 ngày/episode; `terminated` khi cây chết, `truncated` khi hết 30 ngày |
| E5 | 5 test bắt buộc (bảng dưới) | Toàn bộ xanh |
| E6 | `render()` + smoke pipeline (agent ngẫu nhiên → CSV cho UC-05) | Có 1 file CSV đọc được |

| # | Test | Kỳ vọng |
|---|---|---|
| T1 | `gymnasium.utils.env_checker.check_env` | Pass |
| T2 | Tái lập: `reset(seed=42)` × 2, chạy 1.000 bước cùng chuỗi hành động | Mảng obs/reward/te/tr giống tuyệt đối |
| T3 | Tốc độ | ≥ 10.000 bước/giây |
| T4 | Reward 5 tình huống docx | $+6$, $+10$, $-124$, $-4$, $-10$ |
| T5 | Env không import agent; `obs` luôn trong `Box`; `info` đủ khóa | Pass |

---

## 6. Phải chốt trước khi viết `step()`

| # | Vấn đề trong docx | Quyết định đề xuất |
|---|---|---|
| a | Hai con số mâu thuẫn: "864 trạng thái" và công thức $4\times4\times5\times3\times2\times3\times3 = 4.320$ | Dùng **4.320** cho cấu hình đầy đủ, **480** cho bộ tabular dùng chung (mục 3); sửa lại một chỗ trong báo cáo |
| b | Thời lượng episode: docx nói **30 ngày**, tài liệu môi trường cũ nói 365 ngày | Theo docx: **30 ngày** |
| c | Ký hiệu $\gamma$ vừa là discount (0.99) vừa là trọng số phạt nước ($-2$); $\varepsilon$ vừa là trọng số phạt mưa ($-5$) vừa là tốc độ khám phá | Đổi tên trọng số: $c_w = -2$, $c_{\text{waste}} = -10$, $c_{\text{rain}} = -5$, $c_{\text{delay}} = -8$ |
| d | `rain_forecast_mm` ghi là mm nhưng ngưỡng trong code là `0.30` (≈ 15 mm nếu $R_{\max} = 50$ mm) | Chuẩn hóa về $[0,1]$ trong `obs`, ngưỡng 0.30 ≡ 15 mm; ghi rõ hằng số |
| e | Điều kiện `terminated` mới ghi "cây chết do khô/ngập", chưa có ngưỡng cụ thể | Chốt: stress liên tiếp $K = 3$ ngày ⇒ chết; thử $K$ trong {2,3,5} |
| f | Phân công: docx có **5 thành viên** (thêm Vũ Tuấn Khanh) nhưng `requirements.md` chốt **4 tên** | Cần nhóm xác nhận và cập nhật `requirements.md` trước; kế hoạch này giữ nguyên chủ sở hữu đang có trong docx |

---

## 7. Phân công và tiến độ

| Người | Việc trong đợt này |
|---|---|
| Nguyễn Thế Trưởng | **Triển khai môi trường** (E1–E6) — theo đúng vai trò "môi trường" đã có |
| Nguyễn Minh | **MC Control** + `Discretizer` dùng chung + tinh chỉnh Q-Learning (cùng một bộ bảng) |
| Lục Văn Thuận | DQN (giữ nguyên) + `MetricsLogger` + `evaluate.py` xuất CSV |
| Nguyễn Thị Phương Thảo | Chốt mục 6, review reward/obs, tuning siêu tham số, điều phối số liệu so sánh |
| Vũ Tuấn Khanh | Baseline (giữ nguyên) — nếu được xác nhận chính thức thì nhận thêm **MC** để cân bằng tải |

| Tuần | Việc | Cổng |
|---|---|---|
| 1 | E1–E2 + chốt mục 6 | T4 xanh (reward) — **chưa code agent khi reward chưa chốt** |
| 2 | E3–E4 | T1, T5 xanh |
| 3 | E5–E6 + `Discretizer` | T2, T3 xanh |
| 4 | MC + Q-Learning trên cùng bộ bảng, chạy 10 seed | Cả hai > baseline; xuất bảng so sánh 4 chiến lược |

---

## 8. Trạng thái đồng bộ tài liệu (docx V2)

| File | Nội dung đồng bộ | Trạng thái |
|---|---|---|
| `HocTangCuongN10_HoanChinh.md` | Viết lại theo docx V2: S 7 chiều, A 6 mức, R 6 thành phần + 5 tình huống test, P (model-free + 4.320/480 trạng thái), γ, mục tiêu, kiến trúc 4 lớp, UC-02 có MC | ✅ Đã xong |
| `03_04_PhanTich_ThietKe_MoiTruong.md` | `Box(7)`/`Discrete(6)`, episode 30 ngày, cân bằng nước tầng rễ (ET, $K_c$, thấm thoát), 3 kịch bản JSON, sơ đồ lớp 4 agent + `Discretizer`, cây thư mục, 7 test | ✅ Đã xong |
| `III_MaGia_ThuatToan.md` | Bộ **4 chiến lược** (thêm MC Control), bảng phân loại C8, bảng so sánh 4 cột, ánh xạ file → người, lộ trình, nghiệm thu | ✅ Đã xong |
| `KichBan_Slide.md` | Rút **18 → 12 slide**, cập nhật 7 chiều/6 mức/6 thành phần reward, thêm slide MC ↔ TD | ✅ Đã xong |
| `III_MaGia_ThuatToan_Mau_Nop.md` | Template nộp cập nhật 7 chiều/6 mức/480 trạng thái, thêm mục III.4 MC | ✅ Đã xong |
| docx V2, PDF | Cần nhóm sửa thủ công: 864 ↔ 4.320; ký hiệu $\gamma$/$\varepsilon$ của reward; ngưỡng `terminated`; 1 bước = 1 ngày | ⏳ Chờ nhóm (file nhị phân, không sửa bằng công cụ văn bản) |

---

*Ba việc chặn tiến độ, làm trước: (1) chốt mục 6, (2) `reward.py` + `env` chạy được, (3) `Discretizer` chung. MC chỉ là 1 file sau khi có 3 thứ đó.*
