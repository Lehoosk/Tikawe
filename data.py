import db
from werkzeug.security import check_password_hash, generate_password_hash

#These functions are used to query or insert exercises or exercise types or other such stuff
def get_exercise(id):
    sql = "SELECT id, exercise_type_id, exercise_weight, exercise_date, comment FROM exercises WHERE id = ?"
    return db.query(sql, [id])[0]

#updating exercise class still not done...
def update_exercise(ex_id, type_id, weight, date, comment):
    sql = """
        UPDATE exercises
        SET exercise_type_id = ?, exercise_weight = ?,
            exercise_date = ?, comment = ?
        WHERE id = ?
    """
    db.execute(sql, [type_id, weight, date, comment, ex_id])
    
def remove_exercise(item_id):
    sql = "DELETE FROM exercises WHERE id = ?"
    db.execute(sql, [item_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

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

def get_exercises(user_id, type_id=None):

    if type_id:
        #this is used if searching with selected type_id. This is used by search-function.
        sql = """
        SELECT exercises.id, exercises.user_id, exercises.exercise_type_id, exercise_types.exercise_type_name, exercises.exercise_class_id, classes.label, 
        exercises.exercise_weight, exercises.exercise_date, comment FROM exercises, exercise_types, classes 
        WHERE exercise_types.id = exercises.exercise_type_id AND classes.id = exercises.exercise_class_id AND exercises.user_id = ? AND exercises.exercise_type_id = ? ORDER BY exercise_date DESC
        """
        params = [user_id, type_id]
    else:
        #this is the default, it returns all execises done by the user
        sql = """
        SELECT exercises.id, exercises.user_id, exercises.exercise_type_id, exercise_types.exercise_type_name, exercises.exercise_class_id, classes.label, 
        exercises.exercise_weight, exercises.exercise_date, comment FROM exercises, exercise_types, classes 
        WHERE exercise_types.id = exercises.exercise_type_id AND classes.id = exercises.exercise_class_id AND exercises.user_id = ? ORDER BY exercise_date DESC
        """
        params = [user_id]
    return db.query(sql, params)

def add_exercise_type(user_id, name):
    sql = "INSERT INTO exercise_types (user_id, exercise_type_name) VALUES (?, ?)"
    db.execute(sql, [user_id, name.strip()])
