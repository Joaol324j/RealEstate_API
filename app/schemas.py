from pydantic import BaseModel
from typing import Optional
from app.models import UserRole, PropertyType, ListingType

class PropertyBase(BaseModel):
    title: str
    description: str
    price: float
    location: str
    property_type: PropertyType
    listing_type: ListingType

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(PropertyBase):
    pass

class PropertyResponse(PropertyBase):
    id: int

    class Config:
        from_attributes = True

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