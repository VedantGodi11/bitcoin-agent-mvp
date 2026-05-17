from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int

# Session schemas
class SessionCreate(BaseModel):
    pass  # No fields needed for creation

class SessionResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    session_id: int

class MessageResponse(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Chat schemas
class ChatRequest(BaseModel):
    session_id: int
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime

class HistoryResponse(BaseModel):
    messages: List[MessageResponse]

# Script schemas
class ScriptBase(BaseModel):
    content: str

class ScriptCreate(ScriptBase):
    pass

class ScriptResponse(ScriptBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ScriptListResponse(BaseModel):
    scripts: List[ScriptResponse]

class ValidationRequest(BaseModel):
    content: str

class ValidationResponse(BaseModel):
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []