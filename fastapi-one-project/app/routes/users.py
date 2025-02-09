from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from .. import models, schemas, auth
from ..database import get_db
from ..exceptions import (
    raise_not_found_exception,
    raise_bad_request_exception,
    raise_conflict_exception,
)

# Define the APIRouter for the users routes
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Dependency Injection for the database
db_dependency = Annotated[Session, Depends(get_db)]

# User Registration Endpoint
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: db_dependency):
    """
    Create a user
    Takes the user data from the request body
    Checks if the username is already registered
    Hashes the password
    Creates a new user in the database
    Returns the new user
    """
    # Check if username exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise_conflict_exception("Username already registered")
    
    # Check if email exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise_conflict_exception("Email already registered")

    # Create new user
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user"
        ) from e

# Follow User Endpoint
@router.post("/{user_id}/follow", status_code=204)
def follow_user(
    user_id: int,
    db: db_dependency,
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Follow a user
    Takes the user_id of the user to follow
    Checks if the user exists in the database
    Checks if the user is not the current user
    Checks if the user is not already following the current user
    Adds the user to the current user's following list
    Commits the changes to the database
    Returns nothing
    """
    user_to_follow = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_follow:
        raise_not_found_exception("User not found")
    if user_to_follow == current_user:
        raise_bad_request_exception("Cannot follow yourself")
    if user_to_follow in current_user.following:
        raise_bad_request_exception("Already following this user")
    current_user.following.append(user_to_follow)
    db.commit()
    return

# Unfollow User Endpoint
@router.post("/{user_id}/unfollow", status_code=204)
def unfollow_user(
    user_id: int,
    db: db_dependency,
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Unfollow a user
    Takes the user_id of the user to unfollow
    Checks if the user exists in the database
    Checks if the user is not the current user
    Checks if the user is following the current user
    Removes the user from the current user's following list
    Commits the changes to the database
    Returns nothing
    """
    user_to_unfollow = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_unfollow:
        raise_not_found_exception("User not found")
    if user_to_unfollow == current_user:
        raise_bad_request_exception("Cannot unfollow yourself")
    if user_to_unfollow not in current_user.following:
        raise_bad_request_exception("Not following this user")
    current_user.following.remove(user_to_unfollow)
    db.commit()
    return