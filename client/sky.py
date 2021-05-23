import gps
import time
import requests
from datetime import datetime

"""
Setup GPS w/ https://gitlab.com/gpsd/gpsd
"""


def sky_thread(URL, PW):
    gpsd = gps.gps(mode=gps.WATCH_ENABLE)

    def t():
        return f"{datetime.now()}"

    def send_sats():
        print(f"{t()} send_sats - looking..")
        try:
            gpsd.next()
            print(f"{t()} send_sats - gpsd.data: {gpsd.data}")

            sats = set()
            if "satellites" in gpsd.data:
                for sat in gpsd.data["satellites"]:
                    sats.add(sat["PRN"])

            # if none are found it's probably a gpsd<->python problem
            if len(sats) == 0:
                print(f"{t()} send_sats - zero sats found")
                return

            sats = ",".join([str(sat) for sat in sats])
        except Exception as err:
            print(f"{t()} send_sats - looking error .. {err}")

        try:
            print(f"{t()} send_sats - sending: {sats}")
            r = requests.get(f"{URL}/sky/send?sats={sats}&password={PW}")
            if r.status_code != 200:
                print(f"{t()} send_sats - .. status code: {r.status_code}: {r.text}")
        except Exception as err:
            print(f"{t()} send_sats - sending error .. {err}")

    while True:
        now = datetime.now().hour
        # sleep to save on Heroku dyno hours
        if now > 7 and now < 22:
            send_sats()
            time.sleep(10)

        # poll gpsd more often than the reporting time so the buffer doesn't
        # get outdated or fill up
        while True:
            start = time.time()
            gpsd.next()
            end = time.time() - start
            print(end)
            if end > 0.5:
                break
