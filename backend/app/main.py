from fastapi import FastAPI,Depends,HTTPException
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import goals,users
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(goals.router)
app.include_router(users.router)
@app.get("/")
def root():
    return {"message": "Welcome to AI Learning Tracker Backend"}