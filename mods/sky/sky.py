import os
import dataclasses
from functools import wraps
from datetime import datetime
from flask import Blueprint, request, jsonify, abort, render_template

PW = os.environ["PRINTER_PW"] if "PRINTER_PW" in os.environ else None
bp = Blueprint(
    "sky",
    __name__,
    url_prefix="/sky",
    template_folder="templates",
    static_folder="static",
)


def auth(view):
    @wraps(view)
    def check_pw(*args, **kwargs):
        # TODO: this is vulnerable to a timing attack
        password = request.args.get("password")
        if password != PW:
            abort(401)
        else:
            return view(*args, **kwargs)

    return check_pw


@bp.route("/send")
@auth
def confirm_msg():
    sats = request.args.get("sats")
    print(sats)
    return "", 200
