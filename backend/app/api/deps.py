from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.config import settings
from app.models.wedding import User
from app.schemas.token import TokenPayload
from app.api.plans import get_limits

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def check_plan_permission(permission: str):
    def _check(current_user: User = Depends(get_current_user)):
        limits = get_limits(current_user.plan)
        if not limits.get(permission, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Cette fonctionnalité nécessite un forfait supérieur (votre forfait actuel : {current_user.plan})"
            )
        return True
    return _check
