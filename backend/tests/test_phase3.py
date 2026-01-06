from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import pytest
from datetime import datetime, timedelta
from ..main import app, get_session
from ..models import Task, TaskStatus

# In-memory SQLite for testing
sqlite_url = "sqlite://"

engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_recurrence_daily(client: TestClient):
    # 1. Create a task with daily recurrence
    due_date = datetime.utcnow()
    response = client.post(
        "/tasks", 
        json={
            "title": "Daily Workout", 
            "recurrence_rule": "daily",
            "due_date": due_date.isoformat()
        }
    )
    task_id = response.json()["id"]
    
    # 2. Complete the task
    complete_res = client.post(f"/tasks/{task_id}/complete")
    assert complete_res.status_code == 200
    assert complete_res.json()["status"] == "completed"
    
    # 3. Check if a new task was created
    list_res = client.get("/tasks")
    tasks = list_res.json()
    # Should have 2 tasks: 1 completed, 1 pending (new)
    assert len(tasks) == 2
    
    pending_tasks = [t for t in tasks if t["status"] == "pending"]
    assert len(pending_tasks) == 1
    new_task = pending_tasks[0]
    assert new_task["title"] == "Daily Workout"
    assert new_task["recurrence_rule"] == "daily"
    
    # 4. Verify the new due date is approx 1 day after the old one
    new_due = datetime.fromisoformat(new_task["due_date"])
    expected_due = due_date + timedelta(days=1)
    # Compare with some tolerance for microsecond differences in isoformat
    assert abs((new_due - expected_due).total_seconds()) < 1

def test_recurrence_weekly(client: TestClient):
    due_date = datetime.utcnow()
    response = client.post(
        "/tasks", 
        json={
            "title": "Weekly Sync", 
            "recurrence_rule": "weekly",
            "due_date": due_date.isoformat()
        }
    )
    task_id = response.json()["id"]
    client.post(f"/tasks/{task_id}/complete")
    
    list_res = client.get("/tasks")
    pending_tasks = [t for t in list_res.json() if t["status"] == "pending"]
    new_task = pending_tasks[0]
    
    new_due = datetime.fromisoformat(new_task["due_date"])
    expected_due = due_date + timedelta(weeks=1)
    assert abs((new_due - expected_due).total_seconds()) < 1

def test_reminder_at_storage(client: TestClient):
    reminder_at = datetime.utcnow() + timedelta(hours=2)
    response = client.post(
        "/tasks", 
        json={
            "title": "Remind Me", 
            "reminder_at": reminder_at.isoformat()
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "reminder_at" in data
    stored_reminder = datetime.fromisoformat(data["reminder_at"])
    assert abs((stored_reminder - reminder_at).total_seconds()) < 1
