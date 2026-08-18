"""
Author: Kashyap Rajpurohit
Date: 17th Aug, 2026
Description: This file contains the LLMFactory class, which is responsible for creating instances of LLMClient based on the specified provider and configuration.
            The factory pattern is used here to encapsulate the creation logic and provide a simple interface for obtaining LLMClient instances. 
            The factory supports multiple providers, including Ollama, Gemini, and Groq, and ensures that the appropriate client is instantiated with the correct configuration.
            The factory also handles error cases, such as missing API keys or unsupported providers, by raising appropriate exceptions.
            What did we do here"
                We've hidden the below
                LLMClient creation logic
                LLMClient configuration handling
                LLMClient error handling
            and the caller doesn't need to know any of that
"""

from .base import LLMClient
from .config import LLMConfig
from .errors import ProviderError
from .gemini_client import GeminiClient
from .groq_client import GroqClient
from .ollama_client import OllamaClient

class LLMFactory:
    @staticmethod
    def create(provider: str, config: LLMConfig,) -> LLMClient:
        provider = provider.lower().strip()
        if provider == "ollama":
            return OllamaClient(model=config.ollama_model, timeout_seconds=config.timeout_seconds,)

        if provider == "gemini":
            if not config.gemini_api_key:
                raise ProviderError("GEMINI_API_KEY is not configured.")
            return GeminiClient(api_key=config.gemini_api_key, model=config.gemini_model, timeout_seconds=config.timeout_seconds,)

        if provider == "groq":
            if not config.groq_api_key:
                raise ProviderError("GROQ_API_KEY is not configured.")
            return GroqClient(api_key=config.groq_api_key, model=config.groq_model, timeout_seconds=config.timeout_seconds,)
        raise ProviderError(f"Unsupported LLM provider: '{provider}'")