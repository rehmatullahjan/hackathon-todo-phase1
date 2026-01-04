from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import pytest
from ..main import app, get_session
from ..models import Task

# In-memory SQLite for testing
sqlite_file_name = "database.db"
sqlite_url = "sqlite://" # In-memory

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

def test_create_task(client: TestClient):
    response = client.post(
        "/tasks", json={"title": "Test Task", "priority": "high", "tags": "[\"urgent\"]"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"
    assert data["status"] == "pending"
    assert "id" in data

def test_list_tasks(client: TestClient):
    client.post("/tasks", json={"title": "Task 1", "priority": "low"})
    client.post("/tasks", json={"title": "Task 2", "priority": "high"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_filter_tasks(client: TestClient):
    client.post("/tasks", json={"title": "Urgent Job", "priority": "urgent"})
    client.post("/tasks", json={"title": "Routine Job", "priority": "low"})
    
    response = client.get("/tasks?priority=urgent")
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Urgent Job"

def test_search_tasks(client: TestClient):
    client.post("/tasks", json={"title": "Buy Milk", "description": "Go to store"})
    client.post("/tasks", json={"title": "Walk Dog", "description": "In the park"})
    
    response = client.get("/search?query=Milk")
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Buy Milk"
    
    response = client.get("/search?query=park")
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Walk Dog"

def test_update_task(client: TestClient):
    create_res = client.post("/tasks", json={"title": "Old Title"})
    task_id = create_res.json()["id"]
    
    response = client.patch(f"/tasks/{task_id}", json={"title": "New Title", "status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["status"] == "in_progress"

def test_complete_task(client: TestClient):
    create_res = client.post("/tasks", json={"title": "Do It"})
    task_id = create_res.json()["id"]
    
    response = client.post(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["completed_at"] is not None

def test_delete_task(client: TestClient):
    create_res = client.post("/tasks", json={"title": "To Delete"})
    task_id = create_res.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 404
