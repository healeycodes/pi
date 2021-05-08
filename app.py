import os
from queue import HerokuRedisQueue
from flask import Flask, request

PW = os.environ["PRINTER_PW"]
app = Flask(__name__)
q = HerokuRedisQueue("messages")


@app.route("/")
def index():
    return (
        "Use <code>/put-msg?msg=Hello</code> to send a message to my receipt printer!",
        200,
        {"Content-Type": "text/html; charset=utf-8"},
    )


@app.route("/put-msg")
def put_msg():
    msg = request.args.get("msg")
    user = request.remote_addr
    if msg:
        q.put(f"msg – {user}")
    return f"thanks {user} :)"


@app.route("/get-msg")
def get_msg():
    password = request.args.get("password")
    
    # please don't timing attack me..
    if not password or password != PW:
        return "", 400

    msg = q.get()
    if msg:
        return msg
    return "", 204


if __name__ == "__main__":
    app.run()
