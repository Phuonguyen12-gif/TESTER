# TESTER

Đồ án môn Kiểm thử phần mềm — Tìm hiểu công cụ kiểm thử tự động Selenium.

## Cấu trúc

- `automation/` — Bộ test Selenium + pytest trên https://www.saucedemo.com/
  (xem `automation/README.md` để cài đặt & chạy)
- `docs/` — Tài liệu khảo sát chức năng, Test Case Draft, nội dung slide
- `reports/` — Kết quả thực thi: screenshots, logs, báo cáo HTML,
  `TV4_STAGE1_REPORT.md`

## Chạy nhanh

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r automation/requirements.txt
cd automation && pytest --headless -v
```
