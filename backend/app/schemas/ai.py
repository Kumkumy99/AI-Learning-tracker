from pydantic import BaseModel,ConfigDict,EmailStr
 
class GenerateRoadmapRequest(BaseModel):
    skill_level: str
    daily_hours: int
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