from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./microblog.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# sessionmaker: Creates a session factory for creating database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base: Creates a base class for defining ORM models.
Base = declarative_base()

# Dependency Injection for the database
def get_db():
    """
    Get the database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()