import pigpio
from time import sleep

# Servo motor control pin
servo_pin = 18
pi = pigpio.pi()  # pigpio 데몬과 연결
if not pi.connected:
    raise RuntimeError("pigpio daemon is not running")

# Initial angle of the servo motor
current_angle = 90

# Minimum and maximum angle for the servo motor
MIN_ANGLE = 0
MAX_ANGLE = 180


def set_servo_angle(angle):
    global current_angle

    # Clamp angle within bounds
    angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))

    # Convert angle to pulse width (500 to 2500 microseconds)
    pulse_width = int(500 + (angle / 180.0) * 2000)
    print(f"Setting angle to {angle}° (pulse width {pulse_width}us)")
    pi.set_servo_pulsewidth(servo_pin, pulse_width)

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

    # Stop sending PWM signal (detach)
    pi.set_servo_pulsewidth(servo_pin, 0)
    pi.stop()  # Clean up pigpio resources
