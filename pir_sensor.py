import time
import RPi.GPIO as GPIO
from gpio_setup import PIR_PIN


def pir_monitoring(queue):
    try:
        previous_state = 0  # 이전 상태를 저장할 변수

        while True:
            current_state = GPIO.input(PIR_PIN)  # 현재 상태 읽기

            # 상태가 변경되었을 때만 처리
            if current_state != previous_state:
                if current_state == 1:  # 0 -> 1 (사람 감지)
                    print("사람이 감지되었습니다!")
                    queue.put(True)
                else:  # 1 -> 0 (사람이 사라짐)
                    print("사람이 사라졌습니다!")
                    queue.put(False)

                previous_state = current_state  # 상태 업데이트
                time.sleep(2)  # 디바운싱

            time.sleep(0.1)  # CPU 부하 감소

    except KeyboardInterrupt:
        print("PIR 모니터링 종료")