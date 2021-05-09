from flask import Flask

from printer import printer

app = Flask(__name__)
app.register_blueprint(printer.bp)


if __name__ == "__main__":
    app.run()
