# Phase 2: Web Todo App - Five Pillars Specification

This document outlines the strategic implementation of Phase 2 of the Hackathon Todo project, following the Five Pillars methodology.

## 1. Planning 📝

**Goal:** Transform the CLI-based Phase 1 into a robust, persisted, and user-friendly Web Application using a modern tech stack.

### Requirements
- **User Interface**: A responsive web dashboard to manage tasks.
- **Persistence**: Tasks must be saved to a database (SQLite for local, extensible to Postgres) instead of in-memory.
- **Rich Data**: Support for Priority (High/Medium/Low), Tags, Categories, and Due Dates.
- **Search & Discovery**: Full-text search and filtering capabilities.
- **Compatibility**: Phase 1 CLI must remain functional alongside the new web app.

### User Stories
- As a user, I want to see all my tasks in a visual list so I can prioritize my day.
- As a user, I want to filter tasks by "Work" or "Personal" to focus on specific contexts.
- As a user, I want to search for "meeting" to find relevant tasks quickly.
- As a user, I want my tasks to be saved even if I restart the computer.

---

## 2. Constitution (Design & Architecture) 🏛️

**System Architecture:**

- **Frontend**: Next.js (React)
  - **Styling**: Tailwind CSS for rapid, modern UI development.
  - **State Management**: React Hooks (useState, useEffect) for local state and API integration.
  - **Routing**: Next.js App Router/Pages for navigation.

- **Backend**: FastAPI (Python)
  - **API Design**: RESTful endpoints (`GET /tasks`, `POST /tasks`, `PATCH /tasks/{id}`).
  - **Documentation**: Automatic interactive docs via Swagger UI (`/docs`).
  - **Validation**: Pydantic models (via SQLModel) for robust request/response validation.

- **Database**: SQLModel (SQLite)
  - **Schema**: `Task` table with columns for `id`, `title`, `description`, `priority`, `tags`, `category`, `status`, `created_at`.
  - **ORM**: SQLModel for seamless Python-to-SQL mapping.

**Rules & Guidelines:**
- Code must be modular: Separate `crud.py`, `models.py`, and `main.py`.
- API responses must be typed and consistent.
- Frontend must handle loading and error states gracefully.

---

## 3. Execution (Implementation) 🔨

**Step-by-Step Implementation:**

1.  **Backend Foundation**:
    - Defined `Task` model in `models.py`.
    - Implemented database engine and session management in `database.py`.
    - Created CRUD operations in `crud.py`.
    - Built FastAPI endpoints in `main.py` bridging API to CRUD.

2.  **Frontend Development**:
    - Initialized Next.js project.
    - Configured Tailwind CSS.
    - Created `api.js` for centralized Axios HTTP client.
    - Built specific components: `TaskForm` (creation), `TaskList` (display), `TaskFilters` (search/filter).
    - Assembled the `Dashboard` page to integrate all components.

3.  **Integration**:
    - Connected Frontend to Backend via CORS configuration.
    - Verified data flow: Create Task -> Save to DB -> Fetch List -> Update UI.

---

## 4. Verification (Testing) ✅

**Verification Strategy:**

- **Automated Backend Tests**:
  - `pytest` suite ensuring all API endpoints return correct status codes and data.
  - Validation of constraint violations (e.g., invalid priority levels).

- **Browser Verification**:
  - **Functional Testing**: Manually creating tasks, searching, and filtering to ensure UI responsiveness.
  - **Persistence Check**: Restarting the backend server and verifying tasks remain visible.
  - **Cross-Browser**: Tested in Chrome/Edge.

- **Phase 1 Regression**:
  - Ran `verify_robustness.py` to ensure legacy CLI logic remains intact and unaffected by Phase 2 changes.

---

## 5. Deployment & Evolution 🚀

**Deployment**:
- **Version Control**: Git repository with main branch.
- **Hosting**:
  - Backend: Ready for Render/Railway/Heroku (needs `DATABASE_URL` env var).
  - Frontend: Ready for Vercel/Netlify.
- **Local Run**:
  - Backend: `uvicorn backend.main:app --reload`
  - Frontend: `npm run dev`

**Evolution (Future Pillars)**:
- **Phase 3**: Authentication (User Login/Signup).
- **Phase 4**: AI integration for smart task suggestions (Gemini/Gateway).
- **Mobile**: Responsive design allows for mobile usage, but a dedicated Native App could be added.
