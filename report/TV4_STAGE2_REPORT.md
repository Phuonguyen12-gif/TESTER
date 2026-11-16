# TV4 — Báo cáo Giai đoạn 2
## Refactor kiến trúc Page Object Model, đồng bộ TC01–TC09 và hoàn thiện bộ tài liệu bàn giao

**Ngày thực hiện:** 15–16/11/2026
**Phạm vi:** Refactor `automation/` → `selenium_demo/` (POM), đồng bộ bộ Test Case
với mapping chính thức TC01–TC09, chạy kiểm chứng ổn định 3 lần, chuẩn bị toàn bộ
tài liệu bàn giao cho TV5/TV1, chuẩn hóa cấu trúc tài liệu và minh chứng theo
giai đoạn.

---

## 1. Tổng quan công việc

Giai đoạn 2 nâng bộ kiểm thử Giai đoạn 1 (thư mục phẳng `automation/`) lên
kiến trúc **Page Object Model** hoàn chỉnh và đồng bộ bộ Test Case với bảng
mapping chính thức TC01–TC09 của nhóm:

- Refactor toàn bộ sang `selenium_demo/`: tách `config/`, `pages/`, `tests/`,
  `test_data/`, `utils/` — locator và thao tác UI đóng gói trong Page Class,
  assertion tập trung trong test.
- Cài đặt lại mapping test theo bảng TC01–TC09 chính thức (thêm TC03 trống
  username, TC04 locked_out_user, sửa TC08 thành trống Postal Code); logout
  giữ lại làm test bổ sung ngoài bộ TC.
- Áp dụng `pytest.mark.parametrize` cho TC02–TC04 (vẫn traceable qua ID
  `[TC02]`/`[TC03]`/`[TC04]`).
- Thêm **TC09** — test thất bại có chủ đích, đánh dấu `xfail`: suite thường
  báo `xfailed` (exit 0), chạy `--runxfail` thì TC09 FAIL thật kèm screenshot.
- **Kết quả cuối cùng: 9 PASSED + 1 XFAIL, ổn định qua 3 lần chạy headless**
  (14.87s / 16.62s / 16.94s), không flake.
- Hoàn thiện bộ tài liệu: báo cáo thực thi, Excel kết quả cho TV5, nội dung +
  kịch bản thuyết trình slide 18–22, khó khăn & giải pháp cho TV1.
- Chuẩn hóa cấu trúc tài liệu `docs/phase_N/TTGĐN/` và minh chứng
  `screenshots/phase_N/` cho toàn dự án.

## 2. Cấu hình môi trường

| Thành phần | Giá trị |
|---|---|
| OS | macOS 27.0.1, Apple Silicon |
| Python | 3.14.0 |
| Virtual env | `TESTER/.venv` (giữ nguyên từ Giai đoạn 1) |
| selenium | 4.52.0 |
| pytest | 9.2.0 |
| pytest-html | 4.2.0 |
| pytest-metadata | 3.1.1 |
| python-dotenv | 1.2.1 (**mới** — đọc cấu hình từ `.env`) |
| openpyxl / Pillow | 3.1.5 / 13.0.0 (**mới** — công cụ tạo Excel và ảnh tài liệu, không thuộc runtime test) |
| Trình duyệt | Google Chrome 157.0.8103.52 |
| ChromeDriver | Selenium Manager tự quản lý |
| Website | https://www.saucedemo.com/ |

Khác biệt so với Giai đoạn 1: cấu hình tập trung vào
`selenium_demo/config/settings.py`, hỗ trợ biến môi trường qua `.env`
(có `.env.example`, `.env` thật bị gitignore); chế độ headless điều khiển
bằng cờ `--headless` của pytest thay vì sửa code.

## 3. Chức năng và phạm vi kiểm thử

Bộ test vẫn bám các chức năng đã khảo sát ở Giai đoạn 1 nhưng **mapping TC
được cài đặt lại theo bảng chính thức của nhóm**:

- **Login:** hợp lệ (TC01), sai mật khẩu (TC02), trống username (TC03),
  locked_out_user (TC04) — 3 negative case chạy qua parametrize.
- **Giỏ hàng:** thêm sản phẩm (TC05), xóa sản phẩm (TC06); logout là test
  bổ sung ngoài bộ TC.
- **Checkout:** luồng đầy đủ đến "Thank you for your order!" (TC07),
  negative trống Postal Code (TC08).
- **Demo failure:** TC09 cố tình kỳ vọng title `Product` trong khi title
  thực tế là `Products` — dùng minh họa cơ chế xfail/fail của pytest,
  **không phải lỗi của SauceDemo**.

