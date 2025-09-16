import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
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
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if username and password are provided
    if not username or not password:
        return "Username and password are required!", 400

    # Query for the user based on the username
    sql = "SELECT user_id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    # Check if the user exists
    if result:
        user_id, password_hash = result[0]
        # Verify the password
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")

    return "Blabberin' blatherskite! Wrong username or password!", 401

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
    user_id = session["user_id"]

    exercise = request.form.get("exercise")
    sets = request.form["sets"]
    reps = request.form["reps"]
    weight = request.form["weight"]

    exercise_id = gym.get_exercises_by_ids(exercise)
    #I need to bind the user_id into the session
    session_id = gym.add_session(user_id, sets, reps, weight, exercise_id)
    return render_template("result.html", exercise=exercise, sets=sets, reps=reps, weight=weight)

@app.route("/end_workout", methods=["POST"])
def end_workout():
    require_login()
    
    return redirect("/")


