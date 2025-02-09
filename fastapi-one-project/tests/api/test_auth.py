import pytest
from fastapi import status

def test_create_user(client, test_user):
    response = client.post("/api/v1/users/", json=test_user)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]
    assert "id" in data

def test_create_user_duplicate_username(client, test_user):
    # Create first user
    client.post("/api/v1/users/", json=test_user)
    
    # Try to create user with same username
    response = client.post("/api/v1/users/", json=test_user)
    assert response.status_code == status.HTTP_409_CONFLICT

def test_login_user(client, test_user):
    # Create user
    client.post("/api/v1/users/", json=test_user)
    
    # Login
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    # Create user
    client.post("/api/v1/users/", json=test_user)
    
    # Try to login with wrong password
    login_data = {
        "username": test_user["username"],
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/token", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 