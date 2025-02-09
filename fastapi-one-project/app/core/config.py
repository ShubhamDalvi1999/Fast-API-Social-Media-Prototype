from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Social Network"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key"  # In production, use environment variable
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./app.db"
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings() 