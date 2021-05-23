import time
import requests
import pos58
from datetime import datetime


def printer_thread(URL, PW):
    def t():
        return f"{datetime.now()}"

    def get_message():
        try:
            r = requests.get(f"{URL}/printer/get-msg?password={PW}")
            if r.status_code == 200:
                msg = r.json()
                print(f"{t()} get_message - printing: {msg['text']}")
                pos58.output(msg["text"])
                confirm_message(msg["msg_id"])
            elif r.status_code == 204:
                print(f"{t()} get_message - no new messages")
            else:
                print(
                    f"{t()} get_message - error .. status code: {r.status_code}: {r.text}"
                )
        except Exception as err:
            print(f"{t()} get_message - error .. {err}")

    def confirm_message(msg_id):
        try:
            print(f"{t()} confirm_message - confirming: {msg_id}")
            r = requests.get(f"{URL}/printer/confirm-msg?msg_id={msg_id}&password={PW}")
            if r.status_code != 200:
                print(
                    f"{t()} confirm_message - .. status code: {r.status_code}: {r.text}"
                )
        except Exception as err:
            print(f"{t()} confirm_message - error .. {err}")

    while True:
        now = datetime.now().hour
        # sleep to save on Heroku dyno hours
        if now > 7 and now < 22:
            get_message()
        time.sleep(10)
