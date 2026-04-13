from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import SessionLocal
from app.models.wedding import User, Base
from app.core import security
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def reset_and_seed():
    db = SessionLocal()
    
    # On ajoute l'utilisateur de test simple
    email = "test@test.com"
    password = "password123"
    
    # On supprime si existe pour être SÛR
    user = db.query(User).filter(User.email == email).first()
    if user:
        db.delete(user)
        db.commit()
        print(f"Ancien utilisateur {email} supprimé.")

    new_user = User(
        email=email,
        hashed_password=security.get_password_hash(password),
        plan="premium"
    )
    db.add(new_user)
    db.commit()
    print(f"Utilisateur créé avec SUCCÈS : {email} / {password}")
    db.close()

if __name__ == "__main__":
    reset_and_seed()
