from gpiozero import Servo
from time import sleep

servo_pin = 18  # 서보 모터 제어 핀 (예: GPIO 12)
servo = Servo(servo_pin)

def set_servo_angle(angle):
    # 각도를 -1에서 1 사이로 변환
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180

    position = -1 + (angle * 2 / 180)  # 각도 값을 -1 ~ 1 사이 값으로 변환
    print(f"Setting angle to {angle}° (position {position})")
    servo.value = position

def move_motor(angle):
    set_servo_angle(angle)
    sleep(2)
    
    servo.detach()
        
def set_motor():
    set_servo_angle(90)
    sleep(2)
    
    servo.detach()


set_motor()
