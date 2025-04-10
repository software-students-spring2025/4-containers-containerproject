"""
app initialization
"""

import os
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")

app.config["SECRET_KEY"] = os.urandom(24)

mongo = PyMongo(app)

from app import routes  # pylint: disable=wrong-import-position
