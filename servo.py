import RPi.GPIO as GPIO

class ServoMotor:
    MIN_ANGLE = 0
    MAX_ANGLE = 180

    def __init__(self, servo_pin, frequency=50):
        self.servo_pin = servo_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.servo = GPIO.PWM(self.servo_pin, frequency)
        self.servo.start(0)
        self.current_angle = 90  # 초기 각도

    def move_motor(self, target_angle):
        target_angle = max(self.MIN_ANGLE, min(self.MAX_ANGLE, target_angle))
        duty_cycle = (target_angle / 18.0) + 2  # 각도를 DutyCycle로 변환
        self.servo.ChangeDutyCycle(duty_cycle)
        self.current_angle = target_angle
        print(f"Servo moved to {target_angle}°")

    def get_current_angle(self):
        return self.current_angle

    def stop(self):
        self.servo.stop()
        GPIO.cleanup()
