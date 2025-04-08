"""
app initialization
"""

from .routes import main
from flask import Flask
from .db import init_db

def some_function():
    """
    Function that performs some task.
    """
    pass

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    init_db(app)

    app.register_blueprint(main)

    return app
