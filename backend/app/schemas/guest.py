from pydantic import BaseModel, EmailStr
from typing import Optional


class GuestBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    plus_ones: int = 0
    dietary_restrictions: Optional[str] = None

class GuestCreate(GuestBase):
    event_id: int

class GuestRSVP(BaseModel):
    rsvp_status: str # "confirmed" ou "ps la"
    plus_ones: Optional[int] = 0
    dietary_restrictions: Optional[str] = None


class GuestResponse(GuestBase):
    id: int
    event_id: int
    rsvp_status: str

    class Config:
        from_attributes = True