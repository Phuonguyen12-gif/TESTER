"""
settings.py - Cấu hình tập trung của project.

Mọi giá trị phụ thuộc môi trường đều đọc ở đây, có thể override bằng
biến môi trường hoặc file .env (xem .env.example).
Không hardcode credentials ở đây — test data nằm trong test_data/.
"""

import os
from pathlib import Path

# Nạp file .env nếu có python-dotenv (không bắt buộc)
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

# Thư mục gốc của module selenium_demo
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"
REPORT_DIR = PROJECT_ROOT / "reports"


def _env_bool(name, default=False):
    """Đọc biến môi trường dạng boolean."""
    return os.environ.get(name, str(default)).strip().lower() in (
        "1", "true", "yes", "on",
    )


# --- Cấu hình chính (override bằng env vars / .env) ---
BASE_URL = os.environ.get("BASE_URL", "https://www.saucedemo.com/")
BROWSER = os.environ.get("BROWSER", "chrome")
HEADLESS = _env_bool("HEADLESS", False)
TIMEOUT = int(os.environ.get("TIMEOUT", "10"))  # explicit wait, giây
WINDOW_SIZE = os.environ.get("WINDOW_SIZE", "1280,900")  # "width,height"
