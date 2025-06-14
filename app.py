from flask import Flask
from flask import redirect, render_template, request, session, g, flash
import db
import data
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "varmasalasana"

#Page-rendering functions start here:
@app.route("/")
def index():
    exercises = data.get_public_exercises()
    return render_template("index.html", exercises=exercises)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = data.check_login(username, password)
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
        if request.form.get("public") == "1":
            public = 1
        else:
            public = 0
    # Validate username and password and match passwords

        if (len(username) < 4 or len(password1) < 8 or len(password2) < 8):
            flash("Erroe: too short username or password")
            return redirect("/register")

        if password1 != password2:
            flash("Error: passwords don't match")
            return redirect("/register")
        
        try:
            data.create_user(username, password1, public)
            return render_template("register_success.html")
        except sqlite3.IntegrityError:
            flash("Error: username exists")
            return redirect("/register")
        
@app.route("/new_exercise", methods=["GET", "POST"])
def new_exercise():

    user_id = session["user_id"]

    if request.method == "GET":
        types = data.get_exercise_types(user_id)
        default = data.get_user_default(user_id)
        classes = data.get_classes()
        return render_template("new_exercise.html", types=types, classes=classes, default=default)
    
    if request.method == "POST":
        type_id = int(request.form["type_id"])
        weight  = float(request.form["weight"])
        ex_date = request.form["date"]
        class_id = int(request.form["class_id"])
        note = request.form["note"]
        if request.form.get("public") == "1":
            public = 1
        else:
            public = 0

        sql = """
            INSERT INTO exercises
                  (user_id, exercise_type_id, exercise_class_id, exercise_weight, exercise_date, public, note, comment_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """
        db.execute(sql, [user_id, type_id, class_id, weight, ex_date, public, note])
        return redirect("/")

@app.route("/exercises")
def exercises():
    user_id = session["user_id"]
    exercises = data.get_user_exercises(user_id)
    types = data.get_exercise_types(user_id)
    return render_template("exercises.html", exercises=exercises, types=types)


@app.route("/edit/<int:exercise_id>", methods=["GET", "POST"])
def edit_exercise(exercise_id):
    exercise = data.get_exercise(exercise_id)
    user_id = session["user_id"]

    if request.method == "GET":
        types = data.get_exercise_types(user_id)
        return render_template("edit.html", exercise=exercise, types=types)

    if request.method == "POST":
        type_id = int(request.form["type_id"])
        weight  = float(request.form["weight"])
        ex_date = request.form["date"]
        note  = request.form["note"]
        data.update_exercise(exercise_id, type_id, weight, ex_date, note)
        return redirect("/")

@app.route("/remove/<int:exercise_id>", methods=["GET", "POST"])
def remove(exercise_id):

    exercise = data.get_exercise(exercise_id)

    if request.method == "GET":
        return render_template("remove.html", exercise=exercise)

    if request.method == "POST":
        if "remove" in request.form:
            data.remove_exercise(exercise_id)
            return redirect("/exercises")
        else:
            return redirect("/")


@app.route("/edit_exercise_types", methods=["GET", "POST"])
def exercise_types():

    user_id = session["user_id"]
    types = data.get_exercise_types(user_id)

    if request.method == "GET":
        return render_template("edit_exercise_types.html", types=types)

    if request.method == "POST":
        if "delete_id" in request.form:
            type_id = int(request.form["delete_id"])
            db.execute(
            "DELETE FROM exercise_types WHERE id = ? AND user_id = ?",
            [type_id, user_id]
            )

        elif "name" in request.form:
            name = request.form["name"].strip()
            if name:
                try:
                    db.execute(
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
    results = data.get_user_exercises(user_id, type_id)
    types   = data.get_exercise_types(user_id)
    return render_template("exercises.html", types=types, exercises=results, selected_type_id=type_id) 