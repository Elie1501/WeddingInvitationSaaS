from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.models.wedding import User
from app.schemas.user import UserCreate, UserResponse
from app.core import security
import os

# Use a temporary sqlite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_signup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    user_in = UserCreate(email="test@example.com", password="password123")
    
    # Check if user already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        print("User already exists")
        return

    # Create new user
    new_user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"User created: {new_user.email}, plan: {new_user.plan}")
    
    # Try to validate with UserResponse
    try:
        response = UserResponse.from_orm(new_user)
        print(f"UserResponse valid: {response}")
    except Exception as e:
        print(f"UserResponse invalid: {e}")
    
    db.close()
    if os.path.exists("./test.db"):
        os.remove("./test.db")

if __name__ == "__main__":
    test_signup()
