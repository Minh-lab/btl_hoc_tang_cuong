# btl_hoc_tang_cuong

**AgriWater-RL** — Hệ thống ra quyết định tưới tiêu tự động tối ưu hóa nguồn nước trong nông nghiệp.
Bài tập lớn môn *Học tăng cường và ứng dụng* — Nhóm 10, Khoa Công nghệ thông tin, Trường Đại học Thủy lợi.

## Cấu trúc thư mục

```
.
├── README.md
└── docs/
    ├── HocTangCuongN10_HoanChinh.docx      # báo cáo chính (bản nộp, V2)
    ├── HocTangCuongN10_HoanChinh.md        # nguồn Markdown của báo cáo
    ├── requirements.md                     # yêu cầu & luật ràng buộc của môn
    ├── 03_04_PhanTich_ThietKe_MoiTruong.md # phân tích & thiết kế môi trường thử nghiệm
    ├── III_MaGia_ThuatToan.md              # mã giả 4 chiến lược (Q-Learning, MC, DQN, Baseline)
    ├── III_MaGia_ThuatToan_Mau_Nop.md      # template nộp phần mã giả
    ├── KeHoach_NganGon_MC_Va_MoiTruong.md  # kế hoạch bổ sung Monte Carlo + môi trường
    ├── KeHoach_MoiTruong_Minh_Truong.md    # kế hoạch triển khai môi trường (2 người) + todolist
    ├── KichBan_Slide.md                    # kịch bản 12 slide thuyết trình
    └── tham-khao/                          # tài liệu tham khảo, không phải bản nộp
        ├── TH2-Environment-Algorithms.docx # template đề bài của giảng viên
        ├── example.docx, example_images/   # báo cáo mẫu
        ├── GioiThieu_AgriWater-RL.docx     # bản giới thiệu đề tài ban đầu
        ├── KienThuc.md                     # ghi chú lý thuyết RL
        └── hoctangcuong_notes.docx         # tài liệu học tập
```

## Ghi chú

- Báo cáo và các tài liệu thiết kế hiện hành theo **bản V2**: trạng thái 7 chiều, 6 mức tưới $\{0,5,10,15,20,25\}$ L, reward 6 thành phần, episode 30 ngày.
- Các bản PDF cũ (dựa trên thiết kế 3 chiều / 3 hành động) đã được gỡ; PDF cần xuất lại từ file `.docx` hoặc `.md` tương ứng trước khi nộp.
