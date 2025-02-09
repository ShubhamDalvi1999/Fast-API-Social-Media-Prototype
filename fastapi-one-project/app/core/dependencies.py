from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator
from .database import SessionLocal
from ..repositories.post_repository import PostRepository
from ..services.post_service import PostService

# Database dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Repository dependencies
def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(db)

# Service dependencies
def get_post_service(
    repo: PostRepository = Depends(get_post_repository),
) -> PostService:
    return PostService(repo) 