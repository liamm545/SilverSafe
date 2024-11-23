from gpiozero import Servo
from time import sleep

class ServoMotor:
    def __init__(self):
        self.servo = None
        self.current_angle = -1
    def set_servo(self, pin):
        """
        서보 모터의 핀을 설정하고, 초기 위치를 0도로 이동
        """
        self.servo = Servo(18) # 18번 핀으로 설정.
        self.current_angle = 90
        self.move_servo(self.current_angle)  # 초기화: 0도로 이동
        print(f"Servo initialized on pin {pin} and moved to 0 degrees.")

    def move_servo(self, angle):
        """
        서보 모터를 지정된 각도로 이동
        :param angle: 이동할 각도 (0~180)
        """
        new_angle = self.current_angle + angle
        if (0 <= new_angle <= 180):
            normalized_angle = (angle / 180.0) * 2 - 1.0
            self.servo.value = normalized_angle
            self.current_angle = new_angle
            sleep(0.1)  # 안정화 대기 -> 없어도 될 듯.
            print(f"Servo moved to {angle} degrees.")    
        else:
            print("out of range")
        
        



# # Servo motor control pin
# servo_pin = 18
# servo = Servo(servo_pin)

# # Initial angle of the servo motor
# current_angle = 0.0


# # Minimum and maximum angle for the servo motor
# MIN_ANGLE = -180
# MAX_ANGLE = 180


# def set_servo_angle(angle):
#     global current_angle

#     # Clamp angle within bounds
#     angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))

#     # Convert angle to servo position (-1 to 1)
#     position = -1 + (angle * 2 / 180)
#     #print(f"Setting angle to {angle}° (position {position})")
#     servo.value = position

#     # Update current angle
#     current_angle = angle
#     sleep(0.5)  # Allow time for the servo motor to move


# def move_motor(target_angle):
#     set_servo_angle(target_angle)
#     #print(f"Moved motor to {target_angle}°")
#     sleep(2)


# def get_current_angle():
#     return current_angle


# def set_motor():
#     set_servo_angle(90)
#     sleep(2)

#     servo.detach()
