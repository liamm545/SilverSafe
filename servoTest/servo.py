import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pin):
        self.pin = pin
        self.frequency = 50  # 서보모터의 기본 주파수 설정
        GPIO.setmode(GPIO.BCM)  # GPIO 번호 체계 설정
        GPIO.setup(self.pin, GPIO.OUT)  # GPIO 핀을 출력 모드로 설정
        self.pwm = GPIO.PWM(self.pin, self.frequency)  # PWM 객체 생성
        self.pwm.start(0)  # PWM 신호 시작

        self.curAngle = 90
        self.set_angle(90)
   
    def change_angle(self, angle):
        newAngle = self.curAngle + angle
        if(newAngle > 180 or newAngle < 0):
            return
        self.curAngle = newAngle
        angle = self.curAngle


        
        duty = 2 + (angle / 18)  # 각도에 따른 듀티 사이클 계산
        GPIO.output(self.pin, True)  # GPIO 핀 활성화
        self.pwm.ChangeDutyCycle(duty)  # 듀티 사이클 변경
        time.sleep(3)  # 모터가 움직일 시간을 줌
        GPIO.output(self.pin, False)  # GPIO 핀 비활성화
        self.pwm.ChangeDutyCycle(0)  # 듀티 사이클 초기화
    
    def set_angle(self, angle):
        duty = 2 + (angle / 18)  # 각도에 따른 듀티 사이클 계산
        GPIO.output(self.pin, True)  # GPIO 핀 활성화
        self.pwm.ChangeDutyCycle(duty)  # 듀티 사이클 변경
        time.sleep(0.5)  # 모터가 움직일 시간을 줌
        GPIO.output(self.pin, False)  # GPIO 핀 비활성화
        self.pwm.ChangeDutyCycle(0)  # 듀티 사이클 초기화
   
    def cleanup(self):
        self.pwm.stop()  # PWM 정지
        GPIO.cleanup()  # GPIO 설정 초기화
