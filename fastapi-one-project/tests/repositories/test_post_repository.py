import pytest
from app.repositories.post_repository import PostRepository
from app.models import Post, Like, Retweet

def test_create_post(db_session):
    repo = PostRepository(db_session)
    post = repo.create(content="Test post", owner_id=1)
    
    assert post.content == "Test post"
    assert post.owner_id == 1

def test_get_post(db_session):
    # Create a post
    repo = PostRepository(db_session)
    created_post = repo.create(content="Test post", owner_id=1)
    
    # Get the post
    post = repo.get(created_post.id)
    
    assert post is not None
    assert post.content == "Test post"
    assert post.id == created_post.id

def test_get_posts_with_counts(db_session):
    repo = PostRepository(db_session)
    
    # Create a post
    post = repo.create(content="Test post", owner_id=1)
    
    # Add a like
    like = Like(user_id=2, post_id=post.id)
    db_session.add(like)
    
    # Add a retweet
    retweet = Retweet(user_id=3, post_id=post.id)
    db_session.add(retweet)
    db_session.commit()
    
    # Get posts with counts
    posts = repo.get_posts_with_counts(current_user_id=1)
    
    assert len(posts) > 0
    post = posts[0]
    assert hasattr(post, 'likes_count')
    assert hasattr(post, 'retweets_count')

def test_like_post(db_session):
    repo = PostRepository(db_session)
    
    # Create a post
    post = repo.create(content="Test post", owner_id=1)
    
    # Like the post
    result = repo.like_post(post_id=post.id, user_id=2)
    
    assert result is True
    
    # Verify like exists
    like = db_session.query(Like).filter_by(post_id=post.id, user_id=2).first()
    assert like is not None

def test_unlike_post(db_session):
    repo = PostRepository(db_session)
    
    # Create a post and like it
    post = repo.create(content="Test post", owner_id=1)
    repo.like_post(post_id=post.id, user_id=2)
    
    # Unlike the post
    result = repo.unlike_post(post_id=post.id, user_id=2)
    
    assert result is True
    
    # Verify like is removed
    like = db_session.query(Like).filter_by(post_id=post.id, user_id=2).first()
    assert like is None 