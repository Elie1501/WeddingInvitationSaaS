from pydantic import BaseModel
from typing import List, Optional
from app.schemas.guest import GuestResponse

class TableBase(BaseModel):
    name: str
    capacity: int

class TableCreate(TableBase):
    event_id: int

class TableResponse(TableBase):
    id: int
    event_id: int
    # On pourra inclure la liste des invités assis à cette table
    guests: List[GuestResponse] = []

    class Config:
        from_attributes = True