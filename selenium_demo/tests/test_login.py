"""
test_login.py - Kiểm thử chức năng Đăng nhập.

TC01: Đăng nhập hợp lệ          -> vào được trang Products
TC02: Đăng nhập sai mật khẩu    -> hiển thị thông báo lỗi
TC07: Đăng nhập user bị khóa    -> hiển thị thông báo lỗi tương ứng
TC09: Intentional failure demo  -> xfail mặc định, xem README
"""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.login_data import (
    LOCKED_USER,
    NEGATIVE_LOGIN_CASES,
    NEGATIVE_LOGIN_IDS,
    VALID_USER,
    WRONG_PASSWORD_USER,
)


@pytest.mark.login
class TestLogin:
    @pytest.mark.tc01
    def test_TC01_valid_login(self, driver):
        """TC01: Đăng nhập đúng username/password -> hiển thị trang sản phẩm."""
        login_page = LoginPage(driver)
        login_page.login(VALID_USER["username"], VALID_USER["password"])

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()
        assert inventory_page.title_text() == "Products"
        assert inventory_page.product_count() > 0

    @pytest.mark.parametrize(
        "user,expected_error",
        [
            pytest.param(
                *NEGATIVE_LOGIN_CASES[0], id=NEGATIVE_LOGIN_IDS[0],
                marks=pytest.mark.tc02,
            ),
            pytest.param(
                *NEGATIVE_LOGIN_CASES[1], id=NEGATIVE_LOGIN_IDS[1],
                marks=pytest.mark.tc07,
            ),
        ],
    )
    def test_TC02_TC07_invalid_login(self, driver, user, expected_error):
        """TC02/TC07: Đăng nhập thất bại -> hiển thị thông báo lỗi phù hợp."""
        login_page = LoginPage(driver)
        login_page.login(user["username"], user["password"])

        assert expected_error in login_page.error_text()
        # Vẫn ở lại trang login, không vào được trang sản phẩm
        assert "inventory" not in driver.current_url

    @pytest.mark.tc09
    @pytest.mark.demo_fail
    @pytest.mark.xfail(
        reason="TC09: intentional failure demo — cố tình sai expected "
               "result để minh họa FAIL + screenshot. "
               "Chạy riêng: pytest -m demo_fail --runxfail"
    )
    def test_TC09_intentional_failure(self, driver):
        """TC09: Demo test cố tình FAIL (expected title sai có chủ đích)."""
        login_page = LoginPage(driver)
        login_page.login(VALID_USER["username"], VALID_USER["password"])

        # CỐ TÌNH sai: title thật là "Products", không phải "Dashboard"
        inventory_page = InventoryPage(driver)
        assert inventory_page.title_text() == "Dashboard"
