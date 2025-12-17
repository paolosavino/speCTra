from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.api_key import ApiKey

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_api_key(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> ApiKey:
    # simple hash check mechanism placeholder
    # In real world, we would hash the incoming token and compare with stored hash
    # For now, let's assume the token is the key_hash for simplicity in this MVP step
    # or better, let's assume raw token is passed and we query by key_hash (simulated)
    
    query = select(ApiKey).where(ApiKey.key_hash == token)
    api_key = session.exec(query).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not api_key.is_active:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return api_key
