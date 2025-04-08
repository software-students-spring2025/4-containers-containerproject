from flask import Blueprint, render_template
from .db import get_collection

main = Blueprint("main", __name__)

@main.route("/")
def index():
    collection = get_collection()
    results = list(collection.find().sort("_id", -1).limit(10))
    return render_template("index.html", results=results)