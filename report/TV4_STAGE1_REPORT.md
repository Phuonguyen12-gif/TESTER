# TV4 — Báo cáo Giai đoạn 1
## Xây dựng môi trường và thử nghiệm Selenium WebDriver trên SauceDemo

**Ngày thực hiện:** 15/11/2026
**Phạm vi:** Nhiệm vụ A–F của TV4 (Thực thi kiểm thử, Demo và Báo cáo kết quả)

---

## 1. Tổng quan công việc

Đã xây dựng xong một bộ kiểm thử tự động **chạy thực tế** trên
https://www.saucedemo.com/ bằng Python + Selenium WebDriver + pytest:

- Khảo sát 10 chức năng chính của website (selenium_demo/docs/phase_1/TTGĐ1/SAUCEDEMO_FEATURES.md).
- Thiết lập môi trường trong virtual environment riêng của repo.
- Cài đặt 8 test case (TC01–TC08), chạy được cả headed lẫn headless.
- **Kết quả cuối cùng: 8/8 PASSED** sau 2 vòng sửa lỗi thực sự.
- Có screenshot minh họa (thành công lẫn thất bại), execution log,
  báo cáo HTML, Test Case Draft cho TV5 và nội dung slide nháp cho TV1.

## 2. Cấu hình môi trường

| Thành phần | Giá trị |
|---|---|
| OS | macOS 27.0.1, Apple Silicon |
| Python | 3.14.0 (`/Library/Frameworks/Python.framework/...`) |
| Virtual env | `TESTER/.venv` (riêng của repo, không cài global) |
| selenium | 4.52.0 |
| pytest | 9.2.0 |
| pytest-html | 4.2.0 |
| Trình duyệt | Google Chrome 157.0.8103.52 |
| ChromeDriver | Selenium Manager tự tải/quản lý — không cần cài tay |
| Website | https://www.saucedemo.com/ — HTTP 200, truy cập được |

Hướng dẫn cài đặt + chạy chi tiết: `automation/README.md`.
Log xác nhận môi trường: `selenium_demo/screenshots/phase_1/logs/pytest_run_3.log` (8 passed) và
`selenium_demo/screenshots/phase_1/logs/pytest_run_headed2.log` (8 passed, headed).

## 3. Chức năng đã khảo sát (Nhiệm vụ A)

Chi tiết đầy đủ ở `selenium_demo/docs/phase_1/TTGĐ1/SAUCEDEMO_FEATURES.md`. Tóm tắt:

Login, danh sách sản phẩm, xem chi tiết sản phẩm, thêm vào giỏ, xóa khỏi
giỏ, kiểm tra giỏ hàng, checkout, nhập thông tin khách hàng, hoàn tất đơn,
logout — kèm thao tác, kết quả mong đợi và tình huống lỗi cho từng chức
năng.

**Phát hiện đáng chú ý:** website phục vụ luân phiên **2 phiên bản UI**
(classic và redesign mới) — nguyên nhân chính gây khó khăn khi automation
(xem mục 8).

## 4. Cấu trúc source code

```
TESTER/
├── .gitignore
├── README.md
├── automation/
│   ├── conftest.py          # fixture driver, helper wait_for/click/type_text,
│   │                        # hook chụp screenshot khi FAIL
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── README.md            # hướng dẫn cài đặt & chạy
│   ├── capture_demo.py      # script chụp ảnh demo luồng nghiệp vụ
│   └── tests/
│       ├── test_login.py    # TC01, TC02, TC07
│       ├── test_cart.py     # TC03, TC04, TC06
│       └── test_checkout.py # TC05, TC08
├── selenium_demo/docs/phase_1/TTGĐ1/
│   ├── SAUCEDEMO_FEATURES.md
│   └── TV4_SLIDE_CONTENT.md
├── docs/TEST_CASE_FOR_TV5/
│   └── Test Case Draft — SauceDemo (BẢN NHÁP cho TV5 rà soát).md
└── reports/
    ├── TV4_STAGE1_REPORT.md (file này)
    ├── screenshots/
    │   ├── demo/            # 7 ảnh happy path chụp thật
    │   └── failed_runs/     # 6 ảnh FAIL thật ở các lần chạy đầu
    ├── logs/                # 5 file log pytest thực thi
    └── test_results/        # report.html (pytest-html)
```

