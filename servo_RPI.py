import RPi.GPIO as GPIO
from time import sleep

# Servo motor control pin
servo_pin = 18

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Initialize PWM on the servo pin at 50Hz
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz for servo motor
pwm.start(7.5)  # Neutral position (90°)

# Initial angle of the servo motor
current_angle = 90

# Minimum and maximum angle for the servo motor
MIN_ANGLE = 0
MAX_ANGLE = 180


def set_servo_angle(angle):
    global current_angle

    # Clamp angle within bounds
    angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))

    # Convert angle to duty cycle (2.5 to 12.5)
    duty_cycle = 2.5 + (angle / 180.0) * 10
    print(f"Setting angle to {angle}° (duty cycle {duty_cycle}%)")
    pwm.ChangeDutyCycle(duty_cycle)

    # Update current angle
    current_angle = angle
    sleep(0.5)  # Allow time for the servo motor to move


def move_motor(target_angle):
    set_servo_angle(target_angle)
    print(f"Moved motor to {target_angle}°")


def get_current_angle():
    return current_angle


def set_motor():
    set_servo_angle(90)
    sleep(2)

    # Stop PWM (detach)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()  # Reset GPIO settings
