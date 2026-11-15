"""
screenshot.py - Chụp ảnh màn hình khi test thất bại.

File ảnh có timestamp trong tên để không bị ghi đè giữa các lần chạy.
Mọi lỗi khi chụp đều được nuốt (chỉ cảnh báo) để không che mất lỗi gốc
của test.
"""

from datetime import datetime
from pathlib import Path

from config import settings


def save_failure_screenshot(driver, test_name, directory=None):
    """Chụp screenshot, lưu vào screenshots/. Trả về Path hoặc None nếu lỗi."""
    directory = Path(directory or settings.SCREENSHOT_DIR)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = directory / f"{test_name}_{timestamp}_FAILED.png"
        driver.save_screenshot(str(path))
        return path
    except Exception as exc:  # noqa: BLE001 - cố tình nuốt lỗi chụp ảnh
        print(f"\n[screenshot] Không chụp được ảnh cho {test_name}: {exc}")
        return None
