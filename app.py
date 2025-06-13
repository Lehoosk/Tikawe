import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, g, flash
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "varmasalasana"

#Page-rendering functions start here:
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "Error: wrong username or password"

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")
    
@app.route("/register", methods=["GET", "POST"])
def register():


    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
    # Validate username and password and match passwords

        if (len(username) < 4 or len(password1) < 8 or len(password2) < 8):
            flash("Erroe: too short username or password")
            return redirect("/register")

        if password1 != password2:
            flash("Error: passwords don't match")
            return redirect("/register")
        
        try:
            create_user(username, password1)
            return render_template("register_success.html")
        except sqlite3.IntegrityError:
            flash("Error: username exists")
            return redirect("/register")
        
@app.route("/new_exercise", methods=["GET", "POST"])
def new_exercise():

    user_id = session["user_id"]

    if request.method == "GET":
        types = get_exercise_types(user_id)
        classes = get_classes()
        return render_template("new_exercise.html", types=types, classes=classes)
    
    if request.method == "POST":
        type_id = int(request.form["type_id"])
        weight  = float(request.form["weight"])
        ex_date = request.form["date"]
        class_id = int(request.form["class_id"])
        comment = request.form["comment"]

        sql = """
            INSERT INTO exercises
                  (user_id, exercise_type_id, exercise_class_id, exercise_weight, exercise_date, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        execute(sql, [user_id, type_id, class_id, weight, ex_date, comment])
        return redirect("/")

    return render_template("new_exercise.html")

@app.route("/exercises")
def exercises():
    user_id = session["user_id"]
    exercises = get_exercises(user_id)
    types = get_exercise_types(user_id)
    return render_template("exercises.html", exercises=exercises, types=types)


@app.route("/edit/<int:exercise_id>", methods=["GET", "POST"])
def edit_exercise(exercise_id):
    exercise = get_exercise(exercise_id)
    user_id = session["user_id"]

    if request.method == "GET":
        types = get_exercise_types(user_id)
        return render_template("edit.html", exercise=exercise, types=types)

    if request.method == "POST":
        type_id = int(request.form["type_id"])
        weight  = float(request.form["weight"])
        ex_date = request.form["date"]
        comment  = request.form["comment"]
        update_exercise(exercise_id, type_id, weight, ex_date, comment)
        return redirect("/")

@app.route("/remove/<int:exercise_id>", methods=["GET", "POST"])
def remove(exercise_id):

    exercise = get_exercise(exercise_id)

    if request.method == "GET":
        return render_template("remove.html", exercise=exercise)

    if request.method == "POST":
        if "remove" in request.form:
            remove_exercise(exercise_id)
            return redirect("/exercises")
        else:
            return redirect("/")


@app.route("/edit_exercise_types", methods=["GET", "POST"])
def exercise_types():

    user_id = session["user_id"]
    types = get_exercise_types(user_id)

    if request.method == "GET":
        return render_template("edit_exercise_types.html", types=types)

    if request.method == "POST":
        if "delete_id" in request.form:
            type_id = int(request.form["delete_id"])
            execute(
            "DELETE FROM exercise_types WHERE id = ? AND user_id = ?",
            [type_id, user_id]
            )

        elif "name" in request.form:
            name = request.form["name"].strip()
            if name:
                try:
                    execute(
                    "INSERT INTO exercise_types (user_id, exercise_type_name) VALUES (?, ?)",
                    [user_id, name]
                )
                except sqlite3.IntegrityError:
                    pass

    return redirect("/edit_exercise_types")      

@app.route("/search")
def search():
    type_id = request.args.get("type_id", type=int)
    user_id = session["user_id"]
    results = get_exercises(user_id, type_id)
    types   = get_exercise_types(user_id)
    return render_template("exercises.html", types=types, exercises=results, selected_type_id=type_id) 

#These functions are used to query or insert exercises or exercise types or other such stuff
def get_exercise(id):
    sql = "SELECT id, exercise_type_id, exercise_weight, exercise_date, comment FROM exercises WHERE id = ?"
    return query(sql, [id])[0]

#updating exercise class still not done...
def update_exercise(ex_id, type_id, weight, date, comment):
    sql = """
        UPDATE exercises
        SET exercise_type_id = ?, exercise_weight = ?,
            exercise_date = ?, comment = ?
        WHERE id = ?
    """
    execute(sql, [type_id, weight, date, comment, ex_id])
    
def remove_exercise(item_id):
    sql = "DELETE FROM exercises WHERE id = ?"
    execute(sql, [item_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    execute(sql, [username, password_hash])

    user_id = last_insert_id()
    #Create three default exercise types to all users.
    default_types = ["Bench press", "Deadlift", "Back squat"]
    for i in default_types:
        add_exercise_type(user_id, i)

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id

    return None

def get_exercise_types(user_id):
    sql = "SELECT id, exercise_type_name FROM exercise_types WHERE user_id = ?"
    return query(sql, [user_id])

def get_classes():
    sql = "SELECT id, label, sets, reps, alpha FROM classes"
    return query(sql, [])

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
    return query(sql, params)

def add_exercise_type(user_id, name):
    sql = "INSERT INTO exercise_types (user_id, exercise_type_name) VALUES (?, ?)"
    execute(sql, [user_id, name.strip()])

#SQL commands
def get_connection():
    con = sqlite3.connect("database.db", timeout=2)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

def last_insert_id():
    return g.last_insert_id