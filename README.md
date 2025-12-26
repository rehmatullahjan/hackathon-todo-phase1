# Hackathon Todo - Phase 1

**Phase 1 Strict In-Memory implementation of the Hackathon Todo Spec.**

This project is a single-file Python console application that strictly adheres to the Phase 1 specifications. It runs entirely in memory and provides a robust CLI for task management.

## 🚀 Features

- **Strict Phase 1 Compliance**: Only `id`, `title`, `status`, `created_at`, `updated_at`.
- **In-Memory Persistence**: Fast, ephemeral storage during runtime.
- **Robust Validation**: Prevents invalid states, empty titles, and duplicate completions.
- **Zero Dependencies**: Runs on standard Python 3.

## 🛠️ Setup & Usage

### Prerequisites
- Python 3.x installed

### Running the App
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/hackathon-todo-phase1.git
   cd hackathon-todo-phase1
   ```
2. Run the application:
   ```bash
   python src/todo.py
   ```

### Commands

| Command | Usage | Description |
|---------|-------|-------------|
| **Add** | `add <title>` | Create a new task |
| **List** | `list` | Show all tasks |
| **Show** | `show <id>` | View details of a specific task |
| **Update**| `update <id> <value>` | Update title OR status (e.g. `in_progress`) |
| **Complete**| `complete <id>` | Mark a task as completed |
| **Delete** | `delete <id>` | Remove a task |
| **Help** | `help` | Show available commands |
| **Exit** | `exit` | Close the application |

## 🧪 Testing

A verification script is included to demonstrate robustness:

```bash
python verify_robustness.py
```

## 📝 Phase Notes

- **Architecture**: Single-file (`src/todo.py`) for simplicity and portability in Phase 1.
- **Future Phases**: This implementation is designed to be easily extended. The `Task` class and `TodoApp` structure can be adapted for persistence (Phase 2) and additional fields (Phase 3+) without breaking changes.
- **Immutability**: `domain.yaml` and `spec.yaml` contracts are respected.

---
*Ready for Phase 1 Judging*
