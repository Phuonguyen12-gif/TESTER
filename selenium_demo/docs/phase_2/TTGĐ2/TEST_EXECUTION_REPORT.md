# TEST EXECUTION REPORT — Selenium Demo (SauceDemo)

**Môi trường:** macOS 27.0.1 (Apple Silicon) · Python 3.14.0 · Chrome
157.0.8103.52 · selenium 4.52.0 · pytest 9.2.0 · pytest-html 4.2.0
**Chế độ chạy:** headless (`pytest --headless`), 3 lần liên tiếp ngày
16/11/2026 — cùng kết quả.

## 1. Kết quả tổng hợp

| Lần chạy | Kết quả | Thời gian | Log |
|---|---|---|---|
| Run 1 | 9 passed, 1 xfailed | 16.94s | `evidence/run_1.log` |
| Run 2 | 9 passed, 1 xfailed | 14.87s | `evidence/run_2.log` |
| Run 3 | 9 passed, 1 xfailed | 16.62s | `evidence/run_3.log` |

**Tổng:** 10 test được collect → **9 PASSED · 0 FAILED · 1 XFAIL · 0 SKIP**
mỗi lần chạy. (9 test gồm TC01–TC08 + 1 test bổ sung `test_logout`
ngoài bộ TC; TC09 được đánh dấu xfail.)

## 2. Kết quả theo Test Case

| TC | Nội dung | Expected | Actual | Run 1 | Run 2 | Run 3 |
|---|---|---|---|---|---|---|
| TC01 | Đăng nhập hợp lệ | Hiển thị Products | title='Products', 6 items | PASS | PASS | PASS |
| TC02 | Sai mật khẩu | Thông báo lỗi | 'Epic sadface: Username and password do not match...' | PASS | PASS | PASS |
| TC03 | Bỏ trống username | 'Username is required' | Đúng thông báo | PASS | PASS | PASS |
| TC04 | locked_out_user | Báo tài khoản bị khóa | '...has been locked out.' | PASS | PASS | PASS |
| TC05 | Thêm vào giỏ | Cart badge = 1 | Badge='1', đúng item | PASS | PASS | PASS |
| TC06 | Xóa khỏi giỏ | Badge biến mất | item+badge biến mất | PASS | PASS | PASS |
| TC07 | Checkout hợp lệ | 'Thank you for your order!' | checkout-complete + message | PASS | PASS | PASS |
| TC08 | Trống Postal Code | 'Postal Code is required' | Đúng thông báo, ở lại step-one | PASS | PASS | PASS |
| TC09 | Expected title cố tình sai | Thất bại CÓ CHỦ ĐÍCH | 'Product' ≠ 'Products' | XFAIL | XFAIL | XFAIL |
| — | test_logout (bổ sung) | Về trang login | login-button hiển thị | PASS | PASS | PASS |

## 3. TC09 — phân biệt XFAIL và FAILED

- **XFAIL (expected failure):** test fail nhưng pytest *dự kiến* nó fail
  (marker `@pytest.mark.xfail`) → suite vẫn exit code 0, không tính là
  lỗi sản phẩm. Đây là trạng thái của TC09 trong suite thường.
- **FAILED:** khi chạy `pytest -m demo_fail --runxfail`, cơ chế xfail bị
  tắt → TC09 FAILED thật, exit code ≠ 0, và tự động chụp screenshot
  (đã kiểm chứng: `screenshots/test_TC09_..._FAILED.png` được tạo và
  đính kèm HTML report).
- TC09 **không phải lỗi của SauceDemo** — assertion sai có chủ đích
  ('Product' vs 'Products') để demo pipeline xử lý test thất bại.

## 4. Lỗi phát sinh & nguyên nhân

- **3 lần chạy phase 2: không có lỗi.** Không flake, không timeout,
  không lỗi phụ thuộc trạng thái trình duyệt.
- Lịch sử (giai đoạn 1): các lỗi timing/2-phiên-bản-UI đã được xử lý
  bằng explicit wait + JS click/type fallback trong `BasePage`
  (xem `report/TV4_STAGE1_REPORT.md` mục 8).

## 5. Đánh giá độ ổn định

- **Flakiness: 0/30 lần chạy** (10 test × 3 run) — kết quả đồng nhất.
- Test độc lập: mỗi test một browser instance mới (fixture
  function-scope), không phụ thuộc thứ tự chạy.
- Rủi ro còn lại: phụ thuộc website bên ngoài — nếu SauceDemo đổi
  DOM (id/class) test sẽ FAIL; locator hiện ổn định trên cả 2 phiên
  bản UI mà site đang phục vụ.

## 6. Bằng chứng

- Log 3 lần chạy: `selenium_demo/screenshots/phase_2/logs/run_{1,2,3}.log`
- HTML report mới nhất: `selenium_demo/screenshots/phase_2/test_results/report.html`
- Ảnh tổng hợp: `selenium_demo/docs/phase_2/TTGĐ2/SCREENSHOTS/03_pytest_result.png`,
  `04_html_report.png`
