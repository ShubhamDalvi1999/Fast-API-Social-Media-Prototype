"""
Pydantic schemas for data validation and serialization.

This package contains all the Pydantic models used for:
- Request/Response validation
- Data serialization/deserialization
- OpenAPI schema generation

The schemas are organized by domain:
- user.py: User-related schemas
- auth.py: Authentication-related schemas
- post.py: Post, Like, and Retweet schemas
"""

from .user import UserBase, UserCreate, User
from .auth import Token, TokenData
from .post import (
    PostBase,
    PostCreate,
    Post,
    PostWithCounts,
    PostUpdate,
    Like,
    Retweet,
)

__all__ = [
    "UserBase",
    "UserCreate",
    "User",
    "Token",
    "TokenData",
    "PostBase",
    "PostCreate",
    "Post",
    "PostWithCounts",
    "PostUpdate",
    "Like",
    "Retweet",
] 