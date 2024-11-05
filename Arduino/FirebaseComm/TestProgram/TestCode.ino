#include <ESP8266WiFi.h>            // ESP8266용
#include <FirebaseESP8266.h>         // Firebase 라이브러리

// WiFi 네트워크 정보
const char* ssid = "LeetaeSky";
const char* password = "leolee11";

// Firebase 프로젝트 정보
#define FIREBASE_HOST "silvercare-84496-default-rtdb.firebaseio.com"   // Firebase URL
#define FIREBASE_AUTH "zsJMptCdlJKjgAnJZanqtAtSQ4gAtchIWvBt33VI"    // Firebase 인증 토큰

// Firebase 객체 생성
FirebaseData firebaseData;

void setup() {
  Serial.begin(115200);
  
  // WiFi 연결
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("Connected to Wi-Fi");

  // Firebase 초기화
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);

  Serial.println("Enter 1 to set 'TEST' key to 'On' or 0 to set 'TEST' key to 'Off'");
}

void loop() {
  if (Serial.available()) {
    char input = Serial.read();  // Serial Monitor로부터 입력값을 받음

    if (input == '1') {
      updateFirebaseData("TEST", "On");  // '1' 입력 시 "TEST" 값을 "On"으로 변경
    } 
    else if (input == '0') {
      updateFirebaseData("TEST", "Off"); // '0' 입력 시 "TEST" 값을 "Off"로 변경
    }
  }
}

// Firebase 데이터 업데이트 함수
void updateFirebaseData(String path, String value) {
  if (Firebase.setString(firebaseData, path, value)) {
    Serial.print("Data updated to ");
    Serial.println(value);
  } else {
    Serial.print("Failed to update data: ");
    Serial.println(firebaseData.errorReason());
  }
}
