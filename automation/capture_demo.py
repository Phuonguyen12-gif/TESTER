"""capture_demo.py - Chụp screenshot minh họa luồng nghiệp vụ cho slide/demo.

Chạy: .venv/bin/python automation/capture_demo.py
Ảnh lưu vào reports/screenshots/demo/
"""

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By

SHOTS = Path(__file__).resolve().parent.parent / "reports" / "screenshots" / "demo"
SHOTS.mkdir(parents=True, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--window-size=1280,900")
d = webdriver.Chrome(options=options)
js = lambda e: d.execute_script("arguments[0].click();", e)

import time

try:
    # 1. Trang login
    d.get("https://www.saucedemo.com/")
    time.sleep(1)
    d.save_screenshot(str(SHOTS / "01_login_page.png"))

    # 2. Đăng nhập -> trang Products
    d.find_element(By.ID, "user-name").send_keys("standard_user")
    d.find_element(By.ID, "password").send_keys("secret_sauce")
    js(d.find_element(By.ID, "login-button"))
    time.sleep(2)
    d.save_screenshot(str(SHOTS / "02_products_page.png"))

    # 3. Thêm sản phẩm vào giỏ
    js(d.find_element(By.ID, "add-to-cart-sauce-labs-backpack"))
    time.sleep(1)
    d.save_screenshot(str(SHOTS / "03_added_to_cart.png"))

    # 4. Trang giỏ hàng
    js(d.find_element(By.CLASS_NAME, "shopping_cart_link"))
    time.sleep(2)
    d.save_screenshot(str(SHOTS / "04_cart_page.png"))

    # 5. Form thông tin khách hàng
    js(d.find_element(By.ID, "checkout"))
    time.sleep(2)
    for field, value in [("first-name", "Nguyen"), ("last-name", "Van A"), ("postal-code", "700000")]:
        el = d.find_element(By.ID, field)
        d.execute_script(
            "var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
            "s.call(arguments[0],arguments[1]);"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
            el, value)
    time.sleep(0.5)
    d.save_screenshot(str(SHOTS / "05_checkout_info.png"))

    # 6. Trang tổng quan đơn hàng
    js(d.find_element(By.ID, "continue"))
    time.sleep(2)
    d.save_screenshot(str(SHOTS / "06_checkout_overview.png"))

    # 7. Hoàn tất đơn hàng
    js(d.find_element(By.ID, "finish"))
    time.sleep(2)
    d.save_screenshot(str(SHOTS / "07_order_complete.png"))

    print("Đã chụp 7 ảnh vào:", SHOTS)
finally:
    d.quit()
