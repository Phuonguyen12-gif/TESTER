"""
checkout_page.py - Page Object cho quy trình checkout gồm 3 màn hình:
step-one (nhập thông tin) -> step-two (overview) -> complete.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # Step one: Checkout: Your Information
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Step two: Checkout: Overview
    FINISH_BUTTON = (By.ID, "finish")

    # Complete — dùng text để tương thích cả 2 phiên bản UI
    THANK_YOU = (By.XPATH, "//*[contains(text(),'Thank you for your order')]")

    def fill_info(self, first_name, last_name, postal_code):
        """Điền thông tin khách hàng ở step-one."""
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)

    def continue_to_overview(self):
        """Nhấn Continue. Nếu form hợp lệ sẽ sang step-two."""
        self.click(self.CONTINUE_BUTTON)

    def at_overview(self):
        """True nếu đã sang màn Overview (step-two)."""
        self.wait_url_contains("checkout-step-two")
        return True

    def finish(self):
        """Nhấn Finish ở màn Overview."""
        self.click(self.FINISH_BUTTON)

    def is_complete(self):
        """True nếu đơn hàng hoàn tất (URL + thông báo cảm ơn)."""
        self.wait_url_contains("checkout-complete")
        return self.wait_for(self.THANK_YOU).is_displayed()

    def error_text(self):
        """Nội dung lỗi ở step-one (chờ hiển thị)."""
        return self.wait_for(self.ERROR_MESSAGE).text
