"""
webpage routes
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .db import get_collection
from app import app, mongo

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """
    main route
    """
    try:
        return render_template("index.html")

    except Exception as e:
        print(f"Error fetching data: {e}")
        return render_template("index.html", recent_items=[])

@main.route("/register", methods=["GET", "POST"])
def register():
    """
    register
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        weight = request.form["weight"]

        #check if the username is already in use
        existing_user = mongo.db.user.find_one({"username": username})
        if existing_user:
            flash("Username is already in use. Please choose another username.")

        #if the user does not exist, add the new user
        mongo.db.user.insert_one({
            "username": username,
            "password": password, 
            "weight": weight
        })
        
        flash("Account created successfully! Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    """
    login
    """
    if request.method == "POST":
        username = request.form["username"]  #get username from form
        password = request.form["password"]  #get password from form

        #look for the user in the MongoDB 'user' collection
        user = mongo.db.user.find_one({"username": username})

        if user and user["password"] == password:  
            session["user_id"] = str(user["_id"])  #user session
            return redirect(url_for("home"))  #direct to home page
        
        else:
            flash("Invalid username or password. Please try again.")

    return render_template("login.html")  #render login page
