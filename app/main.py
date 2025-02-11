from fastapi import FastAPI
from app.database import Base, engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/Hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}