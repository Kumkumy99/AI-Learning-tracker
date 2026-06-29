from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class GenerateRoadmapRequest(BaseModel):
    skill_level: str
    daily_hours: int
    learning_style: str