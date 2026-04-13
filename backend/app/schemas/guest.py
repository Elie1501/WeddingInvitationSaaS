from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class GuestBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    plus_ones: int = 0
    dietary_restrictions: Optional[str] = None
    message: Optional[str] = None

class GuestCreate(GuestBase):
    event_id: int
    rsvp_status: Optional[str] = "pending"

class GuestRSVP(BaseModel):
    presence: bool
    plus_ones: int = 0
    dietary_restrictions: Optional[str] = None
    message: Optional[str] = None

class GuestResponse(GuestBase):
    id: int
    event_id: int
    rsvp_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class RSVPResponse(BaseModel):
    id: int
    guest_id: int
    presence: bool
    plus_ones: int
    dietary_restrictions: Optional[str]
    message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
