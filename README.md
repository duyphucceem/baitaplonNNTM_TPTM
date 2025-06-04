# 📸 Đồ án: Hệ thống Nhận diện Khuôn mặt và Giám sát Cư dân sử dụng ESP32-CAM & ESP8266

## 📌 Giới thiệu

Đây là đồ án lớn thuộc học phần Nông nghiệp thông minh và Thành phố thông minh. Hệ thống được xây dựng nhằm **giám sát ra vào khu vực cư trú** thông qua **nhận diện khuôn mặt bằng ESP32-CAM** và gửi dữ liệu tới hệ thống trung tâm thông qua **ESP8266**.

Giải pháp hướng tới các mô hình khu dân cư hiện đại, ký túc xá, nhà trọ, với mục tiêu tự động hóa kiểm soát người ra vào, tăng tính an toàn và hỗ trợ lưu trữ, phân tích dữ liệu.

---

## 🎯 Mục tiêu

- Tự động nhận diện khuôn mặt cư dân bằng camera tích hợp trên ESP32-CAM.
- Gửi dữ liệu nhận diện và thời gian truy cập về trung tâm qua WiFi (ESP8266).
- Hiển thị thông tin cảnh báo, log lịch sử ra vào.
- Giảm chi phí so với các hệ thống nhận diện thương mại.

---

## 🧰 Công nghệ sử dụng

| Thành phần       | Mô tả                                                                 |
|------------------|----------------------------------------------------------------------|
| **ESP32-CAM**    | Thiết bị chính dùng để nhận diện khuôn mặt bằng mô hình tích hợp.   |
| **ESP8266**      | Gửi dữ liệu từ ESP32-CAM về máy chủ hoặc hiển thị web real-time.     |
| **Arduino IDE**  | Lập trình và upload firmware cho cả ESP32-CAM và ESP8266.            |
| **Python** (tuỳ chọn) | Hiển thị và lưu log nếu dùng máy tính làm máy chủ.                  |
| **WiFi / TCP/IP**| Giao tiếp giữa các node và hệ thống trung tâm.                      |
| **GitHub**       | Quản lý mã nguồn đồ án.                                               |

---

## 🔄 Quy trình hoạt động

1. **ESP32-CAM** bật camera, tự động nhận diện khuôn mặt người xuất hiện trước camera.
2. Nếu khuôn mặt đã đăng ký, hệ thống xác nhận và ghi nhận thời gian truy cập.
3. **ESP32-CAM** gửi dữ liệu về **ESP8266** (hoặc trực tiếp tới server).
4. **ESP8266** hiển thị trạng thái (đèn, còi, LCD) hoặc chuyển tiếp tới web server.
5. Dữ liệu được log vào hệ thống và có thể cảnh báo nếu phát hiện người lạ.

---

## ✨ Tính năng nổi bật

- 👁️ Nhận diện khuôn mặt thời gian thực ngay trên thiết bị ESP32-CAM.
- 🌐 Giao tiếp không dây qua WiFi, không cần dây tín hiệu.
- 🔔 Có thể mở rộng thêm còi/buzzer khi phát hiện người lạ.
- 🧠 Có thể huấn luyện mô hình nhận diện khuôn mặt trước và upload vào ESP32-CAM.
- 🧩 Dễ dàng mở rộng lên hệ thống quản lý cư dân nhiều tầng.

---

## 🚀 Định hướng phát triển

- Thêm giao diện Web để hiển thị người ra vào theo thời gian thực.
- Đồng bộ dữ liệu với Firebase hoặc MySQL từ xa.
- Phân tích hành vi bất thường qua AI (người lạ xuất hiện nhiều lần, thời gian ra vào bất thường,...)
- Tích hợp màn hình hiển thị hoặc mở cửa thông minh khi nhận diện thành công.

---

## 👤 Thông tin sinh viên

- **Họ tên:** Trần Duy Phúc
- **Mã SV:** 1571020205
- **Lớp:** Lớp CNTT 15-02
- **Trường:** Đại học Đại Nam

---
