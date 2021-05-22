import sys
import threading
from ..mods import CONFIG
from printer import printer_thread
from satellites import satellites_thread

"""
Point this program to your server e.g. "python poller.py https://your-url.herokuapp.com password_here"
                                                         (Note: no trailing slash     ^)
I start in the background via .bashrc
"""

URL = sys.argv[1]
PW = sys.argv[2]

if CONFIG.printer:
    printer_instance = threading.Thread(target=printer_thread, args=(URL, PW,))
    printer_instance.start()
    print("printer mod started!")

if CONFIG.satellites:
    satellites_instance = threading.Thread(target=satellites_thread, args=(URL, PW,))
    satellites_instance.start()
    print("satellites mod started!")
