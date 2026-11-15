"""
inventory_page.py - Page Object cho trang danh sách sản phẩm (/inventory.html).
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.cart_page import CartPage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    # Slug sản phẩm dùng trong id nút Add/Remove, vd: "sauce-labs-backpack"
    ADD_BUTTON = "add-to-cart-{}"
    REMOVE_BUTTON = "remove-{}"

    def is_loaded(self):
        """True nếu trang Products đã load (URL + danh sách sản phẩm)."""
        self.wait_url_contains("inventory")
        self.wait_for(self.INVENTORY_LIST)
        return True

    def title_text(self):
        return self.wait_for(self.TITLE).text

    def product_count(self):
        return len(self.elements(self.INVENTORY_ITEM))

    def add_to_cart(self, slug):
        """Thêm sản phẩm vào giỏ theo slug, vd 'sauce-labs-backpack'."""
        self.click((By.ID, self.ADD_BUTTON.format(slug)))

    def cart_badge_count(self):
        """Số lượng trên badge giỏ hàng; None nếu giỏ trống."""
        badges = self.elements(self.CART_BADGE)
        return int(badges[0].text) if badges else None

    def open_cart(self):
        """Mở trang giỏ hàng, trả về CartPage."""
        self.click(self.CART_LINK)
        self.wait_url_contains("cart")
        return CartPage(self.driver)

    def logout(self):
        """Mở menu burger và đăng xuất."""
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)
