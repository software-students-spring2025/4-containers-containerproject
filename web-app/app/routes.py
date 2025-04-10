"""
webpage routes
"""

from flask import render_template, request, session, redirect, url_for, flash
from app import mongo
from . import app  # pylint: disable=cyclic-import


@app.route("/")
def index():
    """
    temp route
    """
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    login
    """
    if request.method == "POST":
        username = request.form["username"]  # get username from form
        password = request.form["password"]  # get password from form

        # look for the user in the MongoDB 'users' collection
        user = mongo.db.users.find_one({"username": username})

        if user and user["password"] == password:
            session["user_id"] = str(user["_id"])  # user session
            return redirect(url_for("home"))  # direct to home page
        flash("Invalid username or password. Please try again.")

    return render_template("login.html")  # render login page


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    register
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        weight = float(request.form["weight"])

        # check if the username is already in use
        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            flash("Username is already in use. Please choose another username.")
            return render_template("register.html")

        # if the user does not exist, add the new user
        mongo.db.users.insert_one(
            {
                "username": username,
                "password": password,
                "jump_count": 0,
                "calories_burned": 0,
                "weight": weight,
                "seconds_jumped": 0,
            }
        )
        flash("Account created successfully! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/home")
def home():
    """
    home (main page)
    """
    return render_template("home.html")
