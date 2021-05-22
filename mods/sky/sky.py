import os
from functools import wraps
from mods.sky.satellites import save_sats, get_sats
from flask import Blueprint, request, jsonify, abort

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
def send_satellites():
    sats = request.args.get("sats")
    save_sats(sats.split(","))
    return "", 200


@bp.route("/get")
def get_satellites():
    return jsonify(get_sats())
