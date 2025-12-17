from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.api import deps
from app.core.database import get_session
from app.models.api_key import ApiKey
import secrets

router = APIRouter()

class ApiKeyCreate(BaseModel):
    name: str

class ApiKeyRead(BaseModel):
    id: int
    key_hash: str # In real world, we might hide this or show only once. Here show for demo.
    name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

@router.get("/api-keys", response_model=List[ApiKey])
def read_api_keys(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    # current_user: User = Depends(deps.get_current_active_user) # In future
):
    keys = session.exec(select(ApiKey).offset(skip).limit(limit)).all()
    return keys

@router.post("/api-keys", response_model=ApiKey)
def create_api_key(
    key_in: ApiKeyCreate,
    session: Session = Depends(get_session),
    # current_user...
):
    # Generate a random key
    generated_key = f"sk-spectra-{secrets.token_urlsafe(16)}"
    db_key = ApiKey(key_hash=generated_key, name=key_in.name)
    session.add(db_key)
    session.commit()
    session.refresh(db_key)
    return db_key

@router.delete("/api-keys/{key_id}")
def delete_api_key(
    key_id: int,
    session: Session = Depends(get_session),
):
    key = session.get(ApiKey, key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    session.delete(key)
    session.commit()
    return {"ok": True}
