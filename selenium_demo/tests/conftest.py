"""
conftest.py - Fixture dùng chung cho toàn bộ test suite.

- `driver`: khởi tạo / đóng Chrome WebDriver cho MỖI test (scope=function,
  đảm bảo độc lập; trình duyệt luôn được quit kể cả khi test fail).
- `inventory`: driver đã login sẵn, trả về InventoryPage tại trang Products.
- Hook `pytest_runtest_makereport`: test FAIL -> chụp screenshot vào
  screenshots/ và đính kèm vào báo cáo HTML.
"""

import pytest
from pytest_html import extras
from selenium import webdriver

from config import settings
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.login_data import VALID_USER
from utils.screenshot import save_failure_screenshot


def pytest_addoption(parser):
    """Tùy chọn --headless: ưu tiên hơn biến môi trường HEADLESS."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Chạy Chrome headless (không hiển thị cửa sổ)",
    )


@pytest.fixture
def driver(request):
    """Khởi tạo Chrome, mở trang login, đóng sau khi test xong."""
    headless = request.config.getoption("--headless") or settings.HEADLESS

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={settings.WINDOW_SIZE}")

    driver = webdriver.Chrome(options=options)
    driver.get(settings.BASE_URL)

    yield driver

    driver.quit()


@pytest.fixture
def inventory(driver):
    """Driver đã đăng nhập sẵn và đang ở trang Products (InventoryPage)."""
    login_page = LoginPage(driver)
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    inventory_page = InventoryPage(driver)
    inventory_page.is_loaded()  # chờ trang Products render xong
    return inventory_page


def _get_driver(item):
    """Lấy WebDriver từ fixture của test (qua driver hoặc page object)."""
    if "driver" in item.funcargs:
        return item.funcargs["driver"]
    for value in item.funcargs.values():
        if hasattr(value, "driver"):  # fixture trả về Page Object
            return value.driver
    return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Sau mỗi test: nếu FAIL thì chụp screenshot làm bằng chứng."""
    outcome = yield
    report = outcome.get_result()

    # Chỉ xử lý ở phase "call" (thân test), bỏ qua setup/teardown
    if report.when == "call" and report.failed:
        driver = _get_driver(item)
        if driver:
            png_path = save_failure_screenshot(driver, item.name)
            if png_path:
                # Đính kèm ảnh vào báo cáo HTML (pytest-html)
                report_extras = getattr(report, "extras", [])
                report_extras.append(extras.image(str(png_path)))
                report.extras = report_extras
