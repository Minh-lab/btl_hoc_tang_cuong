**TRƯỜNG ĐẠI HỌC THỦY LỢI**

**KHOA CÔNG NGHỆ THÔNG TIN**

**MÔN: HỌC TĂNG CƯỜNG VÀ ỨNG DỤNG**

**Đề tài:**

**HỆ THỐNG RA QUYẾT ĐỊNH TƯỚI TIÊU TỰ ĐỘNG**

**TỐI ƯU HÓA NGUỒN NƯỚC TRONG NÔNG NGHIẸP**

**Nhóm sinh viên thực hiện: **Nhóm 10

**Thành viên nhóm:    	    	**

Nguyễn Minh - 65KTPM - 235117060

Nguyễn Thị Phương Thảo - 65KTPM - 2351170621

Nguyễn Thế Trưởng - 65KTPM - 2351170626

Lục Văn Thuận - 65KTPM - 2351170624

**Giảng viên phụ trách môn học: **Lê Nguyễn Tuấn Thành

Hà Nội, năm 2026

THỰC HÀNH 1: MÔ HÌNH HÓA BÀI TOÁN VỚI MDP

## MỤC LỤC

Giới thiệu bài toán

## **1.1. Các mục tiêu chính**

**Phát triển hệ thống tưới tiêu tự động: **Thiết kế và mô phỏng một hệ thống tưới tiêu trong môi trường Gymnasium, đảm bảo khả năng ra quyết định cung cấp nước tự động mà không cần sự can thiệp của con người.

**Tối ưu hóa nguồn tài nguyên nước: **Xây dựng khả năng nhận diện và xử lý các thông số môi trường (độ ẩm, thời tiết) để hệ thống có thể đưa ra các hành động tưới thích hợp, duy trì lượng nước tiêu thụ một cách tiết kiệm và hiệu quả.

**Áp dụng học tăng cường: **Sử dụng các thuật toán học tăng cường (Reinforcement Learning) để huấn luyện tác tử (agent) có khả năng học từ trải nghiệm, đưa ra quyết định tối ưu dựa trên phần thưởng và hình phạt.

**Mô phỏng và đánh giá: **Thực hiện mô phỏng trong môi trường Gymnasium, đánh giá hiệu quả hoạt động của hệ thống thông qua các tiêu chí như: Khả năng duy trì độ ẩm lý tưởng, tổng lượng nước tiêu thụ, và tốc độ hội tụ của thuật toán.

**Tích hợp và tối ưu hóa: **Nâng cao hiệu quả của mô hình bằng cách thử nghiệm và tối ưu các siêu tham số của thuật toán, đảm bảo hệ thống tưới tiêu hoạt động ổn định và đạt hiệu suất cao nhất.

## **1.2. Công nghệ, nền tảng sử dụng**

- **Gymnasium (OpenAI Gym): **Một thư viện mã nguồn mở mạnh mẽ cho mô phỏng môi trường Học tăng cường. Cung cấp API linh hoạt, dễ dàng cấu hình để mô phỏng tương tác vật lý của độ ẩm đất và hành vi của hệ thống tưới tiêu.

- **Thuật toán học tăng cường: **Dựa vào các thuật toán như Q-learning, Deep Q-Network (DQN), hoặc Soft Actor-Critic (SAC). Những thuật toán này cho phép hệ thống tự học từ các trải nghiệm trong quá trình mô phỏng sinh trưởng của cây.

- **Python/PyTorch: **Sử dụng Python làm ngôn ngữ lập trình chính và PyTorch làm framework học sâu để phát triển mạng nơ-ron, tính toán phần thưởng và giao tiếp với môi trường Gymnasium.

# 3. Đề xuất một số tính năng của phần mềm

Dự án AgriWater-RL gồm 6 tính năng chính, bao quát 4 mục tiêu yêu cầu của môn học (Tích hợp, Thử nghiệm, So sánh, Đánh giá):

Tích hợp mô phỏng nông nghiệp (Integrate): Khởi tạo Environment bằng thư viện Gymnasium, mô phỏng các tương tác vật lý như tốc độ bốc hơi nước của đất, lượng mưa ngẫu nhiên và mức độ tiêu thụ nước của cây.

Tích hợp đa thuật toán (Integrate): Thiết kế pipeline cho phép cắm và chạy linh hoạt các thuật toán RL khác nhau bao gồm Q-Learning và DQN (Deep Q-Network).

Thử nghiệm đa kịch bản (Experiment): Xây dựng giao diện cấu hình chạy thử nghiệm linh hoạt với các điều kiện môi trường khác nhau: mùa khô, mùa mưa, thay đổi seed ngẫu nhiên và hyperparameters (learning rate).

So sánh chiến lược (Compare): Tính năng đối chiếu mô hình RL (DQN, Q-Learning) cạnh tranh trực tiếp với một Baseline truyền thống (Luật cố định - ví dụ chỉ tưới khi độ ẩm đất dưới ngưỡng 30%).

