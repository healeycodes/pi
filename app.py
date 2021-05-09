from flask import Flask

from printer import printer

app = Flask(__name__)
app.register_blueprint(printer.bp)


@app.route("/")
def index():
    return (
        """
        <p>Use <code>/printer/put-msg?text=Hello</code> to send a message to the receipt printer in my living room!<p>
        <p>Or try this handy form I whipped up for ya.</p>
        <form action="/printer/put-msg" method="get">
        <label for="text">Message:</label>
            <input type="text" id="text" name="text">
            <input type="submit" value="Send!">
        </form>
        """,
        200,
        {"Content-Type": "text/html; charset=utf-8"},
    )


if __name__ == "__main__":
    app.run()
