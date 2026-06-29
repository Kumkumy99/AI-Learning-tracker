from pydantic import BaseModel,ConfigDict,EmailStr
from sqlalchemy import Date
from datetime import datetime,date
from typing import Optional


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
