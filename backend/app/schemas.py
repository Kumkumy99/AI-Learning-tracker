from pydantic import BaseModel,ConfigDict,EmailStr
from sqlalchemy import Date
from datetime import datetime,date
from typing import Optional
class GoalCreate(BaseModel):
    title: str
    
class GoalResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    target_date: Optional[date]
    status: str
    progress: int
    owner_id: int

    class Config:
        from_attributes = True

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[date] = None
    status: Optional[str] = None
    progress: Optional[int] = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class GenerateRoadmapRequest(BaseModel):
    skill_level: str
    daily_hours: int
    learning_style: str