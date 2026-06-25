from sqlalchemy import Column, Integer, String, Boolean
from .database import Base
from sqlalchemy import ForeignKey
class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True,index=True)
    hashed_password=Column(String,nullable=False)

