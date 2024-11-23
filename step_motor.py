import RPi.GPIO as GPIO
from time import sleep

# ULN2003 모듈 핀 설정 (IN1, IN2, IN3, IN4)
step_pins = [17, 18, 27, 22]  # GPIO 핀 번호

# 스텝 시퀀스 (한 단계당 4개의 신호)
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]

# 스텝모터 설정
STEPS_PER_REV = 4096  # 스텝모터의 전체 회전 스텝 수 (4096 스텝 = 360도)
DEGREES_PER_STEP = 360 / STEPS_PER_REV  # 각 스텝이 이동하는 각도

# 현재 각도
current_angle = 90

# 최소 및 최대 각도 제한
MIN_ANGLE = 0
MAX_ANGLE = 180

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
for pin in step_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

def rotate_motor(steps, delay=0.002):
    """스텝모터를 지정된 스텝 수만큼 회전"""
    if steps > 0:
        direction = 1  # 정방향
    else:
        direction = -1  # 역방향
        steps = abs(steps)
    
    for _ in range(steps):
        for step in range(len(step_sequence)):
            for pin in range(4):
                GPIO.output(step_pins[pin], step_sequence[step][pin] if direction > 0 else step_sequence[-step - 1][pin])
            sleep(delay)

def set_motor_angle(target_angle):
    """스텝모터를 서보모터처럼 특정 각도로 이동"""
    global current_angle

    # 각도를 제한
    target_angle = max(MIN_ANGLE, min(MAX_ANGLE, target_angle))

    # 현재 각도와 목표 각도 간의 차이 계산
    angle_difference = target_angle - current_angle
    steps_to_move = int(angle_difference / DEGREES_PER_STEP)

    print(f"Moving from {current_angle}° to {target_angle}°")
    rotate_motor(steps_to_move)

    # 현재 각도 업데이트
    current_angle = target_angle
    sleep(0.5)  # 모터가 이동할 시간을 부여

def move_motor(target_angle):
    set_motor_angle(target_angle)
    print(f"Motor moved to {target_angle}°")

def get_current_angle():
    return current_angle

def cleanup_motor():
    """GPIO 핀 정리"""
    GPIO.cleanup()

# 테스트: 스텝모터를 서보모터처럼 사용
try:
    move_motor(0)    # 0도로 이동
    move_motor(90)   # 90도로 이동
    move_motor(180)  # 180도로 이동
    move_motor(90)   # 다시 90도로 이동
finally:
    cleanup_motor()  # GPIO 정리
