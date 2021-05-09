
import os
from printer import messages
from datetime import datetime
from flask import Blueprint, request

PW = os.environ["PRINTER_PW"]
bp = Blueprint('printer', __name__, url_prefix='printer')


@bp.route("/")
def index():
    return (
        """
        <p>Use <code>/put-msg?text=Hello</code> to send a message to my receipt printer!<p>
        <p>Or try this handy form I whipped up for ya.</p>
        <form action="/put-msg" method="get">
        <label for="text">Message:</label>
            <input type="text" id="text" name="text">
            <input type="submit" value="Send!">
        </form>
        """,
        200,
        {"Content-Type": "text/html; charset=utf-8"},
    )


@bp.route("/put-msg")
def put_msg():
    text = request.args.get("text")
    name = request.remote_addr
    if text:
        msg_id = messages.put_msg(text, name)
        return f"{msg_id}"
    else:
        return 'Missing query parameter of "text" :(', 400

@bp.route("/check-msg")
def check_msg():
    msg_id = request.args.get("id")

    status = messages.check_msg(msg_id)
    if status:
        return status
    return "No message by that id :(", 404

@bp.route("/get-msg")
def get_msg():
    password = request.args.get("password")

    # please don't timing attack me..
    if not password or password != PW:
        return "Bad password :(", 400

    msg = messages.get_msg()
    if msg:
        # TODO: only update after printer confirms it's printed
        messages.update_msg_status(msg.msg_id, f"printed at {datetime.now()}")
        return f"{msg.text} – {msg.name}"
    return "", 204


@bp.route("/list-msgs")
def check_msg():
    password = request.args.get("password")
    msg_id = request.args.get("id")

    # please don't timing attack me..
    if not password or password != PW:
        return "Bad password :(", 400

    msgs = messages.list_msgs()
    if msgs:
        return '\n'.join([msg.debug() for msg in msgs])

    return '', 404
