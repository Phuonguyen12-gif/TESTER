# DOCUMENTATION RESTRUCTURE REPORT

**Ngày:** 16/11/2026 · **Branch:** `feat/tv4-selenium-automation`
**Phạm vi:** chuẩn hóa cấu trúc tài liệu — KHÔNG thay đổi nội dung chuyên môn,
không đụng mã nguồn, không commit/push.

## 1. Cấu trúc TRƯỚC → SAU

### Trước

```
TESTER/docs/
├── SAUCEDEMO_FEATURES.md
├── TEST_CASE_DRAFT.md
├── TEST_CASES_FOR_TV5/        (tên sai quy chuẩn)
├── TTGĐ1/TV4_SLIDE_CONTENT.md
├── TTGĐ2/{2 md + SCREENSHOTS/}
└── phase_2/{4 md/xlsx + evidence/}

(selenium_demo/docs/ không tồn tại)
```

### Sau

```
TESTER/
├── docs/
│   ├── TEST_CASE_FOR_TV5/                 (đổi tên từ TEST_CASES_FOR_TV5)
│   │   ├── TEST_CASES_FINAL.md            ← Test Case Design
│   │   ├── TEST_CASES_FINAL.xlsx          ← Test Case Design
│   │   ├── TEST_EXECUTION_RESULTS.xlsx    ← Execution Results (tách biệt)
│   └── DOCUMENTATION_RESTRUCTURE_REPORT.md (file này)
└── selenium_demo/docs/
    ├── phase_1/TTGĐ1/   (3 file — tài liệu giai đoạn 1)
    └── phase_2/TTGĐ2/   (13 file — tài liệu giai đoạn 2)
```

Quy chuẩn giai đoạn tiếp theo: `selenium_demo/docs/phase_N/TTGĐN/`
(không tạo phase_4/5/6 vì chưa có nội dung — tránh thư mục rỗng).

## 2. File đã di chuyển (19 file, dùng git mv cho file tracked, mv cho untracked)

| File | Từ | Đến | Giai đoạn |
|---|---|---|---|
| TV4_SLIDE_CONTENT.md | docs/TTGĐ1/ | selenium_demo/docs/phase_1/TTGĐ1/ | 1 |
| SAUCEDEMO_FEATURES.md | docs/ | selenium_demo/docs/phase_1/TTGĐ1/ | 1 |
| Test Case Draft — SauceDemo (BẢN NHÁP cho TV5 rà soát).md | docs/ | docs/TEST_CASE_FOR_TV5/ | 1 (bản nháp, tách khỏi FINAL) |
| PHASE_2_PROGRESS_REPORT.md | docs/phase_2/ | selenium_demo/docs/phase_2/TTGĐ2/ | 2 |
| TEST_EXECUTION_REPORT.md | docs/phase_2/ | selenium_demo/docs/phase_2/TTGĐ2/ | 2 |
| TEST_CASE_RESULTS_FOR_TV5.xlsx | docs/phase_2/ | selenium_demo/docs/phase_2/TTGĐ2/ | 2 |
| QA_DIFFICULTIES_AND_SOLUTIONS.md | docs/phase_2/ | selenium_demo/docs/phase_2/TTGĐ2/ | 2 |
| evidence/run_1..3.log | selenium_demo/screenshots/phase_2/logs/ | .../phase_2/TTGĐ2/evidence/ | 2 |
| PRESENTATION_CONTENT_TV4.md | docs/TTGĐ2/ | selenium_demo/docs/phase_2/TTGĐ2/ | 2 |
| PRESENTATION_SCRIPT_TV4.md | docs/TTGĐ2/ | selenium_demo/docs/phase_2/TTGĐ2/ | 2 |
| SCREENSHOTS/ (4 png) | docs/TTGĐ2/ | .../phase_2/TTGĐ2/SCREENSHOTS/ | 2 |
| TEST_CASES_FOR_TV5/ (3 file) | docs/TEST_CASES_FOR_TV5/ | docs/TEST_CASE_FOR_TV5/ (đổi tên dir) | TV5 |

## 3. File giữ nguyên vị trí & lý do

| File/Thư mục | Lý do |
|---|---|
| `reports/` (stage 1: report, logs, 13 screenshots) | Bằng chứng thực thi, không phải tài liệu docs; nhiều tài liệu tham chiếu tới |
| `selenium_demo/reports/` | Artifact do pytest sinh ra (gitignored) |
| `README.md` (root, selenium_demo) | Tài liệu gốc của repo/module, không thuộc giai đoạn cụ thể |

