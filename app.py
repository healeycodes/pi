import os
import messages
from datetime import datetime
from flask import Flask, request

PW = os.environ["PRINTER_PW"]
app = Flask(__name__)


@app.route("/")
def index():
    return (
        "Use <code>/put-msg?text=Hello</code> to send a message to my receipt printer!",
        200,
        {"Content-Type": "text/html; charset=utf-8"},
    )


@app.route("/put-msg")
def put_msg():
    text = request.args.get("text")
    name = request.remote_addr
    if text:
        msg_id = messages.put_msg(text, name)
        return f"{msg_id}"
    else:
        return 'Missing query parameter of "text" :(', 400


@app.route("/get-msg")
def get_msg():
    password = request.args.get("password")

    # please don't timing attack me..
    if not password or password != PW:
        return "Bad password :(", 400

    msg = messages.get_msg()
    if msg:
        # TODO: only update after print actually prints it
        messages.update_msg_status(msg.msg_id, f"printed at {datetime.now()}")
        return f"{msg.text} – {msg.name}"
    return "No new messages :|", 204


@app.route("/check-msg")
def check_msg():
    msg_id = request.args.get("id")

    status = messages.check_msg(msg_id)
    if status:
        return status
    return "No message by that id :(", 404


if __name__ == "__main__":
    app.run()
