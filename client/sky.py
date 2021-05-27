import gps
import time
import requests
from datetime import datetime

"""
Setup GPS via https://gitlab.com/gpsd/gpsd
"""


def sky_thread(URL, PW, SLEEP_AT_NIGHT):
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
        if SLEEP_AT_NIGHT:
            if now > 7 and now < 22:
                if gpsd is None:
                    gpsd = gps.gps(mode=gps.WATCH_ENABLE)
                sync_gpsd()
                send_sats()
            else:
                # if we're not reading from the buffer frequently
                # it can cause problems, so close when we're sleeping
                if gpsd is not None:
                    gpsd.close()
                    gpsd = None
        else:
            # TODO: refactor this duplicated block
            if gpsd is None:
                gpsd = gps.gps(mode=gps.WATCH_ENABLE)
            sync_gpsd()
            send_sats()

        time.sleep(10)
