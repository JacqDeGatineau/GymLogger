from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "hei maailma"

@app.route("/page1")
def page1():
    return