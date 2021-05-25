from config import CONFIG
from flask import Flask, redirect

app = Flask(__name__)

if CONFIG.printer:
    from mods.printer import printer

    app.register_blueprint(printer.bp)

if CONFIG.sky:
    from mods.sky import sky

    app.register_blueprint(sky.bp)

if CONFIG.weather:
    from mods.weather import weather

    app.register_blueprint(weather.bp)

if CONFIG.home:
    from mods.home import home

    app.register_blueprint(home.bp)

    @app.route("/")
    def index():
        return redirect("/home")


else:

    @app.route("/")
    def index():
        return "Alive but home module turned off.."


if __name__ == "__main__":
    app.run(debug=True)
