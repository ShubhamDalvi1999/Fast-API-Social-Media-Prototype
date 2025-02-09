from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# USER SCHEMAS
# User is used to represent a user in the microblog.
# It contains an id, username, email, and created_at.
#                 BaseModel
#                     |
#            UserBase : BaseModel
#             |                  |
#      UserCreate : UserBase   User : UserBase     
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    # allows the model to be initialized using objects 
    # (or ORM-like attributes) instead of just plain dictionaries.
    class Config:
        from_attributes = True

# TOKEN SCHEMAS
# Token is used to authenticate users and access protected routes.
# It contains an access token and a token type.
#                     BaseModel
#                 |                  |
#      Token : BaseModel     TokenData : BaseModel       
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# POST SCHEMAS 
# Post is used to represent a post in the microblog.
# It contains an id, timestamp, content, and owner_id.
#                                  BaseModel
#                       |                                 |
#            PostBase : BaseModel                PostUpdate : BaseModel
#             |                |
#      Post : PostBase        PostCreate : PostBase
#              |
#      PostWithCounts : Post
class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    timestamp: datetime
    owner_id: int
    owner_username: str

    class Config:
        from_attributes = True

class PostWithCounts(Post):
    likes_count: int = 0
    retweets_count: int = 0
    is_owner: bool = False

    class Config:
        from_attributes = True

class PostUpdate(PostBase):
    pass

# LIKE SCHEMAS
# Like is used to represent a like in the microblog.
# It contains an id, timestamp, and owner_id.
class Like(BaseModel):
    user_id: int
    post_id: int

    class Config:
        from_attributes = True

# RETWEET SCHEMAS
# Retweet is used to represent a retweet in the microblog.
# It contains an id, timestamp, and owner_id.
class Retweet(BaseModel):
    user_id: int
    post_id: int
    timestamp: datetime

    class Config:
        from_attributes = True