# Nội dung slide phần TV4 — Thực thi kiểm thử, Demo & Kết quả (BẢN NHÁP)

> Nội dung nháp để TV1 tổng hợp vào PowerPoint/Canva chung.
> Ảnh minh họa thật nằm trong `reports/screenshots/demo/` và
> `reports/screenshots/`.

---

## Slide 1 — Môi trường thực nghiệm

**Bullet:**

- Website kiểm thử: **SauceDemo** — https://www.saucedemo.com/
  (trang demo e-commerce chuyên cho thực hành automation, có sẵn tài khoản
  test công khai)
- Ngôn ngữ: **Python 3.14**
- Thư viện: **Selenium WebDriver 4.52**
- Test runner: **pytest 9.2** (+ pytest-html cho báo cáo)
- Trình duyệt: **Google Chrome 157** — ChromeDriver tự động quản lý bởi
  Selenium Manager
- Hệ điều hành: macOS (Apple Silicon)

**Hình gợi ý:** `reports/screenshots/demo/01_login_page.png` (trang login
SauceDemo hiển thị sẵn danh sách tài khoản test).

---

## Slide 2 — Quy trình thực thi kiểm thử

**Sơ đồ/bullet:**

1. `conftest.py` khởi tạo **Chrome WebDriver** (fixture) -> mở trang login
2. Test thực hiện thao tác qua **locator ổn định** (ID, CSS selector,
   `data-test`)
3. Đồng bộ bằng **WebDriverWait + expected conditions** (explicit wait,
   không dùng `sleep` cố định)
4. **Assertion** so sánh kết quả thực tế với Expected Result
5. Fixture **teardown** đóng trình duyệt; nếu test FAIL -> tự động chụp
   **screenshot** làm bằng chứng
6. `pytest` tổng hợp kết quả -> báo cáo HTML

**Code tiêu biểu (đưa lên slide):**

```python
def test_TC01_valid_login(self, driver):
    login(driver, STANDARD_USER, PASSWORD)
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("inventory"))
    assert "inventory" in driver.current_url
    title = wait_for(driver, (By.CLASS_NAME, "title"))
    assert title.text == "Products"
```

---

## Slide 3 — Demo kiểm thử

**Nội dung:**

- Video/quay màn hình hoặc chạy trực tiếp: `pytest -v` (mở Chrome thật,
  thao tác như người dùng)
- Chuỗi ảnh happy path (đã chụp sẵn):
  - `demo/02_products_page.png` — trang sản phẩm sau login
  - `demo/03_added_to_cart.png` — badge giỏ hàng = 1 sau Add to cart
  - `demo/04_cart_page.png` — trang giỏ hàng
  - `demo/06_checkout_overview.png` — tổng quan đơn + thuế
  - `demo/07_order_complete.png` — "Thank you for your order!"
- Điểm kỹ thuật đáng kể (nên nói khi demo): SauceDemo có 2 phiên bản UI
  luân phiên -> phải xử lý click bằng JavaScript và nhập liệu qua
  JS value setter (minh họa tình huống thực tế của automation engineer).

---

## Slide 4 — Kết quả kiểm thử

**Bảng kết quả (lấy từ log thực thi thật):**

| Test | Nội dung | Kết quả |
|---|---|---|
| TC01 | Đăng nhập hợp lệ | PASS |
| TC02 | Đăng nhập sai mật khẩu | PASS |
| TC03 | Thêm sản phẩm vào giỏ | PASS |
| TC04 | Xóa sản phẩm khỏi giỏ | PASS |
| TC05 | Checkout hợp lệ | PASS |
| TC06 | Logout | PASS |
| TC07 | Tài khoản bị khóa | PASS |
| TC08 | Checkout thiếu thông tin | PASS |

**Tổng kết:** 8/8 test PASSED — chạy được cả headed (có cửa sổ) lẫn
headless. Log: `reports/logs/pytest_run_3.log`, báo cáo HTML:
`reports/test_results/report.html`.

**Nhận xét/hạn chế để nói trên slide:**

- Website serve 2 phiên bản UI không dự đoán trước -> bài học về độ
  ổn định của locator và cơ chế chờ.
- Ở lần chạy đầu có 6 test FAIL do lỗi timing/locator -> đã phân tích,
  sửa bằng explicit wait + JS interaction, chạy lại đạt 8/8.
  (Ảnh fail thật lưu ở `reports/screenshots/failed_runs/` — có thể dùng
  để minh họa "test FAIL -> debug -> PASS".)
- Hạn chế: chưa test `problem_user`/`performance_glitch_user`, chưa đo
  hiệu năng, chưa chạy trên CI.
