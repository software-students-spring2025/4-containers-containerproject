"""
app initialization
"""

import os
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from app.routes import index, login, register, logout, home

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/jumparoo")
app.config["SECRET_KEY"] = os.urandom(24)

# Initialize MongoDB
app.mongo = PyMongo(app)

# Register routes
app.route("/")(index)
app.route("/login", methods=["GET", "POST"])(login)
app.route("/register", methods=["GET", "POST"])(register)
app.route("/logout")(logout)
app.route("/home", methods=["GET", "POST"])(home)
