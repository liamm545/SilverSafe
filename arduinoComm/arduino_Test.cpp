#include <Servo.h>

Servo servo;
#define SERVO D9
void setup() {
  Serial.begin(9600); // 시리얼 통신 시작
  servo.attach(SERVO);    // 서보 모터 핀 연결 (예: D9 핀)
}

void loop() {
  if (Serial.available() > 0) { // 데이터가 수신되었는지 확인
    int angle = Serial.parseInt(); // 수신된 데이터를 각도로 변환
    if (angle >= 0 && angle <= 180) { // 각도가 유효한 범위인지 확인
      servo.write(angle); // 서보 모터를 해당 각도로 이동
    }
  }
}
