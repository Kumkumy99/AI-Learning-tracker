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
@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal   
@router.patch("/{goal_id}", response_model=schemas.GoalResponse)
def update_goal(
    goal_id: int,
    update: schemas.GoalUpdate,
    db: Session = Depends(get_db)
):
    goal = db.query(models.Goal).filter(
    models.Goal.id == goal_id
).first()
    if goal is None:
        raise HTTPException(
        status_code=404,
        detail="Goal not found"
    )
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)
    db.commit()
    db.refresh(goal)
    return goal
@router.delete("/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db)
):
    goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id
    ).first()
    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )
    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted successfully"}