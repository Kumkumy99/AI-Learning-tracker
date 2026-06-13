from fastapi import FastAPI
from pydantic import BaseModel
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
