from pydantic import BaseModel,ConfigDict,EmailStr,Field
from enum import Enum

class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
 
class GenerateRoadmapRequest(BaseModel):
    skill_level: SkillLevel
    daily_hours: int = Field(gt=0, le=24)
    learning_style: str

class ResourceResponse(BaseModel):
    id: int
    title: str
    url: str
    resource_type: str | None = None

    class Config:
        from_attributes = True

class SubtaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    resources: list[ResourceResponse]

class RoadmapPhaseResponse(BaseModel):
    id: int
    phase_title: str
    phase_order: int
    subtasks: list[SubtaskResponse]

class FullRoadmapResponse(BaseModel):
    goal_id: int
    phases: list[RoadmapPhaseResponse]


class SubtaskUpdate(BaseModel):
    completed: bool