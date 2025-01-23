from sqlalchemy.orm import Session, joinedload
from app.models.task import Task
from app.models.user import User
from sqlalchemy import or_
from fastapi import HTTPException

def create_task(db: Session, task_data, user):
    """
    Create a new task.
    """
    # Validate assignee
    if task_data.assignee_id:
        assignee = db.query(User).filter(User.id == task_data.assignee_id).first()
        if not assignee:
            raise HTTPException(status_code=404, detail="Assignee not found")

    # Create the task
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,  # Ensure this is datetime
        owner_id=user["id"],
        assignee_id=task_data.assignee_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task



def get_tasks(db: Session, page, limit, status, priority, my_tasks, search, user):
    """
    Get tasks with optional filters and pagination.
    """
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page and limit must be greater than 0.")

    query = (
        db.query(Task)
        .filter(or_(Task.owner_id == user["id"], Task.assignee_id == user["id"]))
        if my_tasks
        else db.query(Task)
    )

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if search:
        query = query.filter(Task.title.contains(search))

    tasks = (
        query.options(joinedload(Task.owner), joinedload(Task.assignee))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    for task in tasks:
        task.owner_name = f"{task.owner.first_name} {task.owner.last_name}"
        task.assignee_name = (
            f"{task.assignee.first_name} {task.assignee.last_name}" if task.assignee else None
        )

    return tasks


def get_task_by_id(db: Session, task_id, user):
    """
    Get a task by its ID if the user is the owner or assignee.
    """
    task = db.query(Task).options(joinedload(Task.owner), joinedload(Task.assignee)).filter(
        Task.id == task_id,
        or_(Task.owner_id == user["id"], Task.assignee_id == user["id"]),
    ).first()

    if task:
        task.owner_name = f"{task.owner.first_name} {task.owner.last_name}"
        task.assignee_name = (
            f"{task.assignee.first_name} {task.assignee.last_name}" if task.assignee else None
        )

    return task


def update_task(db: Session, task_id, task_data, user):
    """
    Update a task if the user is the owner.
    """
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user["id"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data.assignee_id:
        assignee = db.query(User).filter(User.id == task_data.assignee_id).first()
        if not assignee:
            raise HTTPException(status_code=404, detail="Assignee not found")

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id, user):
    """
    Delete a task if the user is the owner.
    """
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user["id"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully", "task_id": task.id, "title": task.title}


def get_users(db: Session):
    """
    Get all users.
    """
    return [{"id": user.id, "name": f"{user.first_name} {user.last_name}"} for user in db.query(User).all()]
