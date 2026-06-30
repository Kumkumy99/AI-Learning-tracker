from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Goal, Roadmap, Subtask, Resource
from app.schemas.ai import GenerateRoadmapRequest,SubtaskUpdate
from app.security import get_current_user
from app.services.ai_service import generate_roadmap
from sqlalchemy.orm import relationship
from app.schemas.ai import FullRoadmapResponse

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/goals/{goal_id}/generate-roadmap")
def create_ai_roadmap(
    goal_id: int,
    ai_input: GenerateRoadmapRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
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
    roadmap_data = generate_roadmap(goal, ai_input)
    try:
        for phase_index, phase in enumerate(
            roadmap_data["phases"],
            start=1
        ):
            new_phase = Roadmap(
                goal_id=goal.id,
                phase_title=phase["phase_title"],
                phase_order=phase_index
            )

            db.add(new_phase)
            db.flush()

            for subtask in phase["subtasks"]:
                new_subtask = Subtask(
                    roadmap_id=new_phase.id,
                    title=subtask["title"],
                    completed=False
                )

                db.add(new_subtask)
                db.flush()

                for resource in subtask["resources"]:
                    new_resource = Resource(
                        subtask_id=new_subtask.id,
                        title=resource["title"],
                        url=resource["url"],
                        resource_type=resource["resource_type"]
                    )

                    db.add(new_resource)

        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save roadmap"
        )

    return roadmap_data


@router.get(
    "/goals/{goal_id}/roadmap",
    response_model=FullRoadmapResponse
)
def get_roadmap(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
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

    phases_data = []

    for phase in goal.roadmaps:
        subtasks_data = []

        for subtask in phase.subtasks:
            resources_data = []

            for resource in subtask.resources:
                resources_data.append({
                    "id": resource.id,
                    "title": resource.title,
                    "url": resource.url,
                    "resource_type": resource.resource_type
                })

            subtasks_data.append({
                "id": subtask.id,
                "title": subtask.title,
                "completed": subtask.completed,
                "resources": resources_data
            })

        phases_data.append({
            "id": phase.id,
            "phase_title": phase.phase_title,
            "phase_order": phase.phase_order,
            "subtasks": subtasks_data
        })

    return {
        "goal_id": goal.id,
        "phases": phases_data
    }


@router.patch("/subtasks/{subtask_id}")
def update_subtask(
    subtask_id: int,
    subtask_data: SubtaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    subtask = db.query(Subtask).filter(
        Subtask.id == subtask_id
    ).first()

    if subtask is None:
        raise HTTPException(
            status_code=404,
            detail="Subtask not found"
        )

    goal = subtask.roadmap.goal

    if goal.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    subtask.completed = subtask_data.completed

    all_subtasks = []

    for phase in goal.roadmaps:
        all_subtasks.extend(phase.subtasks)

    total_subtasks = len(all_subtasks)

    completed_subtasks = sum(
        1 for task in all_subtasks if task.completed
    )

    if total_subtasks == 0:
        progress = 0
    else:
        progress = int(
            (completed_subtasks / total_subtasks) * 100
        )

    goal.progress = progress

    db.commit()

    return {
        "message": "Subtask updated",
        "goal_progress": progress
    }

