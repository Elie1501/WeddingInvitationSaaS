from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class GuestBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    plus_ones: int = 0
    dietary_restrictions: Optional[str] = None
    message: Optional[str] = None
    parent_id: Optional[int] = None

class GuestSubCreate(BaseModel):
    first_name: str
    last_name: str
    dietary_restrictions: Optional[str] = None

class GuestCreate(GuestBase):
    event_id: int
    rsvp_status: Optional[str] = "pending"
    sub_guests: Optional[List[GuestSubCreate]] = []

class GuestUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    rsvp_status: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    message: Optional[str] = None

class GuestRSVP(BaseModel):
    presence: bool
    plus_ones: int = 0
    dietary_restrictions: Optional[str] = None
    message: Optional[str] = None
    sub_guests: Optional[List[GuestSubCreate]] = None

class GuestResponse(GuestBase):
    id: int
    event_id: int
    rsvp_status: str
    created_at: datetime
    # On peut inclure les sous-invités dans la réponse pour l'affichage groupé
    # On utilise forward reference si besoin, mais ici on va rester simple
    
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
