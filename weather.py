import enum
from enum import Enum

import requests
from datetime import datetime, timedelta

from calc import convert_coords
from config import API_KEY
from location import get_location, get_ip


class Weather(Enum):
    맑음 = enum.auto()
    구름많음 = enum.auto()
    흐림 = enum.auto()
    비 = enum.auto()
    비눈 = enum.auto()
    눈 = enum.auto()
    소나기 = enum.auto()


def get_weather_forecast(base_time, nx, ny):
    # Define the base URL and the API key
    base_url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    api_key = API_KEY

    # Set up the parameters for the API call
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 100,
        "dataType": "JSON",
        "base_date": datetime.now().strftime("%Y%m%d"),  # Use current date
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }

    # Make the API request
    response = requests.get(base_url, params=params)
    print(response.url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        # Handle errors
        print("Error:", response.status_code, response.text)
        return None


def extract_forecast_data(forecast_data):
    # Check if the response is normal
    data = []
    if forecast_data['response']['header']['resultCode'] == '00':
        # Extract items from the response body
        items = forecast_data['response']['body']['items']['item']

        # Process each item
        for item in items:
            base_date = item['baseDate']
            base_time = item['baseTime']
            category = item['category']
            fcst_date = item['fcstDate']
            fcst_time = item['fcstTime']
            fcst_value = item['fcstValue']
            nx = item['nx']
            ny = item['ny']

            if category in {'PTY', 'SKY'}:
                # Print or process the forecast data as needed
                print(f"Category: {category}, Forecast Date: {fcst_date}, Base Time: {base_time},"
                      f" Forecast Time: {fcst_time}, Value: {fcst_value}")

                data.append({'category': category, 'time': fcst_date + fcst_time, 'value': fcst_value})

    else:
        print("Error in response:", forecast_data['response']['header']['resultMsg'])

    return data


def get_weather():
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

    current_time = datetime.now()

    # 변환된 nx, ny 값으로 날씨 예보 조회
    forecast_data = get_weather_forecast(current_time.strftime("%H%M"), nx, ny)
    forecast_data = extract_forecast_data(forecast_data)
    forecast_data.sort(key=lambda x: abs(current_time - datetime.strptime(x['time'], '%Y%m%d%H%M')))
    forecast_data = forecast_data[:2]

    # 하늘 상태(SKY) 코드: 맑음(1), 구름많음(3), 흐림(4)

    # 강수 형태(PTY) 코드
    # (초단기) 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
    # (단기) 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4)

    data = dict()
    for item in forecast_data:
        data[item['category']] = item['value']

    weather = Weather.맑음
    if data['PTY'] == 0:
        if data['SKY'] == 3:
            weather = Weather.구름많음
        elif data['SKY'] == 4:
            weather = Weather.흐림
    elif data['PTY'] == 1:
        weather = Weather.비
    elif data['PTY'] == 2:
        weather = Weather.비눈
    elif data['PTY'] == 3:
        weather = Weather.눈
    elif data['PTY'] == 4:
        weather = Weather.소나기

    print(weather)
    return weather
