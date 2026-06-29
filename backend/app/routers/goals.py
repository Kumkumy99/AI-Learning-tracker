from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..schemas import GoalCreate,GoalResponse,GoalUpdate
from ..security import get_current_user
from ..models import Goal
router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)
@router.post("/")
def create_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_goal = models.Goal(
        title=goal.title,
        completed=goal.completed,
        owner_id=current_user.id
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal
@router.get("/", response_model=list[GoalResponse])
def get_goals(db: Session = Depends(get_db)):
    goals = db.query(models.Goal).all()
    return goals
@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
@router.patch("/{goal_id}")
def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.owner_id == current_user.id
    ).first()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    if goal_data.title is not None:
        goal.title = goal_data.title

    if goal_data.completed is not None:
        goal.completed = goal_data.completed

    db.commit()
    db.refresh(goal)

    return goal
@router.delete("/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.owner_id == current_user.id
    ).first()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    db.delete(goal)
    db.commit()

    return {"message": "Goal deleted"}