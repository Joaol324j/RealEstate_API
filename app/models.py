from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class Furniture(Base):
    __tablename__ = "furniture"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    quantity = Column(Integer)
    description = Column(String, nullable=False)
