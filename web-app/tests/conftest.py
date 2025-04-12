"""
Setting up client
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app as flask_app  # pylint: disable=import-error, wrong-import-position


@pytest.fixture
def client():
    """
    Setting up fixture
    """
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as test_client:
        yield test_client
