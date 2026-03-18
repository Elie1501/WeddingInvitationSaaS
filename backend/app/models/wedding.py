from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table, Text
from sqlalchemy.orm import relationship
from app.db.session import Base
import datetime

#table placement
guest_table_association = Table(
    "guest_table",
    Base.metadata,
    Column("guest_id", ForeignKey("guests.id"), primary_key=True),
    Column("table_id", ForeignKey("tables.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    events = relationship("Event", back_populates="owner")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    groom_name = Column(String) # [cite: 46]
    bride_name = Column(String) # [cite: 46]
    date = Column(DateTime)      # [cite: 47]
    location = Column(String)   # [cite: 49]
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="events")
    card = relationship("Card", back_populates="event", uselist=False)
    guests = relationship("Guest", back_populates="event")
    tables = relationship("WeddingTable", back_populates="event")

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), unique=True)
    slug = Column(String, unique=True, index=True) # URL publique [cite: 58]
    intro_text = Column(Text)                      # [cite: 62]
    theme_color = Column(String, default="#FFFFFF") # [cite: 63]
    is_published = Column(Boolean, default=False)  # [cite: 66]

    event = relationship("Event", back_populates="card")

class Guest(Base):
    __tablename__ = "guests"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    rsvp_status = Column(String, default="pending") # pending, confirmed, declined [cite: 78]
    plus_ones = Column(Integer, default=0)          # [cite: 79]
    dietary_restrictions = Column(Text)             # [cite: 87]

    event = relationship("Event", back_populates="guests")
    assigned_tables = relationship("WeddingTable", secondary=guest_table_association, back_populates="guests")

class WeddingTable(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    name = Column(String, nullable=False) # [cite: 95]
    capacity = Column(Integer, nullable=False) # [cite: 96]

    event = relationship("Event", back_populates="tables")
    guests = relationship("Guest", secondary=guest_table_association, back_populates="assigned_tables")