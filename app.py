from flask import Flask

from printer import app

app = Flask(__name__)
app.register_blueprint(app.bp)


if __name__ == "__main__":
    app.run()
