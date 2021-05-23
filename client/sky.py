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
        try:
            print(f"{t()} send_sats - gpsd.data: {gpsd.data}")
            sats = set()
            if "satellites" in gpsd.data:
                for sat in gpsd.data["satellites"]:
                    sats.add(sat["PRN"])

            print(f"{t()} send_sats - found: {sats}")
            sats = ",".join([str(sat) for sat in sats])
        except Exception as err:
            print(f"{t()} send_sats - looking error .. {err}")
            return

        try:
            print(f"{t()} send_sats - sending: {sats}")
            r = requests.get(f"{URL}/sky/send?sats={sats}&password={PW}")
            if r.status_code != 200:
                print(f"{t()} send_sats - .. status code: {r.status_code}: {r.text}")
        except Exception as err:
            print(f"{t()} send_sats - sending error .. {err}")

    while True:
        # the gpsd can be out of date
        while True:
            start = time.time()
            gpsd.next()
            end = time.time() - start

            # wait until we reach the latest info
            if end > 0.1:
                # check that it has the satellite data
                # as opposed to lat/long data i.e. 'TPV'
                if "SKY" in gpsd.data:
                    print(gpsd.data)
                    break

        now = datetime.now().hour
        # sleep to save on Heroku dyno hours
        if now > 7 and now < 22:
            send_sats()

        time.sleep(10)
