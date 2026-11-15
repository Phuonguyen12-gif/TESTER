# TESTER

Đồ án môn Kiểm thử phần mềm — Tìm hiểu công cụ kiểm thử tự động Selenium.

## Cấu trúc

- `selenium_demo/` — Bộ test Selenium + pytest (kiến trúc Page Object Model)
  trên https://www.saucedemo.com/ — xem `selenium_demo/README.md`
- `docs/` — Tài liệu khảo sát chức năng, Test Case Draft, nội dung slide
- `reports/` — Kết quả thực thi giai đoạn 1: screenshots, logs, báo cáo HTML,
  `TV4_STAGE1_REPORT.md`

## Chạy nhanh

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r selenium_demo/requirements.txt
cd selenium_demo && pytest --headless
```
