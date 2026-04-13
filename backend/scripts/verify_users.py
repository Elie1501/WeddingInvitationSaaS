from app.db.session import SessionLocal
from app.models.wedding import User
from app.core import security

def verify():
    db = SessionLocal()
    users = db.query(User).all()
    print(f"Nombre d'utilisateurs en base : {len(users)}")
    for user in users:
        is_ok = security.verify_password("password123", user.hashed_password)
        print(f"Email: {user.email}, Plan: {user.plan}, Password OK: {is_ok}")
    db.close()

if __name__ == "__main__":
    verify()
