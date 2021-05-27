from common import auth
from mods.weather.data import save_weather, get_weather
from flask import Blueprint, request, jsonify

bp = Blueprint(
    "weather",
    __name__,
    url_prefix="/weather",
    template_folder="templates",
    static_folder="static",
)


@bp.route("/send")
@auth
def send_weather():
    humidity = request.args.get("humidity")
    temperature = request.args.get("temperature")
    if not humidity:
        return 'Missing query parameter of "humidity" :(', 400
    if not temperature:
        return 'Missing query parameter of "temperature" :(', 400
    save_weather(temperature, humidity)
    return "", 200


@bp.route("/get")
def get_current():
    return jsonify(get_weather())
