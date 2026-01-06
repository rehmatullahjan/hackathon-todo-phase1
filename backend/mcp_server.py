from mcp.server.fastmcp import FastMCP
from .database import get_session
from .models import TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from .skills import TodoSkills
from datetime import datetime

# Create an MCP server
mcp = FastMCP("Hackathon Todo Server")

@mcp.tool()
def list_todos(status: str = None, priority: str = None, category: str = None):
    """
    List tasks from the todo list with optional filters.
    """
    with next(get_session()) as session:
        tasks = TodoSkills.list_tasks(
            session, 
            status=TaskStatus(status) if status else None,
            priority=TaskPriority(priority) if priority else None,
            category=category
        )
        return [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority, "due_date": str(t.due_date) if t.due_date else None} for t in tasks]

@mcp.tool()
def create_todo(title: str, description: str = None, priority: str = "medium", category: str = None, recurrence: str = None, due_date: str = None):
    """
    Create a new task in the todo list.
    """
    with next(get_session()) as session:
        parsed_due = None
        if due_date:
            try:
                parsed_due = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except:
                pass

        task_data = TaskCreate(
            title=title,
            description=description,
            priority=TaskPriority(priority),
            category=category,
            recurrence_rule=recurrence,
            due_date=parsed_due
        )
        task = TodoSkills.create_task(session, task_data)
        return {"id": task.id, "title": task.title, "status": task.status}

@mcp.tool()
def update_todo(task_id: str, status: str = None, priority: str = None, title: str = None):
    """
    Update an existing task's status or priority.
    """
    with next(get_session()) as session:
        update_data = {}
        if status: update_data["status"] = TaskStatus(status)
        if priority: update_data["priority"] = TaskPriority(priority)
        if title: update_data["title"] = title
        
        task = TodoSkills.update_task(session, task_id, TaskUpdate(**update_data))
        if task:
            return {"id": task.id, "title": task.title, "status": task.status}
        return "Task not found"

@mcp.tool()
def search_todos(query: str):
    """
    Search for tasks using a keyword.
    """
    with next(get_session()) as session:
        tasks = TodoSkills.search_tasks(session, query)
        return [{"id": t.id, "title": t.title, "status": t.status} for t in tasks]

if __name__ == "__main__":
    mcp.run()
