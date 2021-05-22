import os
import dataclasses
from functools import wraps
from datetime import datetime
from mods.printer import messages
from flask import Blueprint, request, jsonify, abort, render_template

PW = os.environ["PRINTER_PW"] if "PRINTER_PW" in os.environ else None
bp = Blueprint(
    "printer",
    __name__,
    url_prefix="/printer",
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


@bp.route("/")
def index():
    return render_template("send_message.html")


@bp.route("/put-msg")
def put_msg():
    text = request.args.get("text")
    if "X-Forwarded-For" in request.headers:
        name = request.headers.getlist("X-Forwarded-For")[0].rpartition(" ")[-1]
    else:
        name = request.remote_addr or "untrackable"
    if text:
        return render_template(
            "thank_you.html", msg_id=messages.put_msg(text, name)
        )
    else:
        return 'Missing query parameter of "text" :(', 400


@bp.route("/check-msg")
def check_msg():
    msg_id = request.args.get("msg_id")

    status = messages.check_msg(msg_id).status
    if status:
        return jsonify({"status": status})
    return "No message by that msg_id :(", 404


@bp.route("/confirm-msg")
@auth
def confirm_msg():
    msg_id = request.args.get("msg_id")
    messages.update_msg_status(msg_id, f"printed at {datetime.now()}")
    return "", 200


@bp.route("/get-msg")
@auth
def get_msg():
    msg = messages.get_msgs()
    if msg:
        return jsonify({"msg_id": msg.msg_id, "text": msg.text, "name": msg.name})
    return "", 204


@bp.route("/count-msgs")
def count_msgs():
    return jsonify({"msg_count": len(messages.list_msgs())})


@bp.route("/list-msgs")
@auth
def list_msgs():
    return jsonify({"msgs": [dataclasses.asdict(msg) for msg in messages.get_msgs()]})
