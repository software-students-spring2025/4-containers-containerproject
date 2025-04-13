"""
Flask application instance for testing.
"""

import os
from flask import Flask
from flask_pymongo import PyMongo
from app.routes import index, login, register, logout, home


def create_test_app():
    """
    Creates a new Flask instance for testing.
    """
    # Create a new Flask app instance
    test_app = Flask(__name__)

    # Configure for testing
    test_app.config["TESTING"] = True
    test_app.config["SECRET_KEY"] = "test_secret_key"
    test_app.config["MONGO_URI"] = "mongodb://localhost:27017/test_db"

    # Set template folder path
    test_app.template_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "app/templates"
    )

    # Use mongomock for testing
    test_app.mongo = PyMongo(test_app)

    # Register routes directly
    test_app.route("/")(index)
    test_app.route("/login", methods=["GET", "POST"])(login)
    test_app.route("/register", methods=["GET", "POST"])(register)
    test_app.route("/logout")(logout)
    test_app.route("/home", methods=["GET", "POST"])(home)

    return test_app
