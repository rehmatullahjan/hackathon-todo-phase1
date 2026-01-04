# Phase 3: AI-Powered Todo Chatbot - Five Pillars Specification

This document outlines the strategic implementation of Phase 3 of the Hackathon Todo project.

## 1. Planning 📝

**Goal:** Integrate an AI-powered Chatbot interface that allows natural language interaction with the Todo list, including advanced features like recurring tasks and smart reminders.

### Requirements
- **AI Interface**: Conversation-based task management (e.g., "Remind me to call John every Friday").
- **Recurring Tasks**: Logic to handle tasks that repeat (daily, weekly, monthly).
- **Reminders**: Browser notifications for due dates/times.
- **Tech Stack**: OpenAI ChatKit, Agents SDK, Official MCP SDK.

### User Stories
- As a user, I want to type "Schedule a weekly sync on Mondays at 10am" and have the system auto-create recurring tasks.
- As a user, I want to receive a browser notification when a task is due.
- As a user, I want to ask "What do I have to do today?" and get a summarized answer from the AI.

## 2. Constitution (Design & Architecture) 🏛️

**System Architecture:**

- **AI Layer**:
  - **OpenAI ChatKit**: For building the UI of the chat interface within the Next.js app.
  - **Agents SDK**: To orchestrate the AI's ability to call tools (Tool Use).
  - **MCP (Model Context Protocol)**: To standardize how the AI reads the `database.db` and understands the "Todo" domain context.

- **Backend Extensions (FastAPI)**:
  - New endpoints for `RecurringTask` management.
  - Integration with an Agent runtime (sidecar or embedded).

- **Frontend Extensions (Next.js)**:
  - `Chat` component (floating or dedicated page).
  - Service Workers / Notification API for browser alerts.

**Data Model Changes**:
- `Task` table: Add `recurrence_rule` (cron-style or text), `reminder_at` (datetime).

## 3. Execution (Implementation) 🔨

**Step-by-Step Implementation:**

1.  **Backend Upgrade**:
    - Update SQLModel schemas to support recurrence and reminders.
    - Implement a background scheduler (e.g., APScheduler or simple cron) to regenerate recurring tasks.

2.  **MCP Server Setup**:
    - Create an MCP server that exposes the `list_tasks`, `create_task`, etc., as tools to the AI Agent.

3.  **Frontend Chat Integration**:
    - Install `@openai/chatkit` (or equivalent UI lib).
    - Connect Chat UI to the Agent endpoint.

4.  **Notification System**:
    - Request Browser Notification permissions on load.
    - Polling mechanism or WebSocket to trigger alerts when `reminder_at` is reached.

## 4. Verification (Testing) ✅

**Verification Strategy:**

- **AI Evaluation**:
  - Test natural language queries: "Add milk" -> Verified creation of task "Add milk".
  - Test complex queries: "Water plants every Sunday" -> Verified `recurrence_rule` is set.

- **Notification Test**:
  - Set a reminder for 1 minute in the future and verify the browser popup appears.

## 5. Deployment & Evolution 🚀

**Deployment**:
- Standard Vercel/Render deployment.
- **Environment Variables**: Add `OPENAI_API_KEY` and Agent configuration.

**Evolution**:
- Phase 4 could involve Voice Input/Output.
- Phase 5 could involve multi-user collaboration via the AI.
