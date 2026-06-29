from sqlalchemy import Column, Integer, String, Boolean,ForeignKey,Date,DateTime
from .database import Base
from datetime import datetime

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    target_date = Column(Date, nullable=True)
    status = Column(String, default="active")
    progress = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    
class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True,index=True)
    hashed_password=Column(String,nullable=False)
    role = Column(String, default="user")

class Roadmap(Base):
    __tablename__ = "roadmaps"
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    phase_title = Column(String, nullable=False)
    phase_order = Column(Integer, nullable=False)

class Subtask(Base):
    __tablename__ = "subtasks"
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    subtask_id = Column(Integer, ForeignKey("subtasks.id"), nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    resource_type = Column(String, nullable=True)