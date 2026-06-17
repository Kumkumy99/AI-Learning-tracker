from pydantic import BaseModel,ConfigDict,EmailStr
class GoalCreate(BaseModel):
    title: str
    completed: bool

class GoalResponse(BaseModel):
    id: int
    title: str
    completed: bool
    model_config = ConfigDict(from_attributes=True)

class GoalUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

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