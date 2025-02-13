from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routes import auth, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Bem-Vindo a API!"}
