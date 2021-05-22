from config import CONFIG
from flask import Flask, redirect


app = Flask(__name__)

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
