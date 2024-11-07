from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    id: Optional[int]
    profile_id: int
    username: str
    user_id: Optional[str]
    post_id: str
    post_url: Optional[str]
    description: Optional[str]
    pub_date: datetime
    share_count: Optional[int]
    like_count: int
    comment_count: int
    product_type: Optional[str]
    tagged_users: Optional[str]
    mentions: Optional[str]
    hashtags: Optional[str]
    location: Optional[str]
    is_ads: Optional[bool]
    saved_at: Optional[datetime]
    sila_id: Optional[int]
    saves: Optional[int]
    from_model: Optional[bool]

    class Config:
        orm_mode = True