"""capture_demo.py - Chụp screenshot minh họa luồng nghiệp vụ cho slide/demo.

Chạy: ../.venv/bin/python capture_demo.py   (từ thư mục selenium_demo)
Ảnh lưu vào screenshots/demo/
"""

from pathlib import Path

from selenium import webdriver

from config import settings
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from test_data.checkout_data import VALID_CHECKOUT
from test_data.login_data import VALID_USER

SHOTS = settings.SCREENSHOT_DIR / "demo"
SHOTS.mkdir(parents=True, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument(f"--window-size={settings.WINDOW_SIZE}")
driver = webdriver.Chrome(options=options)

try:
    driver.get(settings.BASE_URL)
    login = LoginPage(driver)
    login.wait_for(LoginPage.LOGIN_BUTTON)
    driver.save_screenshot(str(SHOTS / "01_login_page.png"))

    login.login(VALID_USER["username"], VALID_USER["password"])
    inventory = InventoryPage(driver)
    inventory.is_loaded()
    driver.save_screenshot(str(SHOTS / "02_products_page.png"))

    inventory.add_to_cart("sauce-labs-backpack")
    inventory.wait_for(InventoryPage.CART_BADGE)
    driver.save_screenshot(str(SHOTS / "03_added_to_cart.png"))

    cart = inventory.open_cart()
    cart.wait_for(CartPage.CART_ITEM)
    driver.save_screenshot(str(SHOTS / "04_cart_page.png"))

    checkout = cart.checkout()
    checkout.fill_info(**VALID_CHECKOUT)
    checkout.wait_for(CheckoutPage.CONTINUE_BUTTON)
    driver.save_screenshot(str(SHOTS / "05_checkout_info.png"))

    checkout.continue_to_overview()
    checkout.at_overview()
    driver.save_screenshot(str(SHOTS / "06_checkout_overview.png"))

    checkout.finish()
    checkout.is_complete()
    driver.save_screenshot(str(SHOTS / "07_order_complete.png"))

    print("Đã chụp 7 ảnh vào:", SHOTS)
finally:
    driver.quit()
