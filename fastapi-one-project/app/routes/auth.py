from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated

from ..database import get_db
from .. import models, schemas
from ..auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..exceptions import raise_unauthorized_exception

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

db_dependency = Annotated[Session, Depends(get_db)]

# Login Endpoint
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint to get access token
    """
    try:
        # Check if the user exists in the database
        user = db.query(models.User).filter(models.User.username == form_data.username).first()
        if not user:
            raise_unauthorized_exception("Incorrect username or password")

        # Verify the password
        if not verify_password(form_data.password, user.hashed_password):
            raise_unauthorized_exception("Incorrect username or password")
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )