import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import config, gym
import db

app = Flask(__name__)
#for development only! Change for production!
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

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
        return "Quivering ectoplasm! Passwords don't match!"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash)VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "Gibbering anthropoids! The username has been taken!" 
    
    return f"Thundering tornadoes! User {username} has been created!"

def require_login():
    if "username" not in session:
        abort(403)

@app.route("/session")
def select_exercises():
    require_login()
    #username = session["username"]
    exercises = gym.get_exercises()
    return render_template("session.html", exercises=exercises)

@app.route("/create-workout", methods=["POST"])
def workout():
    require_login()
    selected_exercises = request.form.getlist('exercises')
    print(selected_exercises)
    exercises = gym.get_exercises_by_ids(selected_exercises)
    print(exercises)
    return render_template("result.html", exercises=exercises)

@app.route("/result", methods=["POST"])
def result():
    require_login()
    exercise = request.form.get("exercise")
    sets = request.form["sets"]
    reps = request.form["reps"]
    weight = request.form["weight"]
    #I need to bind the user_id into the session
    session_id = gym.add_session(user_id, sets, reps, weight)
    return render_template("result.html", exercise=exercise, sets=sets, reps=reps, weight=weight)


