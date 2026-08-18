"""
Author: Kashyap R
Date: 17th Aug, 2026
Change Description:
    What did we do here?
    We abstracted the Grow SDK, API Authentication, request format, response Format

Date: 18th Aug, 2026
Update: Added latency measurement to the generate method. The time taken for the Groq API call is now calculated and included in the LLMResponse object. 
        This allows users to see how long it took to generate a response from the model, which can be useful for performance monitoring and optimization
"""

import time

from groq import Groq
from groq import (
    APIConnectionError,
    APITimeoutError,
    APIStatusError,
    AuthenticationError as GroqAuthenticationError,
    NotFoundError,
    RateLimitError as GroqRateLimitError,
)

from .base import LLMClient, LLMResponse
from .errors import (
    AuthenticationError,
    ModelNotFoundError,
    RateLimitError,
    LLMConnectionError,
    ProviderError,
)

class GroqClient(LLMClient):

    def __init__(self, api_key: str, model: str, timeout_seconds: float):
        self.client = Groq(api_key=api_key, timeout=timeout_seconds)
        self.model = model

    def generate(self, prompt: str) -> LLMResponse:
        start = time.perf_counter()

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        except GroqAuthenticationError as e:
            raise AuthenticationError(
                "Groq authentication failed."
            ) from e

        except NotFoundError as e:
            raise ModelNotFoundError(
                f"Groq model '{self.model}' was not found."
            ) from e

        except GroqRateLimitError as e:
            raise RateLimitError(
                "Groq rate limit or quota exceeded."
            ) from e

        except APIConnectionError as e:
            raise LLMConnectionError(
                "Unable to connect to Groq."
            ) from e

        except APIStatusError as e:
            raise ProviderError(
                f"Groq API error: {e}",
                provider="groq",
                status_code=e.status_code,
            ) from e

        except Exception as e:
            raise ProviderError(
                f"Unexpected Groq error: {e}",
                provider="groq",
            ) from e

        except APITimeoutError as e:
            raise LLMConnectionError(
                "Groq request timed out."
            ) from e

        except APIConnectionError as e:
            raise LLMConnectionError(
                "Unable to connect to Groq."
            ) from e

        latency_ms = (time.perf_counter() - start) * 1000

        usage = response.usage

        return LLMResponse(
            text=response.choices[0].message.content,
            provider="groq",
            model=self.model,
            latency_ms=latency_ms,
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
        )