## 5. Danh sách test case đã cài đặt

| ID | Test | File | Expected Result |
|---|---|---|---|
| TC01 | `test_TC01_valid_login` | test_login.py | Đăng nhập thành công, hiển thị trang Products |
| TC02 | `test_TC02_wrong_password` | test_login.py | Hiển thị lỗi "Epic sadface..." |
| TC03 | `test_TC03_add_to_cart` | test_cart.py | Badge giỏ = 1, đúng sản phẩm trong cart |
| TC04 | `test_TC04_remove_from_cart` | test_cart.py | Sản phẩm biến mất, giỏ trống |
| TC05 | `test_TC05_checkout_success` | test_checkout.py | Đơn hàng hoàn tất, "Thank you for your order!" |
| TC06 | `test_TC06_logout` | test_cart.py | Quay về trang login |
| TC07 | `test_TC07_locked_out_user` | test_login.py | Lỗi "user has been locked out" |
| TC08 | `test_TC08_checkout_missing_info` | test_checkout.py | Lỗi "Error: First Name is required" |

Kỹ thuật dùng: fixture setup/teardown, `WebDriverWait` + expected
conditions (không `sleep` tùy tiện), locator ổn định (ID/CSS/`data-test`),
helper `click`/`type_text` tương thích 2 phiên bản UI, screenshot tự động
khi FAIL qua hook `pytest_runtest_makereport`.

## 6. Kết quả thực thi thực tế (Nhiệm vụ D)

### Lịch sử các lần chạy (log thật trong `selenium_demo/screenshots/phase_1/logs/`)

| Lần chạy | Chế độ | Kết quả | Log |
|---|---|---|---|
| Run 1 | headless | 2 PASS / 6 FAIL | `pytest_run_1.log` |
| Run 2 | headless | 4 PASS / 4 FAIL | `pytest_run_2.log` |
| Run headed 1 | headed | 5 PASS / 3 FAIL | `pytest_run_headed.log` |
| **Run 3** | headless | **8 PASS / 0 FAIL** | `pytest_run_3.log` |
| **Run headed 2** | headed | **8 PASS / 0 FAIL** | `pytest_run_headed2.log` |

### Bảng kết quả cuối cùng (Run 3 — headless, 11.99s)

| Test Case | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|
| TC01 | Vào trang Products | URL `/inventory.html`, title "Products", 6 items | **PASS** | log `pytest_run_3.log`, `demo/02_products_page.png` |
| TC02 | Thông báo lỗi | "Epic sadface: Username and password do not match..." | **PASS** | log `pytest_run_3.log` |
| TC03 | Badge giỏ = 1, đúng SP | Badge "1", cart có Sauce Labs Backpack | **PASS** | `demo/03_added_to_cart.png`, `demo/04_cart_page.png` |
| TC04 | SP biến mất khỏi giỏ | `.cart_item` và badge không còn | **PASS** | log `pytest_run_3.log` |
| TC05 | Đơn hoàn tất | `/checkout-complete.html`, "Thank you for your order!" | **PASS** | `demo/07_order_complete.png` |
| TC06 | Về trang login | `login-button` hiển thị lại | **PASS** | log `pytest_run_3.log` |
| TC07 | Lỗi tài khoản khóa | "...has been locked out." | **PASS** | log `pytest_run_3.log` |
| TC08 | Lỗi thiếu thông tin | "Error: First Name is required" | **PASS** | log `pytest_run_3.log` |

Chạy lại ở headed mode (`pytest -v`, Chrome mở cửa sổ thật): **8/8 PASS,
13.00s** — `pytest_run_headed2.log`.

## 7. Screenshot và log

- **Ảnh demo thành công (7 ảnh, chụp thật bằng Selenium):**
  `selenium_demo/screenshots/phase_1/demo/01_login_page.png` → `07_order_complete.png`
- **Ảnh FAIL thật (tự động chụp khi test lỗi):**
  `selenium_demo/screenshots/phase_1/failed_runs/` — 6 ảnh từ các lần chạy đầu
- **Log thực thi:** `selenium_demo/screenshots/phase_1/logs/pytest_run_*.log` (5 file)
- **Báo cáo HTML:** `selenium_demo/screenshots/phase_1/test_results/report.html` (pytest-html)

