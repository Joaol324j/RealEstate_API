from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    telephone: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

class UserInDB(UserBase):
    id: int
    hashed_password: str