"""
login_page.py - Page Object cho trang đăng nhập SauceDemo.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def login(self, username, password):
        """Điền form và nhấn Login."""
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def error_text(self):
        """Trả về nội dung hộp thông báo lỗi (chờ nó hiển thị)."""
        return self.wait_for(self.ERROR_MESSAGE).text

    def is_at(self):
        """True nếu đang ở trang login (nút Login hiển thị)."""
        return len(self.elements(self.LOGIN_BUTTON)) > 0
