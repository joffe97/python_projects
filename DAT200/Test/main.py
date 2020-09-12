from flask import Flask

app = Flask("__main__")


@app.route("/")
def home():
    return "<h2>My webpage</h2>"


@app.route("/<name>")
def user(name):
    return f"Hello {name}"


if __name__ == '__main__':
    app.run()
