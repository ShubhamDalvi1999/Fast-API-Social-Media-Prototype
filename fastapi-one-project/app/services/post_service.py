from typing import List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from ..repositories.post_repository import PostRepository
from ..models import Post
from ..schemas import PostCreate, PostUpdate

class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def get_post(self, post_id: int) -> Optional[Post]:
        post = self.repository.get(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return post

    def get_posts_with_counts(self, current_user_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
        return self.repository.get_posts_with_counts(current_user_id, skip, limit)

    def create_post(self, user_id: int, post_create: PostCreate) -> Post:
        return self.repository.create(
            content=post_create.content,
            owner_id=user_id
        )

    def update_post(self, post_id: int, user_id: int, post_update: PostUpdate) -> Post:
        post = self.get_post(post_id)
        
        if post.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to edit this post"
            )

        # Check if the post is within the 10-minute edit window
        post_timestamp_aware = post.timestamp.replace(tzinfo=timezone.utc)
        time_since_creation = datetime.now(timezone.utc) - post_timestamp_aware
        if time_since_creation > timedelta(minutes=10):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit a post within 10 minutes of its creation"
            )

        return self.repository.update(post_id, content=post_update.content)

    def delete_post(self, post_id: int, user_id: int) -> bool:
        post = self.get_post(post_id)
        
        if post.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post"
            )

        return self.repository.delete(post_id)

    def like_post(self, post_id: int, user_id: int) -> bool:
        post = self.get_post(post_id)
        return self.repository.like_post(post_id, user_id)

    def unlike_post(self, post_id: int, user_id: int) -> bool:
        post = self.get_post(post_id)
        return self.repository.unlike_post(post_id, user_id)

    def retweet_post(self, post_id: int, user_id: int) -> bool:
        post = self.get_post(post_id)
        return self.repository.retweet_post(post_id, user_id)

    def unretweet_post(self, post_id: int, user_id: int) -> bool:
        post = self.get_post(post_id)
        return self.repository.unretweet_post(post_id, user_id) 