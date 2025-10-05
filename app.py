import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
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
    #print(request.form)
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if username and password are provided
    if not username or not password:
        return "Username and password are required!", 400

    # Query for the user based on the username
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    # Check if the user exists
    if result:
        user_id, password_hash = result[0]
        # Verify the password
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
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

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        username = request.form["username"]
        if not username or len(username) > 16:
            flash("Billions of bilious blue blistering barnacles! Username is too long!")
            return redirect("/create")
        password1 = request.form["password"]
        password2 = request.form["repeat password"]

        if password1 != password2:
            flash("Quivering ectoplasm! Passwords don't match!")
            return redirect("/create")
        
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash)VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
            flash(f"Thundering tornadoes! User {username} has been created!")
            return redirect("/")
        except sqlite3.IntegrityError:
            flash("Gibbering anthropoids! The username has been taken!")
            return redirect("/create")
    
    return render_template("register.html")

def require_login():
    if "username" not in session:
        abort(403)
    
def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/history", methods=["GET", "POST"])
def show_history():
    require_login()

    sessions = gym.get_sessions()
    return render_template("history.html", sessions=sessions)

@app.route("/session")
def select_exercises():
    require_login()
    #username = session["username"]
    exercises = gym.get_exercises()
    return render_template("session.html", exercises=exercises)

@app.route("/create-workout", methods=["POST"])
def workout():
    require_login()
    user_id = session["user_id"]
    selected_exercises = request.form.getlist('exercises')
    #print(selected_exercises)
    exercises = gym.get_exercises_by_ids(selected_exercises)
    #print(exercises)
    return render_template("result.html", exercises=exercises)

@app.route("/result", methods=["POST"])
def result():
    require_login()
    check_csrf()
    user_id = session["user_id"]

    exercises_data = request.form.getlist("exercise")

    try:
        session_id = gym.add_session(user_id)

        for exercise in exercises_data:
            sets = request.form.get("sets[{}]".format(exercise))
            reps = request.form.get("reps[{}]".format(exercise))
            weight = request.form.get("weight[{}]".format(exercise))

            exercise_id = gym.get_exercise_by_id(exercise)
            print(exercise_id)
            if exercise_id is None:
                return "Exercise not found", 404
            
            gym.add_workout(sets, reps, weight, session_id, exercise_id)
        print("Session id", session_id)
    except Exception as e:
        print("Error adding session or workouts:", e)
        return "An error occurred", 500

    return redirect("/")

@app.route("/end_workout", methods=["POST"])
def end_workout():
    require_login()
    user_id = session["user_id"]
    return redirect("/")


