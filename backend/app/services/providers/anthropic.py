from app.services.providers.base import BaseProvider
from app.core.config import settings
import httpx
from fastapi import HTTPException
from typing import Any, AsyncGenerator, Dict, Union

class AnthropicProvider(BaseProvider):
    async def chat_completion(
        self, 
        request: Any
    ) -> Union[Dict[str, Any], AsyncGenerator]:
        
        if not settings.ANTHROPIC_API_KEY:
            raise HTTPException(status_code=500, detail="Anthropic API Key not configured")

        headers = {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        # Mapping standard request to Anthropic format
        # OpenAI: messages=[{"role": "user", "content": "..."}]
        # Anthropic: messages=[{"role": "user", "content": "..."}] (Similar structure now)
        # But max_tokens -> max_tokens, but required.
        
        payload = {
            "model": request.model, # e.g. claude-3-opus-20240229
            "messages": [m.dict() for m in request.messages],
            "max_tokens": request.max_tokens or 1024, # Anthropic requires max_tokens
        }
        
        if request.temperature:
            payload["temperature"] = request.temperature
        
        if request.stream:
             payload["stream"] = True

        if not request.stream:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        "https://api.anthropic.com/v1/messages",
                        json=payload,
                        headers=headers,
                        timeout=60.0
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    # Convert Response back to OpenAI Format
                    # Anthropic: { "id": "msg_...", "content": [{"text": "..."}] }
                    # OpenAI: { "id": "...", "choices": [{"message": {"content": "..."}}] }
                    
                    content_text = ""
                    if "content" in data and len(data["content"]) > 0:
                        content_text = data["content"][0]["text"]
                        
                    return {
                        "id": data.get("id"),
                        "object": "chat.completion",
                        "created": 1234567890, # mock timestamp or parse
                        "model": data.get("model"),
                        "choices": [
                            {
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": content_text
                                },
                                "finish_reason": data.get("stop_reason")
                            }
                        ],
                        "usage": {
                            "prompt_tokens": data.get("usage", {}).get("input_tokens", 0),
                            "completion_tokens": data.get("usage", {}).get("output_tokens", 0),
                            "total_tokens": 0
                        }
                    }

                except httpx.HTTPStatusError as exc:
                     raise HTTPException(status_code=exc.response.status_code, detail=f"Anthropic Provider Error: {exc.response.text}")
                except httpx.RequestError as exc:
                    raise HTTPException(status_code=502, detail=f"Anthropic Connection Error: {str(exc)}")

        # Streaming support (omitted for brevity in this step, can add if requested)
        # For now raising error or returning non-stream
        raise HTTPException(status_code=501, detail="Streaming for Anthropic not yet implemented in MVP")
