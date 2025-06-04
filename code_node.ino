#include <ESP8266WiFi.h>
#include <Servo.h>

const char* ssid = "phuc123";
const char* password = "24092005";

const char* server_ip = "172.20.10.3";
const uint16_t server_port = 5000;

WiFiClient client;

const int buttonPin = D4;  // nút nhấn (phải có điện trở kéo lên nếu không dùng INPUT_PULLUP)
bool lastButtonState = HIGH;

const int servoPin = D2;   // chân kết nối SG90
Servo myServo;

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT_PULLUP);
  myServo.attach(servoPin);
  myServo.write(0);  // đóng cửa ban đầu

  WiFi.begin(ssid, password);
  Serial.print("Đang kết nối WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Đã kết nối WiFi, IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  bool buttonState = digitalRead(buttonPin);

  // Phát hiện nhấn nút
  if (lastButtonState == HIGH && buttonState == LOW) {
    Serial.println("Nút nhấn, gửi lệnh đến Python server...");

    if (client.connect(server_ip, server_port)) {
      Serial.println("Đã kết nối server TCP");

      client.println("REQ_PROCESS");

      unsigned long timeout = millis() + 5000;  // đợi 5 giây
      while (!client.available() && millis() < timeout) {
        delay(10);
      }

      if (client.available()) {
        String response = client.readStringUntil('\n');
        response.trim();
        Serial.print("Phản hồi từ server: ");
        Serial.println(response);

        if (response.startsWith("OK")) {
          Serial.println("Ảnh khớp! Mở cửa...");
          myServo.write(180);  // mở cửa
          delay(3000);        // đợi 3 giây
          Serial.println("Đóng cửa lại.");
          myServo.write(0);   // đóng cửa
        } else if (response.startsWith("FAIL")) {
          Serial.println("Ảnh không khớp!");
        } else {
          Serial.println("Kết quả không rõ");
        }
      } else {
        Serial.println("Không nhận được phản hồi từ server");
      }

      client.stop();
    } else {
      Serial.println("Kết nối server TCP thất bại");
    }
  }

  lastButtonState = buttonState;
  delay(50);
}
