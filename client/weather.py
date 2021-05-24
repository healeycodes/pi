import time
import requests
import Adafruit_DHT
from datetime import datetime

"""
Requires a AM2302 sensor (but compatible with any temp/humidity sensor with modifications).
"""

FRUITS = {
    "11": Adafruit_DHT.DHT11,
    "22": Adafruit_DHT.DHT22,
    "2302": Adafruit_DHT.AM2302,
}


def weather_thread(URL, PW):
    def t():
        return f"{datetime.now()}"

    def get_weather():
        sensor = FRUITS["2302"]
        pin = 4

        # https://github.com/adafruit/Adafruit_Python_DHT/blob/master/examples/AdafruitDHT.py
        # try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            if humidity is not None and temperature is not None:
                return [humidity, temperature]
            else:
                print(f"{t()} get_weather - failed to get reading")

    def send_weather(data):
        temperature, humidity = data
        try:
            print(f"{t()} send_weather - sending: {(temperature, humidity)}")
            r = requests.get(
                f"{URL}/weather/send?temperature={temperature}&humidity={humidity}password={PW}"
            )
            if r.status_code != 200:
                print(f"{t()} send_weather - .. status code: {r.status_code}: {r.text}")
        except Exception as err:
            print(f"{t()} send_weather - sending error .. {err}")

    while True:
        now = datetime.now().hour
        # sleep to save on Heroku dyno hours
        if now > 7 and now < 22:
            data = get_weather()
            if data:
                send_weather(data)

        time.sleep(10)


if __name__ == "__main__":
    weather_thread("_", "_")
