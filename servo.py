from gpiozero import Servo
from time import sleep

# Servo motor control pin
servo_pin = 18
servo = Servo(servo_pin)

# Initial angle of the servo motor
current_angle = 90

# Minimum and maximum angle for the servo motor
MIN_ANGLE = 0
MAX_ANGLE = 180


def set_servo_angle(angle):
    global current_angle

    # Clamp angle within bounds
    angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))

    # Convert angle to servo position (-1 to 1)
    position = -1 + (angle * 2 / 180)
    #print(f"Setting angle to {angle}° (position {position})")
    servo.value = position

    # Update current angle
    current_angle = angle
    sleep(0.5)  # Allow time for the servo motor to move


def move_motor(target_angle):
    set_servo_angle(target_angle)
    #print(f"Moved motor to {target_angle}°")
    sleep(2)


def get_current_angle():
    return current_angle


def set_motor():
    set_servo_angle(90)
    sleep(2)

    servo.detach()
