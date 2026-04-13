from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    groom_name: Optional[str] = None
    bride_name: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None

class EventCreate(EventBase):
    template_id: Optional[str] = "modern-chic"
    has_cover_page: Optional[bool] = True
    has_countdown: Optional[bool] = True

class CardResponse(BaseModel):
    id: int
    slug: str
    is_published: bool

    model_config = {
        "from_attributes": True
    }

class EventResponse(EventBase):
    id: int
    owner_id: int
    card: Optional[CardResponse] = None

    model_config = {
        "from_attributes": True
    }
