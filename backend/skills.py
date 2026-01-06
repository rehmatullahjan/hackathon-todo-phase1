from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, col, or_
from .models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class TodoSkills:
    """
    Reusable Intelligence Layer (Phase 4 Foundation).
    Encapsulates all business logic for the Todo application.
    """
    
    @staticmethod
    def create_task(session: Session, task_create: TaskCreate) -> Task:
        db_task = Task.from_orm(task_create)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
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
        statement = select(Task)
        if status:
            statement = statement.where(Task.status == status)
        if priority:
            statement = statement.where(Task.priority == priority)
        if category:
            statement = statement.where(Task.category == category)
        if tags:
            statement = statement.where(col(Task.tags).contains(tags))

        if sort_by:
            field = getattr(Task, sort_by, None)
            if field:
                statement = statement.order_by(col(field).desc() if sort_order == "desc" else col(field).asc())
        else:
            statement = statement.order_by(col(Task.created_at).desc())

        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()

    @staticmethod
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

    @staticmethod
    def complete_task(session: Session, task_id: str) -> Optional[Task]:
        db_task = session.get(Task, task_id)
        if not db_task:
            return None
        
        if db_task.status != TaskStatus.COMPLETED:
            db_task.status = TaskStatus.COMPLETED
            db_task.completed_at = datetime.utcnow()
            db_task.updated_at = datetime.utcnow()
            session.add(db_task)
            
            # Recurrence Logic
            if db_task.recurrence_rule:
                new_due = TodoSkills._calculate_next_due(db_task)
                if new_due:
                    new_task = Task(
                        title=db_task.title,
                        description=db_task.description,
                        status=TaskStatus.PENDING,
                        priority=db_task.priority,
                        category=db_task.category,
                        tags=db_task.tags,
                        due_date=new_due,
                        recurrence_rule=db_task.recurrence_rule
                    )
                    session.add(new_task)

            session.commit()
            session.refresh(db_task)
        return db_task

    @staticmethod
    def _calculate_next_due(db_task: Task) -> Optional[datetime]:
        try:
            base_date = db_task.due_date or datetime.utcnow()
            rule = db_task.recurrence_rule.lower()
            if "daily" in rule:
                return base_date + relativedelta(days=1)
            elif "weekly" in rule:
                return base_date + relativedelta(weeks=1)
            elif "monthly" in rule:
                return base_date + relativedelta(months=1)
        except:
            pass
        return None

    @staticmethod
    def search_tasks(session: Session, query: str) -> List[Task]:
        statement = select(Task).where(
            or_(
                col(Task.title).contains(query),
                col(Task.description).contains(query)
            )
        )
        return session.exec(statement).all()
