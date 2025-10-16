import sqlite3
from flask import Flask, url_for
from flask import redirect, render_template, request, session, abort, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import config, gym
import db
import markupsafe

app = Flask(__name__)
#for development only! Change for production!
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
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
    #Function to log out the user
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    return render_template("register.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username or len(username) < 5 or len(username) > 16:
            if len(username) > 16:
                flash("Zounds! Username is too long!")
            elif len(username) < 5:
                flash("Billions of bilious blue blistering barnacles! Username is too short!")
            elif not username:
                flash("Gadzooks! Username is required!")
            return redirect("/create")
        password1 = request.form.get("password", "")
        password2 = request.form.get("repeat password", "")

        if password1 != password2 or len(password1) < 8:
            if password1 != password2:
                flash("Quivering ectoplasm! Passwords don't match!")
            elif len(password1) < 8:
                flash("Blistering barnacles! Password must be at least 8 characters long!")
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
    if not csrf_token or csrf_token != session.get("csrf_token"):
        abort(403)

@app.route("/history", methods=["GET", "POST"])
def show_history():
    require_login()
    user_id = session["user_id"]
    sessions = gym.get_sessions(user_id)

    sessions_with_workouts = []
    for s in sessions:
        s_dict = dict(s)
        s_id = s['id']
        s_dict['workouts'] = gym.get_workouts_by_session(s_id)
        sessions_with_workouts.append(s_dict)

    return render_template("history.html", sessions=sessions_with_workouts)

@app.route("/delete_session", methods=["POST"])
def delete_session():
    require_login()
    session_id = request.form.get("session_id")
    gym.delete_session(session_id)
    return redirect("/history")

@app.route("/session")
def select_exercises():
    require_login()
    exercises = gym.get_exercises()
    return render_template("session.html", exercises=exercises, selected_ids=[])

def filter_exercises(query: str):
    exercises = gym.get_exercises()
    q = (query or "").strip().lower()
    if not q:
        return exercises
    return [e for e in exercises if q in e["title"].lower()]

@app.get("/search")
def search():
    query = request.args.get("query", "")

    all_selected = []
    currently_selected_ids = request.args.getlist("selected")
    currently_selected_ids = [int(sid) for sid in currently_selected_ids]

    if currently_selected_ids:
        for sid in currently_selected_ids:
            all_selected.append(sid)

    exercises = filter_exercises(query)
    return render_template(
        "session.html",
        query=query,
        exercises=exercises,
        selected_ids=all_selected
    )

@app.route("/create-workout", methods=["POST"])
def create_workout():
    require_login()
    check_csrf()

    selected_exercises = request.form.getlist('selected')
    exercises = gym.get_exercises_by_ids(selected_exercises)

    return render_template("workout.html", exercises=exercises, set_count=3)

@app.route("/workout", methods=["POST", "GET"])
def result():
    require_login()
    user_id = session["user_id"]
    check_csrf()

    exercises_data = request.form.getlist("exercise_ids[]")
    session_id = gym.add_session(user_id)

    for exercise in exercises_data:
        reps = request.form.getlist("reps[{}][]".format(exercise))
        weight = request.form.getlist("weight[{}][]".format(exercise))
        exercise_id = gym.get_exercise_by_id(exercise)

        if exercise_id is None:
            return "Exercise not found", 404
        
        # Process each set for this exercise
        for i in range(len(reps)):
            gym.add_workout((i+1), reps[i], weight[i], session_id, exercise_id)
    return redirect("/end_workout")


@app.route("/end_workout", methods=["POST", "GET"])
def end_workout():
    require_login()
    return render_template("workout_saved.html")

@app.route("/feed", methods=["POST", "GET"])
def feed():
    require_login()

    feed = gym.get_feed()
    feed_with_comments = []

    for post in feed:
        post_dict = dict(post)  # Convert sqlite3.Row to dict
        post_dict['comments'] = gym.get_comments(post['id'])
        feed_with_comments.append(post_dict)
    
    return render_template("feed.html", feed=feed_with_comments)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    user_id = session["user_id"]

    file = request.files.get("image")
    caption = request.form.get("caption")

    if file:
        image = file.read()
        gym.add_feed(user_id, image, caption)
    else:
        gym.add_feed(user_id, None, caption)
    return redirect("/feed")

@app.route("/image/<int:feed_id>")
def show_image(feed_id):
    image = gym.get_feed_image(feed_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/add_comment", methods=["POST"])
def comment():
    require_login()
    user_id = session["user_id"]
    feed_id = request.form.get("feed_id")

    comment = request.form.get("comment")
    if comment:
        gym.add_comment(user_id, feed_id, comment)
    return redirect("/feed")

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)