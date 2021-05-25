import gps
import time
import requests
from datetime import datetime

"""
Setup GPS w/ https://gitlab.com/gpsd/gpsd
"""


def sky_thread(URL, PW):
    gpsd = None

    def t():
        return f"{datetime.now()}"

    def send_sats():
        try:
            print(f"{t()} send_sats - gpsd.data: {gpsd.data}")

            sats = set()
            if "satellites" not in gpsd.data:
                return

            for sat in gpsd.data["satellites"]:
                sats.add(sat["PRN"])

            print(f"{t()} send_sats - found: {sats}")

            # PRNs are always two digits
            sats = ",".join([str(sat).zfill(2) for sat in sats])
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

    def sync_gpsd():
        # gpsd buffer can be out of date
        while True:
            start = time.time()
            gpsd.next()
            end = time.time() - start

            # find the latest info
            # (a 'slow' update means the data is real time)
            if end > 0.25:
                # check that it has the satellite data
                # as opposed to lat/long data i.e. 'TPV'
                while True:
                    if "satellites" in gpsd.data:
                        return
                    gpsd.next()

    while True:
        now = datetime.now().hour
        # sleep to save on Heroku dyno hours
        if now > 7 and now < 22:
            if gpsd is None:
                gpsd = gps.gps(mode=gps.WATCH_ENABLE)
            sync_gpsd()
            send_sats()
        else:
            if gpsd is not None:
                # close when we rest for the night
                gpsd.close()
                gpsd = None

        time.sleep(10)
