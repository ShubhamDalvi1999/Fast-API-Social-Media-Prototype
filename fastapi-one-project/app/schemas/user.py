from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# User Schemas
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
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)