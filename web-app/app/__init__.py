"""
app initialization
"""

from flask import Flask
from .routes import main
from .db import init_db


def create_app():
    """
    create app
    """
    app = Flask(__name__)
    app.config.from_prefixed_env()
    init_db(app)

    app.register_blueprint(main)

    return app
