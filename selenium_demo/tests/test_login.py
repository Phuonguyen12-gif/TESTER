"""
test_login.py - Kiểm thử chức năng Đăng nhập.

TC01: Đăng nhập hợp lệ            -> hiển thị trang Products
TC02: Sai mật khẩu                -> hiển thị thông báo lỗi
TC03: Bỏ trống username           -> "Username is required"
TC04: Tài khoản locked_out_user   -> thông báo tài khoản bị khóa
TC09: Intentional failure demo    -> xfail mặc định, xem README
"""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.login_data import NEGATIVE_LOGIN_CASES, NEGATIVE_LOGIN_IDS, VALID_USER


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
                marks=pytest.mark.tc03,
            ),
            pytest.param(
                *NEGATIVE_LOGIN_CASES[2], id=NEGATIVE_LOGIN_IDS[2],
                marks=pytest.mark.tc04,
            ),
        ],
    )
    def test_TC02_TC04_invalid_login(self, driver, user, expected_error):
        """TC02/TC03/TC04: Đăng nhập thất bại -> thông báo lỗi phù hợp."""
        login_page = LoginPage(driver)
        login_page.login(user["username"], user["password"])

        assert expected_error in login_page.error_text()
        # Vẫn ở lại trang login, không vào được trang sản phẩm
        assert "inventory" not in driver.current_url

    @pytest.mark.tc09
    @pytest.mark.demo_fail
    @pytest.mark.xfail(
        reason="TC09: intentional failure demo — cố tình đặt expected "
               "title là 'Product' thay vì 'Products' để minh họa kết quả "
               "kiểm thử thất bại có chủ đích. "
               "Chạy FAIL thật: pytest -m demo_fail --runxfail"
    )
    def test_TC09_intentional_failure(self, driver):
        """TC09: Demo test thất bại CÓ CHỦ ĐÍCH (không phải lỗi website)."""
        login_page = LoginPage(driver)
        login_page.login(VALID_USER["username"], VALID_USER["password"])

        # CỐ TÌNH sai: title thực tế là "Products", expected đặt "Product"
        inventory_page = InventoryPage(driver)
        assert inventory_page.title_text() == "Product"
