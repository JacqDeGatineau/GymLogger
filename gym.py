import db
import sqlite3
from flask import g

def get_exercises():
    sql = """SELECT t.id, t.title, t.link
             FROM exercises t
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def get_sessions(user_id):
    sql = """SELECT t.id, t.time
             FROM session t
             WHERE t.user_id = ?
             GROUP BY t.time
             ORDER BY t.time DESC"""
    return db.query(sql, [user_id])

def get_workouts_by_session(session_id):
    sql = """SELECT w.sets, MAX(w.reps) AS reps, MAX(w.weight) AS weight, e.title
             FROM workout w
             JOIN exercises e ON w.exercise_id = e.id
             WHERE w.session_id = ?
             GROUP BY e.title
             ORDER BY w.weight DESC"""
    return db.query(sql, [session_id])

def search(query):
    sql = """SELECT e.title,
                    u.username
             FROM exercises e, users u
             WHERE u.id = e.user_id AND
                   e.title LIKE ?
             ORDER BY e.title DESC"""
    return db.query(sql, ["%" + query + "%"])

def get_exercises_by_ids(selected_exercises):
    if not selected_exercises:
        return []

    placeholders = ', '.join(['?'] * len(selected_exercises))
    sql = f"""SELECT t.id, t.title
               FROM exercises t
               WHERE t.id IN ({placeholders})"""
    
    return db.query(sql, selected_exercises)

def get_exercise_by_id(selected_exercise):
    if not selected_exercise:
        return []

    sql = f"""SELECT t.id, t.title
               FROM exercises t
               WHERE t.id = ?"""
    
    result = db.query(sql, [selected_exercise])  # Wrap selected_exercise in a list
    if result:  
        return result[0]['id']  # Return the exercise ID from the first row
    else:
        return None 

def add_session(user_id):
    sql = "INSERT INTO session (user_id, time) VALUES (?, datetime('now'))"
    db.execute(sql, [user_id])
    session_id = db.last_insert_id()
    return session_id

def delete_session(session_id):
    delete_workouts(session_id)
    sql = "DELETE FROM session WHERE id = ?"
    db.execute(sql, [session_id])

def delete_workouts(session_id):
    sql = "DELETE FROM workout WHERE session_id = ?"
    db.execute(sql, [session_id])
    
def add_workout(sets, reps, weight, session_id, exercise_id):
    sql = """INSERT INTO workout (sets, reps, weight, exercise_id, session_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [sets, reps, weight, exercise_id, session_id])

def get_feed():
    sql = """SELECT f.id, f.image, f.caption, f.time, u.username
             FROM feed f
             JOIN users u ON f.user_id = u.id
             ORDER BY f.time DESC"""
    return db.query(sql)

def add_feed(user_id, image, caption):
    sql = """INSERT INTO feed (user_id, image, caption, time) 
             VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [user_id, image, caption])
    feed_id = db.last_insert_id()
    return feed_id

def get_feed_image(feed_id):
    sql = """SELECT image FROM feed WHERE id = ?"""
    result = db.query(sql, [feed_id])
    if result:
        return result[0]['image']
    return None

def add_comment(user_id, feed_id, comment):
    sql = """INSERT INTO comments (user_id, feed_id, comment, time) 
             VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, [user_id, feed_id, comment])

def get_comments(feed_id):
    sql = """SELECT c.comment, c.time, u.username
             FROM comments c
             JOIN users u ON c.user_id = u.id
             WHERE c.feed_id = ?
             ORDER BY c.time DESC"""
    return db.query(sql, [feed_id])
