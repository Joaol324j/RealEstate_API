from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class Furniture(Base):
    __tablename__ = "furniture"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    quantity = Column(Integer)
    description = Column(String, nullable=False)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
