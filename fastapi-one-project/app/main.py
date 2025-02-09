from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import Base
from .routes import users, posts, auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Advanced Project",
    description="A complete FastAPI project with authentication, users, and posts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to FastAPI Advanced Project!",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)