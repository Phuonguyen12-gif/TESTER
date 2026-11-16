# TESTER

Đồ án môn Kiểm thử phần mềm — Tìm hiểu công cụ kiểm thử tự động Selenium.

## Cấu trúc

- `selenium_demo/` — Bộ test Selenium + pytest (kiến trúc Page Object Model)
  trên https://www.saucedemo.com/ — xem `selenium_demo/README.md`
- `docs/TEST_CASE_FOR_TV5/` — Bộ Test Cases chính thức + kết quả thực thi
  (bàn giao cho TV5)
- `selenium_demo/docs/phase_N/TTGĐN/` — Tài liệu theo giai đoạn
  (phase_1/TTGĐ1, phase_2/TTGĐ2, ...)
- `selenium_demo/screenshots/phase_N/` — Ảnh và minh chứng kiểm thử theo giai
  đoạn (demo, failed_runs, logs, test_results)
- `report/` — Báo cáo Markdown tổng hợp (chỉ chứa `.md`)

## Chạy nhanh

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r selenium_demo/requirements.txt
cd selenium_demo && pytest --headless
```