Khác biệt Giai đoạn 1 → 2: bổ sung TC03, TC04, TC08 đúng spec (Stage 1 chưa
có TC03/TC04 theo mapping mới và TC08 check thiếu First Name); thêm TC09;
TC05/TC06/TC07 đổi nghĩa theo mapping mới (Stage 1: TC03=add cart,
TC04=remove, TC05=checkout).

## 4. Cấu trúc source code

```
TESTER/
├── README.md
├── report/
│   ├── TV4_STAGE1_REPORT.md
│   ├── TV4_STAGE2_REPORT.md        # file này
│   └── DOCUMENTATION_RESTRUCTURE_REPORT.md
├── docs/
│   └── TEST_CASE_FOR_TV5/          # bàn giao TV5
│       ├── Test Case Draft — SauceDemo (BẢN NHÁP cho TV5 rà soát).md
│       ├── TEST_CASES_FINAL.md
│       ├── TEST_CASES_FINAL.xlsx
│       └── TEST_EXECUTION_RESULTS.xlsx
└── selenium_demo/
    ├── config/settings.py          # BASE_URL, timeout, headless, đọc .env
    ├── pages/                      # Page Object Model
    │   ├── base_page.py            # WebDriverWait + EC, click/type có
    │   │                           # fallback JS cho bản UI redesign
    │   ├── login_page.py
    │   ├── inventory_page.py
    │   ├── cart_page.py
    │   └── checkout_page.py
    ├── tests/
    │   ├── conftest.py             # fixture driver (function-scope, quit
    │   │                           # luôn chạy), fixture inventory đã login,
    │   │                           # hook chụp screenshot khi FAIL
    │   ├── test_login.py           # TC01, TC02–TC04 (parametrize), TC09
    │   ├── test_cart.py            # TC05, TC06, logout bổ sung
    │   └── test_checkout.py        # TC07, TC08
    ├── test_data/                  # tách dữ liệu khỏi logic test
    │   ├── login_data.py
    │   └── checkout_data.py
    ├── utils/screenshot.py         # chụp ảnh timestamped + attach pytest-html
    ├── capture_demo.py             # script chụp ảnh demo luồng nghiệp vụ
    ├── pytest.ini                  # testpaths, addopts --html, markers tc01–tc09
    ├── requirements.txt
    ├── .env.example / .gitignore
    ├── docs/
    │   ├── phase_1/TTGĐ1/          # tài liệu giai đoạn 1
    │   └── phase_2/TTGĐ2/          # báo cáo + thuyết trình giai đoạn 2
    └── screenshots/
        ├── phase_1/                # minh chứng giai đoạn 1 (20 file)
        └── phase_2/                # minh chứng giai đoạn 2 (xem mục 7)
```

## 5. Danh sách test case đã cài đặt

| ID | Test | File | Expected Result |
|---|---|---|---|
| TC01 | `test_TC01_valid_login` | test_login.py | Đăng nhập thành công, hiển thị trang Products |
| TC02 | `test_TC02_TC04_invalid_login[TC02]` | test_login.py | Lỗi "Epic sadface: Username and password do not match..." |
| TC03 | `test_TC02_TC04_invalid_login[TC03]` | test_login.py | Lỗi "Username is required" |
| TC04 | `test_TC02_TC04_invalid_login[TC04]` | test_login.py | Lỗi "...has been locked out" |
| TC05 | `test_TC05_add_to_cart` | test_cart.py | Badge giỏ = 1 |
| TC06 | `test_TC06_remove_from_cart` | test_cart.py | Giỏ hàng trở về trống |
| TC07 | `test_TC07_checkout_success` | test_checkout.py | "Thank you for your order!" |
| TC08 | `test_TC08_checkout_missing_postal_code` | test_checkout.py | Lỗi "Postal Code is required" |
| TC09 | `test_TC09_intentional_failure` | test_login.py | Thất bại có chủ đích (expected "Product" vs actual "Products"), `xfail` |
| — | `test_logout` | test_cart.py | Bổ sung ngoài bộ TC: quay về trang login |

pytest thu thập **10 test item** cho 9 TC logic (TC02–TC04 là 3 param của
một hàm parametrize) + 1 test bổ sung logout.

Kỹ thuật dùng: POM (locator + thao tác trong Page Class), fixture
function-scope với `driver.quit()` trong teardown, `WebDriverWait` +
expected conditions (không `sleep`), parametrize cho negative login,
marker `tc01`–`tc09` + `demo_fail`, `pytest.mark.xfail` cho TC09,
screenshot tự động khi FAIL qua `pytest_runtest_makereport`.

## 6. Kết quả thực thi thực tế

### Lịch sử các lần chạy (log thật trong `selenium_demo/screenshots/phase_2/logs/`)

