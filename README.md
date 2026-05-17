# Bitcoin Smart Contract Agent - MVP

A Bitcoin Smart Contract AI Agent with simplified architecture. Users can chat with an AI agent to generate, validate, and manage Bitcoin scripts.

## Features

- User authentication (login/register)
- Chat with AI agent (simple Q&A responses)
- Bitcoin script validation
- Save/retrieve scripts
- View conversation history
- Simple responsive UI

## Tech Stack

- **Backend:** Python FastAPI + SQLAlchemy + PostgreSQL
- **Frontend:** React + Vite + React Router
- **Authentication:** JWT
- **Database:** PostgreSQL

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and secret key
   ```

5. Run the backend:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults to localhost:8000)
   ```

4. Run the frontend:
   ```bash
   npm run dev
   ```

### Database Setup

Create a PostgreSQL database and update the DATABASE_URL in backend/.env.

Run the migrations (tables are created automatically on startup).

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Project Structure

```
bitcoin-agent-mvp/
├── MVP_PLAN.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── services/
│   │   └── routes/
│   ├── tests/
│   ├── requirements.txt
│   └── main.py
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   └── hooks/
    ├── package.json
    └── vite.config.js
```

## Development Timeline

- **Week 1:** Backend development (auth, sessions, agent chat, scripts)
- **Week 2:** Frontend development and integration

## License

MIT