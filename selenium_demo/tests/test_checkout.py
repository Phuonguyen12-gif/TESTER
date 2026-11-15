"""
test_checkout.py - Kiểm thử chức năng Checkout.

TC05: Checkout hợp lệ           -> hoàn tất đơn hàng thành công
TC08: Checkout thiếu thông tin  -> hiển thị thông báo lỗi
"""

import pytest

from test_data.checkout_data import VALID_CHECKOUT

BACKPACK = "sauce-labs-backpack"


@pytest.mark.checkout
class TestCheckout:
    @pytest.mark.tc05
    def test_TC05_checkout_success(self, inventory):
        """TC05: Điền đủ thông tin -> đơn hàng hoàn tất thành công."""
        inventory.add_to_cart(BACKPACK)
        cart = inventory.open_cart()
        checkout = cart.checkout()

        # Bước 1: điền thông tin khách hàng -> Continue
        checkout.fill_info(**VALID_CHECKOUT)
        checkout.continue_to_overview()

        # Bước 2: trang Overview -> Finish
        assert checkout.at_overview()
        checkout.finish()

        # Kết quả mong đợi: trang Complete + thông báo cảm ơn
        assert checkout.is_complete()

    @pytest.mark.tc08
    def test_TC08_checkout_missing_info(self, inventory):
        """TC08: Bỏ trống thông tin bắt buộc -> hiển thị thông báo lỗi."""
        inventory.add_to_cart(BACKPACK)
        cart = inventory.open_cart()
        checkout = cart.checkout()

        # Không điền gì, nhấn Continue luôn
        checkout.continue_to_overview()

        assert "Error" in checkout.error_text()
        # Vẫn ở lại bước nhập thông tin, chưa hoàn tất đơn
        assert "checkout-step-one" in inventory.driver.current_url
