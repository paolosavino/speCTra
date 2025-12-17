from fastapi import APIRouter, Depends, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx
import json
from app.api import deps
from app.models.api_key import ApiKey
from app.core.config import settings
from app.services.providers.factory import ProviderFactory

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: bool = False
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None

@router.post("/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    current_key: ApiKey = Depends(deps.get_current_api_key),
    x_spectra_provider: Optional[str] = Header(default="openai", alias="x-spectra-provider")
):
    """
    Universal Chat Completions Endpoint.
    Proxies requests to the configured provider based on 'x-spectra-provider' header.
    Defaults to 'openai'.
    """
    
    # 1. Get Provider from Factory
    # Auto-detect if provider not explicitly set but model name gives hint
    provider_name = x_spectra_provider
    if provider_name == "openai" and "claude" in request.model:
        provider_name = "anthropic"
    elif provider_name == "openai" and "gemini" in request.model:
        provider_name = "gemini"

    try:
        provider = ProviderFactory.get_provider(provider_name)
    except Exception as e:
         raise HTTPException(status_code=400, detail=f"Invalid Provider: {str(e)}")

    # 2. Delegate to Provider
    return await provider.chat_completion(request)
