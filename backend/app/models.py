from sqlalchemy import Column, Integer, String, Boolean
from typing import email
from .database import Base


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True,index=True)
    hashed_password=Column(String,nullable=False)

