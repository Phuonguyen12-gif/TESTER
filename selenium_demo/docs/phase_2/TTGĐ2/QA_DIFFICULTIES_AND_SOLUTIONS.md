# Khó khăn & Cách giải quyết — TV4 (gửi TV1 tổng hợp)

## 1. Website phục vụ 2 phiên bản UI không ổn định

**Khó khăn:** SauceDemo luân phiên render 2 giao diện (classic và bản
redesign mới). Ở bản mới, `click()` và `send_keys()` chuẩn của Selenium
không được React xử lý — test FAIL ngẫu nhiên dù locator đúng, gây khó
chẩn đoán vì lỗi không tái hiện ổn định.

**Giải pháp:** Khoanh vùng bằng cách chụp screenshot khi FAIL, đối chiếu
DOM trực tiếp, sau đó đóng gói workaround vào `BasePage`: click qua
JavaScript và nhập liệu bằng JS value setter + sự kiện `input` khi
`send_keys` không ghi nhận giá trị. Kết quả: 0 flake trong 30 lượt chạy
(10 test × 3 lần).

## 2. Lỗi timing sau chuyển trang (race condition)

**Khó khăn:** Lần chạy đầu tiên 6/8 test FAIL với `NoSuchElement`/
`StaleElement` vì test dùng `find_element` ngay sau khi URL đổi trong
khi React chưa render xong trang mới.

**Giải pháp:** Loại bỏ hoàn toàn `time.sleep()` và `find_element` trực
tiếp sau điều hướng; thay bằng `WebDriverWait` + expected conditions
(`visibility_of_element_located`, `url_contains`, `invisibility_of_...`)
tập trung trong `BasePage` và chờ trang load trong fixture `inventory`
trước khi test bắt đầu.
