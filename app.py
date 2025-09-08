import sqlite3
from flask import Flask
from flask import redirect, render_template, request
from werkzeug.security import generate_password_hash
import db

app = Flask(__name__)

@app.route("/")
def index():
    words = ["jazzy", "sensation", "can you feel it?"]
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")
    result = db.query("SELECT COUNT(*) FROM visits")
    count = result [0][0]
    load_times = f"Page has been loaded {str(count)} times baby!"
    create_user = f"Sign in here! "
    return render_template("index.html", message=load_times, items=words)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", method=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password"]
    password2 = request.form["repeat password"]
    if password1 != password2:
        return "Quivering ectoplasm! Passwords, don't match!"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash)VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "Gibbering anthropoids! The username has been taken!" 
    
    return f"Thundering tornadoes! User {username} has been created!"

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
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

