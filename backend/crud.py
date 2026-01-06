from sqlmodel import Session
from typing import List, Optional
from .models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from .skills import TodoSkills

def create_task(session: Session, task_create: TaskCreate) -> Task:
    return TodoSkills.create_task(session, task_create)

def get_task(session: Session, task_id: str) -> Optional[Task]:
    return session.get(Task, task_id)

def list_tasks(
    session: Session,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tags: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
    offset: int = 0,
    limit: int = 100
) -> List[Task]:
    return TodoSkills.list_tasks(session, status, priority, tags, category, sort_by, sort_order, offset, limit)

def update_task(session: Session, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
    return TodoSkills.update_task(session, task_id, task_update)

def delete_task(session: Session, task_id: str) -> bool:
    db_task = session.get(Task, task_id)
    if not db_task:
        return False
    session.delete(db_task)
    session.commit()
    return True

def complete_task(session: Session, task_id: str) -> Optional[Task]:
    return TodoSkills.complete_task(session, task_id)

def search_tasks(session: Session, query: str) -> List[Task]:
    return TodoSkills.search_tasks(session, query)
