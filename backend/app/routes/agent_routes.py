from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .. import schemas, models, database
from ..services.agent_service import AgentService
from ..auth import get_current_user

router = APIRouter()

@router.post("/chat", response_model=schemas.ChatResponse)
async def chat_with_agent(
    request: schemas.ChatRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """Send a message to the AI agent"""
    # Verify session belongs to user
    session = db.query(models.AISession).filter(
        models.AISession.id == request.session_id,
        models.AISession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Save user message
    AgentService.save_message(db, request.session_id, "user", request.message)

    # Get agent response
    response_text = AgentService.process_message(request.message)

    # Save agent response
    AgentService.save_message(db, request.session_id, "agent", response_text)

    return schemas.ChatResponse(response=response_text, timestamp=datetime.utcnow())

@router.get("/history/{session_id}", response_model=schemas.HistoryResponse)
async def get_conversation_history(
    session_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """Get conversation history for a session"""
    # Verify session belongs to user
    session = db.query(models.AISession).filter(
        models.AISession.id == session_id,
        models.AISession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = AgentService.get_conversation_history(db, session_id)
    return schemas.HistoryResponse(messages=[schemas.MessageResponse.from_orm(msg) for msg in messages])