from typing import Any, Dict, Optional

from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "speCTra"
    API_V1_STR: str = "/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./spectra.db"
    
    # Security
    SECRET_KEY: str = "super-secret-key-please-change-in-production"
    
    # AI Providers (to be expanded)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
