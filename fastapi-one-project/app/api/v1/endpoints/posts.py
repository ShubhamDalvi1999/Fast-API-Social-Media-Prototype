from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Annotated
from datetime import timedelta, datetime, timezone

from app.models import Post, User, Like, Retweet
from app.schemas import Post as PostSchema, PostCreate, PostUpdate, PostWithCounts
from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.core.exceptions import raise_not_found_exception, raise_forbidden_exception

router = APIRouter(
    tags=["Posts"]
)

db_dependency = Annotated[Session, Depends(get_db)]

# Get Posts Endpoint
@router.get("/", response_model=List[PostSchema])
def read_posts(db: db_dependency, skip: int = 0, limit: int = 10):
    """
    Get posts
     skip : is the number of posts to skip, means the number of posts to skip from the beginning
     limit : is the number of posts to return
    Takes the skip and limit parameters to paginate the posts
    Orders the posts by timestamp in descending order
    Returns the posts
    """
    posts = db.query(Post).order_by(Post.timestamp.desc()).offset(skip).limit(limit).all()
    return posts

# Create New Post Endpoint
@router.post("/", response_model=PostSchema)
def create_new_post(
    post: PostCreate,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new post
    Takes the post data from the request body
    Creates a new post in the database
    Returns the new post
    """
    db_post = Post(content=post.content, owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Add owner_username to response
    return {
        "id": db_post.id,
        "content": db_post.content,
        "timestamp": db_post.timestamp,
        "owner_id": db_post.owner_id,
        "owner_username": current_user.username
    }

# Delete Existing Post Endpoint
@router.delete("/{post_id}", response_model=dict)
async def delete_existing_post(
    post_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    """
    Delete an existing post
    Takes the post_id of the post to delete
    Checks if the post exists in the database
    Checks if the post belongs to the current user
    Deletes the post from the database
    Returns a success message
    """
    try:
        # Get the post
        post = db.query(Post).filter(Post.id == post_id).first()
        
        # Check if post exists
        if post is None:
            raise_not_found_exception('Post not found')
            
        # Check if user owns the post
        if post.owner_id != current_user.id:
            raise_forbidden_exception('Not authorized to delete this post')
        
        # Delete the post
        db.delete(post)
        db.commit()
        
        return {"status": "success", "message": "Post deleted successfully"}
        
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Update Post Endpoint
@router.put("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing post
    Takes the post_id of the post to update
    Takes the post_update data from the request body
    Checks if the post exists in the database
    Checks if the post belongs to the current user
    Updates the post in the database
    Returns the updated post
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise_not_found_exception('Post not found')
    if post.owner_id != current_user.id:
        raise_forbidden_exception('Not authorized to edit this post')

    # Check if the post is within the 10-minute edit window
    post_timestamp_aware = post.timestamp.replace(tzinfo=timezone.utc)
    time_since_creation = datetime.now(timezone.utc) - post_timestamp_aware
    if time_since_creation > timedelta(minutes=10):
        raise_not_found_exception("You can only edit a post within 10 minutes of its creation")
    post.content = post_update.content
    db.add(post)
    db.commit()
    return post

# Like Post Endpoint
@router.post("/{post_id}/like", status_code=204)
def like_post(
    post_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    """
    Like a post
    Takes the post_id of the post to like
    Checks if the post exists in the database
    Checks if the post is not already liked by the current user
    Adds the post to the current user's liked posts
    Returns nothing
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise_not_found_exception('Post not found')
    like = db.query(Like).filter_by(user_id=current_user.id, post_id=post_id).first()
    if like:
        raise_not_found_exception("Already liked")
    new_like = Like(user_id=current_user.id, post_id=post_id)
    db.add(new_like)
    db.commit()
    return

# Unlike Post Endpoint
@router.post("/{post_id}/unlike", status_code=204)
def unlike_post(
    post_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    """
    Unlike a post
    Takes the post_id of the post to unlike
    Checks if the post exists in the database
    Checks if the post is liked by the current user
    Removes the post from the current user's liked posts
    Returns nothing
    """
    like = db.query(Like).filter_by(user_id=current_user.id, post_id=post_id).first()
    if not like:
        raise_not_found_exception("Not liked yet")
    db.delete(like)
    db.commit()
    return

# Retweet Post Endpoint
@router.post("/{post_id}/retweet", status_code=204)
def retweet_post(
    post_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    """
    Retweet a post
    Takes the post_id of the post to retweet
    Checks if the post exists in the database
    Checks if the post is not already retweeted by the current user
    Adds the post to the current user's retweeted posts
    Returns nothing
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise_not_found_exception('Post not found')
    retweet = db.query(Retweet).filter_by(user_id=current_user.id, post_id=post_id).first()
    if retweet:
        raise_not_found_exception("Already retweeted")
    new_retweet = Retweet(user_id=current_user.id, post_id=post_id)
    db.add(new_retweet)
    db.commit()
    return

# Unretweet Post Endpoint
@router.post("/{post_id}/unretweet", status_code=204)
def unretweet_post(
    post_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user),
):
    """
    Unretweet a post
    Takes the post_id of the post to unretweet
    Checks if the post exists in the database
    Checks if the post is retweeted by the current user
    Removes the post from the current user's retweeted posts
    Returns nothing
    """
    retweet = db.query(Retweet).filter_by(user_id=current_user.id, post_id=post_id).first()
    if not retweet:
        raise_not_found_exception("Not retweeted yet")
    db.delete(retweet)
    db.commit()
    return

# Get Posts with Counts Endpoint
@router.get("/with_counts/", response_model=List[PostWithCounts])
def read_posts_with_counts(
    db: db_dependency,
    current_user: User = Depends(get_current_user)
):
    """
    Get posts with counts
    Takes the db dependency and current user
    Creates a subquery to count the number of likes for each post
    Creates a subquery to count the number of retweets for each post
    Fetches the posts along with their like/retweet counts and owner username
    Returns the posts with counts and owner username
    """
    likes_subq = (
        db.query(
            Like.post_id,
            func.count(Like.user_id).label('likes_count')
        )
        .group_by(Like.post_id)
        .subquery()
    )

    retweets_subq = (
        db.query(
            Retweet.post_id,
            func.count(Retweet.user_id).label('retweets_count')
        )
        .group_by(Retweet.post_id)
        .subquery()
    )

    posts = (
        db.query(
            Post,
            User.username.label('owner_username'),
            func.coalesce(likes_subq.c.likes_count, 0).label('likes_count'),
            func.coalesce(retweets_subq.c.retweets_count, 0).label('retweets_count')
        )
        .join(User, Post.owner_id == User.id)
        .outerjoin(likes_subq, Post.id == likes_subq.c.post_id)
        .outerjoin(retweets_subq, Post.id == retweets_subq.c.post_id)
        .order_by(Post.timestamp.desc())
        .all()
    )

    response_posts = []
    for post, owner_username, likes_count, retweets_count in posts:
        response_posts.append(PostWithCounts(
            id=post.id,
            content=post.content,
            timestamp=post.timestamp,
            owner_id=post.owner_id,  # Make sure owner_id is included
            owner_username=owner_username,
            likes_count=likes_count,
            retweets_count=retweets_count,
            is_owner=post.owner_id == current_user.id  # Add is_owner flag
        ))

    return response_posts


