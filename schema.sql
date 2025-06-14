CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    default_public INTEGER
);

CREATE TABLE exercises (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    exercise_type_id INTEGER REFERENCES exercise_types,
    exercise_class_id INTEGER REFERENCES classes,
    exercise_weight REAL,
    exercise_date TEXT,
    public INTEGER,
    note TEXT,
    comment_count INTEGER
);

CREATE TABLE exercise_types (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    exercise_type_name TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    label TEXT,
    sets INTEGER,
    reps  INTEGER,
    alpha REAL
);

INSERT INTO classes
VALUES
 (1, '3 series of 2 reps', 3, 2, 0.35),
 (2, '5 series of 5 reps', 5, 5, 0.20),
 (3, '3 series of 10 reps', 3, 10, 0.10);

 CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises,
    user_id INTEGER REFERENCES users,
    comment_text TEXT,
    created_date TEXT
);
