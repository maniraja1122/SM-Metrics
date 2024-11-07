from sqlalchemy import Column, Integer, String, DateTime,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    username = Column(String(255), nullable=False)
    user_id = Column(String(255))
    post_id = Column(String(255))
    post_url = Column(String(255))
    description = Column(String(255))
    pub_date = Column(DateTime)
    share_count = Column(Integer)
    like_count = Column(Integer)
    comment_count = Column(Integer)
    product_type = Column(String(255))
    tagged_users = Column(String(255))
    mentions = Column(String(255))
    hashtags = Column(String(255))
    location = Column(String(255))
    is_ads = Column(Boolean)
    saved_at = Column(DateTime)
    sila_id = Column(Integer)
    saves = Column(Integer)
    from_model = Column(Boolean)

    # Relationship to profile
    profile = relationship("Profile", back_populates="posts")
