from fastapi import FastAPI
from pydantic import BaseModel
from .database import engine
from . import models
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
goals = []
class GoalCreate(BaseModel):
    title: str
    completed: bool
@app.get("/")
def root():
    return {"message": "Welcome to AI Learning Tracker Backend"}
@app.post("/goals")
def create_goal(goal: GoalCreate):
    goals.append(goal.dict())
    print(goals)
    return goal
