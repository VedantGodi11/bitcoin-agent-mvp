from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database
from ..auth import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.SessionResponse)
async def create_session(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """Create a new chat session"""
    db_session = models.AISession(user_id=current_user.id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return schemas.SessionResponse.from_orm(db_session)

@router.get("", response_model=List[schemas.SessionResponse])
async def list_sessions(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """List user's sessions"""
    sessions = db.query(models.AISession).filter(
        models.AISession.user_id == current_user.id
    ).order_by(models.AISession.created_at.desc()).all()
    return [schemas.SessionResponse.from_orm(session) for session in sessions]

@router.get("/{session_id}", response_model=schemas.SessionResponse)
async def get_session(
    session_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """Get session details"""
    session = db.query(models.AISession).filter(
        models.AISession.id == session_id,
        models.AISession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return schemas.SessionResponse.from_orm(session)

@router.delete("/{session_id}")
async def delete_session(
    session_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """Delete a session"""
    session = db.query(models.AISession).filter(
        models.AISession.id == session_id,
        models.AISession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}