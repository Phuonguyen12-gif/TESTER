"""
checkout_data.py - Dữ liệu cho các test checkout.
"""

VALID_CHECKOUT = {
    "first_name": "Nguyen",
    "last_name": "Van A",
    "postal_code": "700000",
}

# TC08: bỏ trống Postal Code -> kỳ vọng "Postal Code is required"
MISSING_POSTAL_CHECKOUT = {
    "first_name": "Nguyen",
    "last_name": "Van A",
    "postal_code": "",
}
