# Phase 1: CLI Todo Tool - Five Pillars Specification

This document outlines the strategic implementation of Phase 1 of the Hackathon Todo project, following the Five Pillars methodology.

## 1. Planning 📝

**Goal:** Create a simple, functional Command Line Interface (CLI) tool for task management to establish the core domain logic.

### Requirements
- **Interface**: Command Line Interface (CLI).
- **Persistence**: In-memory (transient) for MVP, or basic file I/O.
- **Core Features**: Add, List, Complete, Delete tasks.
- **Speed**: Must be lightweight and fast.

### User Stories
- As a developer, I want to add a task quickly from my terminal so I don't break flow.
- As a developer, I want to see a list of pending tasks to know what to do next.
- As a developer, I want to mark tasks as done to feel a sense of accomplishment.

## 2. Constitution (Design & Architecture) 🏛️

**System Architecture:**

- **Language**: Python 3.10+
- **Entry Point**: `src/todo.py`
- **Architecture**: Single-file script (Monolithic Script) for simplicity and portability.
- **Data Structure**: List of Dictionaries `[{"id": 1, "title": "...", "status": "pending"}]`.

**Rules & Guidelines:**
- No external dependencies (Standard Library only).
- Usage of `argparse` for parsing command line arguments.
- Clean output using print statements.

## 3. Execution (Implementation) 🔨

**Step-by-Step Implementation:**

1.  **Setup**:
    - Created `src/` directory.
    - specialized `todo.py`.

2.  **Core Logic**:
    - Implemented `Task` class (or dictionary structure).
    - Implemented functions: `add_task`, `list_tasks`, `delete_task`, `complete_task`.

3.  **CLI Wrapper**:
    - Configured `argparse` to handle subcommands:
      - `python src/todo.py add "Buy milk"`
      - `python src/todo.py list`
      - `python src/todo.py done <id>`

## 4. Verification (Testing) ✅

**Verification Strategy:**

- **Test Script**:
  - Created `verify_todo.py` to act as an integration test.
  - It runs the `todo.py` script as a subprocess and asserts the output matches expected behavior.

- **Manual Verification**:
  - User runs commands in terminal and verifies output visually.

## 5. Deployment & Evolution 🚀

**Deployment**:
- **Distribution**: Source code via Git.
- **Installation**: Clone repo and run with Python.
- **Alias**: Users can create a shell alias `alias todo="python /path/to/src/todo.py"` for easy access.

**Evolution (Transition to Phase 2)**:
- Phase 1 serves as the prototype.
- Logic from Phase 1 informs the Database Schema and API design for Phase 2.
- Phase 1 remains useful as a lightweight alternative to the Web App.
