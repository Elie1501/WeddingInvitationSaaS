from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Le mot de passe doit faire au moins 8 caractères.")

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    plan: str # classic, premium
    is_admin: bool
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class UserUpdatePlan(BaseModel):
    plan: str # classic, premium

class UserUpdateStatus(BaseModel):
    is_active: bool

class GoogleLoginRequest(BaseModel):
    id_token: str
    plan: str = "classic"  # plan choisi à l'inscription (nouveau compte uniquement)