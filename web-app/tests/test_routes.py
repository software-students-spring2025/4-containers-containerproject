"""
Initial test for workflow
"""

import pytest


@pytest.fixture
def test_client(app):
    """
    Checking for client
    """
    return app.test_client()


def test_root_redirects_to_login(client):
    """
    Checking for proper redirect
    """
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302  # 302 Found (redirect)
    assert "/login" in response.headers["Location"]
