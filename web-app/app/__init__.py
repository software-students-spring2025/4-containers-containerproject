from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

app = Flask(__name__)

#configure MongoDB settings
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

app.config["SECRET_KEY"] = os.urandom(24)

mongo = PyMongo(app)

#test the mongodb connection 
try:
    mongo.cx.server_info()
    print("MongoDB connected successfully")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise e

#importing routes after app is created to avoid circular imports
from app import routes


