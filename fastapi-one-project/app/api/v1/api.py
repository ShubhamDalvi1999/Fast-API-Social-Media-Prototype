from fastapi import APIRouter
from .endpoints import posts, auth

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(posts.router, prefix="/posts", tags=["Posts"]) 