from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database
from ..services.bitcoin_service import BitcoinService
from ..auth import get_current_user

router = APIRouter()

@router.post("", response_model=schemas.ScriptResponse)
async def create_script(
    script: schemas.ScriptCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """Create a new script"""
    db_script = models.Script(
        user_id=current_user.id,
        content=script.content
    )
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return schemas.ScriptResponse.from_orm(db_script)

@router.get("", response_model=List[schemas.ScriptResponse])
async def list_scripts(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """List user's scripts"""
    scripts = db.query(models.Script).filter(
        models.Script.user_id == current_user.id
    ).order_by(models.Script.created_at.desc()).all()
    return [schemas.ScriptResponse.from_orm(script) for script in scripts]

@router.get("/{script_id}", response_model=schemas.ScriptResponse)
async def get_script(
    script_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """Get script details"""
    script = db.query(models.Script).filter(
        models.Script.id == script_id,
        models.Script.user_id == current_user.id
    ).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    return schemas.ScriptResponse.from_orm(script)

@router.post("/validate", response_model=schemas.ValidationResponse)
async def validate_script(
    request: schemas.ValidationRequest,
    current_user: models.User = Depends(get_current_user)
):
    """Validate a Bitcoin script"""
    result = BitcoinService.validate_script(request.content)
    return schemas.ValidationResponse(**result)

@router.delete("/{script_id}")
async def delete_script(
    script_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """Delete a script"""
    script = db.query(models.Script).filter(
        models.Script.id == script_id,
        models.Script.user_id == current_user.id
    ).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")

    db.delete(script)
    db.commit()
    return {"message": "Script deleted successfully"}