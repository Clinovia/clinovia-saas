# backend/app/schemas/auth.py

from pydantic import BaseModel
from app.schemas.users import UserRead

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SignUpResponse(BaseModel):
    user: UserRead
    # access_token: Optional[str] = None
    # token_type: Optional[str] = "bearer"
