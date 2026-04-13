from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.wedding import User, Base
from app.core import security
from app.core.config import settings
import os

# On utilise l'URL des settings (qui pointe vers 'db' dans docker)
db_url = settings.DATABASE_URL

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_users():
    db = SessionLocal()
    # Création des tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    users_to_create = [
        {"email": "marie@classic.com", "password": "password123", "plan": "classic"},
        {"email": "thomas@premium.com", "password": "password123", "plan": "premium"},
        {"email": "admin@wedding.com", "password": "password123", "plan": "premium"},
    ]
    for user_data in users_to_create:
        # Vérifier si l'utilisateur existe déjà
        user = db.query(User).filter(User.email == user_data["email"]).first()
        if not user:
            new_user = User(
                email=user_data["email"],
                hashed_password=security.get_password_hash(user_data["password"]),
                plan=user_data["plan"]
            )
            db.add(new_user)
            print(f"Utilisateur créé : {user_data['email']} (Plan: {user_data['plan']})")
        else:
            print(f"L'utilisateur {user_data['email']} existe déjà.")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_users()
