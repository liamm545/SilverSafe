from gpiozero import Servo
from time import sleep

# Servo motor control pin
# servo_pin = 18
# servo = Servo(servo_pin)

# Initial angle of the servo motor
current_angle = 90

# Minimum and maximum angle for the servo motor
MIN_ANGLE = 0
MAX_ANGLE = 180

# Speed factor for smooth movement
SPEED_FACTOR = 0.02  # Increase for slower movement


def set_servo_angle(angle):
    global current_angle

    servo_pin = 18
    servo = Servo(servo_pin)

    # Clamp angle within bounds
    angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))

    # Convert angle to servo position (-1 to 1)
    position = -1 + (angle * 2 / 180)
    servo.value = position

    # Update current angle
    current_angle = angle
    sleep(SPEED_FACTOR)  # Allow time for the servo motor to move slightly


def move_motor_smoothly(target_angle):
    global current_angle

    servo_pin = 18
    servo = Servo(servo_pin)

    # Determine the step direction (1 for increasing, -1 for decreasing)
    step = 1 if target_angle > current_angle else -1

    # Gradually move the servo to the target angle
    for angle in range(current_angle, target_angle + step, step):
        set_servo_angle(angle)
        sleep(SPEED_FACTOR)  # Further slow down movement

    servo.detach()


def get_current_angle():
    return current_angle
