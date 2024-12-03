from servo import ServoMotor
import time

servo = ServoMotor(pin=18)  # 서보모터 연결된 GPIO 핀 번호
try:
    while True:
        servo.change_angle(3)    # 0도
        time.sleep(1)
        servo.change_angle(3)   # 90도
        time.sleep(1)
        servo.change_angle(3)  # 180도
        time.sleep(1)
except KeyboardInterrupt:
    print("종료합니다.")
finally:
    servo.cleanup()  # 리소스 해제