## 4. File trùng lặp / chưa xác định giai đoạn

- **Trùng nội dung (có chủ đích, giữ cả hai):**
  `selenium_demo/docs/phase_2/TTGĐ2/TEST_CASE_RESULTS_FOR_TV5.xlsx` ≡
  `docs/TEST_CASE_FOR_TV5/TEST_EXECUTION_RESULTS.xlsx` — bản đầu là
  deliverable của giai đoạn 2, bản sau là bản chính thức bàn giao TV5.
  Hai vai trò khác nhau, không phải sao chép dư thừa.
- **Không có file nào chưa xác định được giai đoạn** — mọi file đã được phân loại.

## 5. Kiểm tra toàn vẹn

- Số file trước: **19** · sau: **19** — không mất file.
- `git status`: rename được ghi nhận (R) cho TV4_SLIDE_CONTENT.md; các
  file untracked di chuyển nguyên vẹn (nội dung không đổi — chỉ đường dẫn).
- XLSX mở được, đủ TC01–TC09, evidence path đã cập nhật (27 ô/file).
- Không còn tham chiếu cũ `docs/phase_2`, `docs/TTGĐ*`,
  `docs/TEST_CASES_FOR_TV5` (grep sạch).

## 6. Tham chiếu đã cập nhật

| File | Cập nhật |
|---|---|
| report/TV4_STAGE1_REPORT.md | 4 đường dẫn docs/ + khối tree |
| phase_2/TTGĐ2/PHASE_2_PROGRESS_REPORT.md | 4 tham chiếu đường dẫn |
| phase_2/TTGĐ2/TEST_EXECUTION_REPORT.md | evidence + SCREENSHOTS paths |
| phase_1/TTGĐ1/TEST_CASE_DRAFT.md | `automation/tests/` → `selenium_demo/tests/` (sau đó file đã chuyển sang `docs/TEST_CASE_FOR_TV5/` — xem Phần 3) |
| 2 file .xlsx | 27 ô đường dẫn evidence/report mỗi file |
| README.md (root) | mô tả cấu trúc docs mới |

## 7. Git

- Branch: `feat/tv4-selenium-automation` @ `8878077` (+ các thay đổi
  chưa commit từ trước).
- **Không commit, không push, không đụng branch khác.**

---

# PHẦN 2 — CHUẨN HÓA SCREENSHOTS VÀ REPORTS

## A. Cấu trúc trước → sau

```
TRƯỚC                                          SAU
TESTER/reports/                                TESTER/report/                    (chỉ .md)
├── TV4_STAGE1_REPORT.md                       ├── TV4_STAGE1_REPORT.md
├── screenshots/demo/        (7 png)           └── DOCUMENTATION_RESTRUCTURE_REPORT.md
├── screenshots/failed_runs/ (6 png)
├── logs/                    (5 log)           TESTER/selenium_demo/screenshots/
├── test_results/            (2 html)          ├── phase_1/
selenium_demo/screenshots/                     │   ├── demo/          (7 png, từ reports/)
│   ├── demo/                (7 png, phase2)   │   ├── failed_runs/   (6 png)
│   └── test_TC09_...png     (phase2)          │   ├── logs/          (5 log)
selenium_demo/reports/                         │   └── test_results/  (2 html)
└── report.html              (phase2)          └── phase_2/
docs/phase_2/TTGĐ2/evidence/   (3 log)             ├── demo/          (7 png, capture_demo)
                                                   ├── failed_runs/   (1 png, TC09 xfail demo)
                                                   ├── logs/          (3 log, run_1..3)
                                                   └── test_results/  (1 html, report.html)
```

Thư mục `reports/` cũ đã bị xóa sau khi rỗng. Không tạo `phase_4/5/6` —
chưa có dữ liệu, tránh thư mục rỗng.

## B. Phân loại dữ liệu theo giai đoạn

