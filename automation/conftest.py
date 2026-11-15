"""
conftest.py - Cấu hình chung cho toàn bộ test suite.

- Fixture `driver`: khởi tạo / đóng Chrome WebDriver cho mỗi test.
- Fixture `logged_in_driver`: driver đã đăng nhập sẵn bằng tài khoản chuẩn.
- Hook `pytest_runtest_makereport`: tự động chụp screenshot khi test FAIL
  và đính kèm vào báo cáo HTML.
"""

from pathlib import Path

import pytest
from pytest_html import extras
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Đường dẫn gốc của repo TESTER (thư mục cha của automation/)
REPO_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = REPO_ROOT / "reports" / "screenshots"

BASE_URL = "https://www.saucedemo.com/"
TIMEOUT = 10  # giây - thời gian chờ tối đa cho explicit wait

# Tài khoản demo công khai do SauceDemo cung cấp (in ngay trên trang login)
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


def pytest_addoption(parser):
    """Thêm tùy chọn --headless: pytest --headless để chạy không mở cửa sổ."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Chạy Chrome ở chế độ headless (không hiển thị cửa sổ)",
    )


@pytest.fixture
def driver(request):
    """Khởi tạo Chrome WebDriver, mở trang login, đóng sau khi test xong."""
    options = webdriver.ChromeOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)

    yield driver

    driver.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Driver đã đăng nhập sẵn và đang ở trang Products."""
    login(driver, STANDARD_USER, PASSWORD)
    # Chờ trang Products render xong trước khi trả về cho test dùng
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("inventory"))
    wait_for(driver, (By.CLASS_NAME, "inventory_list"))
    return driver


def wait_for(driver, locator, timeout=TIMEOUT):
    """Chờ cho đến khi element hiển thị rồi trả về element đó (explicit wait)."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def click(driver, locator, timeout=TIMEOUT):
    """Chờ element hiển thị rồi click bằng JavaScript.

    SauceDemo phục vụ luân phiên 2 phiên bản giao diện (classic và bản
    redesign mới). Ở bản mới, click chuẩn của WebDriver đôi khi không
    được React xử lý; click qua JavaScript hoạt động trên cả 2 phiên bản.
    """
    element = wait_for(driver, locator, timeout)
    driver.execute_script("arguments[0].click();", element)
    return element


def type_text(driver, locator, text, timeout=TIMEOUT):
    """Nhập text vào ô input.

    Thử send_keys trước; nếu giá trị không được ghi nhận (xảy ra với
    controlled input của React ở bản UI mới) thì set value trực tiếp
    bằng JavaScript kèm sự kiện 'input' để React cập nhật state.
    """
    element = wait_for(driver, locator, timeout)
    element.clear()
    element.send_keys(text)
    if element.get_attribute("value") != text:
        driver.execute_script(
            """
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            setter.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
            """,
            element,
            text,
        )
    return element


def login(driver, username, password):
    """Điền form login và nhấn nút Login."""
    type_text(driver, (By.ID, "user-name"), username)
    type_text(driver, (By.ID, "password"), password)
    click(driver, (By.ID, "login-button"))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Sau mỗi test: nếu FAIL thì chụp screenshot làm bằng chứng."""
    outcome = yield
    report = outcome.get_result()

    # Chỉ xử lý ở phase "call" (thân test), bỏ qua setup/teardown
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get(
            "logged_in_driver"
        )
        if driver:
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            png_path = SCREENSHOT_DIR / f"{item.name}_FAILED.png"
            driver.save_screenshot(str(png_path))
            # Đính kèm ảnh vào báo cáo HTML (pytest-html)
            report_extras = getattr(report, "extras", [])
            report_extras.append(extras.image(str(png_path)))
            report.extras = report_extras
