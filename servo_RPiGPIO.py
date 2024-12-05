import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
SERVO_PIN = 18  # 서보모터가 연결된 GPIO 핀 번호

# GPIO 설정
GPIO.setmode(GPIO.BCM)  # GPIO 핀 번호 체계를 BCM으로 설정
GPIO.setup(SERVO_PIN, GPIO.OUT)  # 서보모터 핀을 출력으로 설정

# PWM 설정
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz 주파수 (서보모터 기본값)
pwm.start(0)  # PWM 신호 시작 (초기값 0)

def set_angle(angle):
    """
    주어진 각도로 서보모터를 회전함
    :param angle: 0~180 사이의 각도
    """
    duty = 2 + (angle / 18)  # 각도에 따라 듀티 사이클 계산
    GPIO.output(SERVO_PIN, True)  # 핀 활성화
    pwm.ChangeDutyCycle(duty)  # 듀티 사이클 변경
    time.sleep(0.5)  # 잠시 대기 (모터가 움직이는 시간)
    GPIO.output(SERVO_PIN, False)  # 핀 비활성화
    pwm.ChangeDutyCycle(0)  # 듀티 사이클 초기화

try:
    while True:
        # 0도 설정
        set_angle(0)
        time.sleep(1)
       
        # 90도 설정
        set_angle(90)
        time.sleep(1)
       
        # 180도 설정
        set_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    print("종료합니다.")
   
finally:
    pwm.stop()  # PWM 종료
    GPIO.cleanup()  # GPIO 상태 초기화

