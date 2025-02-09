from pydantic import BaseModel
from datetime import datetime
from pydantic import ConfigDict

# Post Schemas 
# Post is used to represent a post in the microblog.
# It contains an id, timestamp, content, and owner_id.
#                                  BaseModel
#                       |                                 |
#            PostBase : BaseModel                PostUpdate : BaseModel
#             |                |
#      Post : PostBase        PostCreate : PostBase
#              |
#      PostWithCounts : Post

# Like Schemas
# Like is used to represent a like in the microblog.
# It contains a user_id and post_id.
#                 BaseModel
#                    |
#             Like : BaseModel

# Retweet Schemas
# Retweet is used to represent a retweet in the microblog.
# It contains a user_id, post_id, and timestamp.
#                 BaseModel
#                    |
#          Retweet : BaseModel

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    timestamp: datetime
    owner_id: int
    owner_username: str

    model_config = ConfigDict(from_attributes=True)

class PostWithCounts(Post):
    likes_count: int = 0
    retweets_count: int = 0
    is_owner: bool = False

    model_config = ConfigDict(from_attributes=True)

class PostUpdate(PostBase):
    pass

class Like(BaseModel):
    user_id: int
    post_id: int

    class Config:
        from_attributes = True

class Retweet(BaseModel):
    user_id: int
    post_id: int
    timestamp: datetime

    class Config:
        from_attributes = True 