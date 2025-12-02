# backend/app/schemas/users.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --------------------
# Input / request models
# --------------------
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserMeUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

# --------------------
# Output / response models
# --------------------
class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    is_superuser: bool
    roles: List[str] = []

    class Config:
        from_attributes = True  # Pydantic v2
