"""
Point this program to your server e.g. "python poller.py https://your-url.herokuapp.com password_here"
                                                         (Note: no trailing slash     ^)
I start in the background via .bashrc
"""
import sys
import time
import pos58
import requests
from datetime import datetime

URL = sys.argv[1]
PW = sys.argv[2]

while True:
    now = datetime.now().hour

    # we need to sleep to save on Heroku dyno hours
    if now > 8 and now < 23:
        try:
            r = requests.get(f"{URL}/printer/get-msg?password={PW}")
            if r.status_code == 200:
                print(f"Printing: {r.text}")
                pos58.output(r.text)
            elif r.status_code == 204:
                print("No new messages")
            else:
                print(f"Error .. status code: {r.status_code} – {r.text}")
        except Exception as err:
            print(f"Error .. {err}")
    time.sleep(30)
