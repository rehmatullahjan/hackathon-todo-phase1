import os
import logging
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any
from sqlmodel import Session
from .models import TaskCreate, Task
from .crud import create_task, list_tasks, search_tasks
import google.generativeai as genai

# Load env vars
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

class TodoAgent:
    def __init__(self, session: Session):
        self.session = session
        self.enabled = bool(GOOGLE_API_KEY)

    def process_message(self, message: str) -> str:
        if not self.enabled:
            return "AI Agent is disabled. Please set GOOGLE_API_KEY in .env file."
            
        try:
            # --- Tool Definitions (Closures to capture session) ---
            from .skills import TodoSkills
            from .models import TaskStatus, TaskPriority, TaskCreate, TaskUpdate
            from datetime import datetime

            def create_todo(
                title: str, 
                priority: str = "medium", 
                category: str = None, 
                recurrence: str = None,
                due_date: str = None,
                reminder_at: str = None
            ):
                """Create a new task in the todo list."""
                logger.info(f"Tool Call: create_todo(title={title})")
                try:
                    from dateutil.parser import parse
                    parsed_due = parse(due_date) if due_date else None
                    parsed_reminder = parse(reminder_at) if reminder_at else None

                    task_data = TaskCreate(
                        title=title, 
                        priority=TaskPriority(priority), 
                        category=category,
                        recurrence_rule=recurrence,
                        due_date=parsed_due,
                        reminder_at=parsed_reminder
                    )
                    task = TodoSkills.create_task(self.session, task_data)
                    return f"SUCCESS: Created task '{task.title}' [ID: {task.id}]"
                except Exception as e:
                    return f"ERROR: {str(e)}"

            def update_todo(
                id: str,
                title: str = None,
                status: str = None,
                priority: str = None,
                category: str = None,
                due_date: str = None,
                recurrence: str = None
            ):
                """Update an existing task."""
                logger.info(f"Tool Call: update_todo(id={id})")
                try:
                    from dateutil.parser import parse
                    update_data = {}
                    if title: update_data["title"] = title
                    if status: update_data["status"] = TaskStatus(status)
                    if priority: update_data["priority"] = TaskPriority(priority)
                    if category: update_data["category"] = category
                    if recurrence: update_data["recurrence_rule"] = recurrence
                    if due_date: update_data["due_date"] = parse(due_date)
                    
                    task = TodoSkills.update_task(self.session, id, TaskUpdate(**update_data))
                    return f"SUCCESS: Updated task {id}" if task else f"ERROR: Task {id} not found"
                except Exception as e:
                    return f"ERROR: {str(e)}"

            def get_todos(status: str = "pending"):
                """List tasks from the todo list."""
                logger.info(f"Tool Call: get_todos(status={status})")
                try:
                    tasks = TodoSkills.list_tasks(self.session, status=TaskStatus(status), limit=20)
                    if not tasks:
                        return "No tasks found."
                    return "\n".join([f"- {t.title} [ID: {t.id}] (Status: {t.status}, Priority: {t.priority})" for t in tasks])
                except Exception as e:
                    return f"ERROR: {str(e)}"

            def search_todos(query: str):
                """Search tasks by keyword."""
                logger.info(f"Tool Call: search_todos(query={query})")
                try:
                    tasks = TodoSkills.search_tasks(self.session, query)
                    if not tasks:
                        return "No matching tasks found."
                    return "\n".join([f"- {t.title} [ID: {t.id}] (Status: {t.status})" for t in tasks])
                except Exception as e:
                    return f"ERROR: {str(e)}"

            # --- Agent Execution ---
            
            tools = [create_todo, get_todos, search_todos, update_todo]
            
            # verified model that supports functions
            # gemini-flash-latest usually maps to the stable 1.5 Flash model
            system_instruction = (
                "You are a helpful Todo List Assistant. You can create, list, search, and update tasks. "
                "When a user mentions a time or recurrence (like 'every Friday' or 'tomorrow'), "
                "extract that information carefully. Statuses: pending, in_progress, completed, cancelled. "
                "Priorities: low, medium, high, urgent. Recurrence: daily, weekly, monthly."
            )
            model = genai.GenerativeModel(
                model_name='gemini-flash-latest', 
                tools=tools,
                system_instruction=system_instruction
            )
            
            # Automatic function calling handles the loop
            chat = model.start_chat(enable_automatic_function_calling=True)
            
            response = chat.send_message(message)
            return response.text
            
        except Exception as e:
            logger.error(f"Agent Logic Error: {e}", exc_info=True)
            return f"I encountered an error processing your request: {str(e)}"
