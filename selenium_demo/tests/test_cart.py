"""
test_cart.py - Kiểm thử chức năng Giỏ hàng.

TC05: Thêm sản phẩm vào giỏ      -> cart badge = 1
TC06: Xóa sản phẩm khỏi giỏ     -> cart badge biến mất
(+) Logout                      -> test bổ sung, ngoài bộ TC01–TC09
"""

import pytest

from pages.login_page import LoginPage

BACKPACK = "sauce-labs-backpack"


@pytest.mark.cart
class TestCart:
    @pytest.mark.tc05
    def test_TC05_add_to_cart(self, inventory):
        """TC05: Thêm 1 sản phẩm -> số lượng trên icon giỏ hàng = 1."""
        inventory.add_to_cart(BACKPACK)
        assert inventory.cart_badge_count() == 1

        cart = inventory.open_cart()
        assert cart.item_count() == 1
        assert "Sauce Labs Backpack" in cart.item_names()

    @pytest.mark.tc06
    def test_TC06_remove_from_cart(self, inventory):
        """TC06: Thêm rồi xóa sản phẩm -> cart badge biến mất."""
        # Pre-condition: có 1 sản phẩm trong giỏ
        inventory.add_to_cart(BACKPACK)
        assert inventory.cart_badge_count() == 1

        cart = inventory.open_cart()
        cart.remove(BACKPACK)
        cart.wait_empty()
        assert cart.item_count() == 0
        # Badge số lượng cũng biến mất
        assert inventory.cart_badge_count() is None

    def test_logout(self, inventory):
        """Bổ sung (ngoài TC01–TC09): Logout -> quay về trang login."""
        inventory.logout()

        login_page = LoginPage(inventory.driver)
        login_page.wait_for(LoginPage.LOGIN_BUTTON)
        assert login_page.is_at()
