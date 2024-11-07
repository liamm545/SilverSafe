#include <ESP8266WiFi.h>            // ESP8266용
#include <FirebaseESP8266.h>         // Firebase 라이브러리

#define BUTTON_PIN D5  // 버튼 핀 번호

// WiFi 네트워크 정보
const char* ssid = "LeetaeSky";
const char* password = "leolee11";
// LED 핀 번호
const int ledPin = D7;

// Firebase 프로젝트 정보
#define FIREBASE_HOST "silvercare-84496-default-rtdb.firebaseio.com"   // Firebase URL
#define FIREBASE_AUTH "zsJMptCdlJKjgAnJZanqtAtSQ4gAtchIWvBt33VI"    // Firebase 인증 토큰

// Firebase 객체 생성
FirebaseData firebaseData;



void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT); // LED 핀 설정
  pinMode(BUTTON_PIN, INPUT_PULLUP); // 버튼 핀을 풀업 입력 모드로 설정함

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
  //Serial 모니터 Firebase update
  if (Serial.available()) {
    char input = Serial.read();  // Serial Monitor로부터 입력값을 받음

    if (input == '1') {
      updateFirebaseData("TEST", "On");  // '1' 입력 시 "TEST" 값을 "On"으로 변경
    } 
    else if (input == '0') {
      updateFirebaseData("TEST", "Off"); // '0' 입력 시 "TEST" 값을 "Off"로 변경
    }
  }
  // 버튼 동작: 버튼 누르면 -> Test 1로 변경, 아니면 => TEST OFF
  int buttonState = digitalRead(BUTTON_PIN); // 버튼의 현재 상태 읽음
    Serial.print("bottonState: ");
    Serial.println(buttonState);
    if (buttonState == 0) {   // 버튼이 눌렸을 때 (LOW 상태)
      updateFirebaseData("TEST", "On");  
    } else {                      // 버튼이 눌리지 않았을 때
      updateFirebaseData("TEST", "Off"); // '0' 입력 시 "TEST" 값을 "Off"로 변경
    }


  // Firebase에서 "TEST" 값 확인 및 LED 제어
  if (Firebase.getString(firebaseData, "/TEST")) {
    String value = firebaseData.stringData();
    Serial.println(value);
    if (value == "On") {
      digitalWrite(ledPin, HIGH);
      Serial.println("LED is ON");
    } else if (value == "Off") {
      digitalWrite(ledPin, LOW);
      Serial.println("LED is OFF");
    }
  } else {
    Serial.print("Failed to get data: ");
    Serial.println(firebaseData.errorReason());
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
