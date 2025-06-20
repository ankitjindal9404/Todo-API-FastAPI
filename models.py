from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class TodoModel(Base): #table model named TodoModel
    __tablename__ = 'todos' #actual table in DB named todos
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(500), index=True, nullable=True)
    completed = Column(Boolean, default=False)