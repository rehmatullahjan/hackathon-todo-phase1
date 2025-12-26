import sys
import uuid
import datetime
import json

# Constants
STATUS_PENDING = 'pending'
STATUS_IN_PROGRESS = 'in_progress'
STATUS_COMPLETED = 'completed'
VALID_STATUSES = {STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED}

class Task:
    """
    Represents a single task in the Todo system.
    Strictly adheres to Phase 1 fields.
    """
    def __init__(self, title):
        self.id = str(uuid.uuid4())
        self.title = title
        self.status = STATUS_PENDING
        # Use UTC for consistency
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.created_at = now
        self.updated_at = now

    def update_title(self, title):
        """Update task title and timestamp."""
        self.title = title
        self.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def update_status(self, status):
        """Update task status and timestamp."""
        self.status = status
        self.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def complete(self):
        """Mark task as completed."""
        self.status = STATUS_COMPLETED
        self.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def to_dict(self):
        """Return dictionary representation for JSON output or testing."""
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __str__(self):
        """Consistent string format for list display."""
        return f"[{self.id}] {self.title} | {self.status} | {self.created_at}"

class TodoApp:
    """
    Main application controller for the In-Memory Todo CLI.
    """
    def __init__(self):
        self.tasks = {} # id -> Task
        self.running = True

    def reset_store(self):
        """Reset the in-memory store for testing."""
        self.tasks = {}

    def get_all_tasks_as_dicts(self):
        """Helper for testing to retrieve all data."""
        return [t.to_dict() for t in self.tasks.values()]

    def print_help(self):
        print("Available commands:")
        print("  add <title>                          - Add a new task")
        print("  list                                 - List all tasks")
        print("  show <id>                            - Show task details")
        print("  update <id> <new_title | new_status> - Update task title or status")
        print("  delete <id>                          - Delete a task")
        print("  complete <id>                        - Mark task as completed")
        print("  help                                 - Show this help message")
        print("  exit / quit                          - Exit the application")

    def handle_add(self, args):
        if not args:
            print("Error: Missing title.")
            return
        title = " ".join(args).strip()
        if not title:
            print("Error: Title cannot be empty.")
            return
        task = Task(title)
        self.tasks[task.id] = task
        print(f"Task added: {task}")

    def handle_list(self, args):
        if not self.tasks:
            print("No tasks found.")
            return
        # Sort by created_at for consistent display
        sorted_tasks = sorted(self.tasks.values(), key=lambda t: t.created_at)
        for t in sorted_tasks:
            print(t)

    def handle_show(self, args):
        if not args:
            print("Error: Missing task ID.")
            return
        id_ = args[0]
        if id_ not in self.tasks:
            print(f"Error: Task with ID {id_} not found.")
            return
        
        t = self.tasks[id_]
        # Enhanced detailed view
        print(f"[{t.id}]")
        print(f"Title:      {t.title}")
        print(f"Status:     {t.status}")
        print(f"Created At: {t.created_at}")
        print(f"Updated At: {t.updated_at}")

    def handle_update(self, args):
        if len(args) < 2:
            print("Error: Usage: update <id> <new_title | new_status>")
            return
        id_ = args[0]
        value = " ".join(args[1:]).strip()
        
        if id_ not in self.tasks:
            print(f"Error: Task with ID {id_} not found.")
            return
        
        if not value:
            print("Error: Update value cannot be empty.")
            return

        # Check if value is a status (case-insensitive)
        lower_value = value.lower()
        if lower_value in VALID_STATUSES:
            self.tasks[id_].update_status(lower_value)
            print(f"Task status updated: {self.tasks[id_]}")
        else:
            # Treat as title
            self.tasks[id_].update_title(value)
            print(f"Task title updated: {self.tasks[id_]}")

    def handle_delete(self, args):
        if not args:
            print("Error: Missing task ID.")
            return
        id_ = args[0]
        if id_ not in self.tasks:
            print(f"Error: Task with ID {id_} not found.")
            return
        del self.tasks[id_]
        print(f"Task deleted: {id_}")

    def handle_complete(self, args):
        if not args:
            print("Error: Missing task ID.")
            return
        id_ = args[0]
        if id_ not in self.tasks:
            print(f"Error: Task with ID {id_} not found.")
            return
        
        task = self.tasks[id_]
        if task.status == STATUS_COMPLETED:
            print("Task is already completed.")
            return
            
        task.complete()
        print(f"Task completed: {task}")

    def process_command(self, line):
        """Process a single command line."""
        if not line:
            return
        
        parts = line.split()
        if not parts:
            return

        command = parts[0].lower()
        args = parts[1:]

        # Check for hooks (placeholders for future phases)
        # In a real CLI lib, we'd parse these properly. 
        # Here we just strip them if present to avoid breaking Phase 1 logic if passed.
        # But per requirements, "don't implement future fields", so strict adherence means 
        # we treat them as arguments if they are passed, UNLESS they interfere.
        # For simplicity, we assume standard usage per Phase 1 spec.

        if command in ('exit', 'quit'):
            print("Goodbye!")
            self.running = False
            return
        elif command == 'add':
            self.handle_add(args)
        elif command == 'list':
            self.handle_list(args)
        elif command == 'show':
            self.handle_show(args)
        elif command == 'update':
            self.handle_update(args)
        elif command == 'delete':
            self.handle_delete(args)
        elif command == 'complete':
            self.handle_complete(args)
        elif command == 'help':
            self.print_help()
        else:
            print(f"Unknown command: '{command}'. Type 'help' for available commands.")

    def run(self):
        print("Hackathon Todo CLI (Type 'exit' to quit)")
        print("Type 'help' for commands.")
        
        while self.running:
            try:
                # Use sys.stdout.flush to ensure prompt appears immediately
                sys.stdout.write("> ")
                sys.stdout.flush()
                
                line = sys.stdin.readline()
                if not line: # EOF
                    break
                
                line = line.strip()
                self.process_command(line)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app = TodoApp()
    app.run()
