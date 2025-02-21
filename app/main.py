from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routes import auth, users, property

from contextlib import asynccontextmanager
from app.init_db import create_tables

@asynccontextmanager
async def lifespan(app : FastAPI):
    try:
        create_tables()
        yield
    finally:
        pass

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(property.router, prefix="/properties", tags=["Properties"])

@app.get("/")
async def root():
    return {"message": "Bem-Vindo a API!"}
