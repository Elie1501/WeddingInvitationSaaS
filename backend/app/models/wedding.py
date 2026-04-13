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
    plan = Column(String, default="classic") # classic, premium
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

class CardTemplate(Base):
    __tablename__ = "card_templates"
    id = Column(String, primary_key=True, index=True) # e.g., 'modern-chic'
    name = Column(String, nullable=False)
    description = Column(Text)
    required_plan = Column(String, default="classic") # classic, premium
    manifest_json = Column(Text, nullable=False) # Configuration par défaut et options
    thumbnail_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), unique=True)
    template_id = Column(String, ForeignKey("card_templates.id"), nullable=True)
    slug = Column(String, unique=True, index=True) # URL publique
    intro_text = Column(Text)
    theme_color = Column(String, default="#FFFFFF")
    is_published = Column(Boolean, default=False)
    current_version = Column(Integer, default=1)
    config_json = Column(Text, nullable=True) # Configuration dynamique (couleurs, typos, layout)
    has_cover_page = Column(Boolean, default=False)
    media_url = Column(String, nullable=True) # Image de fond/couverture
    music_url = Column(String, nullable=True) # Musique de fond
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    event = relationship("Event", back_populates="card")
    template = relationship("CardTemplate")
    versions = relationship("CardVersion", back_populates="card", cascade="all, delete-orphan")
    sub_events = relationship("SubEvent", back_populates="card", cascade="all, delete-orphan")

class SubEvent(Base):
    __tablename__ = "sub_events"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    title = Column(String, nullable=False) # Ex: Cérémonie Civile
    time = Column(String) # Ex: 14:30
    location = Column(String) # Ex: Mairie de Lyon
    description = Column(Text, nullable=True)

    card = relationship("Card", back_populates="sub_events")

class CardVersion(Base):
    __tablename__ = "card_versions"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    version_number = Column(Integer)
    content_json = Column(Text) # Stockage JSON du contenu à cette version
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    card = relationship("Card", back_populates="versions")

class Guest(Base):
    __tablename__ = "guests"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    rsvp_status = Column(String, default="pending") # pending, confirmed, declined
    plus_ones = Column(Integer, default=0)
    dietary_restrictions = Column(Text)
    message = Column(Text, nullable=True) # Message personnel de l'invité
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    event = relationship("Event", back_populates="guests")
    assigned_tables = relationship("WeddingTable", secondary=guest_table_association, back_populates="guests")
    rsvps = relationship("RSVP", back_populates="guest", cascade="all, delete-orphan")

class RSVP(Base):
    __tablename__ = "rsvps"
    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey("guests.id"))
    presence = Column(Boolean, default=True) # Présent ou non
    plus_ones = Column(Integer, default=0)
    dietary_restrictions = Column(Text, nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    guest = relationship("Guest", back_populates="rsvps")

class WeddingTable(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    name = Column(String, nullable=False) # [cite: 95]
    capacity = Column(Integer, nullable=False) # [cite: 96]

    event = relationship("Event", back_populates="tables")
    guests = relationship("Guest", secondary=guest_table_association, back_populates="assigned_tables")