from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CardVersionBase(BaseModel):
    version_number: int
    content_json: str
    created_at: datetime

class CardVersionResponse(CardVersionBase):
    id: int

    class Config:
        from_attributes = True

class SubEventBase(BaseModel):
    title: str
    time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None

class SubEventCreate(SubEventBase):
    pass

class SubEventResponse(SubEventBase):
    id: int

    class Config:
        from_attributes = True

class EventLite(BaseModel):
    title: str
    groom_name: Optional[str] = None
    bride_name: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True

class CardBase(BaseModel):
    event_id: int
    template_id: Optional[str] = None
    intro_text: Optional[str] = None
    theme_color: Optional[str] = "#FFFFFF"
    has_cover_page: Optional[bool] = False
    media_url: Optional[str] = None
    music_url: Optional[str] = None

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    template_id: Optional[str] = None
    intro_text: Optional[str] = None
    theme_color: Optional[str] = None
    has_cover_page: Optional[bool] = None
    media_url: Optional[str] = None
    music_url: Optional[str] = None
    config_json: Optional[str] = None
    sub_events: Optional[List[SubEventCreate]] = None
    # Event fields
    title: Optional[str] = None
    groom_name: Optional[str] = None
    bride_name: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None

class CardResponse(CardBase):
    id: int
    slug: Optional[str] = None
    is_published: bool
    current_version: int
    config_json: Optional[str] = None
    has_cover_page: bool
    updated_at: datetime
    event: Optional[EventLite] = None
    sub_events: List[SubEventResponse] = []

    class Config:
        from_attributes = True

class TemplateResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    required_plan: str
    manifest_json: str
    thumbnail_url: Optional[str] = None

    class Config:
        from_attributes = True
