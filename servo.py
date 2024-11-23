from gpiozero import Servo
from time import sleep

servo_pin = 18
servo = None
current_angle = 90
MIN_ANGLE = 0
MAX_ANGLE = 180
SPEED_FACTOR = 0.05


def initialize_servo():
    global servo
    if servo is None:
        servo = Servo(servo_pin)
        set_servo_angle(90)
        sleep(1)


def detach_servo():
    global servo
    if servo is not None:
        servo.detach()
        servo = None


def set_servo_angle(angle):
    global current_angle, servo
    if servo is None:
        initialize_servo()
    angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))
    position = -1 + (angle * 2 / 180)
    servo.value = position
    current_angle = angle
    sleep(SPEED_FACTOR)


def move_motor_smoothly(target_angle):
    global current_angle
    if servo is None:
        initialize_servo()
    step = 1 if target_angle > current_angle else -1
    for angle in range(int(current_angle), int(target_angle) + step, step):
        set_servo_angle(angle)
        sleep(SPEED_FACTOR)
    detach_servo()


def get_current_angle():
    return current_angle
