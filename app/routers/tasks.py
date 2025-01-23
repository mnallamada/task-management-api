from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.user import UserResponse
from app.services.task_service import (
    create_task,
    get_tasks,
    update_task,
    delete_task,
    get_task_by_id,
    get_users,
)
from app.utils.dependencies import get_current_user
from app.utils.db import get_session_local
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=TaskResponse)
def create(
    task: TaskCreate,
    db: Session = Depends(get_session_local),
    current_user: dict = Depends(get_current_user),
):
    """Create a new task."""
    return create_task(db, task, current_user)


@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    page: int = 1,
    limit: int = 10,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    my_tasks: bool = False,
    search: Optional[str] = None,
    db: Session = Depends(get_session_local),
    current_user: dict = Depends(get_current_user),
):
    """List tasks with filters, pagination, and search."""
    return get_tasks(db, page, limit, status, priority, my_tasks, search, current_user)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_session_local),
    current_user: dict = Depends(get_current_user),
):
    """Get a specific task."""
    task = get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_session_local),
    current_user: dict = Depends(get_current_user),
):
    """Update an existing task."""
    return update_task(db, task_id, task, current_user)


@router.delete("/{task_id}")
def delete(
    task_id: int,
    db: Session = Depends(get_session_local),
    current_user: dict = Depends(get_current_user),
):
    """Delete a task."""
    delete_task(db, task_id, current_user)
    return {"message": "Task deleted successfully"}


@router.get("/users", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_session_local),
    current_user: dict = Depends(get_current_user),
):
    """List all users for task assignment."""
    return get_users(db)
