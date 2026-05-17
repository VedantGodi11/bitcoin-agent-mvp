#!/usr/bin/env python3
"""
Bitcoin Smart Contract Agent - Backend Entry Point
"""
import uvicorn
from app.main import app
from app.database import engine, Base

if __name__ == "__main__":
    # Create database tables before serving the app.
    Base.metadata.create_all(bind=engine)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )