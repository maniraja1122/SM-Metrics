from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Metrics(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    active_reach = Column(Float)
    followers = Column(Float)
    country = Column(String)
    username = Column(String)
    profileUrl= Column(String)
    postCount = Column(Integer)
    emv = Column(Float)
    average_engagements = Column(Float)
    average_video_views = Column(Float)
    average_story_reach = Column(Float)
    average_story_engagements = Column(Float)
    average_story_views = Column(Float)
    average_saves = Column(Float)
    average_likes = Column(Float)
    average_comments = Column(Float)
    average_shares = Column(Float)
    calculation_date = Column(DateTime)

    # Relationship to profile
    profile = relationship("Profile", back_populates="metrics")