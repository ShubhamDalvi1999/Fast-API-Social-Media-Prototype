from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone

# Define the Follow association table before the User class
Follow = Table(
    "follows",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followee_id", Integer, ForeignKey("users.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    posts = relationship("Post", back_populates="owner")

    followers = relationship(
        "User",
        secondary=Follow, # Define the association table
        primaryjoin=id == Follow.c.followee_id, # Join condition for the primary table
        secondaryjoin=id == Follow.c.follower_id, # Join condition for the secondary table
        backref="following", # Backref to the User model
    )

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(280), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts") # Relationship to the User model
    likes = relationship("Like", back_populates="post") # Relationship to the Like model
    retweets = relationship("Retweet", back_populates="post") # Relationship to the Retweet model

class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)

    user = relationship("User") # Relationship to the User model
    post = relationship("Post", back_populates="likes") # Relationship to the Post model

class Retweet(Base):
    __tablename__ = "retweets"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User") # Relationship to the User model
    post = relationship("Post", back_populates="retweets") # Relationship to the Post model