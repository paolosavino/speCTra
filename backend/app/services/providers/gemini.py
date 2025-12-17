from app.services.providers.base import BaseProvider
from app.core.config import settings
import httpx
from fastapi import HTTPException
from typing import Any, AsyncGenerator, Dict, Union

class GeminiProvider(BaseProvider):
    async def chat_completion(
        self, 
        request: Any
    ) -> Union[Dict[str, Any], AsyncGenerator]:
        
        if not settings.GEMINI_API_KEY:
             raise HTTPException(status_code=500, detail="Gemini API Key not configured")

        # Gemini REST API URL
        # e.g. https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=...
        model_name = request.model if "gemini" in request.model else "gemini-pro"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
        
        # Mapping standard request to Gemini format
        # OpenAI: messages=[{"role": "user", "content": "..."}]
        # Gemini: contents=[{"role": "user", "parts": [{"text": "..."}]}]
        # Note: Gemini uses "user" and "model" roles (not assistant)
        
        contents = []
        for m in request.messages:
            role = "user" if m.role == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": m.content}]
            })
            
        payload = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": request.max_tokens or 1024,
                "temperature": request.temperature or 0.9
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Normalize Response
                # Gemini: { "candidates": [ { "content": { "parts": [ { "text": "..." } ] } } ] }
                
                content_text = ""
                if "candidates" in data and len(data["candidates"]) > 0:
                     parts = data["candidates"][0].get("content", {}).get("parts", [])
                     if parts:
                         content_text = parts[0].get("text", "")
                
                return {
                    "id": "gemini-id", # Gemini doesn't return ID in the same way
                    "object": "chat.completion",
                    "created": 1234567,
                    "model": model_name,
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": content_text
                            },
                            "finish_reason": "stop"
                        }
                    ],
                    "usage": { "total_tokens": 0 } # Usage not always returned simply in REST
                }

            except httpx.HTTPStatusError as exc:
                    raise HTTPException(status_code=exc.response.status_code, detail=f"Gemini Provider Error: {exc.response.text}")
            except httpx.RequestError as exc:
                raise HTTPException(status_code=502, detail=f"Gemini Connection Error: {str(exc)}")
