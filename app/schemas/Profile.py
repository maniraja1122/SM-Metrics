from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Profile(BaseModel):
    id: Optional[int]
    sila_id: Optional[int]
    username: str
    sila_name: Optional[str]
    profile_url: Optional[str]
    created_at: Optional[datetime]
    country: Optional[str]
    category1: Optional[str]
    media_count: Optional[int]
    followers: Optional[int]
    followings: Optional[int]
    bio: Optional[str]
    profile_pic: Optional[str]
    is_business: Optional[bool]
    is_private: Optional[bool]
    is_verified: Optional[bool]
    saved_at: Optional[datetime]
    saved_posts_at: Optional[datetime]

    class Config:
        orm_mode = True



