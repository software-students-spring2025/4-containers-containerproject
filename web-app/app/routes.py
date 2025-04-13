"""
webpage routes
"""

import time
from flask import render_template, request, session, redirect, url_for, flash, current_app
from bson.objectid import ObjectId

def get_mongo():
    """Helper function to get the current MongoDB instance"""
    return current_app.mongo

def index():
    """
    temp route
    """
    return redirect(url_for("login"))

def login():
    """
    login
    """
    if request.method == "POST":
        username = request.form["username"]  # get username from form
        password = request.form["password"]  # get password from form

        # look for the user in the MongoDB 'users' collection
        user = get_mongo().db.users.find_one({"username": username})

        if user and user["password"] == password:
            session["user_id"] = str(user["_id"])  # user session
            return redirect(url_for("home"))  # direct to home page
        flash("Invalid username or password. Please try again.")

    return render_template("login.html")  # render login page

def register():
    """
    register
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        weight = float(request.form["weight"])

        # check if the username is already in use
        existing_user = get_mongo().db.users.find_one({"username": username})
        if existing_user:
            flash("Username is already in use. Please choose another username.")
            return render_template("register.html")

        # if the user does not exist, add the new user
        get_mongo().db.users.insert_one(
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

def logout():
    """
    session logout
    """
    session.clear()
    flash("Thanks for jumping with Jumparoo!")
    return redirect(url_for("login"))

def home():
    """
    central page
    """

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if "session_active" not in session:
        session["session_active"] = False

    user = None
    if "user_id" in session:
        user = get_mongo().db.users.find_one({"_id": ObjectId(session["user_id"])})

    calories_burned = 0

    if request.method == "POST":

        if not session["session_active"]:
            session["session_active"] = True
            session["start_time"] = time.time()

        else:
            session["session_active"] = False
            end_time = time.time()
            session_length = int(end_time - session.get("start_time", end_time))

            # Get jump count from form
            jump_count = int(request.form.get("jump_count", 0))
            seconds_jumped = int(request.form.get("seconds_jumped", session_length))
            calories_from_form = float(request.form.get("calories_burned", 0))

            if user:
                weight = float(user.get("weight", 0))
                # Defensive programming -> calculate calories if js doesn't work
                if calories_from_form > 0:
                    added_calories = calories_from_form
                else:
                    added_calories = (session_length * 12 * weight) / (60 * 150)

                get_mongo().db.users.update_one(
                    {"_id": ObjectId(session["user_id"])},
                    {
                        "$inc": {
                            "jump_count": jump_count,
                            "seconds_jumped": seconds_jumped,
                            "calories_burned": round(added_calories, 2),
                        }
                    },
                )

                user = get_mongo().db.users.find_one({"_id": ObjectId(session["user_id"])})
                calories_burned = round(added_calories, 2)

            session.pop("start_time", None)

    leaderboard = list(
        get_mongo().db.users.find({}, {"username": 1, "jump_count": 1, "_id": 0})
        .sort("jump_count", -1)
        .limit(5)
    )

    return render_template(
        "home.html",
        session_active=session["session_active"],
        user=user,
        leaderboard=leaderboard,
        calories_burned=calories_burned,
    )
