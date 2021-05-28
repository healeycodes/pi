from server.common import auth
from mods.sky.satellites import save_sats, get_sats
from flask import Blueprint, request, jsonify

bp = Blueprint(
    "sky",
    __name__,
    url_prefix="/sky",
    template_folder="templates",
    static_folder="static",
)


@bp.route("/send")
@auth
def send_satellites():
    sats = request.args.get("sats")
    save_sats(sats.split(","))
    return "", 200


@bp.route("/get")
def get_satellites():
    return jsonify(get_sats())
