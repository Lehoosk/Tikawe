import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

#These functions are used to query or insert exercises or exercise types or other such stuff
def get_exercise(id):
    sql = "SELECT id, exercise_type_id, exercise_weight, exercise_date, note, comment_count FROM exercises WHERE id = ?"
    return db.query(sql, [id])[0]

#updating exercise class still not done...
def update_exercise(ex_id, type_id, weight, date, note):
    sql = """
        UPDATE exercises
        SET exercise_type_id = ?, exercise_weight = ?,
            exercise_date = ?, note = ?
        WHERE id = ?
    """
    db.execute(sql, [type_id, weight, date, note, ex_id])
    
def remove_exercise(item_id):
    sql = "DELETE FROM exercises WHERE id = ?"
    db.execute(sql, [item_id])

def create_user(username, password, default_public):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash, default_public) VALUES (?, ?, ?)"
    db.execute(sql, [username, password_hash, default_public])

    user_id = db.last_insert_id()
    #Create three default exercise types to all users.
    default_types = ["Bench press", "Deadlift", "Back squat"]
    for i in default_types:
        add_exercise_type(user_id, i)

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id

    return None

def get_exercise_types(user_id):
    sql = "SELECT id, exercise_type_name FROM exercise_types WHERE user_id = ?"
    return db.query(sql, [user_id])

def get_classes():
    sql = "SELECT id, label, sets, reps, alpha FROM classes"
    return db.query(sql, [])

#this is used to get default public setting from user. This is not row, but one value, thus we need to use prompt to get the first value from the list: [0]["default_public"] .
def get_user_default(user_id):
    sql = "SELECT default_public FROM users WHERE id = ?"
    return db.query(sql, [user_id])[0]["default_public"] 

def get_user_exercises(user_id, type_id=None):

    if type_id:
        #this is used if searching with selected type_id. This is used by search-function.
        sql = """
        SELECT exercises.user_id, exercises.id, username, exercise_type_name, label, exercise_weight, exercise_date, note, comment_count FROM users, exercises, exercise_types, classes 
        WHERE exercises.user_id = users.id AND exercise_types.id = exercises.exercise_type_id AND classes.id = exercises.exercise_class_id AND exercises.user_id = ? AND exercises.exercise_type_id = ? ORDER BY exercise_date DESC
        """
        params = [user_id, type_id]
    else:
        #this is the default, it returns all execises done by the user
        sql = """
        SELECT exercises.user_id, exercises.id, username, exercise_type_name, label, exercise_weight, exercise_date, note, comment_count FROM users, exercises, exercise_types, classes 
        WHERE exercises.user_id = users.id AND exercise_types.id = exercises.exercise_type_id AND classes.id = exercises.exercise_class_id AND exercises.user_id = ? ORDER BY exercise_date DESC
        """
        params = [user_id]
    return db.query(sql, params)

def get_public_exercises():

    sql = """
    SELECT exercises.id, username, exercise_type_name, label, exercise_weight, exercise_date, note, comment_count FROM users, exercises, exercise_types, classes 
    WHERE exercises.user_id = users.id AND exercise_types.id = exercises.exercise_type_id AND classes.id = exercises.exercise_class_id AND exercises.public = 1 ORDER BY exercise_date DESC
    """

    return db.query(sql)

def add_exercise_type(user_id, name):
    sql = "INSERT INTO exercise_types (user_id, exercise_type_name) VALUES (?, ?)"
    db.execute(sql, [user_id, name.strip()])

def post_comment(exercise_id, user_id, text, new_count):
    sql = "INSERT INTO comments (exercise_id, user_id, comment_text, created_date) VALUES (?, ?, ?, datetime('now', 'localtime'))"
    db.execute(sql, [exercise_id, user_id, text])

    sql = """
        UPDATE exercises
        SET comment_count = ?
        WHERE id = ?
    """
    db.execute(sql, [new_count, exercise_id])


def get_comments(exercise_id):

    sql = """
    SELECT username, comment_text, created_date FROM users, comments 
    WHERE comments.user_id = users.id AND comments.exercise_id =? ORDER BY created_date DESC
    """
    params = [exercise_id]
    return db.query(sql, params)

def get_statistics(user_id):

    sql = """
    SELECT exercise_type_name, label AS class_label, MAX(exercise_weight) AS max_weight, COUNT(*) AS lift_count, MAX(exercise_date) AS last_date
    FROM   exercises, exercise_types, classes
    WHERE  exercises.user_id = ? AND exercise_types.id = exercise_type_id AND classes.id = exercise_class_id
    GROUP BY  exercise_type_id, exercise_class_id
    """
    return db.query(sql, [user_id])
