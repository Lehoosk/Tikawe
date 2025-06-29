import sqlite3
import secrets

from flask import abort, Flask, redirect, render_template, request, session, flash
import data

app = Flask(__name__)
app.config["SECRET_KEY"] = "varmasalasana"

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


#Page-rendering functions start here:
@app.route("/")
def index():
    """Render front page"""
    exercises_list = data.get_public_exercises()
    return render_template("index.html", exercises=exercises_list)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Render login page"""
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = data.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "Error: wrong username or password"

@app.route("/logout")
def logout():
    "Render logout page"
    session.pop("user_id", None)
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    "Render register page. GET method used when first loading the page, POST when user has clicked register button"

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
    """Used to log a new exercise to user"""
    require_login()
    user_id = session["user_id"]

    if request.method == "GET":
        types = data.get_exercise_types(user_id)
        default = data.get_user_default(user_id)
        classes = data.get_classes()
        return render_template("new_exercise.html", types=types, classes=classes, default=default)

    if request.method == "POST":
        check_csrf()
        type_id = int(request.form["type_id"])
        weight  = float(request.form["weight"])
        ex_date = request.form["date"]
        class_id = int(request.form["class_id"])
        note = request.form["note"]
        if request.form.get("public") == "1":
            public = 1
        else:
            public = 0
        data.add_exercise(user_id=user_id, type_id=type_id, class_id=class_id, weight=weight, ex_date=ex_date, public=public, note=note)
        data.add_pr(user_id=user_id, type_id=type_id, class_id=class_id, weight=weight, ex_date=ex_date)
        data.add_exercise_counter(user_id, 1)
    return redirect("/")

@app.route("/exercises")
def exercises():
    "Renders user's exercise history page"
    require_login()
    user_id = session["user_id"]
    exercises_list = data.get_user_exercises(user_id)
    types_list = data.get_exercise_types(user_id)
    return render_template("exercises.html", exercises=exercises_list, types=types_list)


@app.route("/edit/<int:exercise_id>", methods=["GET", "POST"])
def edit_exercise(exercise_id):
    "Renders page to edit single exercise"
    require_login()
    exercise = data.get_exercise(exercise_id)
    user_id = session["user_id"]

    if request.method == "GET":
        types = data.get_exercise_types(user_id)
        return render_template("edit.html", exercise=exercise, types=types)

    if request.method == "POST":
        check_csrf()
        if exercise["user_id"] != user_id:
            abort(403)
        type_id = int(request.form["type_id"])
        weight  = float(request.form["weight"])
        ex_date = request.form["date"]
        note  = request.form["note"]
        data.update_exercise(exercise_id, type_id, weight, ex_date, note)
        return redirect("/")

@app.route("/remove/<int:exercise_id>", methods=["GET", "POST"])
def remove(exercise_id):
    "Renders page to delete a single exercise"
    require_login()
    exercise = data.get_exercise(exercise_id)
    user_id = session["user_id"]

    if request.method == "GET":
        return render_template("remove.html", exercise=exercise)

    if request.method == "POST":
        check_csrf()

        if exercise["user_id"] != user_id:
            abort(403)

        if "remove" in request.form:
            data.remove_exercise(exercise_id)
            data.add_exercise_counter(exercise["user_id"], -1)
            return redirect("/exercises")
    return redirect("/")

@app.route("/edit_exercise_types", methods=["GET", "POST"])
def exercise_types():
    "Renders page to edit users exercise types"
    require_login()
    user_id = session["user_id"]
    types = data.get_exercise_types(user_id)

    if request.method == "GET":
        return render_template("edit_exercise_types.html", types=types)

    if request.method == "POST":
        check_csrf()

        if "delete_id" in request.form:
            type_id = int(request.form["delete_id"])

            #check, if the owner of the exercise type is the current user. Because the previous query result is a list, need to go thought the list
            remove_type_id = None
            for t in types:
                if t["id"] == type_id:
                    remove_type_id = t
                    break

            if remove_type_id is None or remove_type_id["user_id"] != user_id:
                abort(403)

            data.delete_exercise_type(user_id, type_id)

        elif "name" in request.form:
            name = request.form["name"].strip()
            if name:
                data.add_exercise_type(user_id, name)

    return redirect("/edit_exercise_types")

@app.route("/search")
def search():
    "Renders a page to view all exercises or by a certain type"
    require_login()
    type_id = request.args.get("type_id", type=int)
    user_id = session["user_id"]
    results = data.get_user_exercises(user_id, type_id)
    types   = data.get_exercise_types(user_id)
    return render_template("exercises.html", types=types, exercises=results, selected_type_id=type_id)

@app.route("/comments/<int:exercise_id>", methods=["GET", "POST"])
def comments(exercise_id):
    "Renders the comment page"
    require_login()
    exercise = data.get_exercise(exercise_id)
    comments_list = data.get_comments(exercise_id)
    user_id = session["user_id"]
    count = int(exercise["comment_count"])

    if request.method == "GET":
        return render_template("comments.html", exercise=exercise, comments=comments_list)

    if request.method == "POST":
        comment_text = request.form["comment"]
        if comment_text:
            data.post_comment(exercise_id, user_id, comment_text, count+1)
            data.add_comment_counter(user_id)
        
        return redirect(f"/comments/{exercise_id}")

@app.route("/stats")
def stats():
    "Renders the statistics page"
    require_login()
    user_id = session["user_id"]
    stats_list = data.get_statistics(user_id)
    pr_list = data.get_pr_statistics(user_id)
    return render_template("stats.html", stats=stats_list, pr=pr_list)

@app.route("/user_page", defaults={"user_id": None})
@app.route("/user_page/<int:user_id>")
def user_page(user_id):
    "Renders the user page"
    if user_id is None:
        user_id = session["user_id"]
    stats_list = data.get_user_page_stats(user_id)
    return render_template("user.html", user=stats_list)
