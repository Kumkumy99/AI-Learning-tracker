from pydantic import BaseModel
class GoalCreate(BaseModel):
    title: str
    completed: bool
class GoalResponse(BaseModel):
    id: int
    title: str
    completed: bool
    class Config:
        from_attributes = True