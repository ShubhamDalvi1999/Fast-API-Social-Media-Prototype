from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .base import BaseRepository
from ..models import Post, Like, Retweet

class PostRepository(BaseRepository[Post]):
    def __init__(self, db: Session):
        super().__init__(Post, db)

    def get_posts_with_counts(self, current_user_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
        likes_subq = (
            self.db.query(
                Like.post_id,
                func.count(Like.user_id).label('likes_count')
            )
            .group_by(Like.post_id)
            .subquery()
        )

        retweets_subq = (
            self.db.query(
                Retweet.post_id,
                func.count(Retweet.user_id).label('retweets_count')
            )
            .group_by(Retweet.post_id)
            .subquery()
        )

        return (
            self.db.query(Post)
            .outerjoin(likes_subq, Post.id == likes_subq.c.post_id)
            .outerjoin(retweets_subq, Post.id == retweets_subq.c.post_id)
            .order_by(Post.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def like_post(self, post_id: int, user_id: int) -> bool:
        if not self.db.query(Like).filter_by(post_id=post_id, user_id=user_id).first():
            like = Like(post_id=post_id, user_id=user_id)
            self.db.add(like)
            self.db.commit()
            return True
        return False

    def unlike_post(self, post_id: int, user_id: int) -> bool:
        like = self.db.query(Like).filter_by(post_id=post_id, user_id=user_id).first()
        if like:
            self.db.delete(like)
            self.db.commit()
            return True
        return False

    def retweet_post(self, post_id: int, user_id: int) -> bool:
        if not self.db.query(Retweet).filter_by(post_id=post_id, user_id=user_id).first():
            retweet = Retweet(post_id=post_id, user_id=user_id)
            self.db.add(retweet)
            self.db.commit()
            return True
        return False

    def unretweet_post(self, post_id: int, user_id: int) -> bool:
        retweet = self.db.query(Retweet).filter_by(post_id=post_id, user_id=user_id).first()
        if retweet:
            self.db.delete(retweet)
            self.db.commit()
            return True
        return False 