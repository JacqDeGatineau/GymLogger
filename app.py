from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "hei maailma"

@app.route("/page1")
def page1():
    content = ""
    for i in range(1, 100):
        content += str(i) + " "
    return content

@app.route("/page/<int:page_id>")
def page2(page_id):
    return "Tämä on sivu " + str(page_id)

