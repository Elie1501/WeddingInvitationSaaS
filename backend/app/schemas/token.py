from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    is_new_user: bool = False

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    type: Optional[str] = None