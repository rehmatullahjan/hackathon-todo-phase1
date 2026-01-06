# Hackathon Todo - Phase 3 (AI Chatbot)

**Full-stack Web Application for Task Management with Persistence, Search, and Filtering.**

Built on top of the Phase 1 CLI, Phase 2 adds a FastAPI backend, SQLModel persistence (SQLite/Postgres), and a Next.js frontend.

## 🚀 Features

- **AI Chatbot**: "Todo Assistant" powered by Google Gemini (or OpenAI) to create/search tasks via natural language.
- **Recurring Tasks**: Support for daily/weekly task recurrence rules.
- **Smart Reminders**: Due date tracking.
- **Web Dashboard**: View tasks with status colors, priority badges, and due dates.
- **Rich Task Management**: Create, Edit, Delete, Complete tasks.
- **Search & Filter**: Full-text search, filter by status/priority/tags.
- **Persistence**: Data saved to `database.db` (SQLite) or external DB.
- **Phase 1 Compatible**: Legacy CLI tool (`src/todo.py`) still works independently.

## 🛠️ Project Structure

- `backend/` - FastAPI app, SQLModel, CRUD logic.
- `frontend/` - Next.js React app.
- `src/` - Phase 1 CLI tool (In-Memory).
- `spec/` - Feature specifications.

## ⚙️ Setup & Running

### 1. Backend (FastAPI)

1. Navigate to the root folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn backend.main:app --reload
   ```
   *Server runs at http://localhost:8000*
   *Automatic API Docs: http://localhost:8000/docs*

### 2. Frontend (Next.js)

1. Open a new terminal.
2. Navigate to frontend:
   ```bash
   cd frontend
   ```
3. Install packages:
   ```bash
   npm install
   ```
4. Run the dev server:
   ```bash
   npm run dev
   ```
   *App runs at http://localhost:3000*

### 3. Phase 1 CLI (Legacy)

You can still use the CLI tool (runs in isolation):
```bash
python src/todo.py
```

## 🧪 Testing

### Backend Tests
Run pytest to verify the API logic:
```bash
pytest backend/tests/test_backend.py
```

### Phase 1 Regression
Run the robustness checker:
```bash
python verify_robustness.py
```

## 📝 Configuration

- **Database**: Defaults to `sqlite:///./backend/database.db`. Set `DATABASE_URL` environment variable to use PostgreSQL/Neon.
  - Example: `DATABASE_URL=postgresql://user:pass@host/db uvicorn ...`

### 🔑 API Keys (For AI Features)

To use the AI Chatbot, you must provide an API Key. Rename `.env.example` to `.env` and add your key:

```env
# Use Google Gemini (Recommended/Free Tier available)
GOOGLE_API_KEY=AIzaSy...

# OR OpenAI
OPENAI_API_KEY=sk-...
```

The system automatically detects which key is present. If no key is found, the chat widget will display "AI Agent is disabled".
