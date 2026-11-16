# Nội dung slide 18–22 — Phần TV4
## Thực thi kiểm thử tự động Selenium trên SauceDemo

> Copy trực tiếp các block nội dung vào Canva. Số liệu lấy từ kết quả
> chạy thật ngày 16/11/2026. Ảnh trong thư mục `SCREENSHOTS/` cùng cấp.

---

## Slide 18 — Môi trường & Công cụ cài đặt

**Nội dung (copy vào slide):**

- Website kiểm thử: **SauceDemo** — saucedemo.com
- Ngôn ngữ: **Python 3.14** · Framework: **Selenium WebDriver 4.52**
- Test runner: **pytest 9.2** · Báo cáo: **pytest-html 4.2**
- Trình duyệt: **Google Chrome 157** — ChromeDriver tự quản lý bởi
  Selenium Manager (không cần cài tay)
- Môi trường cô lập: **virtual environment** + `requirements.txt`

**Screenshot đề xuất:** `SCREENSHOTS/01_project_structure.png`
(hoặc ảnh trang login SauceDemo trong `selenium_demo/screenshots/phase_1/demo/01_login_page.png`)

**Gợi ý bố cục:** Trái — danh sách công cụ dạng icon/stack; Phải —
screenshot terminal hoặc cây thư mục dự án.

---

## Slide 19 — Cấu trúc dự án & Kiến trúc POM

**Nội dung:**

- **Page Object Model**: mỗi trang web = 1 class đóng gói locator +
  thao tác → test chỉ chứa kịch bản + assertion
- `pages/`: LoginPage, InventoryPage, CartPage, CheckoutPage
- `pages/base_page.py`: explicit wait + click/nhập liệu dùng chung
- `tests/`: test logic · `test_data/`: dữ liệu tách riêng
- `config/settings.py`: cấu hình tập trung, hỗ trợ biến môi trường
- `utils/screenshot.py`: tự động chụp ảnh khi test FAIL

**Screenshot đề xuất:** `SCREENSHOTS/01_project_structure.png`
+ `SCREENSHOTS/02_pom_base_page.png`

**Gợi ý bố cục:** Trái — cây thư mục; Phải — sơ đồ luồng
`Test → Page Object → BasePage → WebDriver → Browser`.

---

## Slide 20 — Minh họa code Selenium & pytest

**Nội dung (chọn 1 trong 2 đoạn code đưa lên slide):**

```python
# Page Object — đóng gói locator + thao tác
class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    LOGIN_BUTTON = (By.ID, "login-button")

    def login(self, username, password):
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
```

```python
# Test — chỉ kịch bản + assertion, dùng explicit wait
@pytest.mark.tc01
def test_TC01_valid_login(self, driver):
    LoginPage(driver).login(**VALID_USER)
    page = InventoryPage(driver)
    assert page.is_loaded()
    assert page.title_text() == "Products"
```

**Điểm nhấn để nói:** Explicit Wait thay `time.sleep()`; fixture
setup/teardown trình duyệt; parametrize cho negative login (TC02–TC04).

**Screenshot đề xuất:** `SCREENSHOTS/02_pom_base_page.png`

**Gợi ý bố cục:** 2 khung code song song (Page Object | Test), footer
ghi 3 gạch đầu dòng kỹ thuật.

---

## Slide 21 — Kết quả thực thi TC01–TC09

**Nội dung:**

| TC | Nội dung | Kết quả |
|---|---|---|
| TC01 | Đăng nhập hợp lệ | **PASS** |
| TC02 | Sai mật khẩu | **PASS** |
| TC03 | Bỏ trống username | **PASS** |
| TC04 | locked_out_user | **PASS** |
| TC05 | Thêm vào giỏ hàng | **PASS** |
| TC06 | Xóa khỏi giỏ hàng | **PASS** |
| TC07 | Checkout hợp lệ | **PASS** |
| TC08 | Trống Postal Code | **PASS** |
| TC09 | Expected sai CÓ CHỦ ĐÍCH | **XFAIL** |

- Tổng: **8/8 test thật PASS · TC09 = XFAIL (dự kiến thất bại)**
- Chạy 3 lần liên tiếp: kết quả giống hệt nhau — **0 flake**
- XFAIL ≠ FAILED: TC09 là demo thất bại có chủ đích, không phải lỗi
  website

**Screenshot đề xuất:** `SCREENSHOTS/03_pytest_result.png`

**Gợi ý bố cục:** Bảng kết quả bên trái (có màu xanh/vàng), bên phải
ảnh terminal kết quả + con số lớn "8 PASS · 1 XFAIL".

---

## Slide 22 — HTML Test Report & Nhận xét

**Nội dung:**

- **pytest-html** tự sinh `reports/report.html` mỗi lần chạy:
  tổng số test, trạng thái từng case, lỗi chi tiết, môi trường
- Test FAIL → tự động **chụp screenshot** và đính kèm vào report
- Nhận xét:
  - 8/8 chức năng chính của SauceDemo hoạt động đúng expected
  - Framework ổn định (explicit wait, POM, fixture teardown)
  - Phát hiện thực tế: website có 2 phiên bản UI → bài học về
    locator & cơ chế chờ
- Hạn chế: phụ thuộc website bên ngoài; chưa test các user lỗi
  (`problem_user`), chưa có CI

**Screenshot đề xuất:** `SCREENSHOTS/04_html_report.png`

**Gợi ý bố cục:** Trên — ảnh HTML report chiếm ~60%; Dưới — 2 cột
"Nhận xét" và "Hạn chế".
