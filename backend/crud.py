from sqlmodel import Session, select, col, or_
from typing import List, Optional
from .models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from datetime import datetime

def create_task(session: Session, task_create: TaskCreate) -> Task:
    db_task = Task.from_orm(task_create)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_task(session: Session, task_id: str) -> Optional[Task]:
    return session.get(Task, task_id)

def list_tasks(
    session: Session,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tags: Optional[str] = None, # Simple substring match for now or specific logic if JSON
    category: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    offset: int = 0,
    limit: int = 100
) -> List[Task]:
    statement = select(Task)
    
    # Filtering
    if status:
        statement = statement.where(Task.status == status)
    if priority:
        statement = statement.where(Task.priority == priority)
    if category:
        statement = statement.where(Task.category == category)
    if tags:
        # Minimal tag filtering: check if tag string is contained in the JSON string
        # Robust JSON querying depends on DB (pg vs sqlite). 
        # For Phase 2 simple implementation, we assume basic string containment if sqlite.
        statement = statement.where(col(Task.tags).contains(tags))

    # Sorting
    if sort_by:
        field = getattr(Task, sort_by, None)
        if field:
            if sort_order == "desc":
                statement = statement.order_by(col(field).desc())
            else:
                statement = statement.order_by(col(field).asc())
    else:
        # Default sort by created_at desc
        statement = statement.order_by(col(Task.created_at).desc())

    statement = statement.offset(offset).limit(limit)
    return session.exec(statement).all()

def update_task(session: Session, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
    db_task = session.get(Task, task_id)
    if not db_task:
        return None
    
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: str) -> bool:
    db_task = session.get(Task, task_id)
    if not db_task:
        return False
    session.delete(db_task)
    session.commit()
    return True

def complete_task(session: Session, task_id: str) -> Optional[Task]:
    db_task = session.get(Task, task_id)
    if not db_task:
        return None
    
    if db_task.status != TaskStatus.COMPLETED:
        db_task.status = TaskStatus.COMPLETED
        db_task.completed_at = datetime.utcnow()
        db_task.updated_at = datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    return db_task

def search_tasks(session: Session, query: str) -> List[Task]:
    # Search in title and description
    statement = select(Task).where(
        or_(
            col(Task.title).contains(query),
            col(Task.description).contains(query)
        )
    )
    return session.exec(statement).all()
