from pydantic import BaseModel,ConfigDict,EmailStr
 
class GenerateRoadmapRequest(BaseModel):
    skill_level: str
    daily_hours: int
    learning_style: str