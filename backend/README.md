# Bitcoin Agent MVP Backend

Backend API for Bitcoin Smart Contract AI Agent using FastAPI and PostgreSQL.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run migrations and start:
```bash
python -m alembic upgrade head
uvicorn app.main:app --reload
```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing
```bash
pytest
pytest --cov=app  # With coverage
```
