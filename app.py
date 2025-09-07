from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    words = ["jazzy", "sensation", "can you feel it?"]
    return render_template("index.html", message="Hoywd!", items=words)

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def reult():
    exercise = request.form.get("exercise")
    sets = request.form["sets"]
    reps = request.form["reps"]
    return render_template("result.html", exercise=exercise, sets=sets, reps=reps)

@app.route("/page1")
def page1():
    content = ""
    for i in range(1, 100):
        content += str(i) + " "
    return content

@app.route("/page/<int:page_id>")
def page2(page_id):
    return "Tämä on sivu " + str(page_id)

