# Kịch bản thuyết trình — Phần TV4 (~4 phút)

> Lời thoại gợi ý, nói tự nhiên — không đọc nguyên văn slide.
> Mốc thời gian tương đối, điều chỉnh theo tốc độ nói thực tế.

---

## Slide 18 — Môi trường & công cụ (~40 giây)

"Phần tiếp theo em sẽ trình bày về quá trình thực thi kiểm thử tự động.
Website nhóm chọn là SauceDemo — một trang demo thương mại điện tử do
Sauce Labs xây dựng riêng cho mục đích học kiểm thử, có sẵn tài khoản
test công khai.

Về công cụ, em dùng Python kết hợp Selenium WebDriver để điều khiển
trình duyệt Chrome như người dùng thật, pytest để tổ chức và chạy test,
và pytest-html để xuất báo cáo. Một điểm tiện là từ bản Selenium 4.6
trở lên, ChromeDriver được Selenium Manager tự động tải và quản lý,
nên việc cài đặt môi trường chỉ gói gọn trong một file requirements.txt
chạy trong virtual environment."

## Slide 19 — Kiến trúc POM (~60 giây)

"Khi viết test, nếu để locator và thao tác lẫn trong từng file test thì
một thay đổi nhỏ trên giao diện sẽ phải sửa ở rất nhiều chỗ. Vì vậy em
áp dụng mô hình **Page Object Model**: mỗi trang web tương ứng một class
riêng — LoginPage, InventoryPage, CartPage và CheckoutPage — đóng gói
toàn bộ locator và thao tác của trang đó.

Tất cả các page kế thừa BasePage, nơi chứa các thao tác dùng chung —
quan trọng nhất là cơ chế **Explicit Wait**: thay vì dùng `time.sleep`
cố định, test sẽ chờ đúng điều kiện cần thiết, ví dụ chờ element hiển
thị hay chờ URL chuyển trang. Nhờ vậy test chạy nhanh mà vẫn ổn định.

Ngoài ra test data được tách riêng vào thư mục test_data, cấu hình tập
trung ở config/settings.py, và có tự động chụp screenshot khi test
thất bại."

## Slide 20 — Code minh họa (~45 giây)

"Đây là ví dụ thực tế: bên trái là LoginPage — chứa locator username,
password và hàm `login()` đóng gói toàn bộ thao tác đăng nhập. Bên phải
là test case TC01 — rất ngắn gọn: gọi login, rồi assert trang hiển thị
tiêu đề 'Products'.

Các negative test cho đăng nhập — sai mật khẩu, bỏ trống username, tài
khoản bị khóa — được viết chung một hàm test dùng `@pytest.mark.parametrize`,
mỗi bộ dữ liệu vẫn giữ được mã test case riêng nên vẫn truy vết được
TC02, TC03, TC04 trong báo cáo."

## Slide 21 — Kết quả thực thi (~60 giây)

"Kết quả thực thi: cả 8 test case chức năng từ TC01 đến TC08 đều **PASS**
— bao phủ đăng nhập đúng và các kịch bản sai, giỏ hàng thêm-xóa, và
checkout hoàn chỉnh đến trang 'Thank you for your order'.

Em đã chạy suite **3 lần liên tiếp** và kết quả giống hệt nhau — không
có test nào chập chờn.

Riêng **TC09** là test có chủ đích: em cố tình đặt expected title là
'Product' trong khi title thật là 'Products'. Mục đích là minh họa
pipeline xử lý khi test thất bại. TC09 được đánh dấu `xfail` nên trong
suite thường kết quả hiển thị **XFAIL** — nghĩa là pytest ghi nhận
'thất bại theo dự kiến' và không tính là lỗi của sản phẩm. Cần nhấn
mạnh: đây **không phải lỗi của website SauceDemo**. Khi cần demo, chạy
`pytest -m demo_fail --runxfail` thì TC09 sẽ FAILED thật và tự động
chụp screenshot."

## Slide 22 — HTML Report & nhận xét (~45 giây)

"Mỗi lần chạy, pytest-html tự sinh file report.html — mở trực tiếp
trên trình duyệt, liệt kê đầy đủ từng test, trạng thái, thời gian chạy
và chi tiết lỗi nếu có. Khi test fail, framework tự động chụp màn hình
và đính kèm vào report làm bằng chứng.

Kết luận: 8 chức năng chính của SauceDemo hoạt động đúng kỳ vọng. Quá
trình làm cũng phát hiện một điểm thú vị — website hiện phục vụ luân
phiên hai phiên bản giao diện, và bản mới có hành vi sự kiện khác khiến
click chuẩn không hoạt động; em đã xử lý bằng JavaScript fallback trong
BasePage nên suite chạy ổn định trên cả hai.

Hạn chế còn lại: bộ test phụ thuộc website bên ngoài và chưa chạy trên
CI — đây cũng là hướng phát triển tiếp theo của nhóm. Em xin hết phần
của mình."
