from app.database import Base, engine
from app import models

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")