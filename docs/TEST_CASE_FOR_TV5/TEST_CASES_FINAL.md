# TEST CASES FINAL — SauceDemo (TC01–TC09)

**Đối tượng:** https://www.saucedemo.com/
**Trạng thái:** Bộ Test Cases chính thức để TV5 rà soát & tổng hợp.
**Lưu ý:** Đây là tài liệu *thiết kế* kiểm thử — Expected Result ở đây là
kỳ vọng ban đầu, KHÔNG phải kết quả chạy. Kết quả thực thi nằm ở
`TEST_EXECUTION_RESULTS.xlsx`.

Tài khoản demo công khai của SauceDemo: `standard_user`,
`locked_out_user` — mật khẩu chung `secret_sauce`.

| Test Case ID | Description | Pre-condition | Test Steps | Test Data | Expected Result |
|---|---|---|---|---|---|
| TC01 | Đăng nhập hợp lệ | Đang ở trang login | 1. Nhập username 2. Nhập password 3. Nhấn Login | user=`standard_user`, pass=`secret_sauce` | Chuyển sang `/inventory.html`, hiển thị trang **Products** |
| TC02 | Đăng nhập sai mật khẩu | Đang ở trang login | Như TC01 | user=`standard_user`, pass=`wrong_password` | Hiển thị thông báo lỗi "Epic sadface: Username and password do not match any user in this service" |
| TC03 | Bỏ trống username | Đang ở trang login | 1. Bỏ trống username 2. Nhập password 3. Nhấn Login | user=*(trống)*, pass=`secret_sauce` | Hiển thị lỗi "**Username is required**" |
| TC04 | Đăng nhập bằng locked_out_user | Đang ở trang login | Như TC01 | user=`locked_out_user`, pass=`secret_sauce` | Hiển thị lỗi "Sorry, this user has been **locked out**" |
| TC05 | Thêm sản phẩm vào giỏ hàng | Đã login `standard_user`, ở trang Products | 1. Nhấn "Add to cart" ở Sauce Labs Backpack 2. Mở giỏ hàng | Sauce Labs Backpack | **Cart badge = 1**; giỏ hàng có đúng 1 sản phẩm |
| TC06 | Xóa sản phẩm khỏi giỏ hàng | Giỏ có 1 sản phẩm | 1. Mở `/cart.html` 2. Nhấn Remove | Sauce Labs Backpack | Sản phẩm biến mất, **cart badge biến mất** |
| TC07 | Checkout hợp lệ | Giỏ có ≥1 sản phẩm | 1. Checkout 2. Điền First/Last/Postal Code 3. Continue 4. Finish | First=`Nguyen`, Last=`Van A`, Zip=`700000` | Trang `/checkout-complete.html`, "**Thank you for your order!**" |
| TC08 | Bỏ trống Postal Code | Giỏ có ≥1 sản phẩm, ở checkout step-one | 1. Điền First + Last name 2. Bỏ trống Postal Code 3. Continue | First=`Nguyen`, Last=`Van A`, Zip=*(trống)* | Hiển thị lỗi "**Postal Code is required**" |
| TC09 | Kiểm tra đăng nhập với expected title cố tình sai | Đã login `standard_user` | 1. Đọc title trang Products 2. So sánh với expected sai | expected=`"Product"` (cố tình thiếu "s") | **Thất bại CÓ CHỦ ĐÍCH** — minh họa pipeline xử lý test FAIL/XFAIL. Không phải lỗi của website |

## Ghi chú

- TC01–TC04: chức năng Login (TC01 positive, TC02–TC04 negative).
- TC05–TC06: chức năng Giỏ hàng. TC07–TC08: chức năng Checkout.
- TC09: demonstration — trạng thái ghi nhận trong automation là
  `xfail`; xem TEST_EXECUTION_RESULTS.xlsx để phân biệt XFAIL/FAILED.
- Test bổ sung ngoài bộ TC (logout) không thuộc phạm vi tài liệu này.
