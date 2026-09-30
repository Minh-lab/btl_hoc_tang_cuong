# Tóm tắt Tiến trình Học tập Reinforcement Learning (RL)

*Dựa trên các ghi chép từ file `Học Tăng Cường.docx`.*

## 1. Mức độ tiến độ hiện tại
Bạn đã học xong các khái niệm nền tảng về MDP, phương pháp **Dynamic Programming** (Quy hoạch động - Model-based) và đang chuyển sang các phương pháp **Model-free RL**, cụ thể là phương pháp **Monte Carlo**.

## 2. Các kiến thức cốt lõi đã nắm bắt
### 2.1. Khái niệm cơ bản & Hàm giá trị
- Các thành phần cơ bản: Tác tử (Agent), Môi trường (Environment), Hành động (Action), Phần thưởng (Reward), Chính sách (Policy).
- **Tính chất Markov**: Trạng thái tương lai chỉ phụ thuộc vào trạng thái và hành động hiện tại, không phụ thuộc vào toàn bộ quá khứ.
- **Chuỗi phần thưởng kỳ vọng (Return - $G_t$)**: $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + ...$ (với $\gamma$ là hệ số chiết khấu).
- **State-value function ($V^\pi(s)$)**: Giá trị kỳ vọng khi bắt đầu từ trạng thái $s$ và tuân theo chính sách $\pi$.
- **Action-value function ($Q^\pi(s, a)$)**: Giá trị kỳ vọng khi ở trạng thái $s$, thực hiện hành động $a$, sau đó tuân theo chính sách $\pi$.
- **Phương trình Bellman**: Mối liên hệ đệ quy giữa các giá trị trạng thái.

### 2.2. Markov Decision Process (MDP)
- Mô hình hóa dưới dạng Tuple: $\langle S, A, P, R, \gamma \rangle$.
- Vòng lặp: Tác tử nhận trạng thái $S_t$, thực hiện $A_t$ $\to$ Môi trường trả về phần thưởng $R_{t+1}$ và trạng thái mới $S_{t+1}$.
- **Mục tiêu**: Tìm chính sách tối ưu $\pi^*$ để tối đa hóa tổng phần thưởng kỳ vọng.

### 2.3. Dynamic Programming (Quy hoạch động)
- **Điều kiện**: Phải **biết đầy đủ mô hình môi trường** (Model-based: biết rõ ma trận $P$ và $R$).
- Giải bài toán bằng cách chia nhỏ thành các bài toán con đệ quy.
- **Thuật toán chính**: Policy Iteration, Value Iteration, GPI (Generalized Policy Iteration).

### 2.4. Phương pháp Monte Carlo (MC)
- **Đặc điểm**: Thuộc nhóm **Model-free RL** (không biết đầy đủ mô hình $P, R$ của môi trường).
- **Điều kiện áp dụng**: Bài toán phải có **trạng thái kết thúc** (Episodic tasks).
- **Ý tưởng**: Học từ kinh nghiệm (các lần chơi/tập mẫu), tính tổng phần thưởng $G_t$ của mỗi episode và lấy trung bình để cập nhật hàm $V, Q$.
- Các phần chính đang học:
  - MC Prediction (Ước lượng giá trị của một chính sách).
  - MC Control: Tối ưu hóa chính sách (gồm **On-policy** - dùng 1 chính sách để vừa khám phá vừa tối ưu; và **Off-policy** - dùng 2 chính sách khác nhau).

## 3. Ghi chú cho phần Thực hành & Kiểm tra
- **Bài tập/Dự án**: Quy trình thực hiện gồm: Lên đề tài $\to$ Mô hình hóa MDP $\langle S, A, P, R \rangle$ $\to$ Giải bài toán (dùng DP nếu biết model, dùng MC hoặc phương pháp model-free khác nếu không biết) $\to$ Code mã giả và chứng minh hoạt động.
- **Kiểm tra**: Có bài kiểm tra lý thuyết (dự kiến tuần tới nữa theo ghi chú).

---
*Ghi chú: File này sẽ được AI sử dụng làm bối cảnh để hiểu kiến thức hiện tại của bạn, qua đó cung cấp các hỗ trợ, giải thích hoặc đề xuất phù hợp với mức độ bạn đang tiếp thu môn học.*