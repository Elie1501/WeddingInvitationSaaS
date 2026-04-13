from sqlalchemy import create_engine
from app.db.session import engine, Base
from app.models.wedding import * # Ensure all models are loaded

def reset_db_schema():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database schema reset successfully!")

if __name__ == "__main__":
    reset_db_schema()
