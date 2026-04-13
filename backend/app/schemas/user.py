from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Le mot de passe doit faire au moins 8 caractères.")
    plan: Optional[str] = "classic" # classic, premium

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    plan: str # classic, premium

    model_config = {
        "from_attributes": True
    }

class UserUpdatePlan(BaseModel):
    plan: str # classic, premium