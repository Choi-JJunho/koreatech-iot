import requests
from datetime import datetime
from config import API_KEY


def get_weather_forecast(base_time, nx, ny):
    # Define the base URL and the API key
    base_url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    api_key = API_KEY

    # Set up the parameters for the API call
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "JSON",
        "base_date": datetime.now().strftime("%Y%m%d"),  # Use current date
        "base_time": base_time,
        "nx": nx,
        "ny": ny
    }

    # Make the API request
    response = requests.get(base_url, params=params)

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

            # Print or process the forecast data as needed
            print(f"Category: {category}, Forecast Date: {fcst_date}, Base Time: {base_time},"
                  f" Forecast Time: {fcst_time}, Value: {fcst_value}")
    else:
        print("Error in response:", forecast_data['response']['header']['resultMsg'])
