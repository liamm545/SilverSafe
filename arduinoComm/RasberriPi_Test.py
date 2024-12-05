import serial
import time

# 아두이노와 연결된 포트 설정 (예: /dev/ttyUSB0 또는 /dev/ttyACM0)
arduino = serial.Serial(port='/dev/ttyHI', baudrate=9600, timeout=None)

def send_angle(angle):
    """각도를 아두이노로 전송"""
    if 0 <= angle <= 180:
        arduino.write(f"{angle}\n".encode())  # 각도를 문자열로 변환 후 전송
        time.sleep(0.1)  # 약간의 대기 시간

try:
    while True:
        angle = int(input("Enter angle (0-180): "))  # 사용자 입력
        send_angle(angle)  # 입력된 각도 전송
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    arduino.close()  # 시리얼 포트 닫기
