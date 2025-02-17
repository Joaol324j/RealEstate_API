from pydantic import BaseModel
from typing import Optional
from app.models import UserRole

class UserBase(BaseModel):
    username: str
    email: str
    telephone: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: UserRole

class UserInDB(UserBase):
    id: int
    hashed_password: str