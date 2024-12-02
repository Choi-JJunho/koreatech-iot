import hashlib
import hmac
import base64
import requests
import time
from config import ACCESS_KEY, SECRET_KEY


def get_ip():
    return requests.get('https://jsonip.com').json()['ip']


def get_location(ip, enc='utf8', ext='t', response_format_type='json'):
    secret_key = bytes(SECRET_KEY, 'UTF-8')
    timestamp = str(int(time.time() * 1000))

    method = "GET"
    uri = f"/geolocation/v2/geoLocation?enc={enc}&ext={ext}&ip={ip}&responseFormatType={response_format_type}"

    message = bytes(f'{method} {uri}\n{timestamp}\n{ACCESS_KEY}', 'UTF-8')
    signature = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    response = requests.get(
        url=f'https://geolocation.apigw.ntruss.com{uri}',
        headers={
            'x-ncp-apigw-signature-v2': signature,
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': ACCESS_KEY,
            'accept': 'application/json',
        }
    )

    return response.json()
