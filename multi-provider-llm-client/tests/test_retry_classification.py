from llm_client.errors import (
    AuthenticationError,
    ModelNotFoundError,
    RateLimitError,
    LLMConnectionError,
    ProviderError,
)

from llm_client.retry import is_retryable


tests = [
    (
        AuthenticationError("bad key"),
        False,
    ),

    (
        ModelNotFoundError("bad model"),
        False,
    ),

    (
        RateLimitError("quota exceeded"),
        True,
    ),

    (
        LLMConnectionError("network failure"),
        True,
    ),

    (
        ProviderError(
            "bad request",
            provider="groq",
            status_code=400,
        ),
        False,
    ),

    (
        ProviderError(
            "rate limited",
            provider="groq",
            status_code=429,
        ),
        True,
    ),

    (
        ProviderError(
            "server error",
            provider="groq",
            status_code=500,
        ),
        True,
    ),

    (
        ProviderError(
            "gateway timeout",
            provider="groq",
            status_code=504,
        ),
        True,
    ),

    (
        ProviderError(
            "unknown provider failure",
            provider="groq",
        ),
        False,
    ),
]


for error, expected in tests:

    actual = is_retryable(error)

    status = "PASS" if actual == expected else "FAIL"

    print(
        f"{status}: "
        f"{type(error).__name__} "
        f"→ retry={actual}"
    )