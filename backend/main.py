from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import List, Optional
from .database import create_db_and_tables, get_session
from .models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from . import crud
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Hackathon Todo API", version="2.0.0")

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    return crud.create_task(session, task)

@app.get("/tasks", response_model=List[Task])
def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tags: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    return crud.list_tasks(
        session, status, priority, tags, category, sort_by, sort_order, offset, limit
    )

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str, session: Session = Depends(get_session)):
    task = crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: TaskUpdate, session: Session = Depends(get_session)):
    task = crud.update_task(session, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, session: Session = Depends(get_session)):
    success = crud.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}

@app.post("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: str, session: Session = Depends(get_session)):
    task = crud.complete_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/search", response_model=List[Task])
def search_tasks(query: str, session: Session = Depends(get_session)):
    return crud.search_tasks(session, query)
