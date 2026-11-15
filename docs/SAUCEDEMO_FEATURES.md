# Khảo sát chức năng website SauceDemo

**URL:** https://www.saucedemo.com/
**Người khảo sát:** TV4
**Ngày khảo sát:** 15/11/2026

## Thông tin chung

SauceDemo là website demo thương mại điện tử ("Swag Labs") do Sauce Labs xây
dựng chuyên cho mục đích thực hành kiểm thử tự động.

**Tài khoản demo công khai** (in sẵn trên trang login):

| Username | Ghi chú |
|---|---|
| `standard_user` | Tài khoản chuẩn, dùng cho hầu hết test |
| `locked_out_user` | Tài khoản bị khóa, dùng cho negative test |
| `problem_user` | Tài khoản gặp lỗi UI (ảnh sản phẩm sai, ...) |
| `performance_glitch_user` | Tài khoản tải trang chậm |
| `error_user`, `visual_user` | Các biến thể lỗi khác |

Mật khẩu chung cho tất cả: `secret_sauce`

> **Lưu ý quan trọng khi khảo sát:** hiện tại website phục vụ luân phiên
> **2 phiên bản giao diện** — bản classic (lưới sản phẩm dạng text) và bản
> redesign mới (card có hình ảnh). DOM giữ nguyên `id`/`class` của các element
> chính, nhưng hành vi sự kiện khác nhau (xem mục "Vấn đề phát hiện").

## Luồng nghiệp vụ chính (happy path)

```
Login (standard_user)
  -> Trang Products (/inventory.html)
    -> (Tùy chọn) Xem chi tiết sản phẩm (/inventory-item.html?id=N)
    -> Add to cart
  -> Trang Cart (/cart.html)
    -> Checkout
  -> Checkout: Your Information (/checkout-step-one.html)
  -> Checkout: Overview (/checkout-step-two.html)
  -> Finish
  -> Checkout: Complete! (/checkout-complete.html)
  -> (Tùy chọn) Logout qua menu burger
```

## Danh sách chức năng đã khảo sát

### 1. Đăng nhập (Login)

- **Mục đích:** Xác thực người dùng trước khi mua hàng.
- **Thao tác:** Nhập `user-name`, `password` -> nhấn `login-button`.
- **Kết quả mong đợi:** Chuyển sang `/inventory.html`, hiển thị tiêu đề
  "Products" và danh sách sản phẩm.
- **Tình huống lỗi:**
  - Sai mật khẩu -> hộp lỗi đỏ `[data-test="error"]`:
    "Epic sadface: Username and password do not match any user in this service"
  - User bị khóa (`locked_out_user`) -> "Epic sadface: Sorry, this user has
    been locked out."
  - Bỏ trống username/password -> "Epic sadface: Username is required" /
    "Password is required"

### 2. Hiển thị danh sách sản phẩm (Inventory)

- **Mục đích:** Hiển thị 6 sản phẩm để người dùng lựa chọn.
- **Thao tác:** Đăng nhập thành công, quan sát `.inventory_list`.
- **Kết quả mong đợi:** 6 `.inventory_item`, mỗi item có tên, mô tả, giá và
  nút "Add to cart". Có bộ lọc sắp xếp (Name A->Z, Z->A, Price low->high,
  high->low).
- **Tình huống lỗi:** Trang tải chậm (performance_glitch_user), ảnh lỗi
  (problem_user).

### 3. Xem thông tin sản phẩm (Product detail)

- **Mục đích:** Xem chi tiết một sản phẩm.
- **Thao tác:** Click vào tên/ảnh sản phẩm.
- **Kết quả mong đợi:** Chuyển sang `/inventory-item.html?id=<n>` hiển thị
  đầy đủ tên, mô tả, giá; nút "Back to products" quay lại danh sách.
- **Tình huống lỗi:** Sai id sản phẩm, link chi tiết không phản hồi.

### 4. Thêm sản phẩm vào giỏ hàng (Add to cart)

- **Mục đích:** Chọn sản phẩm để mua.
- **Thao tác:** Nhấn nút `add-to-cart-<tên-sản-phẩm>` (vd:
  `add-to-cart-sauce-labs-backpack`).
- **Kết quả mong đợi:** Badge trên icon giỏ hàng (`.shopping_cart_badge`)
  hiển thị số lượng tăng; nút đổi thành "Remove".
