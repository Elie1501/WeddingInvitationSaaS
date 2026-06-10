from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


class GuestSubCreate(BaseModel):
    first_name: str
    last_name: str
    dietary_restrictions: Optional[str] = None

    @field_validator('first_name', 'last_name')
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Ce champ est requis')
        return v.strip()


class GuestBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    plus_ones: int = 0
    dietary_restrictions: Optional[str] = None
    message: Optional[str] = None
    parent_id: Optional[int] = None


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


class PublicRSVPCreate(BaseModel):
    event_id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    presence: bool
    sub_guests: List[GuestSubCreate] = []
    dietary_restrictions: Optional[str] = None
    message: Optional[str] = None

    @field_validator('first_name', 'last_name')
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Ce champ est requis')
        return v.strip()

    @field_validator('sub_guests')
    @classmethod
    def max_guests(cls, v: list) -> list:
        if len(v) > 29:
            raise ValueError('Maximum 30 personnes par groupe (1 principal + 29 accompagnants)')
        return v


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
