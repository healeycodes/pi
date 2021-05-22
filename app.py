from flask import Flask, redirect

from mods.printer import printer
from mods.satellites import satellites

app = Flask(__name__)
app.register_blueprint(printer.bp)
app.register_blueprint(satellites.bp)


@app.route("/")
def index():
    return redirect("/printer")


if __name__ == "__main__":
    app.run(debug=True)
