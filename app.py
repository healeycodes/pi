import os
from config import CONFIG
from functools import wraps
from flask import Flask, redirect, abort, request

app = Flask(__name__)


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


if CONFIG.printer:
    from mods.printer import printer

    app.register_blueprint(printer.bp)
if CONFIG.sky:
    from mods.sky import sky

    app.register_blueprint(sky.bp)


@app.route("/")
def index():
    return redirect("/printer")


if __name__ == "__main__":
    app.run(debug=True)
