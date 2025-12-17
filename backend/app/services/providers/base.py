from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, Union
from pydantic import BaseModel

# We will move models here or import them to avoid circular deps
# For now, defining a common interface using dicts or generic types 
# to keep it flexible, but ideally validation happens before hitting the provider.

class BaseProvider(ABC):
    @abstractmethod
    async def chat_completion(
        self, 
        request: Any # Typed as ChatCompletionRequest
    ) -> Union[Dict[str, Any], AsyncGenerator]:
        """
        Standard interface for standard non-streaming and streaming responses.
        Must return standard OpenAI-compatible format if possible, or the provider's format 
        normalized by the adapter.
        """
        pass
