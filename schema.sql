CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE IF NOT EXISTS exercises (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE,
    user_id INTEGER REFERENCES users,
    link  TEXT,
    muscle_group TEXT CHECK (muscle_group IN ('Back', 'Arms', 'Chest', 'Shoulders', 'Core', 'Legs', 'Other')),
    resistance TEXT CHECK (resistance IN ('Barbell', 'Machine', 'Dumbbell', 'Bodyweight', 'Other'))
);

CREATE TABLE IF NOT EXISTS workout (
    id INTEGER PRIMARY KEY,
    sets INTEGER,
    reps INTEGER,
    weight REAL,
    exercise_id INTEGER REFERENCES exercises
);

CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS session_workouts (
    session_id INTEGER REFERENCES session,
    workout_id INTEGER REFERENCES workout,
    PRIMARY KEY (session_id, workout_id)
);


