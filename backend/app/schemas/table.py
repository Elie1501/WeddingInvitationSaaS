from pydantic import BaseModel
from typing import List, Optional
from app.schemas.guest import GuestResponse

class TableBase(BaseModel):
    name: str
    capacity: int
    remaining_seats: Optional[int] = None

class TableCreate(TableBase):
    event_id: int

class TableUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None

class TableResponse(TableBase):
    id: int
    event_id: int
    remaining_seats: int
    # On pourra inclure la liste des invités assis à cette table
    guests: List[GuestResponse] = []

    class Config:
        from_attributes = True
