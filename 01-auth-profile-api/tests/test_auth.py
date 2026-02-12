"""
Tests for auth endpoints (register, login).

Coverage:
- POST /auth/register (success, duplicate email, validation errors)
- POST /auth/login (success, wrong email, wrong password)
"""

import pytest


def test_register_success(client):
    """
    Test successful registration.
    
    What we check:
    - 201 status code
    - Returns access_token
    - Returns user info (email, name, id)
    - Does NOT return password_hash
    """
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "name": "Test User",
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    
    # Check token
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Check user
    user = data["user"]
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"
    assert "id" in user
    assert "created_at" in user
    
    # Security: password should never be returned
    assert "password" not in user
    assert "password_hash" not in user


def test_register_duplicate_email(client):
    """
    Test registration with already registered email.
    
    Expected:
    - 409 Conflict
    """
    # Register first user
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "name": "Test User",
        },
    )
    
    # Try to register again with same email
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "different123",
            "name": "Another User",
        },
    )
    
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"].lower()


def test_register_invalid_email(client):
    """
    Test registration with invalid email format.
    
    Expected:
    - 422 Unprocessable Entity (FastAPI validation error)
    """
    response = client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "test1234",
            "name": "Test User",
        },
    )
    
    assert response.status_code == 422


def test_register_short_password(client):
    """
    Test registration with password < 6 characters.
    
    Expected:
    - 422 Unprocessable Entity
    """
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "123",
            "name": "Test User",
        },
    )
    
    assert response.status_code == 422


def test_login_success(client):
    """
    Test successful login.
    
    Flow:
    1. Register a user
    2. Login with same credentials
    3. Check we get a token back
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
    assert register_response.status_code == 201
    
    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "test1234",
        },
    )
    
    assert login_response.status_code == 200
    data = login_response.json()
    
    # Check token
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Check user
    user = data["user"]
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"


def test_login_wrong_email(client):
    """
    Test login with non-existent email.
    
    Expected:
    - 401 Unauthorized
    """
    response = client.post(
        "/auth/login",
        json={
            "email": "notexist@example.com",
            "password": "test1234",
        },
    )
    
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_login_wrong_password(client):
    """
    Test login with wrong password.
    
    Expected:
    - 401 Unauthorized
    """
    # Register
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test1234",
            "name": "Test User",
        },
    )
    
    # Try to login with wrong password
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword",
        },
    )
    
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()
