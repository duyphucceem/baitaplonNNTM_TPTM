# Đồ án môn học: Hệ thống giám sát và điều khiển sử dụng Arduino & Python

## 📌 Giới thiệu

Đây là đồ án lớn thuộc học phần Nông nghiệp thông minh và Thành phố thông minh (NNTM & TPTM), sử dụng kết hợp giữa nền tảng **Arduino** (ESP32, Uno) và **Python** để xây dựng hệ thống giám sát và điều khiển từ xa.

## 🔧 Thành phần chính

- `CameraWebServer.ino`: Chương trình Arduino điều khiển camera giám sát và các cảm biến.
- `code_node.ino`: Điều khiển thiết bị từ xa, nhận tín hiệu và xử lý.
- `MAIN.py`: Phần mềm viết bằng Python, dùng để thu thập dữ liệu và điều khiển phần cứng qua giao tiếp nối tiếp (Serial).

## 🖥️ Công nghệ sử dụng

- Arduino IDE
- ESP32 hoặc Arduino Uno
- Python 3.x (chạy trên máy tính hoặc Raspberry Pi)
- Giao tiếp Serial (UART)
- Git & GitHub để quản lý mã nguồn

## 🚀 Hướng dẫn chạy

### 1. Upload mã Arduino
- Mở `.ino` bằng Arduino IDE
- Chọn đúng bo mạch (ESP32, Uno, v.v.)
- Bấm **Upload**

### 2. Chạy chương trình Python
```bash
python MAIN.py
