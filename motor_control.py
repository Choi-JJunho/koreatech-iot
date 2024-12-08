import time
import RPi.GPIO as gpio
from gpio_setup import MOTOR_PIN
from weather import Weather


def calculate_angle(weather):
    """
    Weather enum 값을 기반으로 서보 모터 각도 계산
    전체 원판을 8등분(0-7)하여 각 부분의 중앙 각도를 계산
    서보 모터는 보통 0-180도 범위를 사용
    """
    sections = len(Weather)  # Weather enum의 총 개수 (8)
    degrees_per_section = 180 / sections  # 각 구역당 각도 (22.5도)

    # weather.value에 degrees_per_section을 곱하여 해당 위치의 각도 계산
    angle = weather.value * degrees_per_section

    return angle


def control_motor(weather):
    try:
        # PWM 설정 (50Hz)
        servo = gpio.PWM(MOTOR_PIN, 50)
        servo.start(0)

        # 각도를 듀티 사이클로 변환 (서보 모터 각도 범위: 0-180도, 듀티 사이클 범위: 2.5-12.5)
        angle = calculate_angle(weather)
        duty_cycle = (angle / 18) + 2.5

        # 서보 모터 제어
        servo.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # 모터가 지정된 위치로 이동할 시간 부여

        # PWM 정지
        servo.stop()

    except Exception as e:
        print(f"모터 제어 중 오류 발생: {e}")
