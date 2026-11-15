"""
test_checkout.py - Kiểm thử chức năng Checkout.

TC05: Checkout hợp lệ           -> hoàn tất đơn hàng thành công
TC08: Checkout thiếu thông tin  -> hiển thị thông báo lỗi
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import TIMEOUT, click, type_text, wait_for


def add_backpack_and_open_cart(driver):
    """Thao tác dùng chung: thêm sản phẩm rồi mở trang giỏ hàng."""
    click(driver, (By.ID, "add-to-cart-sauce-labs-backpack"))
    click(driver, (By.CLASS_NAME, "shopping_cart_link"))
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("cart"))
    wait_for(driver, (By.ID, "checkout"))


class TestCheckout:
    def test_TC05_checkout_success(self, logged_in_driver):
        """TC05: Điền đủ thông tin -> đơn hàng hoàn tất thành công."""
        driver = logged_in_driver
        add_backpack_and_open_cart(driver)

        # Bước 1: nhấn Checkout, điền thông tin khách hàng
        driver.find_element(By.ID, "checkout").click()
        type_text(driver, (By.ID, "first-name"), "Nguyen")
        type_text(driver, (By.ID, "last-name"), "Van A")
        type_text(driver, (By.ID, "postal-code"), "700000")
        click(driver, (By.ID, "continue"))

        # Bước 2: trang tổng quan đơn hàng -> Finish
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("checkout-step-two")
        )
        click(driver, (By.ID, "finish"))

        # Kết quả mong đợi: trang Complete + thông báo cảm ơn
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("checkout-complete")
        )
        header = wait_for(
            driver,
            (By.XPATH, "//*[contains(text(),'Thank you for your order')]"),
        )
        assert header.is_displayed()

    def test_TC08_checkout_missing_info(self, logged_in_driver):
        """TC08: Bỏ trống thông tin bắt buộc -> hiển thị thông báo lỗi."""
        driver = logged_in_driver
        add_backpack_and_open_cart(driver)

        driver.find_element(By.ID, "checkout").click()
        # Không điền gì, nhấn Continue luôn
        click(driver, (By.ID, "continue"))

        error = wait_for(driver, (By.CSS_SELECTOR, "[data-test='error']"))
        assert "Error" in error.text
        # Vẫn ở lại bước nhập thông tin, chưa hoàn tất đơn
        assert "checkout-step-one" in driver.current_url
