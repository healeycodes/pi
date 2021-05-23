# setup GPS w/ https://gitlab.com/gpsd/gpsd
import gps
import time
import requests
from datetime import datetime


def sky_thread(URL, PW):
    def t():
        return f"{datetime.now()}"

    def send_sats():
        print(f"{t()} send_sats - looking..")
        try:
            gpsd = gps.gps(mode=gps.WATCH_ENABLE)
            sats = set()
            for _ in range(0, 10):
                gpsd.next()
                if "satellites" in gpsd.data:
                    for sat in gpsd.data["satellites"]:
                        sats.add(sat["PRN"])
                time.sleep(1)

            # if none are found it's probably a gpsd<->python problem
            if len(sats) == 0:
                print(f"{t()} send_sats - zero sats found")
                return

            sats = ",".join([str(sat) for sat in sats])
        except Exception as err:
            print(f"{t()} send_sats - looking error .. {err}")

        try:
            print(f"{t()} send_sats - sending: {sats}")
            r = requests.get(f"{URL}/satellites/send?sats={sats}&password={PW}")
            if r.status_code != 200:
                print(f"{t()} send_sats - .. status code: {r.status_code}: {r.text}")
        except Exception as err:
            print(f"{t()} send_sats - sending error .. {err}")

    while True:
        now = datetime.now().hour
        # sleep to save on Heroku dyno hours
        if now > 7 and now < 22:
            send_sats()
