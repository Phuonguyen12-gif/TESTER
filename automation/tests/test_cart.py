"""
test_cart.py - Kiểm thử chức năng Giỏ hàng.

TC03: Thêm sản phẩm vào giỏ     -> badge giỏ hàng tăng lên 1
TC04: Xóa sản phẩm khỏi giỏ     -> sản phẩm biến mất khỏi giỏ
TC06: Logout                    -> quay về trang login
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import TIMEOUT, click, wait_for

ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
CART_LINK = (By.CLASS_NAME, "shopping_cart_link")


class TestCart:
    def test_TC03_add_to_cart(self, logged_in_driver):
        """TC03: Thêm 1 sản phẩm -> số lượng trên icon giỏ hàng = 1."""
        driver = logged_in_driver

        click(driver, ADD_BACKPACK)

        badge = wait_for(driver, CART_BADGE)
        assert badge.text == "1"

        # Kiểm tra trong trang giỏ hàng có đúng sản phẩm
        click(driver, CART_LINK)
        WebDriverWait(driver, TIMEOUT).until(EC.url_contains("cart"))
        wait_for(driver, (By.CLASS_NAME, "cart_item"))
        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) == 1
        assert "Sauce Labs Backpack" in items[0].text

    def test_TC04_remove_from_cart(self, logged_in_driver):
        """TC04: Thêm rồi xóa sản phẩm -> giỏ hàng trống."""
        driver = logged_in_driver

        # Pre-condition: có 1 sản phẩm trong giỏ
        click(driver, ADD_BACKPACK)
        wait_for(driver, CART_BADGE)

        # Vào giỏ hàng và xóa
        click(driver, CART_LINK)
        click(driver, REMOVE_BACKPACK)

        # Sản phẩm phải biến mất khỏi DOM
        WebDriverWait(driver, TIMEOUT).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        # Badge số lượng cũng biến mất
        badges = driver.find_elements(*CART_BADGE)
        assert len(badges) == 0

    def test_TC06_logout(self, logged_in_driver):
        """TC06: Logout -> quay về trang login."""
        driver = logged_in_driver

        click(driver, (By.ID, "react-burger-menu-btn"))
        click(driver, (By.ID, "logout_sidebar_link"))

        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "login-button"))
        )
        assert driver.current_url.rstrip("/").endswith("saucedemo.com")
