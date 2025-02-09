import pytest
from datetime import timedelta
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token
)

def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0

def test_create_access_token_with_expiry():
    data = {"sub": "testuser"}
    expires = timedelta(minutes=15)
    token = create_access_token(data, expires_delta=expires)
    
    assert isinstance(token, str)
    assert len(token) > 0 