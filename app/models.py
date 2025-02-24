from app.database import Base
from sqlalchemy import Column, Integer, Float, String, Enum, ForeignKey, DateTime
from datetime import datetime, timedelta
import enum

class PropertyType(str, enum.Enum):
    house = "house"
    apartment = "apartment"

class ListingType(str, enum.Enum):
    rent = "rent"
    sale = "sale"
    both = "both"

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    property_type = Column(Enum(PropertyType), nullable=False)
    listing_type = Column(Enum(ListingType), nullable=False)

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)

class PasswordResetToken(Base):

    __tablename__ = "reset_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(hours=1))
