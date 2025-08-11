from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    # refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str