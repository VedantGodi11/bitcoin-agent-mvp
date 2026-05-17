# Bitcoin Smart Contract Agent - MVP Plan

## Project Overview
A Bitcoin Smart Contract AI Agent with simplified architecture. Users can chat with an AI agent to generate, validate, and manage Bitcoin scripts.

**Timeline:** 2 weeks  
**Tech Stack:** Python FastAPI + React JavaScript + PostgreSQL  
**Complexity:** Easy-Medium with Basic Testing

---

## Decision History

### Architecture Choices Made
1. **Migrate from TypeScript to Python + React**
   - Backend: TypeScript/Node.js → Python/FastAPI
   - Frontend: Streamlit → React JavaScript
   - Database: Keep PostgreSQL (already in use)

2. **MVP First Approach**
   - Build minimal features first
   - Ship in 2 weeks
   - Add features incrementally later
   - Basic testing included

3. **Frontend Only Simplified**
   - Backend: Full complexity (all 20+ endpoints available)
   - Frontend: Simplified UI (4 pages, 8-10 components)
   - Best of both worlds

---

## What the Agent Does

The agent helps users with Bitcoin smart contracts in 5 modes:
1. **Contract Generation** - Creates Bitcoin scripts from descriptions
2. **Script Explanation** - Explains existing scripts in plain English
3. **Script Validation** - Checks scripts for security/correctness
4. **Beginner Mode** - Step-by-step guidance
5. **Use Case Consulting** - Recommends solutions for business scenarios

**MVP Version:** Simplified to basic Chat + Validation (expandable to other modes later)

---

## MVP Features

### ✅ INCLUDED
- User authentication (login/register)
- Chat with AI agent (simple Q&A responses)
- Bitcoin script validation
- Save/retrieve scripts
- View conversation history
- Simple responsive UI
- Basic error handling
- Docker setup
- Basic testing (pytest + Jest)

### ❌ NOT INCLUDED (Add Later)
- Advanced AI (LLM integration - will be added)
- Multiple agent modes
- Admin panel
- WebSocket (real-time)
- Audit logging
- Role-based access control
- E2E tests
- CI/CD pipeline
- Dark mode
- Advanced visualizations

---

## Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration & env vars
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── database.py             # Database connection setup
│   ├── auth.py                 # JWT authentication
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py    # AI agent logic
│   │   ├── bitcoin_service.py  # Bitcoin script operations
│   │   └── auth_service.py     # User auth logic
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py      # /api/auth/* endpoints
│       ├── agent_routes.py     # /api/agent/* endpoints
│       └── scripts_routes.py   # /api/scripts/* endpoints
├── tests/
│   ├── __init__.py
│   ├── test_auth.py            # Auth endpoint tests
│   ├── test_agent.py           # Agent service tests
│   └── test_scripts.py         # Script service tests
├── requirements.txt
├── .env.example
└── main.py                     # App entry point
```

---

## Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Navigation header
│   │   ├── LoginForm.jsx       # Login/Register form
│   │   ├── ChatWindow.jsx      # Chat display
│   │   ├── MessageInput.jsx    # Message input box
│   │   ├── ScriptForm.jsx      # Script creation form
│   │   ├── ScriptList.jsx      # Scripts list display
│   │   ├── ProtectedRoute.jsx  # Auth wrapper
│   │   └── __tests__/          # Component tests
│   ├── pages/
│   │   ├── LoginPage.jsx       # Login/Register page
│   │   ├── ChatPage.jsx        # Chat interface page
│   │   └── ScriptsPage.jsx     # Script management page
│   ├── services/
│   │   └── api.js              # Axios HTTP client
│   ├── hooks/
│   │   └── useAuth.js          # Custom auth hook
│   ├── App.jsx                 # Root component
│   ├── App.css                 # Global styles
│   └── main.jsx                # Entry point
├── package.json
├── .env.example
├── vite.config.js              # Vite configuration
└── index.html
```

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### AI Sessions Table
```sql
CREATE TABLE ai_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Messages Table
```sql
CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  session_id INTEGER NOT NULL REFERENCES ai_sessions(id) ON DELETE CASCADE,
  role VARCHAR(50) NOT NULL, -- 'user' or 'agent'
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Scripts Table
```sql
CREATE TABLE scripts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## API Endpoints (MVP)

### Authentication Endpoints
```
POST   /api/auth/login
       Request: { username, password }
       Response: { access_token, user_id }

POST   /api/auth/register
       Request: { username, email, password }
       Response: { access_token, user_id }
