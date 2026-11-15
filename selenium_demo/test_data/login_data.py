"""
login_data.py - Tài khoản và dataset cho các test đăng nhập.

Đây là tài khoản DEMO CÔNG KHAI do SauceDemo cung cấp (in sẵn trên
trang login) — không phải credentials thật.
"""

VALID_USER = {"username": "standard_user", "password": "secret_sauce"}

WRONG_PASSWORD_USER = {"username": "standard_user", "password": "wrong_password"}

LOCKED_USER = {"username": "locked_out_user", "password": "secret_sauce"}

# Dataset negative login: (tài khoản, chuỗi kỳ vọng trong thông báo lỗi)
# Mỗi phần tử tương ứng 1 Test Case ID — dùng cho pytest parametrize.
NEGATIVE_LOGIN_CASES = [
    (WRONG_PASSWORD_USER, "Epic sadface"),                    # TC02
    (LOCKED_USER, "Sorry, this user has been locked out"),    # TC07
]
NEGATIVE_LOGIN_IDS = ["TC02", "TC07"]
