"""
Routes module for the web application.
Defines all the URL routes and their corresponding view functions.
"""

from flask import jsonify, render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId
from app import app, mongo


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
