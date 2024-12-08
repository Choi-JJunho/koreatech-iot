import RPi.GPIO as gpio
from gpio_setup import LED_PIN
from weather import Weather


def control_led(weather):
    if weather == Weather.맑음:
        ...
        # GPIO.output(LED_R_PIN, GPIO.HIGH)
        # GPIO.output(LED_G_PIN, GPIO.LOW)
        # GPIO.output(LED_B_PIN, GPIO.LOW)
    elif weather in {Weather.구름많음, Weather.흐림}:
        ...
        # GPIO.output(LED_R_PIN, GPIO.LOW)
        # GPIO.output(LED_G_PIN, GPIO.LOW)
        # GPIO.output(LED_B_PIN, GPIO.HIGH)
    elif weather == Weather.비:
        ...
    elif weather == Weather.비눈:
        ...
        # GPIO.output(LED_R_PIN, GPIO.LOW)
        # GPIO.output(LED_G_PIN, GPIO.HIGH)
        # GPIO.output(LED_B_PIN, GPIO.LOW)
    elif weather == Weather.눈:
        ...
    elif weather == Weather.소나기:
        ...
