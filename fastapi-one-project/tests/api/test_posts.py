import pytest
from fastapi import status

def get_auth_headers(client, test_user):
    # Create user and get token
    client.post("/api/v1/users/", json=test_user)
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/api/v1/auth/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_post(client, test_user, test_post):
    headers = get_auth_headers(client, test_user)
    response = client.post("/api/v1/posts/", json=test_post, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["content"] == test_post["content"]
    assert "id" in data
    assert "timestamp" in data

def test_create_post_unauthorized(client, test_post):
    response = client.post("/api/v1/posts/", json=test_post)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_posts(client, test_user, test_post):
    headers = get_auth_headers(client, test_user)
    
    # Create a post
    client.post("/api/v1/posts/", json=test_post, headers=headers)
    
    # Get all posts
    response = client.get("/api/v1/posts/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["content"] == test_post["content"]

def test_delete_post(client, test_user, test_post):
    headers = get_auth_headers(client, test_user)
    
    # Create a post
    response = client.post("/api/v1/posts/", json=test_post, headers=headers)
    post_id = response.json()["id"]
    
    # Delete the post
    response = client.delete(f"/api/v1/posts/{post_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    
    # Verify post is deleted
    response = client.get("/api/v1/posts/", headers=headers)
    posts = response.json()
    assert not any(post["id"] == post_id for post in posts)

def test_like_post(client, test_user, test_post):
    headers = get_auth_headers(client, test_user)
    
    # Create a post
    response = client.post("/api/v1/posts/", json=test_post, headers=headers)
    post_id = response.json()["id"]
    
    # Like the post
    response = client.post(f"/api/v1/posts/{post_id}/like", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Get post with counts
    response = client.get("/api/v1/posts/with_counts/", headers=headers)
    posts = response.json()
    post = next(p for p in posts if p["id"] == post_id)
    assert post["likes_count"] == 1