| Nguồn | Đích | Giai đoạn | Căn cứ |
|---|---|---|---|
| `reports/screenshots/demo/` | `screenshots/phase_1/demo/` | 1 | Capture từ `automation/` bản phẳng |
| `reports/screenshots/failed_runs/` | `screenshots/phase_1/failed_runs/` | 1 | 6 ảnh FAIL lần chạy đầu (giai đoạn 1) |
| `reports/logs/` | `screenshots/phase_1/logs/` | 1 | Log pytest 5 lần chạy stage 1 |
| `reports/test_results/` | `screenshots/phase_1/test_results/` | 1 | 2 HTML report giai đoạn 1 |
| `selenium_demo/screenshots/demo/` | `screenshots/phase_2/demo/` | 2 | Capture bằng `capture_demo.py` bản POM |
| `screenshots/test_TC09_..._FAILED.png` | `screenshots/phase_2/failed_runs/` | 2 | Ảnh TC09 xfail demo giai đoạn 2 |
| `docs/phase_2/TTGĐ2/evidence/run_*.log` | `screenshots/phase_2/logs/` | 2 | Log 3 lần chạy phase 2 |
| `selenium_demo/reports/report.html` | `screenshots/phase_2/test_results/` | 2 | HTML report phase 2 |
| `reports/TV4_STAGE1_REPORT.md` | `report/` | — | `report/` chỉ chứa .md |

## C. File không xác định nguồn gốc

Không có. Mọi file đều phân loại được (phase 1 hoặc 2).
Thư mục `TESTER/report/screenshort/`, `TESTER/report/screenshort/tesr_results`,
`TESTER/selenium/screenshorts` được đề cập trong yêu cầu **không tồn tại**
trên thực tế — dữ liệu thật nằm ở `reports/screenshots/` (đã xử lý ở trên).

## D. Kiểm tra tính toàn vẹn

- File đếm lại trước/sau: 22 file evidence + 2 báo cáo md — không mất file.
- `git mv` dùng cho tất cả file tracked (phase 1 + báo cáo) → rename giữ history.
- Đã cập nhật `.gitignore`: artifact sinh ra ở `screenshots/*.png` (root),
  `screenshots/demo/`, `reports/*.html` vẫn bị ignore; `screenshots/phase_N/`
  được phép commit.
- `.gitkeep` giữ lại tại `selenium_demo/screenshots/` và `reports/`.

## E. Tham chiếu đã cập nhật

- `report/TV4_STAGE1_REPORT.md` — đường dẫn evidence → `screenshots/phase_1/`
- `docs/phase_1/TTGĐ1/TV4_SLIDE_CONTENT.md`, `SAUCEDEMO_FEATURES.md` — path demo
- `docs/phase_2/TTGĐ2/TEST_EXECUTION_REPORT.md`, `PHASE_2_PROGRESS_REPORT.md`,
  `PRESENTATION_CONTENT_TV4.md` — evidence/ và report.html mới
- `README.md` root — mục `reports/` thay bằng `screenshots/phase_N/` + `report/`
- 2 file xlsx (108 ô) — cột Evidence cập nhật path mới
- `DOCUMENTATION_RESTRUCTURE_REPORT.md` (file này) — path trong Phần 1

## F. Xác nhận

Không commit, không push. Không đụng branch khác. Không sửa mã nguồn Selenium.


---

# PHẦN 3 — BỔ SUNG TEST CASE DRAFT CHO TV5

- **File:** `Test Case Draft — SauceDemo (BẢN NHÁP cho TV5 rà soát).md`
- **Nguồn:** `selenium_demo/docs/phase_1/TTGĐ1/TEST_CASE_DRAFT.md` (đổi tên theo đúng tiêu đề tài liệu)
- **Đích:** `docs/TEST_CASE_FOR_TV5/` — cùng nhóm bàn giao TV5 nhưng giữ nguyên
  nhãn BẢN NHÁP trong nội dung, phân biệt với `TEST_CASES_FINAL.*`.
- **Nội dung:** giữ nguyên 100% (di chuyển, không sửa). Thư mục đích không có
  file trùng tên — không ghi đè. Không tìm thấy phiên bản thứ hai nào khác.
- **Cây `docs/TEST_CASE_FOR_TV5/` sau bổ sung:**
  - `Test Case Draft — SauceDemo (BẢN NHÁP cho TV5 rà soát).md` ← bản nháp
  - `TEST_CASES_FINAL.md` / `.xlsx` ← thiết kế chính thức
  - `TEST_EXECUTION_RESULTS.xlsx` ← kết quả thực thi
- **Tham chiếu cập nhật:** `report/TV4_STAGE1_REPORT.md` (cây thư mục + bảng
  deliverables), file báo cáo này.
- Không commit, không push.
