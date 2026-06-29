from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..schemas.goals import GoalCreate,GoalResponse,GoalUpdate
from ..security import get_current_user
from ..models import Goal
router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)
@router.post("/", response_model=GoalResponse)
def create_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_goal = Goal(
        title=goal.title,
        description=goal.description,
        target_date=goal.target_date,
        status="active",
        progress=0,
        owner_id=current_user.id
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

@router.get("/", response_model=list[GoalResponse])
def get_goals(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    goals = db.query(Goal).filter(
        Goal.owner_id == current_user.id
    ).all()
    return goals

@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
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
    return goal
    

@router.patch("/{goal_id}", response_model=GoalResponse)
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

    if goal_data.description is not None:
        goal.description = goal_data.description

    if goal_data.target_date is not None:
        goal.target_date = goal_data.target_date

    if goal_data.status is not None:
        goal.status = goal_data.status

    if goal_data.progress is not None:
        goal.progress = goal_data.progress

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