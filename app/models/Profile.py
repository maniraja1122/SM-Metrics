from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from db import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    sila_id = Column(Integer, index=True)
    username = Column(String(255), unique=True, nullable=False)
    sila_name = Column(String(255))
    profile_url = Column(String(255))
    created_at = Column(DateTime)
    country = Column(String(255))
    category1 = Column(String(255))
    media_count = Column(Integer)
    followers = Column(Integer)
    followings = Column(Integer)
    bio = Column(String(255))
    profile_pic = Column(String(255))
    is_business = Column(Boolean)
    is_private = Column(Boolean)
    is_verified = Column(Boolean)
    saved_at = Column(DateTime)
    saved_posts_at = Column(DateTime)

    # Relationship to posts
    posts = relationship("Post", back_populates="profile")
    # Relationship to metrics
    metrics = relationship("Metrics", back_populates="profile", uselist=False)

