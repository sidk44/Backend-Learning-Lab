"""
Tests for profile endpoints (GET /me, PATCH /me).

Coverage:
- GET /me (success, missing token, invalid token)
- PATCH /me (update name, update bio, update both, no auth)
"""

import pytest


def test_get_profile_success(client):
    """
    Test GET /me with valid token.
    
    Flow:
    1. Register user (get token)
    2. Call GET /me with token
    3. Check we get user info back
    """
    # Register
    register_response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "name": "Test User",
        },
    )
    token = register_response.json()["access_token"]
    
    # Get profile
    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    user = response.json()
    
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"
    assert user["bio"] is None  # Not set yet
    assert "id" in user


def test_get_profile_no_token(client):
    """
    Test GET /me without Authorization header.
    
    Expected:
    - 403 Forbidden (HTTPBearer requirement)
    """
    response = client.get("/me")
    
    assert response.status_code == 403


def test_get_profile_invalid_token(client):
    """
    Test GET /me with invalid token.
    
    Expected:
    - 401 Unauthorized
    """
    response = client.get(
        "/me",
        headers={"Authorization": "Bearer invalid_token_123"},
    )
    
    assert response.status_code == 401


def test_update_profile_name(client):
    """
    Test updating profile name.
    
    Flow:
    1. Register user
    2. Update name via PATCH /me
    3. Verify name changed
    """
    # Register
    register_response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "name": "Old Name",
        },
    )
    token = register_response.json()["access_token"]
    
    # Update name
    response = client.patch(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "New Name"},
    )
    
    assert response.status_code == 200
    user = response.json()
    
    assert user["name"] == "New Name"
    assert user["email"] == "test@example.com"  # Unchanged


def test_update_profile_bio(client):
    """
    Test updating profile bio.
    """
    # Register
    register_response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "name": "Test User",
        },
    )
    token = register_response.json()["access_token"]
    
    # Update bio
    response = client.patch(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"bio": "This is my bio"},
    )
    
    assert response.status_code == 200
    user = response.json()
    
    assert user["bio"] == "This is my bio"
    assert user["name"] == "Test User"  # Unchanged


def test_update_profile_both_fields(client):
    """
    Test updating name and bio together.
    """
    # Register
    register_response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "name": "Old Name",
        },
    )
    token = register_response.json()["access_token"]
    
    # Update both
    response = client.patch(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "New Name",
            "bio": "New bio",
        },
    )
    
    assert response.status_code == 200
    user = response.json()
    
    assert user["name"] == "New Name"
    assert user["bio"] == "New bio"


def test_update_profile_no_auth(client):
    """
    Test PATCH /me without authentication.
    
    Expected:
    - 403 Forbidden
    """
    response = client.patch(
        "/me",
        json={"name": "Hacker"},
    )
    
    assert response.status_code == 403


def test_update_profile_empty_payload(client):
    """
    Test PATCH /me with empty JSON (no fields to update).
    
    Expected:
    - 200 OK (nothing changed)
    """
    # Register
    register_response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "name": "Test User",
        },
    )
    token = register_response.json()["access_token"]
    original_user = register_response.json()["user"]
    
    # Update with empty JSON
    response = client.patch(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
        json={},
    )
    
    assert response.status_code == 200
    user = response.json()
    
    # Nothing should change
    assert user["name"] == original_user["name"]
    assert user["email"] == original_user["email"]


def test_update_profile_validation_error(client):
    """
    Test PATCH /me with invalid data (name too short).
    
    Expected:
    - 422 Unprocessable Entity
    """
    # Register
    register_response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "name": "Test User",
        },
    )
    token = register_response.json()["access_token"]
    
    # Try to update with invalid name (< 2 chars)
    response = client.patch(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "A"},
    )
    
    assert response.status_code == 422
