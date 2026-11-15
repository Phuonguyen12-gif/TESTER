# Test Case Draft — SauceDemo (BẢN NHÁP cho TV5 rà soát)

> Tài liệu nháp do TV4 lập để TV5 (thiết kế Test Case) rà soát và thống nhất.
> Đây KHÔNG phải bộ Test Case chính thức của nhóm.
> Mỗi Test Condition có tối thiểu 1 Positive Test và 1 Negative Test
> (theo quy định môn học). Các mục đánh dấu [*] đã được TV4 cài đặt
> automation và chạy thực tế.

## Chức năng 1: Đăng nhập

| ID | Loại | Description | Pre-condition | Test Steps | Input | Expected Result |
|---|---|---|---|---|---|---|
| TC01 [*] | Positive | Đăng nhập hợp lệ | Đang ở trang login | 1. Nhập username 2. Nhập password 3. Nhấn Login | user=`standard_user`, pass=`secret_sauce` | Vào `/inventory.html`, tiêu đề "Products", có >=1 sản phẩm |
| TC02 [*] | Negative | Đăng nhập sai mật khẩu | Đang ở trang login | Như TC01 | user=`standard_user`, pass=`wrong_password` | Lỗi "Epic sadface: Username and password do not match...", vẫn ở trang login |
| TC02b | Negative | Bỏ trống username | Đang ở trang login | 1. Chỉ nhập password 2. Nhấn Login | pass=`secret_sauce` | Lỗi "Epic sadface: Username is required" |
| TC07 [*] | Negative | Tài khoản bị khóa | Đang ở trang login | Như TC01 | user=`locked_out_user`, pass=`secret_sauce` | Lỗi "Epic sadface: Sorry, this user has been locked out." |

## Chức năng 2: Hiển thị sản phẩm

| ID | Loại | Description | Pre-condition | Test Steps | Input | Expected Result |
|---|---|---|---|---|---|---|
| TC-P01 | Positive | Danh sách sản phẩm hiển thị | Đã login standard_user | Quan sát trang Products | — | Hiển thị đúng 6 sản phẩm, mỗi sp có tên/giá/nút Add to cart |
| TC-P02 | Positive | Sắp xếp theo giá | Đã login | Chọn sort "Price (low to high)" | — | Sản phẩm đầu tiên có giá thấp nhất ($7.99) |

## Chức năng 3: Xem chi tiết sản phẩm

| ID | Loại | Description | Pre-condition | Test Steps | Input | Expected Result |
|---|---|---|---|---|---|---|
| TC-D01 | Positive | Mở trang chi tiết | Đã login | Click tên "Sauce Labs Backpack" | — | URL `/inventory-item.html?id=4`, hiển thị đúng tên + giá $29.99 |
| TC-D02 | Positive | Quay lại danh sách | Đang ở trang chi tiết | Nhấn "Back to products" | — | Về `/inventory.html` |

## Chức năng 4: Giỏ hàng

| ID | Loại | Description | Pre-condition | Test Steps | Input | Expected Result |
|---|---|---|---|---|---|---|
| TC03 [*] | Positive | Thêm sản phẩm vào giỏ | Đã login | 1. Nhấn "Add to cart" ở Sauce Labs Backpack 2. Mở giỏ hàng | — | Badge = "1"; trong `/cart.html` có đúng 1 item Sauce Labs Backpack |
| TC04 [*] | Negative | Xóa sản phẩm khỏi giỏ | Giỏ có 1 sản phẩm | 1. Mở `/cart.html` 2. Nhấn Remove | — | `.cart_item` biến mất, badge biến mất |
| TC-C03 | Positive | Tiếp tục mua sắm | Đang ở `/cart.html` | Nhấn "Continue Shopping" | — | Về `/inventory.html` |

## Chức năng 5: Checkout

| ID | Loại | Description | Pre-condition | Test Steps | Input | Expected Result |
|---|---|---|---|---|---|---|
| TC05 [*] | Positive | Checkout hợp lệ | Giỏ có >=1 sản phẩm | 1. Nhấn Checkout 2. Điền First/Last/Postal 3. Continue 4. Finish | First=`Nguyen`, Last=`Van A`, Zip=`700000` | URL `/checkout-complete.html`, hiển thị "Thank you for your order!" |
| TC08 [*] | Negative | Checkout thiếu thông tin | Giỏ có >=1 sản phẩm, đang ở step-one | Nhấn Continue không điền gì | — | Lỗi "Error: First Name is required", vẫn ở step-one |
| TC-C02 | Negative | Thiếu Postal Code | Như TC08 | Điền First+Last, bỏ trống Zip -> Continue | First=`A`, Last=`B` | Lỗi "Error: Postal Code is required" |
| TC-C04 | Negative | Hủy checkout | Đang ở step-one | Nhấn Cancel | — | Quay về `/cart.html` |
| TC-C05 | Negative | Checkout giỏ trống | Đã login, giỏ trống | Vào `/cart.html` -> Checkout -> điền form -> Finish | — | **Cần thống nhất expected:** website hiện vẫn cho hoàn tất đơn trống (hành vi thực tế) |

## Chức năng 6: Đăng xuất

| ID | Loại | Description | Pre-condition | Test Steps | Input | Expected Result |
|---|---|---|---|---|---|---|
| TC06 [*] | Positive | Logout | Đã login | 1. Mở menu burger 2. Chọn Logout | — | Về trang login, hiển thị nút Login |
| TC-L02 | Negative | Truy cập trang trong khi chưa login | Chưa login | Mở trực tiếp `/inventory.html` | — | Bị chặn, hiển thị lỗi yêu cầu login |

## Tình huống đề xuất bổ sung (chưa cài đặt)

- Đăng nhập `problem_user` -> phát hiện ảnh sản phẩm sai (dùng để minh họa
  "test phát hiện lỗi website").
- Đăng nhập `performance_glitch_user` -> đo thời gian tải trang.
- Kiểm tra tính tổng giá + thuế ở trang Overview.

## Ghi chú cho TV5

- ID TC01–TC08 khớp với tên hàm test trong `automation/tests/` để dễ đối
  chiếu khi demo.
- Cần TV5 quyết định bộ Test Case chính thức của nhóm, định dạng theo mẫu
  môn học (Test Case ID, Description, Pre-condition, Test Steps, Inputs,
  Expected Result, Pass/Fail).
