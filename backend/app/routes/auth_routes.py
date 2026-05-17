from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database
from ..services.auth_service import AuthService
from ..auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=schemas.TokenResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Register a new user"""
    try:
        db_user = AuthService.register_user(db, user)
        access_token = AuthService.create_access_token(db_user)
        return schemas.TokenResponse(access_token=access_token, user_id=db_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=schemas.TokenResponse)
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    """Login user"""
    try:
        user = AuthService.authenticate_user(db, user_credentials.username, user_credentials.password)
        access_token = AuthService.create_access_token(user)
        return schemas.TokenResponse(access_token=access_token, user_id=user.id)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))