from multiprocessing import Process, Queue
import time
from gpio_setup import init_gpio, cleanup_gpio
from pir_sensor import pir_monitoring
from led_control import control_led
from motor_control import control_motor
from weather import get_weather, Weather

# 프로세스 간 통신을 위한 큐 생성
queue = Queue()


def weather_and_control(queue):
    try:
        while True:
            if not queue.empty():
                if queue.get():
                    weather = get_weather()
                    control_led(weather)
                    control_motor(weather)
                else:
                    control_motor(Weather.UNKNOWN)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("제어 프로세스 종료")


if __name__ == '__main__':
    # from weather import get_weather
    # get_weather()
    try:
        # GPIO 초기화
        init_gpio()

        # 프로세스 생성 및 시작
        pir_process = Process(target=pir_monitoring, args=(queue,))
        control_process = Process(target=weather_and_control, args=(queue,))

        pir_process.start()
        control_process.start()

        # 프로세스 종료 대기
        pir_process.join()
        control_process.join()

    except KeyboardInterrupt:
        print("프로그램 종료")
    finally:
        cleanup_gpio()
