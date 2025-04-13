"""
Test configuration and fixtures for the Flask application.
"""

import pytest
from .test_app import create_test_app


@pytest.fixture
def test_app():
    """
    Create a new test application instance.
    """
    app_instance = create_test_app()
    return app_instance


@pytest.fixture
def test_client(test_app):  # pylint: disable=redefined-outer-name
    """
    Create a test client for the application.
    """
    with test_app.test_client() as client:
        with test_app.app_context():
            # Clear test database before each test
            test_app.mongo.db.users.delete_many({})
            yield client
            # Clear test database after each test
            test_app.mongo.db.users.delete_many({})


@pytest.fixture
def auth_client(test_client, test_app):  # pylint: disable=redefined-outer-name
    """
    Create an authenticated test client.
    """
    # Create a test user
    test_user = {
        "username": "testuser",
        "password": "testpass",
        "weight": 70,
        "jump_count": 0,
        "calories_burned": 0,
        "seconds_jumped": 0,
    }
    test_app.mongo.db.users.insert_one(test_user)

    # Login the test user
    test_client.post("/login", data={"username": "testuser", "password": "testpass"})
