"""
cart_page.py - Page Object cho trang giỏ hàng (/cart.html).
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    REMOVE_BUTTON = "remove-{}"

    def item_count(self):
        return len(self.elements(self.CART_ITEM))

    def item_names(self):
        """Tên các sản phẩm trong giỏ."""
        return [el.text for el in self.elements(self.ITEM_NAME)]

    def remove(self, slug):
        """Xóa sản phẩm khỏi giỏ rồi chờ nó biến mất."""
        self.click((By.ID, self.REMOVE_BUTTON.format(slug)))

    def wait_empty(self):
        """Chờ đến khi giỏ không còn item nào."""
        self.wait_invisible(self.CART_ITEM)

    def checkout(self):
        """Nhấn Checkout -> trả về CheckoutPage (bước nhập thông tin)."""
        from pages.checkout_page import CheckoutPage  # tránh import vòng

        self.click(self.CHECKOUT_BUTTON)
        self.wait_url_contains("checkout-step-one")
        return CheckoutPage(self.driver)