- **Tình huống lỗi:** Ở bản UI mới, click chuẩn của WebDriver đôi khi không
  được React xử lý -> badge không cập nhật (xem mục "Vấn đề phát hiện").

### 5. Xóa sản phẩm khỏi giỏ hàng (Remove)

- **Mục đích:** Bỏ sản phẩm đã chọn.
- **Thao tác:** Tại trang Products nhấn "Remove", hoặc trong trang Cart nhấn
  `remove-<tên-sản-phẩm>`.
- **Kết quả mong đợi:** Sản phẩm biến mất khỏi `.cart_item`, badge giảm/biến
  mất.
- **Tình huống lỗi:** Xóa khi giỏ trống, xóa sản phẩm không tồn tại.

### 6. Kiểm tra giỏ hàng (Cart page)

- **Mục đích:** Xem lại các sản phẩm đã chọn trước khi thanh toán.
- **Thao tác:** Click icon giỏ hàng `.shopping_cart_link`.
- **Kết quả mong đợi:** Chuyển sang `/cart.html`, liệt kê đúng sản phẩm/số
  lượng; có nút "Continue Shopping" và "Checkout".
- **Tình huống lỗi:** Ở bản UI mới, cart link là `<a role="button">` không
  có `href` — click chuẩn không điều hướng được.

### 7. Checkout

- **Mục đích:** Bắt đầu quy trình thanh toán.
- **Thao tác:** Tại `/cart.html` nhấn `checkout`.
- **Kết quả mong đợi:** Chuyển sang `/checkout-step-one.html`.
- **Tình huống lỗi:** Checkout với giỏ trống (website vẫn cho phép — đây là
  điểm đáng chú ý để đưa vào test).

### 8. Nhập thông tin khách hàng (Checkout: Your Information)

- **Mục đích:** Thu thập First Name, Last Name, Zip/Postal Code.
- **Thao tác:** Điền `first-name`, `last-name`, `postal-code` -> nhấn
  `continue`.
- **Kết quả mong đợi:** Chuyển sang `/checkout-step-two.html`.
- **Tình huống lỗi:**
  - Thiếu First Name -> "Error: First Name is required"
  - Thiếu Last Name -> "Error: Last Name is required"
  - Thiếu Postal Code -> "Error: Postal Code is required"
  - Ở bản UI mới, `send_keys` không ghi vào được controlled input của React
    (xem mục "Vấn đề phát hiện").

### 9. Hoàn tất đơn hàng (Checkout: Overview -> Complete)

- **Mục đích:** Xác nhận đơn hàng.
- **Thao tác:** Tại trang Overview kiểm tra danh sách, giá, thuế -> nhấn
  `finish`.
- **Kết quả mong đợi:** Chuyển sang `/checkout-complete.html`, hiển thị
  "Thank you for your order!" và nút "Back Home".
- **Tình huống lỗi:** Nhấn Cancel ở các bước trước, reload giữa chừng.

### 10. Đăng xuất (Logout)

- **Mục đích:** Kết thúc phiên làm việc.
- **Thao tác:** Nhấn menu burger `react-burger-menu-btn` -> chọn
  `logout_sidebar_link`.
- **Kết quả mong đợi:** Quay về trang login, hiển thị `login-button`.
- **Tình huống lỗi:** Menu cần thời gian animate trước khi link logout
  clickable.

## Vấn đề phát hiện trong quá trình khảo sát/tự động hóa

1. **Website phục vụ 2 phiên bản UI** (classic / redesign) không dự đoán
   trước -> test phải viết tương thích cả hai.
2. Ở bản UI mới: `WebElement.click()` chuẩn thường xuyên không tác động
   lên các nút React -> giải pháp: click qua JavaScript.
3. Ở bản UI mới: `send_keys` không ghi được vào input checkout -> giải
   pháp: set value bằng JavaScript + dispatch sự kiện `input`.
4. Cart link ở bản mới là `<a role="button">` không `href` -> chỉ điều
   hướng qua sự kiện click của React.
5. Không dùng `time.sleep()` tùy tiện — thay bằng `WebDriverWait` với
   expected conditions.

## Bằng chứng khảo sát

- Ảnh luồng nghiệp vụ: `reports/screenshots/demo/01..07_*.png`
- HTML DOM đã kiểm tra bằng Selenium (class/id giữ nguyên ở cả 2 UI).
