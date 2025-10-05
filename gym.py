import db
import sqlite3
from flask import g

def get_exercises():
    sql = """SELECT t.id, t.title, t.link
             FROM exercises t
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def get_sessions():
    sql = """SELECT t.id, t.time
             FROM session t
             GROUP BY t.time
             ORDER BY t.time DESC"""
    return db.query(sql)

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
    #print(placeholders)
    sql = f"""SELECT t.id, t.title
               FROM exercises t
               WHERE t.id IN ({placeholders})"""
    
    return db.query(sql, selected_exercises)

def get_exercise_by_id(selected_exercise):
    if not selected_exercise:
        return []

    #placeholders = ', '.join(['?'] * len(selected_exercise))
    #print(placeholders)
    sql = f"""SELECT t.id, t.title
               FROM exercises t
               WHERE t.id = ?"""
    
    result = db.query(sql, [selected_exercise])  # Wrap selected_exercise in a list
    if result:  # Check if the result is not empty
        return result[0]['id']  # Return the exercise ID from the first row
    else:
        return None 

def add_session(user_id): #sets, reps, weight, exercise_id):
    sql = "INSERT INTO session (user_id, time) VALUES (?, datetime('now'))"
    db.execute(sql, [user_id])
    session_id = db.last_insert_id()
    #add_workout(sets, reps, weight, session_id, exercise_id)
    return session_id
    
def add_workout(sets, reps, weight, session_id, exercise_id):
    sql = """INSERT INTO workout (sets, reps, weight, exercise_id, session_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [sets, reps, weight, exercise_id, session_id])
