1. NGỮ CẢNH MÔN HỌC
Tên môn: Học tăng cường và Ứng dụng (Reinforcement Learning and Applications)

Loại bài tập: Dự án nhóm – thực hành xuyên suốt học kỳ

Mục đích chính thức của môn:

Phát triển phần mềm (có tính thực tiễn) tích hợp, thử nghiệm, so sánh, đánh giá các thuật toán học tăng cường.

Số lượng thành viên: 4 sinh viên (cố định, không thay đổi)

Buổi đánh giá đầu tiên: Thực hành 1 – sáng thứ 7, ngày 03/10/2026

Hình thức báo cáo: Thuyết trình trực tiếp + slide

2. THÔNG TIN NHÓM (BẮT BUỘC GHI ĐÚNG)
STT	Họ và tên	Vai trò dự kiến
1	Nguyễn Thị Phương Thảo	Nhóm trưởng – điều phối + kiến trúc + áp dụng RL
2	Nguyễn Minh	Thành viên – code thuật toán RL 1
3	Nguyễn Thế Trưởng	Thành viên – môi trường + code thuật toán RL 2
4	Lục Văn Thuận	Thành viên – đánh giá/GUI/báo cáo + thuật toán RL 3 (hoặc Baseline)
⚠️ AI phải dùng đúng 4 tên này khi sinh nội dung phân công. Không được bịa thêm thành viên thứ 5 trở lên.

3. YÊU CẦU BẮT BUỘC CỦA THỰC HÀNH 1
AI phải đảm bảo đầu ra bao gồm đủ 4 mục sau (không được thiếu mục nào):

3.1. Đề xuất đề tài/dự án phần mềm có sử dụng RL
Phải là bài toán thực tiễn (không chỉ là demo học thuật thuần túy).

Phải áp dụng được RL (không dùng supervised learning thay thế).

Phải có tên dự án rõ ràng, mô tả ngắn gọn, lý do chọn.

3.2. Đề xuất một số tính năng của phần mềm
Tối thiểu 6 tính năng.

Phải thể hiện được 4 động từ trong mục đích môn học:

Tích hợp (integrate): cắm nhiều thuật toán / nhiều môi trường.

Thử nghiệm (experiment): chạy nhiều cấu hình, nhiều seed.

So sánh (compare): đặt nhiều thuật toán cạnh nhau.

Đánh giá (evaluate): có metric, biểu đồ, báo cáo.

3.3. Phân công công việc dự kiến cho các thành viên
Phải ghi đúng 4 tên ở Mục 2.

Mỗi người phải có: vai trò + nhiệm vụ cụ thể + deadline dự kiến.

Bắt buộc tất cả thành viên đều phải trực tiếp lập trình/áp dụng kiến thức RL (ví dụ: code thuật toán, thiết kế Reward, tuning). Không ai được chỉ làm mỗi công việc phụ trợ như slide, báo cáo hay GUI thuần túy.

Không được để ai "không có việc".

3.4. Mô hình hóa bài toán thành Quy trình quyết định Markov (MDP)
Phải trình bày đầy đủ 5 thành phần: (S, A, P, R, γ).

Mỗi thành phần phải có định nghĩa cụ thể, không viết chung chung.

Phải có công thức reward rõ ràng.

Phải có mục tiêu tối ưu (policy tối ưu).

Nên có sơ đồ MDP (agent–environment loop).
3.5. Slide thuyết trình
Khoảng 10–12 slide.

