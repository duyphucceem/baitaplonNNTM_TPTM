import cv2
import numpy as np
import requests
from tkinter import *
from PIL import Image, ImageTk
import threading
import socket

ESP32_STREAM_URL = "http://172.20.10.2/stream"

sample_image = None  # Ảnh mẫu toàn cục


# Hàm đọc 1 frame từ luồng MJPEG
def get_frame_from_stream(url):
    stream = requests.get(url, stream=True)
    bytes_data = b""
    for chunk in stream.iter_content(chunk_size=1024):
        bytes_data += chunk
        a = bytes_data.find(b'\xff\xd8')  # JPEG start
        b = bytes_data.find(b'\xff\xd9')  # JPEG end
        if a != -1 and b != -1:
            jpg = bytes_data[a:b + 2]
            bytes_data = bytes_data[b + 2:]
            img_array = np.frombuffer(jpg, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            return img
    return None


# Lưu ảnh mẫu
def save_sample():
    global sample_image
    img = get_frame_from_stream(ESP32_STREAM_URL)
    if img is not None:
        sample_image = img.copy()
        cv2.imwrite("sample.jpg", sample_image)
        result_label.config(text="✅ Đã lưu ảnh mẫu")
    else:
        result_label.config(text="❌ Không lấy được ảnh")


# So sánh ảnh hiện tại với ảnh mẫu (dùng trong GUI)
def compare_image():
    global sample_image
    img = get_frame_from_stream(ESP32_STREAM_URL)
    if img is None or sample_image is None:
        result_label.config(text="⚠️ Thiếu ảnh mẫu hoặc ảnh mới")
        return

    # Resize cho giống kích thước
    img_resized = cv2.resize(img, (sample_image.shape[1], sample_image.shape[0]))

    # So sánh đơn giản dùng diff
    diff = cv2.absdiff(sample_image, img_resized)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    percent_diff = (np.count_nonzero(thresh) / thresh.size) * 100

    if percent_diff < 20:
        result_label.config(text="✅ Hình ảnh khớp (%.2f%% khác biệt)" % percent_diff)
    else:
        result_label.config(text="❌ Hình ảnh KHÔNG khớp (%.2f%% khác biệt)" % percent_diff)


# So sánh ảnh trả về kết quả string (dùng cho TCP server)
def compare_image_socket():
    global sample_image
    img = get_frame_from_stream(ESP32_STREAM_URL)
    if img is None or sample_image is None:
        return "NO_IMAGE"

    img_resized = cv2.resize(img, (sample_image.shape[1], sample_image.shape[0]))
    diff = cv2.absdiff(sample_image, img_resized)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    percent_diff = (np.count_nonzero(thresh) / thresh.size) * 100

    if percent_diff < 20:
        return f"OK:{percent_diff:.2f}"
    else:
        return f"FAIL:{percent_diff:.2f}"


# Hiển thị ảnh live liên tục trên GUI
def update_preview():
    img = get_frame_from_stream(ESP32_STREAM_URL)
    if img is not None:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        preview_label.imgtk = img_tk
        preview_label.configure(image=img_tk)
    preview_label.after(100, update_preview)


# Xử lý kết nối từ ESP
def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8').strip()
            if not msg:
                break
            print(f"Nhận lệnh từ ESP: {msg}")
            if msg == "REQ_PROCESS":
                result = compare_image_socket()
                client_socket.send((result + "\n").encode('utf-8'))
            else:
                client_socket.send(b"UNKNOWN_COMMAND\n")
        except Exception as e:
            print(f"Lỗi kết nối client: {e}")
            break
    client_socket.close()


# Khởi chạy TCP server để ESP kết nối
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))  # Mở port 5000 chờ kết nối
    server.listen(5)
    print("Server đang chờ ESP kết nối ở port 5000...")
    while True:
        client_socket, addr = server.accept()
        print(f"ESP kết nối từ {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


# GUI tkinter
root = Tk()
root.title("ESP32-CAM So sánh ảnh")

preview_label = Label(root)
preview_label.pack()

btn_frame = Frame(root)
btn_frame.pack()

Button(btn_frame, text="📷 Lưu ảnh mẫu", command=save_sample, width=20).pack(side=LEFT, padx=10, pady=10)
Button(btn_frame, text="🔍 So sánh ảnh", command=compare_image, width=20).pack(side=LEFT, padx=10, pady=10)

result_label = Label(root, text="", font=("Arial", 12), fg="blue")
result_label.pack(pady=5)

# Bắt đầu cập nhật live stream
update_preview()

# Chạy server trong thread riêng để không block GUI
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

root.mainloop()
