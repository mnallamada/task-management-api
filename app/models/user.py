from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.models import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    # Define relationships with tasks
    owned_tasks = relationship("Task", foreign_keys="Task.owner_id", back_populates="owner")
    assigned_tasks = relationship("Task", foreign_keys="Task.assignee_id", back_populates="assignee")
