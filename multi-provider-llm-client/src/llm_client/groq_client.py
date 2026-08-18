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
from groq import (
    Groq,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError as GroqAuthenticationError,
    NotFoundError,
    RateLimitError as GroqRateLimitError,
)

from .base import LLMClient, LLMResponse
from .errors import (
    AuthenticationError,
    LLMConnectionError,
    ModelNotFoundError,
    ProviderError,
    RateLimitError,
)
from .metrics import LLMUsage


class GroqClient(LLMClient):

    def __init__(
        self,
        api_key: str,
        model: str,
        timeout_seconds: float,
    ):
        self.client = Groq(
            api_key=api_key,
            timeout=timeout_seconds,
        )

        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        try:

            response = (
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                )
            )

        except GroqAuthenticationError as e:

            raise AuthenticationError(
                "Groq authentication failed. "
                "Check GROQ_API_KEY."
            ) from e

        except GroqRateLimitError as e:

            raise RateLimitError(
                "Groq rate limit or quota "
                "was exceeded."
            ) from e

        except NotFoundError as e:

            raise ModelNotFoundError(
                f"Groq model "
                f"'{self.model}' was not found."
            ) from e

        except APITimeoutError as e:

            raise LLMConnectionError(
                "Groq request timed out."
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

        # ---------------------------------
        # Token usage
        # ---------------------------------

        usage_data = getattr(
            response,
            "usage",
            None,
        )

        input_tokens = getattr(
            usage_data,
            "prompt_tokens",
            None,
        )

        output_tokens = getattr(
            usage_data,
            "completion_tokens",
            None,
        )

        total_tokens = getattr(
            usage_data,
            "total_tokens",
            None,
        )

        usage = LLMUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )

        # ---------------------------------
        # Normalized response
        # ---------------------------------

        return LLMResponse(
            text=response.choices[0].message.content,
            provider="groq",
            model=self.model,
            usage=usage,
        )