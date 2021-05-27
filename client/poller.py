import sys
import threading
from clientconfig import CONFIG
from sky import sky_thread
from printer import printer_thread
from weather import weather_thread

"""
Point this program to your server e.g. "python poller.py https://your-url.herokuapp.com password_here"
                                                          (Note: no trailing slash     ^)
I start it in the background via .bashrc
"""

URL = sys.argv[1]
PW = sys.argv[2]
SLEEP_AT_NIGHT = (
    True  # to use a Heroku Dyno in the free tier without maxing out your hours
)

if CONFIG.printer:
    printer_instance = threading.Thread(
        target=printer_thread, args=(URL, PW, SLEEP_AT_NIGHT)
    )
    printer_instance.start()
    print("printer mod started!")

if CONFIG.sky:
    sky_instance = threading.Thread(target=sky_thread, args=(URL, PW, SLEEP_AT_NIGHT))
    sky_instance.start()
    print("sky mod started!")

if CONFIG.weather:
    weather_instance = threading.Thread(
        target=weather_thread, args=(URL, PW, SLEEP_AT_NIGHT)
    )
    weather_instance.start()
    print("weather mod started!")
