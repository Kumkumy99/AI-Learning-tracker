from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..schemas import GoalCreate,GoalResponse
router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)

@router.post("/")
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
@router.get("/", response_model=list[GoalResponse])
def get_goals(db: Session = Depends(get_db)):
    goals = db.query(models.Goal).all()
    return goals