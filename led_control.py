import board
import neopixel
from weather import Weather

# LED Ring 설정
PIXEL_COUNT = 24
pixel_pin = board.D18
ORDER = neopixel.GRB

# 날씨별 색상 정의 (R, G, B)
WEATHER_COLORS = {
    Weather.맑음: (255, 255, 0),  # 노란색
    Weather.구름많음: (192, 192, 192),  # 회색
    Weather.흐림: (128, 128, 128),  # 어두운 회색
    Weather.비: (0, 191, 255),  # 하늘색
    Weather.비눈: (176, 224, 230),  # 파스텔 블루
    Weather.눈: (255, 255, 255),  # 흰색
    Weather.소나기: (0, 0, 139),  # 다크 블루
    Weather.UNKNOWN: (20, 20, 25)  # 매우 어두운 회색빛 보라 (꺼진 것이 아닌 어두운 빛)
}


class LEDController:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(
            pixel_pin,
            PIXEL_COUNT,
            brightness=0.5,
            auto_write=False,
            pixel_order=ORDER
        )

    def set_color(self, weather=Weather.UNKNOWN, off=False):
        if off:
            self.pixels.fill((0, 0, 0))  # 완전히 끄기
        else:
            color = WEATHER_COLORS[weather]  # UNKNOWN도 동일하게 색상 표현
            self.pixels.fill(color)

        self.pixels.show()

    def cleanup(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()


def control_led(weather=Weather.UNKNOWN, off=False):
    try:
        led_controller = LEDController()
        led_controller.set_color(weather, off)
    except Exception as e:
        print(f"LED 제어 중 오류 발생: {e}")
