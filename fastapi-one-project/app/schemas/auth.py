from pydantic import BaseModel
from typing import Optional

# Token Schemas
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