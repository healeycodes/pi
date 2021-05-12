from flask import Flask, redirect

from printer import printer

app = Flask(__name__)
app.register_blueprint(printer.bp)


@app.route("/")
def index():
    return redirect("/printer")


if __name__ == "__main__":
    app.run(debug=True)
