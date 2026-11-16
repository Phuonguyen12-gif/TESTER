# PHASE 2 — Báo cáo tiến độ TV4

**Ngày cập nhật:** 16/11/2026
**Branch:** `feat/tv4-selenium-automation`
**Commit mới nhất:** `8878077` — "refactor(tv4): restructure selenium automation with POM" (đã push)

## 1. Công việc đã hoàn thành

### Giai đoạn 1 (đã bàn giao)

- Khảo sát 10 chức năng SauceDemo (`selenium_demo/docs/phase_1/TTGĐ1/SAUCEDEMO_FEATURES.md`).
- Thiết lập môi trường: Python 3.14 + venv riêng + selenium 4.52 +
  pytest 9.2 + pytest-html, Chrome 157.
- Bộ test Selenium chạy thật, kết quả cuối: 8/8 PASS.
- Tài liệu: Test Case Draft cho TV5, nội dung slide cho TV1, báo cáo
  `report/TV4_STAGE1_REPORT.md`.

### Giai đoạn 2 — Refactor & hoàn thiện

- **Refactor sang Page Object Model**: module `automation/` ->
  `selenium_demo/` gồm `config/`, `pages/`, `tests/`, `test_data/`,
  `utils/` (đã push commit `8878077`).
- **Đồng bộ Test Case ID theo mapping chính thức của nhóm** (đợt này):
  mapping cũ trong code khác với bảng TC01–TC09 nhóm thống nhất — đã sửa
  lại test files, test data và markers cho khớp (chi tiết mục 3).
- **Chạy kiểm chứng ổn định**: suite chạy 3 lần liên tiếp, kết quả
  giống hệt nhau: `9 passed, 1 xfailed` mỗi lần.
- **Xuất bộ tài liệu bàn giao** trong `selenium_demo/docs/`.

## 2. Công việc còn tồn đọng

- Chưa commit/push các thay đổi mới (đồng bộ TC mapping + thư mục
  `docs/`) — **chờ TV4 duyệt** trước khi push.
- Thiết kế slide 18–22 trên Canva (TV4 tự làm — nội dung đã soạn sẵn tại
  `selenium_demo/docs/phase_2/TTGĐ2/`).
- Gửi `TEST_CASE_RESULTS_FOR_TV5.xlsx` cho TV5 — **TV4 tự gửi** khi nhóm
  sẵn sàng.
- Chưa mở rộng coverage: sort sản phẩm, `problem_user`,
  `performance_glitch_user` (ngoài phạm vi TC01–TC09 hiện tại).

## 3. Thay đổi trong source code (đợt này)

| File | Thay đổi | Lý do |
|---|---|---|
| `tests/test_login.py` | Negative login gộp parametrize TC02–TC04; TC09 expected đổi "Dashboard" -> "Product" | Khớp mapping nhóm (TC03=trống username, TC04=locked); spec TC09 nói "Product vs Products" |
| `tests/test_cart.py` | TC03->TC05 (add), TC04->TC06 (remove); logout không còn mã TC | Theo bảng TC chính thức; logout là test bổ sung ngoài TC01–TC09 |
| `tests/test_checkout.py` | TC05->TC07; TC08 sửa từ "thiếu First Name" thành "thiếu Postal Code" | Bảng TC chính thức yêu cầu "Postal Code is required" |
| `test_data/login_data.py` | Thêm `EMPTY_USERNAME_USER`; dataset gồm 3 case | Phục vụ TC03 |
| `test_data/checkout_data.py` | Thêm `MISSING_POSTAL_CHECKOUT` | Phục vụ TC08 |
| `pytest.ini` | Cập nhật mô tả markers tc01–tc09 | Traceability |
| `README.md` | Cập nhật dòng mô tả suite | Đồng bộ tài liệu |

Không thay đổi: page objects, conftest, settings — đang hoạt động tốt.

## 4. Trạng thái Git hiện tại

- Branch: `feat/tv4-selenium-automation` @ `8878077` (đã push lên origin).
- Chưa commit: sửa `tests/`, `test_data/`, `pytest.ini`, `README.md`;
  thêm `selenium_demo/docs/` (tài liệu bàn giao này).
- `main` không bị động vào; không merge/rebase.

## 5. Kết quả thực thi mới nhất

`pytest --headless` × 3 lần: **9 passed, 1 xfailed** mỗi lần
(TC01–TC08 PASS + test bổ sung logout PASS; TC09 XFAIL chủ đích).
Chi tiết: `TEST_EXECUTION_REPORT.md`, `evidence/run_1..3.log`.