Đánh giá hiệu suất tổng thể (Evaluate): Tự động đo lường các metric quan trọng: Tổng lượng nước tiêu thụ, Chỉ số sinh trưởng của cây (Crop Health), Reward tích lũy và tốc độ hội tụ của thuật toán.

Báo cáo và Dashboard (Evaluate): Trực quan hóa biến thiên độ ẩm đất theo thời gian thực và tự động trích xuất bảng biểu đồ đánh giá so sánh hiệu năng để hỗ trợ làm báo cáo.

4. Phân tích bài toán

4.1. Biểu đồ phân rã chức năng

4.2. Biểu đồ use case tổng quát

5. Kiến trúc hệ thống

# 2. Phân công công việc

## 2.1. Nhiệm vụ cần thực hiện

- Phân tích bài toán
- Xây dựng kiến trúc hệ thống
- Mô hình hóa bài toán với MDP

## 2.2. Phân chia nhiệm vụ

| Thành viên | Nhiệm vụ |
| --- | --- |
| **Nguyễn Thị Phương Thảo** | (Nhiệm vụ 1)<br>- Phân tích bài toán (Xây dựng biểu đồ phân rã chức năng)<br>- Mô hình hóa bài toán với MDP (Xác định Trạng thái S) |
| **Nguyễn Minh** | (Nhiệm vụ 2)<br>- Phân tích bài toán (Xây dựng biểu đồ Use case)<br>- Mô hình hóa bài toán với MDP (Thiết kế Hàm phần thưởng R) |
| **Nguyễn Thế Trưởng** | (Nhiệm vụ 3)<br>- Xây dựng kiến trúc hệ thống<br>- Mô hình hóa bài toán với MDP (Ma trận chuyển đổi P, hành động A) |
| **Lục Văn Thuận** | (Nhiệm vụ 4)<br>- Làm báo cáo, tổng hợp Slide<br>- Mô hình hóa bài toán với MDP (Hệ số chiết khấu γ và mục tiêu MDP) |

# 3. Mô hình hóa bài toán với MDP

# 1. Giới thiệu về quy trình quyết định Markov

Quy trình Quyết định Markov (MDP) là một khung lý thuyết toán học dùng để mô hình hóa các bài toán ra quyết định tuần tự. Trong đó, kết quả của mỗi hành động không chỉ phụ thuộc vào hành động đó mà còn phụ thuộc vào trạng thái hiện tại. Cấu trúc MDP gồm 5 thành phần: Tập trạng thái (S), Tập hành động (A), Hàm chuyển đổi (P), Hàm phần thưởng (R), Hệ số chiết khấu (γ).

# 2. Mô hình hoá MDP bài toán

## 2.1. Trạng thái (S)

Trạng thái S là một vector biểu diễn tình trạng nông trại tại thời điểm t:
S_t = [Moisture, Temp, RainProb].
- Moisture: Độ ẩm đất hiện tại (0-100%).
- Temp: Nhiệt độ môi trường.
- RainProb: Xác suất có mưa.
Ý nghĩa: Cung cấp đủ thông tin bối cảnh để Agent có thể ra quyết định tưới chính xác.

2.2. Hành động (A)

Tập hành động A là các quyết định tưới tiêu rời rạc:
- Hành động 0: Không tưới (để tiết kiệm nước).
- Hành động 1: Tưới ít (duy trì độ ẩm cơ bản).
- Hành động 2: Tưới nhiều (sử dụng khi đất quá khô hạn).

2.3. Hàm phần thưởng (R(s,a))

Hàm phần thưởng R(s,a) = +10 (nếu độ ẩm lý tưởng) - α * Water (phạt lượng nước tiêu thụ) - 100 (phạt héo úa).
Lý do thiết kế: Khuyến khích Agent giữ độ ẩm tốt nhưng phải trừ điểm nếu lãng phí nước. Định hình phần thưởng (shaping) phạt cực nặng (-100) nếu cây héo để Agent học cách ưu tiên sự sống của cây lên hàng đầu.

2.4. Ma trận chuyển đổi trạng thái (P)

Hệ thống hoạt động ở dạng Model-free, ma trận xác suất chuyển đổi P không được cho sẵn. Sự biến thiên trạng thái từ S_t sang S_{t+1} được mô phỏng động bởi Gymnasium dựa trên lượng nước tưới, thời tiết và tốc độ bốc hơi tự nhiên của đất.

2.5. Hệ số chiết khấu (γ)

Hệ số chiết khấu γ = 0.99.
Lý do: Chu kỳ sinh trưởng của cây kéo dài nhiều tháng, việc đặt γ gần 1 buộc Agent phải tối ưu hóa phần thưởng dài hạn (thu hoạch cây trồng) thay vì chỉ tiết kiệm nước thiển cận trong một ngày.

Miêu tả các thành phần MDP tương ứng với bài toán