| Lần chạy | Chế độ | Kết quả | Thời gian | Log |
|---|---|---|---|---|
| Run 1 | headless | 9 PASS / 1 XFAIL / 0 FAIL | 16.94s | `run_1.log` |
| Run 2 | headless | 9 PASS / 1 XFAIL / 0 FAIL | 14.87s | `run_2.log` |
| Run 3 | headless | 9 PASS / 1 XFAIL / 0 FAIL | 16.62s | `run_3.log` |
| TC09 demo | headless, `-m demo_fail --runxfail` | TC09 **FAIL thật** (exit ≠ 0) + screenshot | — | `phase_2/failed_runs/test_TC09_..._FAILED.png` |

Ngoài ra trong quá trình validate refactor, suite cũng được chạy ở headed
mode (mở Chrome thật) và chạy theo nhóm marker (`-m "cart or checkout"`,
5 passed) — kết quả khớp headless; log các lần này không được lưu file
riêng nên chỉ ghi nhận mô tả, không trích số liệu chi tiết.

### Bảng kết quả chi tiết (đồng nhất cả 3 lần chạy)

| Test Case | Expected Result | Actual Result | Status | Evidence |
|---|---|---|---|---|
| TC01 | Vào trang Products | URL `/inventory.html`, title "Products" | **PASS** | `logs/run_*.log`, `demo/02_products_page.png` |
| TC02 | Thông báo lỗi đăng nhập | "Epic sadface: ...do not match..." | **PASS** | `logs/run_*.log` |
| TC03 | "Username is required" | Đúng thông báo | **PASS** | `logs/run_*.log` |
| TC04 | Tài khoản bị khóa | "...has been locked out" | **PASS** | `logs/run_*.log` |
| TC05 | Badge giỏ = 1 | Badge "1" sau khi add | **PASS** | `demo/03_added_to_cart.png` |
| TC06 | Giỏ trở về trống | `.cart_item` không còn | **PASS** | `logs/run_*.log` |
| TC07 | Đơn hoàn tất | `/checkout-complete.html`, "Thank you for your order!" | **PASS** | `demo/07_order_complete.png` |
| TC08 | "Postal Code is required" | Đúng thông báo | **PASS** | `logs/run_*.log` |
| TC09 | Thất bại có chủ đích | XFAIL trong suite; FAIL thật khi `--runxfail` | **XFAIL** | `failed_runs/test_TC09_..._FAILED.png` |
| logout | Về trang login | `login-button` hiển thị lại | **PASS** | `logs/run_*.log` |

**Tổng kết:** 10 collected → **9 passed, 1 xfailed**, 0 failed, 0 skipped —
đồng nhất 3/3 lần, không flaky test.

## 7. Screenshot và log

- **Ảnh demo thành công (7 ảnh, chụp thật bằng `capture_demo.py` trên bản POM):**
  `selenium_demo/screenshots/phase_2/demo/01_login_page.png` → `07_order_complete.png`
- **Ảnh FAIL thật (TC09 chạy `--runxfail`):**
  `selenium_demo/screenshots/phase_2/failed_runs/test_TC09_intentional_failure_20261115_233434_FAILED.png`
- **Log thực thi:** `selenium_demo/screenshots/phase_2/logs/run_{1,2,3}.log`
- **Báo cáo HTML:** `selenium_demo/screenshots/phase_2/test_results/report.html`
  (pytest-html, self-contained — mở trực tiếp bằng trình duyệt)
- **Ảnh minh họa cho slide:** `selenium_demo/docs/phase_2/TTGĐ2/SCREENSHOTS/`
  (4 ảnh: cấu trúc project, code base_page, kết quả pytest, HTML report)

## 8. Lỗi đã gặp và cách xử lý

| # | Triệu chứng | Phân loại | Nguyên nhân | Cách xử lý |
|---|---|---|---|---|
| 1 | Mapping TC trong code lệch bảng TC01–TC09 chính thức của nhóm | Lỗi yêu cầu/spec | Giai đoạn 1 đặt tên TC theo mapping cũ | Cài đặt lại: thêm TC03/TC04, sửa TC08 thành Postal Code, remap cart/checkout; logout giữ làm test bổ sung |
| 2 | PIL default font không hiển thị dấu tiếng Việt khi render ảnh minh họa | Lỗi công cụ tài liệu | Pillow bitmap font không có glyph Unicode | Generate lại ảnh với tiêu đề ASCII-safe |
| 3 | Tham chiếu đường dẫn cũ còn sót sau khi di chuyển tài liệu | Lỗi tổ chức tài liệu | Đổi cấu trúc `docs/` và `screenshots/` nhiều lần | Quét `grep` toàn repo, cập nhật 8 file `.md` + 108 ô evidence trong 2 file `.xlsx`; verify sạch refs cũ |
| 4 | `.gitignore` `screenshots/**/*.png` chặn luôn evidence `phase_N/` | Lỗi cấu hình Git | Pattern quá rộng | Thu hẹp còn `screenshots/*.png` + `screenshots/demo/`; verify bằng `git check-ignore` |

