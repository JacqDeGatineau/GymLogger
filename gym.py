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

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("database.db")
        g.db.row_factory = sqlite3.Row  # This allows you to access columns by name
    return g.db