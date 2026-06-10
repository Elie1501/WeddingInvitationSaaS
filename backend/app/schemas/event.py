from pydantic import BaseModel, field_validator
from datetime import datetime, date as date_type
from typing import Optional


class EventBase(BaseModel):
    title: str
    groom_name: Optional[str] = None
    bride_name: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None


class EventCreate(EventBase):
    template_id: Optional[str] = "eclat-eternel"
    has_cover_page: Optional[bool] = True
    has_countdown: Optional[bool] = True

    @field_validator('date')
    @classmethod
    def date_not_in_past(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v.date() < date_type.today():
            raise ValueError('La date du mariage ne peut pas être dans le passé.')
        return v


class CardResponse(BaseModel):
    id: int
    slug: str
    is_published: bool

    model_config = {"from_attributes": True}


class EventResponse(EventBase):
    id: int
    owner_id: int
    card: Optional[CardResponse] = None

    model_config = {"from_attributes": True}
