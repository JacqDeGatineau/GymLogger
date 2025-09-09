import json
import sqlite3

con = sqlite3.connect("database.db")
cursor = con.cursor()

with open("exercise.json", "r") as file:
    exercises = json.load(file)

for ex in exercises:
    cursor.execute("""
                   INSERT INTO exercises (title, user_id, link, resistance)
                   VALUES (?, ?, ?, ?)
                   """, (ex['title'], None, ex['link'], ex['resistance']))
    
    exercise_id = cursor.lastrowid

    for muscle in ex['muscle_group']:
        cursor.execute('''
            INSERT INTO exercise_muscle_groups (exercise_id, muscle_group_id) 
            VALUES (?, (SELECT id FROM muscle_groups WHERE name = ?))
        ''', (exercise_id, muscle))

con.commit()
con.close()