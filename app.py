import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort, flash, url_for
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
        username = request.form.get("username", "").strip()
        if not username or len(username) > 16:
            flash("Billions of bilious blue blistering barnacles! Username is too long!")
            return redirect("/create")
        password1 = request.form.get("password", "")
        password2 = request.form.get("repeat password", "")

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
    csrf_token = request.form.get("csrf_token")
    #if request.form["csrf_token"] != session["csrf_token"]:
    if not csrf_token or csrf_token != session.get("csrf_token"):
        abort(403)

@app.route("/history", methods=["GET", "POST"])
def show_history():
    require_login()
    
    sessions = gym.get_sessions()

    sessions_with_workouts = []
    for session in sessions:
        session_dict = dict(session)
        session_id = session['id']
        session_dict['workouts'] = gym.get_workouts_by_session(session_id)
        sessions_with_workouts.append(session_dict)

    return render_template("history.html", sessions=sessions_with_workouts)

@app.route("/session")
def select_exercises():
    require_login()
    #username = session["username"]
    exercises = gym.get_exercises()
    return render_template("session.html", exercises=exercises)

def filter_exercises(query: str):
    exercises = gym.get_exercises()
    q = (query or "").strip().lower()
    if not q:
        return exercises
    return [e for e in exercises if q in e["title"].lower()]

@app.get("/search")
def search():
    query = request.args.get("query", "")
    # Selected IDs are propagated via GET so we can preserve them between searches
    selected_ids = set(request.args.getlist("selected"))
    exercises = filter_exercises(query)
    return render_template(
        "session.html",
        query=query,
        exercises=exercises,
        selected_ids=selected_ids
    )

"""@app.route("/search")
def search():
    query = request.args.get("query")
    results = gym.search(query) if query else []
    return render_template("session.html", query=query, results=results)"""

@app.route("/create-workout", methods=["POST"])
def create_workout():
    require_login()
    user_id = session["user_id"]
    selected_exercises = request.form.getlist('exercises')
    #print(selected_exercises)
    exercises = gym.get_exercises_by_ids(selected_exercises)
    #print(exercises)
    return render_template("workout.html", exercises=exercises,  set_count=1)

@app.route("/workout", methods=["POST"])
def result():
    require_login()
    set_count = 1

    if 'add_set' in request.form:
        set_count = int(request.form.get('set_count',1)) + 1
        # Get the exercises from the form to preserve them
        selected_exercises = request.form.getlist('exercise_ids[]')
        exercises = gym.get_exercises_by_ids(selected_exercises)
        print(exercises)
        return render_template("workout.html", exercises=exercises, set_count=set_count)
    
    check_csrf()
    user_id = session["user_id"]

    exercises_data = request.form.getlist("exercise_ids[]")
    try:
        session_id = gym.add_session(user_id)

        for exercise in exercises_data:
            reps = request.form.getlist("reps[{}][]".format(exercise))
            weight = request.form.getlist("weight[{}][]".format(exercise))

            exercise_id = gym.get_exercise_by_id(exercise)
            print(exercise_id)
            if exercise_id is None:
                return "Exercise not found", 404
            
            # Process each set for this exercise
            for i in range(len(reps)):
                gym.add_workout((i+1), reps[i], weight[i], session_id, exercise_id)

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


