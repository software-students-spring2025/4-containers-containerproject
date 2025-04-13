"""
Tests for flask application.
"""

import time


def test_login_page(test_client):
    """Test that login page loads correctly"""
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_register_page(test_client):
    """Test that register page loads correctly"""
    response = test_client.get("/register")
    assert response.status_code == 200
    assert b"register" in response.data.lower()


def test_register_new_user(test_client):
    """Test user registration"""
    response = test_client.post(
        "/register",
        data={"username": "newuser", "password": "newpass", "weight": "70"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_register_duplicate_username(test_client):
    """Test registration with duplicate username"""
    # First register a user
    test_client.post(
        "/register",
        data={"username": "duplicateuser", "password": "pass1", "weight": "70"},
    )

    # Try to register with same username
    response = test_client.post(
        "/register",
        data={"username": "duplicateuser", "password": "pass2", "weight": "80"},
    )

    assert response.status_code == 200
    assert b"username is already in use" in response.data.lower()


def test_login_success(test_client):
    """Test successful login"""
    # First register a user
    test_client.post(
        "/register",
        data={"username": "testuser2", "password": "testpass2", "weight": "70"},
    )

    # Then try to login
    response = test_client.post(
        "/login",
        data={"username": "testuser2", "password": "testpass2"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"home" in response.data.lower()


def test_login_failure(test_client):
    """Test failed login"""
    response = test_client.post(
        "/login", data={"username": "wronguser", "password": "wrongpass"}
    )

    assert response.status_code == 200
    assert b"invalid" in response.data.lower()


def test_home_page_requires_login(test_client):
    """Test that home page requires login"""
    response = test_client.get("/home", follow_redirects=True)
    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_home_page_with_login(auth_client):
    """Test home page access with logged in user"""
    response = auth_client.get("/home")
    assert response.status_code == 200
    assert b"home" in response.data.lower()


def test_logout(auth_client):
    """Test logout functionality"""
    response = auth_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"login" in response.data.lower()


def test_home_page_jump_session(auth_client, test_app):
    """Test jump session functionality"""
    # Set up session state
    with auth_client.session_transaction() as sess:
        sess["session_active"] = True
        sess["start_time"] = 0  # Some initial time

    # End the jump session with data
    response = auth_client.post(
        "/home",
        data={"jump_count": "50", "seconds_jumped": "60", "calories_burned": "100"},
    )

    assert response.status_code == 200

    # Check if user data was updated
    user = test_app.mongo.db.users.find_one({"username": "testuser"})
    assert user["jump_count"] == 50
    assert user["seconds_jumped"] == 60
    assert user["calories_burned"] == 100


def test_home_page_calorie_calculation(auth_client, test_app):
    """Test automatic calorie calculation when no calories provided"""
    # Set up session state with a specific start time
    start_time = time.time() - 120  # 120 seconds ago
    with auth_client.session_transaction() as sess:
        sess["session_active"] = True
        sess["start_time"] = start_time

    # End the jump session without providing calories
    response = auth_client.post(
        "/home",
        data={
            "jump_count": "30",
            "seconds_jumped": "120",  # This should match our session length
        },
    )

    assert response.status_code == 200

    # Check if calories were calculated automatically
    user = test_app.mongo.db.users.find_one({"username": "testuser"})

    # Calculate expected calories: (120 * 12 * 70) / (60 * 150) = 11.2
    expected_calories = 11.2

    assert abs(user["calories_burned"] - expected_calories) < 0.1


def test_leaderboard_display(auth_client, test_app):
    """Test leaderboard display"""
    # Create multiple users with different jump counts
    users = [
        {"username": "user1", "password": "pass1", "weight": 70, "jump_count": 100},
        {"username": "user2", "password": "pass2", "weight": 70, "jump_count": 200},
        {"username": "user3", "password": "pass3", "weight": 70, "jump_count": 150},
    ]

    for user in users:
        test_app.mongo.db.users.insert_one(user)

    # Check leaderboard display
    response = auth_client.get("/home")
    assert response.status_code == 200

    # Check if top users are displayed in correct order
    response_data = response.data.decode("utf-8").lower()
    assert "user2" in response_data  # Should be first (200 jumps)
    assert "user3" in response_data  # Should be second (150 jumps)
    assert "user1" in response_data  # Should be third (100 jumps)