Có đủ 4 mục trên + slide mở đầu + slide Q&A.
4. LUẬT VỀ NỘI DUNG (CONTENT RULES)
Mã luật	Nội dung
C1	Mọi đề tài đề xuất phải dùng RL làm phương pháp chính, không thay bằng ML/DL thông thường.
C2	Phần mềm phải có tính thực tiễn – phải trả lời được câu hỏi "ứng dụng này giải quyết vấn đề gì trong đời sống/công việc?".
C3	Phải tích hợp tối thiểu 2 thuật toán RL để so sánh (ví dụ: Q-Learning vs DQN).
C4	Phải có baseline (random, fixed-rule, hoặc thuật toán truyền thống) để so sánh.
C5	Phải có tiêu chí đánh giá định lượng: reward, convergence speed, stability, sample efficiency, thời gian train.
C6	MDP phải nhất quán với bài toán đã chọn – không được copy MDP của bài toán khác.
C7	Reward function phải có lý do thiết kế (tại sao chọn +10/−10, tại sao có shaping…).
C8	Không được dùng quá 3 thuật toán cho nhóm 4 người (tránh dàn trải).
5. LUẬT VỀ HÌNH THỨC (FORMAT RULES)
Mã luật	Nội dung
F1	Văn phong: tiếng Việt học thuật, rõ ràng, không dùng từ ngữ cảm tính.
F2	Công thức toán viết bằng LaTeX ($...$ hoặc $$...$$).
F3	Bảng dùng Markdown table.
F4	Mỗi đề tài đề xuất phải trình bày theo cấu trúc thống nhất: Mô tả → Tính năng → Phân công → MDP.
F5	Slide phải có bố cục từng slide rõ ràng, không viết một đoạn văn dài.
F6	Tên thành viên viết đúng chính tả, có dấu tiếng Việt.
6. LUẬT VỀ PHÂN CÔNG (ASSIGNMENT RULES)
Mã luật	Nội dung
A1	Mỗi thành viên phải có vai trò riêng, không trùng lặp hoàn toàn.
A2	Phân công phải rõ ràng, NHƯNG bắt buộc tất cả thành viên đều phải có nhiệm vụ lập trình và áp dụng kiến thức RL. Tuyệt đối không ai chỉ làm slide, viết báo cáo hay làm giao diện thuần túy.
A3	Nhóm trưởng (Nguyễn Thị Phương Thảo) ngoài điều phối + kiến trúc tổng thể phải trực tiếp tham gia mô hình hóa/code RL.
A4	Deadline phải chia theo tuần, không dồn hết vào cuối kỳ.
A5	Bắt buộc mỗi thành viên phải trực tiếp lập trình/huấn luyện ít nhất 1 thuật toán RL, baseline, hoặc thành phần cốt lõi của mô hình. Không được khoán trắng phần thuật toán cho một cá nhân.
7. LUẬT VỀ MDP (MDP RULES)
Khi mô hình hóa MDP, AI bắt buộc phải trình bày đủ 5 phần sau theo đúng thứ tự:

7.1. State space (S)
Định nghĩa vector/matrix trạng thái.

Ghi rõ kích thước (rời rạc hay liên tục, bao nhiêu chiều).

Giải thích ý nghĩa từng thành phần.

7.2. Action space (A)
Liệt kê tất cả hành động.

Ghi rõ rời rạc hay liên tục, kích thước |A|.

7.3. Transition probability (P)
Ghi rõ do đâu mà có (simulator, vật lý, dữ liệu lịch sử…).

Ghi rõ môi trường là model-free hay model-based.

7.4. Reward function (R)
Viết công thức tường minh.

Có giải thích lý do thiết kế.

Nếu có shaping reward → phải nói rõ.

7.5. Discount factor (γ)
Ghi giá trị cụ thể (ví dụ 0.95, 0.99).

Giải thích tại sao chọn giá trị đó.

7.6. Mục tiêu tối ưu (bắt buộc thêm)
Viết công thức:

π
∗
=
arg
⁡
max
⁡
π
E
[
∑
t
=
0
∞
γ
t
r
t
∣
π
]
π 
∗
 =arg 
π
max
​
 E[ 
t=0
∑
∞
​
 γ 
t
 r 
t
​
 ∣π]
7.7. Sơ đồ MDP (khuyến khích)
Vẽ vòng lặp Agent ↔ Environment.

