import pytest
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostUpdate

def test_create_post(db_session):
    post_service = PostService(db_session)
    post_data = PostCreate(content="Test post")
    user_id = 1

    post = post_service.create_post(user_id=user_id, post_create=post_data)
    
    assert post.content == "Test post"
    assert post.owner_id == user_id

def test_get_post_not_found(db_session):
    post_service = PostService(db_session)
    
    with pytest.raises(HTTPException) as exc_info:
        post_service.get_post(post_id=999)
    
    assert exc_info.value.status_code == 404

def test_update_post_within_time_limit(db_session):
    # Create a post
    post_service = PostService(db_session)
    post_data = PostCreate(content="Original content")
    post = post_service.create_post(user_id=1, post_create=post_data)
    
    # Update the post within 10 minutes
    update_data = PostUpdate(content="Updated content")
    updated_post = post_service.update_post(
        post_id=post.id,
        user_id=1,
        post_update=update_data
    )
    
    assert updated_post.content == "Updated content"

def test_update_post_after_time_limit(db_session):
    # Create a post with timestamp more than 10 minutes ago
    post_service = PostService(db_session)
    post_data = PostCreate(content="Original content")
    post = post_service.create_post(user_id=1, post_create=post_data)
    
    # Manually update the timestamp to be older than 10 minutes
    old_timestamp = datetime.now(timezone.utc) - timedelta(minutes=11)
    post.timestamp = old_timestamp
    db_session.commit()
    
    # Try to update the post
    update_data = PostUpdate(content="Updated content")
    with pytest.raises(HTTPException) as exc_info:
        post_service.update_post(
            post_id=post.id,
            user_id=1,
            post_update=update_data
        )
    
    assert exc_info.value.status_code == 403

def test_delete_post_unauthorized(db_session):
    # Create a post as user 1
    post_service = PostService(db_session)
    post_data = PostCreate(content="Test post")
    post = post_service.create_post(user_id=1, post_create=post_data)
    
    # Try to delete as user 2
    with pytest.raises(HTTPException) as exc_info:
        post_service.delete_post(post_id=post.id, user_id=2)
    
    assert exc_info.value.status_code == 403 