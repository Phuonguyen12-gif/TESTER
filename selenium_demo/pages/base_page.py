"""
base_page.py - Thao tác Selenium dùng chung cho mọi Page Object.

Bao gồm workaround cho đặc thù của SauceDemo: website phục vụ luân phiên
2 phiên bản UI (classic và redesign); ở bản mới, click/send_keys chuẩn của
WebDriver đôi khi không được React xử lý -> dùng JavaScript fallback.
Chi tiết: docs/SAUCEDEMO_FEATURES.md mục "Vấn đề phát hiện".
"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import settings


class BasePage:
    """Lớp cha: giữ driver + các thao tác chờ/click/nhập liệu dùng chung."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.TIMEOUT)

    # ---------- Explicit wait helpers ----------

    def wait_for(self, locator):
        """Chờ element hiển thị rồi trả về element."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_url_contains(self, fragment):
        """Chờ URL chứa fragment."""
        self.wait.until(EC.url_contains(fragment))

    def wait_invisible(self, locator):
        """Chờ element biến mất khỏi DOM/hiển thị."""
        self.wait.until(EC.invisibility_of_element_located(locator))

    def elements(self, locator):
        """Trả về danh sách element khớp locator (có thể rỗng)."""
        return self.driver.find_elements(*locator)

    # ---------- Tương tác tương thích 2 phiên bản UI ----------

    def click(self, locator):
        """Chờ element hiển thị rồi click bằng JavaScript.

        Click qua JS hoạt động trên cả 2 phiên bản UI của SauceDemo;
        click chuẩn của WebDriver đôi khi bị React ở bản mới bỏ qua.
        """
        element = self.wait_for(locator)
        self.driver.execute_script("arguments[0].click();", element)
        return element

    def type_text(self, locator, text):
        """Nhập text vào ô input.

        Thử send_keys trước; nếu giá trị không được ghi nhận (controlled
        input của React ở bản UI mới) thì set value bằng JavaScript kèm
        sự kiện 'input' để React cập nhật state.
        """
        element = self.wait_for(locator)
        element.clear()
        element.send_keys(text)
        if element.get_attribute("value") != text:
            self.driver.execute_script(
                """
                var setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value').set;
                setter.call(arguments[0], arguments[1]);
                arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                """,
                element,
                text,
            )
        return element
