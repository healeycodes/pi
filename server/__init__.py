from server.config import CONFIG
from flask import Flask, redirect


def create_app():
    app = Flask(__name__)

    if CONFIG.printer:
        from mods.printer import printermod

        app.register_blueprint(printermod.bp)

    if CONFIG.sky:
        from mods.sky import skymod

        app.register_blueprint(skymod.bp)

    if CONFIG.weather:
        from mods.weather import weathermod

        app.register_blueprint(weathermod.bp)

    if CONFIG.home:
        from mods.home import homemod

        app.register_blueprint(homemod.bp)

        @app.route("/")
        def index():
            return redirect("/home")

    else:

        @app.route("/")
        def index():
            return "Alive but home module turned off.."

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