Không phát sinh lỗi runtime nào trong 3 lần chạy Giai đoạn 2 — các workaround
click/type JS từ Giai đoạn 1 được giữ nguyên trong `BasePage` và hoạt động
ổn định trên cả hai phiên bản UI của SauceDemo.

## 9. Hạng mục chưa hoàn thành / hạn chế

- Chưa cài đặt test cho `problem_user`, `performance_glitch_user`, sort
  sản phẩm, trang chi tiết sản phẩm, kiểm tra tổng tiền + thuế ở trang
  Overview (đã liệt kê trong Test Case Draft chờ TV5 rà soát).
- Chưa tích hợp CI/CD (GitHub Actions).
- Log lần chạy headed và lần chạy theo marker trong quá trình validate
  refactor không được lưu file — chỉ có mô tả, không trích dẫn số liệu.
- Slide 18–22 mới dừng ở nội dung + kịch bản + ảnh nguồn; **thiết kế trên
  Canva là việc TV4/TV1 tự thực hiện**.
- TC09 là test minh họa cơ chế pytest, không phải lỗi website — cần giữ
  đúng cách diễn giải khi thuyết trình.

## 10. Hướng phát triển giai đoạn tiếp theo

- Mở rộng coverage theo Test Case Draft sau khi TV5 rà soát: sort/filter,
  chi tiết sản phẩm, verify tổng tiền + thuế ở Checkout Overview, các tài
  khoản đặc biệt.
- Data-driven mở rộng: thêm dataset cho checkout negative (thiếu First
  Name, thiếu Last Name) qua parametrize hiện có.
- Chạy trên CI (GitHub Actions) với headless + upload HTML report làm
  artifact; badge kết quả trên README.
- Mở rộng marker/miền test theo tính năng khi bộ TC của nhóm tăng.

---

## Bảng tổng kết Deliverable

| Deliverable | Status | Evidence/Path |
|---|---|---|
| POM Refactor | **PASS** | `selenium_demo/` — `pages/` (5 file), `tests/` (4 file), `config/`, `test_data/`, `utils/`; commit `8878077` |
| Đồng bộ TC01–TC09 | **PASS** | `selenium_demo/tests/`, `test_data/`; mapping khớp `docs/TEST_CASE_FOR_TV5/TEST_CASES_FINAL.md` |
| Pytest Execution (×3) | **PASS** | `selenium_demo/screenshots/phase_2/logs/run_{1,2,3}.log` — 9 passed, 1 xfailed mỗi lần |
| TC09 xfail/fail demo | **PASS** | `pytest -m demo_fail --runxfail` → FAIL thật; ảnh `phase_2/failed_runs/` |
| HTML Report | **PASS** | `selenium_demo/screenshots/phase_2/test_results/report.html` |
| Screenshots | **PASS** | `phase_2/demo/` (7 ảnh), `phase_2/failed_runs/` (1 ảnh), `docs/phase_2/TTGĐ2/SCREENSHOTS/` (4 ảnh) |
| Báo cáo Giai đoạn 2 | **PASS** | `selenium_demo/docs/phase_2/TTGĐ2/PHASE_2_PROGRESS_REPORT.md`, `TEST_EXECUTION_REPORT.md` |
| Excel cho TV5 | **PASS** | `docs/TEST_CASE_FOR_TV5/` (3 file) + `phase_2/TTGĐ2/TEST_CASE_RESULTS_FOR_TV5.xlsx` — TC01–TC08 PASSED ×3, TC09 XFAIL ×3 |
| Slide content + script | **PASS** | `selenium_demo/docs/phase_2/TTGĐ2/PRESENTATION_CONTENT_TV4.md` (slide 18–22), `PRESENTATION_SCRIPT_TV4.md` (~4 phút) |
| Khó khăn & giải pháp | **PASS** | `selenium_demo/docs/phase_2/TTGĐ2/QA_DIFFICULTIES_AND_SOLUTIONS.md` |
| Chuẩn hóa tài liệu | **PASS** | `docs/phase_N/TTGĐN/`, `screenshots/phase_N/`, `report/` chỉ `.md`; chi tiết `report/DOCUMENTATION_RESTRUCTURE_REPORT.md` |
| Git publish | **PASS** | `feat/tv4-selenium-automation` @ `eef1801`, working tree clean, `main` không đổi |

**Ghi chú trung thực:** kết quả phụ thuộc website bên ngoài; SauceDemo có
thể đổi UI bất cứ lúc nào. Bộ test chạy ổn định 3/3 lần trên cả hai phiên
bản UI hiện có nhờ helper tương thích trong `BasePage`, nhưng nếu website
thay đổi DOM (id/class) thì cần cập nhật locator tương ứng.
