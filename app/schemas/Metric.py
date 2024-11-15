from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Metrics(BaseModel):
    id: Optional[int]
    profile_id: int
    active_reach: Optional[float]
    followers: Optional[float]
    country: Optional[str]
    username: Optional[str]
    profileUrl: Optional[str]
    postCount: Optional[int]
    emv: Optional[float]
    average_engagements: Optional[float]
    average_video_views: Optional[float]
    average_story_reach: Optional[float]
    average_story_engagements: Optional[float]
    average_story_views: Optional[float]
    average_saves: Optional[float]
    average_likes: Optional[float]
    average_comments: Optional[float]
    average_shares: Optional[float]
    calculation_date: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes=True