# selenium_demo — Selenium + pytest trên SauceDemo (kiến trúc POM)

Bộ kiểm thử tự động cho đồ án "Tìm hiểu công cụ kiểm thử tự động Selenium".
Website mục tiêu: https://www.saucedemo.com/

Đây là bản refactor của module `automation/` cũ sang kiến trúc
**Page Object Model**: tách cấu hình, page objects, test data, test logic
và utilities.

## Cấu trúc thư mục

```
selenium_demo/
├── config/settings.py    # Cấu hình tập trung (BASE_URL, timeout, headless...)
├── pages/                # Page Object Model
│   ├── base_page.py      #   wait/click/type_text dùng chung (+ workaround 2 UI)
│   ├── login_page.py     #   form login + thông báo lỗi
│   ├── inventory_page.py #   danh sách sản phẩm, giỏ hàng, menu
│   ├── cart_page.py      #   giỏ hàng: item, remove, checkout
│   └── checkout_page.py  #   3 bước checkout: info -> overview -> complete
├── tests/                # Test layer (assertion nằm ở đây)
│   ├── conftest.py       #   fixture driver/inventory + hook screenshot FAIL
│   ├── test_login.py     #   TC01, TC02, TC07, TC09(demo xfail)
│   ├── test_cart.py      #   TC03, TC04, TC06
│   └── test_checkout.py  #   TC05, TC08
├── test_data/            # Test data tách khỏi logic
│   ├── login_data.py     #   tài khoản demo + dataset negative
│   └── checkout_data.py  #   thông tin checkout hợp lệ
├── utils/screenshot.py   # Chụp ảnh khi FAIL (tên file có timestamp)
├── screenshots/          # Ảnh FAIL tự động lưu tại đây
├── reports/              # report.html sinh ra tại đây
├── .env.example          # Template biến môi trường
├── pytest.ini            # testpaths, HTML report, markers TC01–TC09
└── requirements.txt
```

## Cài đặt

```bash
cd TESTER                                   # thư mục gốc repo
python3 -m venv .venv && source .venv/bin/activate
pip install -r selenium_demo/requirements.txt
```

Môi trường đã xác nhận: Python 3.14, Chrome 157, selenium 4.52,
pytest 9.2, pytest-html 4.2. ChromeDriver do Selenium Manager tự quản lý.

## Cấu hình trình duyệt

Mặc định chạy Chrome có cửa sổ (headed) — phù hợp demo trực tiếp.
Override bằng biến môi trường hoặc file `.env` (copy từ `.env.example`):

```bash
cp .env.example .env   # rồi sửa HEADLESS=true, TIMEOUT, BASE_URL...
```

## Chạy kiểm thử

```bash
cd selenium_demo

# Toàn bộ suite thường (8 test: TC01–TC08; TC09 là xfail demo)
pytest

# Chạy headless
pytest --headless

# Theo nhóm chức năng
pytest -m login
pytest -m cart
pytest -m checkout

# Theo Test Case ID riêng lẻ
pytest -m tc01
pytest -m tc05

# Một test cụ thể
pytest tests/test_login.py::TestLogin::test_TC01_valid_login
```

## TC09 — Intentional failure demonstration

`test_TC09_intentional_failure` cố tình assert sai ("Dashboard" thay vì
"Products") để minh họa cơ chế FAIL + screenshot. Mặc định nó được đánh
dấu `xfail` nên **không tính là lỗi sản phẩm** trong suite thường
(kết quả hiển thị là XFAIL).

Để xem nó FAIL thật kèm screenshot + đính kèm ảnh vào HTML report:

```bash
pytest -m demo_fail --runxfail
# hoặc: pytest -m tc09 --runxfail
```

## Kết quả & bằng chứng

- **HTML report:** `reports/report.html` (tự sinh mỗi lần chạy, self-contained)
- **Screenshot khi FAIL:** `screenshots/<test>_<timestamp>_FAILED.png`

## Ghi chú kỹ thuật

SauceDemo phục vụ luân phiên 2 phiên bản UI (classic/redesign). Bản mới
không xử lý `click()`/`send_keys` chuẩn -> `pages/base_page.py` dùng
JS click và JS value setter làm fallback, hoạt động trên cả 2 phiên bản.
Không dùng `time.sleep()` — mọi chờ đều qua `WebDriverWait`.
