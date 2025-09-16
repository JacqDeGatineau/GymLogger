import db
import sqlite3
from flask import g

def get_exercises():
    sql = """SELECT t.id, t.title, t.link
             FROM exercises t
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def get_exercises_by_ids(selected_exercises):
    if not selected_exercises:
        return []

    placeholders = ', '.join(['?'] * len(selected_exercises))
    print(placeholders)
    sql = f"""SELECT t.id, t.title
               FROM exercises t
               WHERE t.id IN ({placeholders})"""
    
    return db.query(sql, selected_exercises)

def add_session(user_id, sets, reps, weight,):
    sql = "INSERT INTO session (user_id, time) VALUES (?, datetime('now'),)"
    db.execute(sql, [user_id])
    session_id = db.last_insert_id() #Add this function to db.py
    add_workout(sets, reps, weight, session_id)
    return session_id
    
def add_workout(sets, reps, weight, session_id):
    #where do we get exercise_id?
    sql = """INSERT INTO workout (sets, reps, weight, exercise_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [(sets, reps, weight, exercise_id, session_id)])
