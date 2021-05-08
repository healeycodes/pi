import os
import messages
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
        return msg_id
    else:
        return 'missing query parameter of "text" :(', 400


@app.route("/get-msg")
def get_msg():
    password = request.args.get("password")

    # please don't timing attack me..
    if not password or password != PW:
        return "", 400

    msg = messages.get_msg()
    if msg:
        # TODO: only update after print actually prints it
        messages.update_msg_status(msg.msg_id, 'printed')
        return msg
    return "", 204


if __name__ == "__main__":
    app.run()
