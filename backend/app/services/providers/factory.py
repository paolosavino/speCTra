from typing import Dict, Type
from app.services.providers.base import BaseProvider
from app.services.providers.openai import OpenAIProvider
from app.services.providers.anthropic import AnthropicProvider
from app.services.providers.gemini import GeminiProvider

class ProviderFactory:
    _providers: Dict[str, Type[BaseProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
        "google": GeminiProvider # alias
    }

    @classmethod
    def get_provider(cls, provider_name: str) -> BaseProvider:
        provider_class = cls._providers.get(provider_name.lower())
        if not provider_class:
            # Default to OpenAI if unknown or logic implies fallback
            # Or raise error. Let's default to OpenAI for robustness as "Universal" usually implies a default.
            # But strictness is better for debugging.
            # Let's check if provider_name is mapping to a model name prefix for auto-routing?
            # For now, simplistic factory.
            if "claude" in provider_name.lower():
                 return AnthropicProvider()
            if "gemini" in provider_name.lower():
                 return GeminiProvider()
            
            return OpenAIProvider()
            
        return provider_class()
