from pydantic import BaseModel,ConfigDict
class GoalCreate(BaseModel):
    title: str
    completed: bool
class GoalResponse(BaseModel):
    id: int
    title: str
    completed: bool
    model_config = ConfigDict(from_attributes=True)