## 8. Lỗi đã gặp và cách xử lý

| # | Triệu chứng | Phân loại | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|
| 1 | `pytest.extras` không tồn tại -> INTERNALERROR | Lỗi code automation | pytest-html 4.x đổi API | Import `extras` từ `pytest_html` |
| 2 | `NoSuchElementException` `.title`, `#add-to-cart-*` ngay sau login (Run 1) | Lỗi timing/wait | Dùng `find_element` ngay sau khi URL đổi, React chưa render | `wait_for` đổi sang `visibility_of_element_located`; fixture chờ `.inventory_list` trước khi test chạy |
| 3 | `StaleElementReferenceException` | Lỗi timing | React re-render element giữa chừng | Tìm lại element qua wait thay vì giữ reference |
| 4 | Click nút không tác động, `send_keys` không ghi vào checkout form (Run 2, headed 1) | Lỗi website (đặc thù bản UI mới) | SauceDemo serve luân phiên 2 UI; bản mới không xử lý click/keys chuẩn | Helper `click()` dùng JS click; `type_text()` fallback JS value setter + sự kiện `input` |

Không có test FAIL nào bị bỏ qua không giải thích; toàn bộ lỗi đã sửa và
chạy lại đạt 8/8.

## 9. Hạng mục chưa hoàn thành / hạn chế

- Chưa cài đặt test cho `problem_user`, `performance_glitch_user`,
  sort sản phẩm, trang chi tiết sản phẩm (đã khảo sát, có trong Test Case
  Draft cho TV5).
- Chưa tích hợp CI.
- Behavior "checkout với giỏ trống" của website chưa rõ expected result —
  đã đánh dấu trong Test Case Draft (BẢN NHÁP) chờ TV5/nhóm thống nhất.

## 10. Hướng phát triển Giai đoạn 2

- Mở rộng test: negative test đầy đủ hơn, kiểm tra tổng tiền + thuế ở
  trang Overview, sort/filter sản phẩm, `problem_user` (minh họa test phát
  hiện lỗi website).
- Data-driven test bằng `@pytest.mark.parametrize` cho nhiều tài khoản.
- Page Object Model nếu nhóm muốn nâng cấp kiến trúc (hiện giữ đơn giản
  theo yêu cầu dễ trình bày).
- Chạy trên CI (GitHub Actions) với headless.

---

## Bảng tổng kết Deliverable

| Deliverable | Status | Evidence/Path |
|---|---|---|
| Environment | **PASS** | `.venv`, `automation/requirements.txt`, log `pytest_run_3.log` dòng đầu ghi platform/python/pytest |
| Website Ready | **PASS** | SauceDemo HTTP 200; login thật thành công (`demo/02_products_page.png`) |
| Selenium Script | **PASS** | `automation/tests/` (3 file, 8 test), `automation/conftest.py` |
| pytest Execution | **PASS** | `selenium_demo/screenshots/phase_1/logs/pytest_run_3.log` (8 passed, headless), `pytest_run_headed2.log` (8 passed, headed), `selenium_demo/screenshots/phase_1/test_results/report.html` |
| Screenshots | **PASS** | `selenium_demo/screenshots/phase_1/demo/` (7 ảnh thành công), `selenium_demo/screenshots/phase_1/failed_runs/` (6 ảnh FAIL thật) |
| Test Case Draft | **PASS** | `docs/TEST_CASE_FOR_TV5/Test Case Draft — SauceDemo (BẢN NHÁP cho TV5 rà soát).md` (nháp cho TV5, có positive+negative mỗi chức năng) |
| Documentation | **PASS** | `automation/README.md`, `selenium_demo/docs/phase_1/TTGĐ1/SAUCEDEMO_FEATURES.md`, file này |
| Slide Content | **PASS** | `selenium_demo/docs/phase_1/TTGĐ1/TV4_SLIDE_CONTENT.md` + ảnh `demo/` |

**Ghi chú trung thực:** bộ test phụ thuộc website bên ngoài; SauceDemo có
thể đổi UI/phiên bản bất cứ lúc nào. Code đã viết tương thích cả 2 phiên
bản hiện có, nhưng nếu website thay đổi DOM (id/class) thì cần cập nhật
locator.
