from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.wedding import User, Base
from app.core import security
from app.core.config import settings

# On utilise l'URL des settings (qui pointe vers 'db' dans docker)
db_url = settings.DATABASE_URL

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_users():
    db = SessionLocal()
    # Création des tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    users_to_create = [
        {"email": "marie@classic.com", "password": "password123", "plan": "classic", "is_admin": False},
        {"email": "thomas@premium.com", "password": "password123", "plan": "premium", "is_admin": False},
        {"email": "admin@wedding.com", "password": "password123", "plan": "premium", "is_admin": True},
    ]
    for user_data in users_to_create:
        # Vérifier si l'utilisateur existe déjà
        user = db.query(User).filter(User.email == user_data["email"]).first()
        if not user:
            new_user = User(
                email=user_data["email"],
                hashed_password=security.get_password_hash(user_data["password"]),
                plan=user_data["plan"],
                is_admin=user_data["is_admin"]
            )
            db.add(new_user)
            print(f"Utilisateur créé : {user_data['email']} (Plan: {user_data['plan']}, Admin: {user_data['is_admin']})")
        else:
            # S'il existe, on s'assure que le statut admin est correct
            user.is_admin = user_data["is_admin"]
            db.add(user)
            print(f"L'utilisateur {user_data['email']} a été mis à jour (Admin: {user_data['is_admin']}).")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_users()
