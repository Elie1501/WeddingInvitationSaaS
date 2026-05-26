import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)

    # Seed le template par défaut utilisé par create_event ("eclat-eternel")
    # Sans lui, PostgreSQL lève une FK violation (card_templates.id)
    from app.models.wedding import CardTemplate
    db = TestingSessionLocal()
    if not db.query(CardTemplate).filter_by(id="eclat-eternel").first():
        db.add(CardTemplate(
            id="eclat-eternel",
            name="Éclat Éternel",
            manifest_json='{"default_config": {}}',
            is_active=True
        ))
        db.commit()
    db.close()

    yield
    Base.metadata.drop_all(bind=engine)
