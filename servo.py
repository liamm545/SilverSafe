import RPi.GPIO as GPIO
from time import sleep

class ServoMotor:
    MIN_DUTY = 2  # 0도에 해당
    MAX_DUTY = 12  # 120도에 해당

    def __init__(self, pin, frequency=50):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, frequency)
        self.pwm.start(0)

    def set_angle(self, angle):
        if 0 <= angle <= 120:
            duty = self.MIN_DUTY + (angle / 120) * (self.MAX_DUTY - self.MIN_DUTY)
            self.pwm.ChangeDutyCycle(duty)
            print(f"Servo angle set to {angle}° (Duty: {duty}%)")
        else:
            print("Angle out of range. Must be between 0 and 120 degrees.")

    def stop(self):
        self.pwm.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    servo = ServoMotor(pin=12)  # GPIO 핀 12 사용

    try:
        while True:
            angle = float(input("Enter angle (0-120): "))
            servo.set_angle(angle)
            sleep(1)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        servo.stop()