8. LUẬT VỀ ĐỀ TÀI ĐỀ XUẤT (TOPIC RULES)
Khi AI gợi ý đề tài, phải tuân thủ:

Mã luật	Nội dung
T1	Đề tài phải phù hợp nhóm 4 người – không quá lớn, không quá nhỏ.
T2	Đề tài phải hoàn thành được trong 1 học kỳ.
T3	Đề tài phải có môi trường có sẵn (Gymnasium, SUMO, PyBullet…) hoặc tự viết đơn giản.
T4	Đề tài phải cho phép so sánh ít nhất 2 thuật toán RL.
T5	Đề tài phải có demo trực quan (render, dashboard, video…).
T6	Ưu tiên đề tài có tính thực tiễn (giao thông, tài chính, robot, y tế, năng lượng…).
T7	Không đề xuất đề tài trùng lặp hoàn toàn với nhóm khác nếu đã biết.
9. LUẬT VỀ ĐẦU RA CỦA AI (OUTPUT RULES)
Khi người dùng yêu cầu AI hỗ trợ, AI phải:

Mã luật	Nội dung
O1	Trả lời đúng trọng tâm, không lan man.
O2	Nếu yêu cầu là "viết file md" → xuất Markdown thuần, không kèm lời bình ngoài lề.
O3	Nếu yêu cầu là "viết slide" → trình bày từng slide riêng biệt, có số thứ tự.
O4	Nếu yêu cầu là "MDP" → bắt buộc trình bày đủ 5 thành phần theo Mục 7.
O5	Nếu yêu cầu là "phân công" → bắt buộc dùng đúng 4 tên ở Mục 2.
O6	Nếu yêu cầu là "đề tài" → bắt buộc có: Mô tả + Tính năng + Phân công + MDP.
O7	Không bịa thông tin về giảng viên, deadline, hay tài liệu tham khảo không có thật.
O8	Nếu thiếu thông tin → hỏi lại thay vì tự suy diễn.
10. CHECKLIST TRƯỚC KHI AI XUẤT KẾT QUẢ
AI phải tự kiểm tra các mục sau trước khi trả lời:

□ Đã có tên đề tài rõ ràng chưa?
□ Đã có mô tả dự án chưa?
□ Đã có ≥ 6 tính năng chưa?
□ Đã có phân công đủ 4 thành viên với đúng tên chưa?
□ Đã có MDP đủ 5 thành phần chưa?
□ Đã có công thức reward chưa?
□ Đã có mục tiêu tối ưu chưa?
□ Đã có sơ đồ MDP chưa?
□ Đã có bố cục slide chưa?
□ Đã tuân thủ 4 động từ: tích hợp – thử nghiệm – so sánh – đánh giá chưa?
Nếu thiếu bất kỳ mục nào → bổ sung trước khi xuất.

11. CÁC TỪ KHÓA NGỮ CẢNH (CONTEXT KEYWORDS)
Khi người dùng nhắc đến các từ khóa sau, AI phải hiểu đây là bối cảnh môn RL:

Học tăng cường, Reinforcement Learning, RL, MDP, Markov Decision Process, Q-Learning, DQN, PPO, A2C, SAC, TD3, DDPG, REINFORCE, Actor-Critic, Gymnasium, SUMO, PyBullet, CartPole, Snake, trading, giao thông, robot, Thực hành 1, 03/10/2026, nhóm 4 thành viên.

12. GHI CHÚ CUỐI
File này là luật bất biến cho AI khi hỗ trợ nhóm.

Nếu có yêu cầu mới từ giảng viên → người dùng phải cập nhật file này trước khi AI tiếp tục.

AI không được tự ý thay đổi tên thành viên, mục đích môn học, hay deadline.

Mọi đầu ra phải kiểm tra lại Checklist Mục 10 trước khi gửi.

Hết file luật.

