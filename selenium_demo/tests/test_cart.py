"""
test_cart.py - Kiểm thử chức năng Giỏ hàng.

TC03: Thêm sản phẩm vào giỏ     -> badge giỏ hàng tăng lên 1
TC04: Xóa sản phẩm khỏi giỏ     -> sản phẩm biến mất khỏi giỏ
TC06: Logout                    -> quay về trang login
"""

import pytest

from pages.login_page import LoginPage

BACKPACK = "sauce-labs-backpack"


@pytest.mark.cart
class TestCart:
    @pytest.mark.tc03
    def test_TC03_add_to_cart(self, inventory):
        """TC03: Thêm 1 sản phẩm -> số lượng trên icon giỏ hàng = 1."""
        inventory.add_to_cart(BACKPACK)
        assert inventory.cart_badge_count() == 1

        cart = inventory.open_cart()
        assert cart.item_count() == 1
        assert "Sauce Labs Backpack" in cart.item_names()

    @pytest.mark.tc04
    def test_TC04_remove_from_cart(self, inventory):
        """TC04: Thêm rồi xóa sản phẩm -> giỏ hàng trống."""
        # Pre-condition: có 1 sản phẩm trong giỏ
        inventory.add_to_cart(BACKPACK)
        assert inventory.cart_badge_count() == 1

        cart = inventory.open_cart()
        cart.remove(BACKPACK)
        cart.wait_empty()
        assert cart.item_count() == 0
        # Badge số lượng cũng biến mất
        assert inventory.cart_badge_count() is None

    @pytest.mark.tc06
    def test_TC06_logout(self, inventory):
        """TC06: Logout -> quay về trang login."""
        inventory.logout()

        login_page = LoginPage(inventory.driver)
        login_page.wait_for(LoginPage.LOGIN_BUTTON)
        assert login_page.is_at()
