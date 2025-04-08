"""
database link
"""

from flask import g  # , current_app
from pymongo import MongoClient


def some_function():
    """
    Function that performs some task.
    """
    # TODO: Implement this function


def init_db(app):
    @app.before_request
    def connect_db():
        if "db" not in g:
            mongo_uri = app.config.get("MONGO_URI")
            g.client = MongoClient(mongo_uri)
            g.db = g.client["ml_data"]

    @app.teardown_appcontext
    def close_db(_error):
        client = g.pop("client", None)
        if client is not None:
            client.close()


def get_collection():
    return g.db["results"]
