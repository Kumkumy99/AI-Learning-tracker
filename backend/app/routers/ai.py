from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Goal, Roadmap, Subtask, Resource
from app.schemas.ai import GenerateRoadmapRequest
from app.security import get_current_user
from app.services.ai_service import generate_roadmap
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

    phases = db.query(Roadmap).filter(
        Roadmap.goal_id == goal_id
    ).order_by(Roadmap.phase_order).all()

    result = {
        "goal_id": goal_id,
        "phases": []
    }

    for phase in phases:
        phase_data = {
            "id": phase.id,
            "phase_title": phase.phase_title,
            "phase_order": phase.phase_order,
            "subtasks": []
        }

        subtasks = db.query(Subtask).filter(
            Subtask.roadmap_id == phase.id
        ).all()

        for subtask in subtasks:
            resources = db.query(Resource).filter(
                Resource.subtask_id == subtask.id
            ).all()

            resource_list = []

            for resource in resources:
                resource_list.append({
                    "id": resource.id,
                    "title": resource.title,
                    "url": resource.url,
                    "resource_type": resource.resource_type
                })

            subtask_data = {
                "id": subtask.id,
                "title": subtask.title,
                "completed": subtask.completed,
                "resources": resource_list
            }

            phase_data["subtasks"].append(subtask_data)

        result["phases"].append(phase_data)

    return result