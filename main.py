from calc import convert_coords
from location import *
from weather import *


if __name__ == '__main__':
    # 위치 정보 가져오기
    location_json = get_location(ip=get_ip())

    print(location_json)

    # 위도/경도 추출
    lat = location_json['geoLocation']['lat']
    lon = location_json['geoLocation']['long']

    print(lat, lon)

    # 기상청 격자 좌표로 변환
    nx, ny = convert_coords(0, lon, lat)

    print(f"위도/경도: ({lat}, {lon}) -> 기상청 좌표: (nx={nx}, ny={ny})")

    current_time = datetime.now().strftime("%H%M")

    # 변환된 nx, ny 값으로 날씨 예보 조회
    forecast_data = get_weather_forecast(current_time, nx, ny)
    extract_forecast_data(forecast_data)
