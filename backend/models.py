from typing import Optional, List
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
import uuid

# Models need to match domain.yaml spec

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PAUSED = "paused"
    ON_HOLD = "on_hold"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=500, index=True)
    description: Optional[str] = Field(default=None, max_length=5000)
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    
    # Phase 2 Fields
    priority: Optional[TaskPriority] = Field(default=TaskPriority.MEDIUM)
    category: Optional[str] = Field(default=None, index=True)
    # Tags are stored as simple comma-separated string for simplicity in SQLite/Simple SQLModel, 
    # or we could use specific relationship tables. For hackathon speed, string or JSON is often accepted,
    # but let's try to be clean. Actually, specification says "tags: type: array". 
    # SQLModel doesn't support List[str] natively in SQLite without JSON type. 
    # We'll stick to JSON column if possible or just a separate table? 
    # To keep it simple and perfectly "single table" aligned unless spec demands relational:
    # "tags" is an array. We'll simulate it with a JSON string or a relationship. 
    # Let's use a simple JSON field if utilizing Postgres, but for SQLite compatibility without complex setup, 
    # we might define it as a string separated by commas in Python logic, or valid JSON string.
    # Let's use JSON type from python standard lib serialization in Pydantic.
    tags: Optional[str] = Field(default="[]", description="JSON list of tags") 

    due_date: Optional[datetime] = Field(default=None)
    start_date: Optional[datetime] = Field(default=None)
    
    # Phase 3 Fields
    recurrence_rule: Optional[str] = Field(default=None, description="Natural language recurrence rule e.g. 'daily'")
    reminder_at: Optional[datetime] = Field(default=None)
    ai_summary: Optional[str] = Field(default=None, description="AI-generated summary")

class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    reminder_at: Optional[datetime] = None
    ai_summary: Optional[str] = None
