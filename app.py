import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db

app = Flask(__name__)
#for development only! Change for production!
app.secret_key = config.secret_key

@app.route("/")
def index():
    words = ["jazzy", "sensation", "can you feel it?"]
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")
    result = db.query("SELECT COUNT(*) FROM visits")
    count = result [0][0]
    load_times = f"Page has been loaded {str(count)} times baby!"
    #create_user = f"Sign in here! {redirect("/register")}"
    return render_template("index.html", message=load_times, items=words)

@app.route("/login", methods=["POST"])
def login():
    print(request.form)
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "Blabberin' blatherskite! Wrong username or password!"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
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

