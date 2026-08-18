"""
Author: Kashyap Rajpurohit
Date: 18th Aug, 2026
Description: This file contains custom error classes for the LLM client. 
These errors are used to handle specific situations that may arise when interacting with different LLM providers. 
By defining these custom exceptions, we can provide more meaningful error messages and handle errors in a more structured way.
"""

class LLMError(Exception):
    """Base class for all LLM client errors."""
    pass

class AuthenticationError(LLMError):
    """Raised when there is an authentication error with the LLM provider."""
    pass

class ModelNotFoundError(LLMError):
    """Raised when the specified model is not found with the LLM provider."""
    pass

class RateLimitError(LLMError):
    """Raised when the LLM provider rate limit is exceeded."""
    pass

class LLMConnectionError(LLMError):
    """Raised when there is a connection error with the LLM provider."""
    pass

class ProviderError(LLMError):
    """Unexpected provider/API failure."""

    def __init__(
        self,
        message: str,
        *,
        provider: str | None = None,
        status_code: int | None = None,
    ):
        super().__init__(message)

        self.provider = provider
        self.status_code = status_code

class InvalidRequestError(LLMError):
    """Raised when the request to the LLM provider is invalid."""
    pass