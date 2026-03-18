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
    pass

class EventResponse(EventBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
