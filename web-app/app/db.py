"""
database link
"""

import os
from flask import g  # , current_app
from pymongo import MongoClient


def init_db(app):
    """
    init db function
    """

    @app.before_request
    def connect_db():
        if "db" not in g:
            mongo_uri = os.environ.get("MONGODB_URI")
            g.client = MongoClient(mongo_uri)
            g.db = g.client["jumping-jack-db"]

    @app.teardown_appcontext
    def close_db(_error):
        client = g.pop("client", None)
        if client is not None:
            client.close()


def get_collection():
    """
    get collection function
    """
    return g.db["user"]
