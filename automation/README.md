# Automation — Selenium + pytest trên SauceDemo

Bộ kiểm thử tự động mẫu cho đồ án "Tìm hiểu công cụ kiểm thử tự động
Selenium". Website mục tiêu: https://www.saucedemo.com/

## Môi trường đã xác nhận chạy được

| Thành phần | Phiên bản |
|---|---|
| macOS | 27.0.1 (Apple Silicon) |
| Python | 3.14.0 |
| Google Chrome | 157.0.8103.52 |
| selenium | 4.52.0 |
| pytest | 9.2.0 |
| pytest-html | 4.2.0 |
| ChromeDriver | Tự động quản lý bởi Selenium Manager (không cần cài tay) |

## Cài đặt

```bash
cd TESTER
python3 -m venv .venv
source .venv/bin/activate
pip install -r automation/requirements.txt
```

## Chạy kiểm thử

```bash
cd automation

# Chạy toàn bộ suite (mở cửa sổ Chrome thật — phù hợp demo trực tiếp)
pytest -v

# Chạy headless (không mở cửa sổ, nhanh hơn)
pytest --headless -v

# Chạy 1 file / 1 test cụ thể
pytest tests/test_login.py -v
pytest tests/test_login.py::TestLogin::test_TC01_valid_login -v

# Chạy kèm báo cáo HTML
pytest --headless -v --html=../reports/test_results/report.html --self-contained-html
```

## Chụp ảnh demo luồng nghiệp vụ

```bash
cd TESTER
.venv/bin/python automation/capture_demo.py
# Ảnh lưu tại reports/screenshots/demo/
```

## Cấu trúc

```
automation/
├── conftest.py          # Fixture driver, helper wait_for/click/type_text,
│                        # hook chụp screenshot khi test FAIL
├── pytest.ini           # Cấu hình pytest (testpaths, pythonpath)
├── requirements.txt     # Dependencies
├── capture_demo.py      # Script chụp ảnh minh họa luồng nghiệp vụ
└── tests/
    ├── test_login.py    # TC01, TC02, TC07 — đăng nhập
    ├── test_cart.py     # TC03, TC04, TC06 — giỏ hàng & logout
    └── test_checkout.py # TC05, TC08 — checkout
```

## Ghi chú kỹ thuật quan trọng

SauceDemo hiện phục vụ luân phiên **2 phiên bản UI** (classic và redesign).
Bản mới có 2 đặc điểm khiến Selenium "chuẩn" không hoạt động:

1. `element.click()` không được React xử lý -> `conftest.click()` dùng
   `execute_script("arguments[0].click()")`.
2. `send_keys` không ghi vào checkout form (controlled input) ->
   `conftest.type_text()` thử `send_keys`, nếu thất bại thì set `value`
   bằng JavaScript và dispatch sự kiện `input`.

Cả 2 helper đều hoạt động trên cả 2 phiên bản UI.
Chi tiết: `docs/SAUCEDEMO_FEATURES.md` mục "Vấn đề phát hiện".
