# How to Run Phase 3 (AI Chatbot)

Follow these steps to quickly launch the Phase 3 application.

## Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Google Gemini API Key**: Set as `GOOGLE_API_KEY` in your `.env` file.

## Quick Start Commands

### 1. Start Backend (FastAPI)
Run this command from the project root:
```powershell
uvicorn backend.main:app --reload
```
- API URL: http://localhost:8000
- Docs: http://localhost:8000/docs

### 2. Start Frontend (Next.js)
Open a new terminal and run:
```powershell
cd frontend
npm run dev
```
- Web UI: http://localhost:3000

## Verifying the Chatbot
1. Open http://localhost:3000.
2. Click the **Indigo Chat Bubble** in the bottom-right corner.
3. Try a prompt like: *"Add a task to Fix the sink with high priority"*
4. The chatbot should respond with a success message and the task will appear in the list.
