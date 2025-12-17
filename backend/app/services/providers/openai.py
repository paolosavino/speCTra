from app.services.providers.base import BaseProvider
from app.core.config import settings
import httpx
from fastapi import HTTPException
from typing import Any, AsyncGenerator, Dict, Union

class OpenAIProvider(BaseProvider):
    async def chat_completion(
        self, 
        request: Any
    ) -> Union[Dict[str, Any], AsyncGenerator]:
        
        if not settings.OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail="OpenAI API Key not configured")

        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = request.dict(exclude_none=True)
        
        if not request.stream:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        json=payload,
                        headers=headers,
                        timeout=60.0
                    )
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as exc:
                     raise HTTPException(status_code=exc.response.status_code, detail=f"OpenAI Provider Error: {exc.response.text}")
                except httpx.RequestError as exc:
                    raise HTTPException(status_code=502, detail=f"OpenAI Connection Error: {str(exc)}")

        # Streaming
        async def stream_generator():
            async with httpx.AsyncClient() as client:
                try:
                    async with client.stream(
                        "POST", 
                        "https://api.openai.com/v1/chat/completions", 
                        json=payload, 
                        headers=headers,
                        timeout=60.0
                    ) as response:
                         response.raise_for_status()
                         async for chunk in response.aiter_bytes():
                             yield chunk
                except httpx.HTTPStatusError as exc:
                    # In stream, we can't easily raise HTTP exception to the user once stream started, 
                    # but if it fails immediately, we can catch it.
                    # A better approach for production is robust error handling in stream.
                     yield f"data: {{\"error\": \"{exc.response.text}\"}}\n\n"

        return stream_generator()
