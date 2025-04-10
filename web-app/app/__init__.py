"""
app initialization
"""

import os
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["MONGODB_URI"] = os.getenv("MONGODB_URI")

mongo = PyMongo(app)



