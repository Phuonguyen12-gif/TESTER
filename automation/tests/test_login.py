"""
test_login.py - Kiểm thử chức năng Đăng nhập.

TC01: Đăng nhập hợp lệ          -> vào được trang Products
TC02: Đăng nhập sai mật khẩu    -> hiển thị thông báo lỗi
TC07: Đăng nhập user bị khóa    -> hiển thị thông báo lỗi tương ứng
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import PASSWORD, STANDARD_USER, TIMEOUT, login, wait_for


class TestLogin:
    def test_TC01_valid_login(self, driver):
        """TC01: Đăng nhập đúng username/password -> hiển thị trang sản phẩm."""
        login(driver, STANDARD_USER, PASSWORD)

        # Chờ URL chuyển sang trang inventory (explicit wait)
        WebDriverWait(driver, TIMEOUT).until(EC.url_contains("inventory"))

        assert "inventory" in driver.current_url
        title = wait_for(driver, (By.CLASS_NAME, "title"))
        assert title.text == "Products"
        # Trang sản phẩm phải có ít nhất 1 item
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(items) > 0

    def test_TC02_wrong_password(self, driver):
        """TC02: Đăng nhập sai mật khẩu -> hiển thị thông báo lỗi."""
        login(driver, STANDARD_USER, "wrong_password")

        error = WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Epic sadface" in error.text
        # Vẫn ở lại trang login, không vào được trang sản phẩm
        assert "inventory" not in driver.current_url

    def test_TC07_locked_out_user(self, driver):
        """TC07: Tài khoản bị khóa đăng nhập -> hiển thị thông báo lỗi."""
        login(driver, "locked_out_user", PASSWORD)

        error = WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Sorry, this user has been locked out" in error.text