```

### Session Endpoints
```
POST   /api/sessions
       Create new chat session
       Response: { session_id }

GET    /api/sessions
       List user's sessions
       Response: [{ id, created_at }, ...]

GET    /api/sessions/{id}
       Get session details
       Response: { id, created_at }

DELETE /api/sessions/{id}
       Delete session
```

### Agent Chat Endpoints
```
POST   /api/agent/chat
       Send message to agent
       Request: { session_id, message }
       Response: { response, timestamp }

GET    /api/agent/history/{session_id}
       Get conversation history
       Response: [{ role, content, timestamp }, ...]
```

### Scripts Endpoints
```
POST   /api/scripts
       Create new script
       Request: { content }
       Response: { id, created_at }

GET    /api/scripts
       List user's scripts
       Response: [{ id, content, created_at }, ...]

GET    /api/scripts/{id}
       Get script details
       Response: { id, content, created_at }

POST   /api/scripts/validate
       Validate a script
       Request: { content }
       Response: { is_valid, errors, warnings }

DELETE /api/scripts/{id}
       Delete script
```

---

## Technology Stack

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **PyJWT** - JWT authentication
- **bcrypt** - Password hashing
- **bitcoinlib** - Bitcoin operations
- **pytest** - Testing framework
- **python-dotenv** - Environment variables

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **React Router** - Navigation
- **Axios** - HTTP client
- **Jest** - Testing framework
- **React Testing Library** - Component testing

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Local development
- **PostgreSQL** - Database

---

## Timeline (2 Weeks)

### Week 1: Backend
| Day | Task | Deliverable |
|-----|------|-------------|
| 1 | Setup + Auth | Login/Register working |
| 2 | Sessions + Messages | Session management working |
| 3 | Agent Chat | Chat endpoint working |
| 4 | Bitcoin Scripts | Script CRUD working |
| 5 | Testing + Fixes | All tests passing |

### Week 2: Frontend + Integration
| Day | Task | Deliverable |
|-----|------|-------------|
| 6 | Frontend Setup + Login | React + login page |
| 7 | Chat Interface | Chat page working |
| 8 | Scripts Page | Scripts management page |
| 9 | Integration | Frontend ↔ Backend working |
| 10 | Polish + Deployment | Production-ready MVP |

---

## Testing Strategy

### Backend Testing (pytest)
- Authentication tests (login, register, JWT)
- API endpoint tests (happy path, error cases)
- Database model tests
- Service logic tests

### Frontend Testing (Jest + React Testing Library)
- Component rendering tests
- Form submission tests
- API call mocking tests
- Navigation tests

---

## Future Enhancements (After MVP)

### Phase 1: Advanced Agent (Week 3)
- [ ] LLM integration (OpenAI/Claude API)
- [ ] Multiple agent modes
- [ ] Conversation context awareness
- [ ] Template library UI

### Phase 2: Admin Features (Week 4)
- [ ] Admin dashboard
- [ ] User management
- [ ] Prompt editing
- [ ] System statistics

### Phase 3: Advanced Features (Week 5)
- [ ] WebSocket real-time chat
- [ ] File upload/export
- [ ] Advanced script analysis
- [ ] E2E tests

### Phase 4: Polish (Week 6)
- [ ] Dark mode
- [ ] Advanced visualizations
- [ ] Performance optimization
- [ ] CI/CD pipeline

---

## Development Workflow

### Getting Started
1. Set up Python virtual environment
2. Install backend dependencies: `pip install -r requirements.txt`
3. Set up PostgreSQL database
4. Configure .env file
5. Run migrations
6. Start FastAPI: `uvicorn app.main:app --reload`

### Frontend Development
1. Install Node.js dependencies: `npm install`
2. Start dev server: `npm run dev`
3. Open http://localhost:5173

### Testing
```bash
# Backend tests
pytest

# Frontend tests
npm test
```

### Docker Development
```bash
docker-compose up
```

---

## Success Criteria

✅ All API endpoints working  
✅ Authentication flow working  
✅ Frontend communicates with backend  
✅ Database operations working  
✅ Basic tests passing (70%+ coverage)  
✅ Docker setup working  
✅ Error handling robust  
✅ Deployable to cloud  

---

## Notes

- This MVP is the foundation for future features
- Backend is built for scale (all endpoints available for expansion)
- Frontend is intentionally simple (can add advanced UI later)
- Testing is basic but essential (can add E2E/CI-CD later)
- AI responses are hardcoded for MVP (will integrate real LLM later)
