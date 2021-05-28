import json
from server.config import CONFIG
from flask import Blueprint, render_template

bp = Blueprint(
    "home",
    __name__,
    url_prefix="/home",
    template_folder="templates",
    static_folder="static",
)


def class_vars(c):
    return [
        attr
        for attr in dir(c)
        if not callable(getattr(c, attr)) and not attr.startswith("__")
    ]


@bp.route("/")
def index():
    return render_template(
        "index.html", mods=class_vars(CONFIG), mods_json=json.dumps(class_vars(CONFIG))
    )
