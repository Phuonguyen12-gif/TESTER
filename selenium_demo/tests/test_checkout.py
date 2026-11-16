"""
test_checkout.py - Kiểm thử chức năng Checkout.

TC07: Checkout hợp lệ                -> "Thank you for your order!"
TC08: Bỏ trống Postal Code           -> "Postal Code is required"
"""

import pytest

from test_data.checkout_data import MISSING_POSTAL_CHECKOUT, VALID_CHECKOUT

BACKPACK = "sauce-labs-backpack"


@pytest.mark.checkout
class TestCheckout:
    @pytest.mark.tc07
    def test_TC07_checkout_success(self, inventory):
        """TC07: Điền đủ thông tin -> đơn hàng hoàn tất thành công."""
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
    def test_TC08_checkout_missing_postal_code(self, inventory):
        """TC08: Bỏ trống Postal Code -> "Postal Code is required"."""
        inventory.add_to_cart(BACKPACK)
        cart = inventory.open_cart()
        checkout = cart.checkout()

        # Điền First + Last name, chỉ bỏ trống Postal Code
        checkout.fill_info(**MISSING_POSTAL_CHECKOUT)
        checkout.continue_to_overview()

        assert "Postal Code is required" in checkout.error_text()
        # Vẫn ở lại bước nhập thông tin, chưa hoàn tất đơn
        assert "checkout-step-one" in inventory.driver.current_url
