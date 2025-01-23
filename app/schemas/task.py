from pydantic import BaseModel, constr, validator
from datetime import datetime, timezone
from typing import Optional
from enum import Enum


class StatusEnum(str, Enum):
    TO_DO = "To-Do"
    IN_PROGRESS = "In-Progress"
    COMPLETED = "Completed"


class PriorityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskBase(BaseModel):
    title: constr(max_length=255)  # Limit the title length
    description: Optional[constr(max_length=1000)] = None  # Optional long description
    status: StatusEnum = StatusEnum.TO_DO  # Restrict to allowed values
    priority: PriorityEnum = PriorityEnum.MEDIUM  # Restrict to allowed values
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None  # Optional assignment


class TaskCreate(TaskBase):
    @validator("due_date", pre=True, always=True)
    def validate_due_date(cls, value):
        """
        Validate that due_date is not in the past during task creation.
        """
        if value:
            if isinstance(value, str):
                value = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            if value < datetime.now(tz=timezone.utc):
                raise ValueError("Due date cannot be in the past.")
        return value


class TaskUpdate(TaskBase):
    """
    Allow updating tasks without due_date validation to enable modifications.
    """
    pass


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    owner_id: int
    owner_name: Optional[str] = None  # Include owner name
    assignee_name: Optional[str] = None  # Include assignee name

    class Config:
        orm_mode = True
