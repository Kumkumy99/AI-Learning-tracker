from fastapi import FastAPI,Depends
from pydantic import BaseModel
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
class GoalCreate(BaseModel):
    title: str
    completed: bool
class GoalResponse(BaseModel):
    id: int
    title: str
    completed: bool
    class Config:
        from_attributes = True
@app.get("/")
def root():
    return {"message": "Welcome to AI Learning Tracker Backend"}
@app.post("/goals")
def create_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db)
):
    db_goal = models.Goal(
        title=goal.title,
        completed=goal.completed
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal
@app.get("/goals", response_model=list[GoalResponse])
def get_goals(db: Session = Depends(get_db)):
    goals = db.query(models.Goal).all()
    return goals