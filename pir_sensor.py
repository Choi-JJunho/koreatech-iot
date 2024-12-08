import time
import RPi.GPIO as GPIO
from gpio_setup import PIR_PIN

def pir_monitoring(queue):
    try:
        while True:
            if GPIO.input(PIR_PIN):
                print("움직임 감지!")
                queue.put(True)
                time.sleep(2)  # 디바운싱
            else:
                queue.put(False)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("PIR 모니터링 종료")
