import RPi.GPIO as gpio

# GPIO 핀 번호 상수 정의
PIR_PIN = 21
LED_PIN = 24
MOTOR_PIN = 18

def init_gpio():
    gpio.setmode(gpio.BCM)
    gpio.setup(PIR_PIN, gpio.IN)
    gpio.setup(LED_PIN, gpio.OUT)
    gpio.setup(MOTOR_PIN, gpio.OUT)

def cleanup_gpio():
    gpio.cleanup()
    print("GPIO cleanup")
