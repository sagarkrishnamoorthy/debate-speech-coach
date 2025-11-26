"""AI provider factory."""
from typing import Optional
from .base import BaseAIProvider
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from ..models.speech import AIProvider as AIProviderEnum
from ..config import settings


class AIProviderFactory:
    """Factory for creating AI provider instances."""
    
    @staticmethod
    def create(
        provider: Optional[AIProviderEnum] = None,
        api_key: Optional[str] = None
    ) -> BaseAIProvider:
        """
        Create an AI provider instance.
        
        Args:
            provider: The AI provider to use (defaults to settings)
            api_key: Optional API key override
            
        Returns:
            BaseAIProvider instance
        """
        provider = provider or AIProviderEnum(settings.default_ai_provider)
        
        if provider == AIProviderEnum.GEMINI:
            return GeminiProvider(api_key=api_key)
        elif provider == AIProviderEnum.OPENAI:
            return OpenAIProvider(api_key=api_key)
        elif provider == AIProviderEnum.ANTHROPIC:
            return AnthropicProvider(api_key=api_key)
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
