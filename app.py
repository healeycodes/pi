from config import CONFIG
from flask import Flask, redirect


app = Flask(__name__)

if CONFIG.printer:
    from mods.printer import printer

    app.register_blueprint(printer.bp)
if CONFIG.satellites:
    from mods.satellites import satellites

    app.register_blueprint(satellites.bp)


@app.route("/")
def index():
    return redirect("/printer")


if __name__ == "__main__":
    app.run(debug=True)
