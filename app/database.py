import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Directly setting the DATABASE_URL for testing purposes
DATABASE_URL = "postgresql://myuser:password@localhost:5432/realestate_postgres"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

print(f"DATABASE_URL: {DATABASE_URL}")  # Add this line to print the DATABASE_URL

try:
    engine = _sql.create_engine(DATABASE_URL)
    print("Engine created successfully")
except Exception as e:
    print(f"Error creating engine: {e}")
    raise

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()