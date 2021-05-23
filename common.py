import os
from functools import wraps
from flask import abort, request


def auth(view):
    @wraps(view)
    def check_pw(*args, **kwargs):
        # TODO: this is vulnerable to a timing attack
        password = request.args.get("password")
        PW = os.environ["PRINTER_PW"] if "PRINTER_PW" in os.environ else None
        if password != PW:
            abort(401)
        else:
            return view(*args, **kwargs)

    return check_pw
