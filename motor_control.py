import time
import RPi.GPIO as GPIO
from gpio_setup import MOTOR_PIN
from weather import Weather


def control_motor(weather):
    try:
        if weather == Weather.UNKNOWN: return

        GPIO.output(MOTOR_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(MOTOR_PIN, GPIO.LOW)
    except Exception as e:
        print(f"모터 제어 중 오류 발생: {e}")
