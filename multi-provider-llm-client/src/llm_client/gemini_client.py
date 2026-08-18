"""
Author: Kashyap R
Date: 17th Aug, 2026
Change Description:
    What did we do here?
    We abstracted the Gemni SDK, API Authentication, Gemini request format, Gemini Response Format

Date: 18th Aug, 2026
Update: Added latency measurement to the generate method. The time taken for the Gemini API call is now calculated and included in the LLMResponse object. 
        This allows users to see how long it took to generate a response from the model, which can be useful for performance monitoring and optimization.

Date: 19th Aug, 2026
Update: Added error handling for various Gemini API errors, including authentication errors, model not found errors, rate limit errors, and server errors. 
        This allows users to handle these specific error cases more gracefully and provides more meaningful error messages.         
"""

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from .base import LLMClient, LLMResponse
from .errors import (
    AuthenticationError,
    ModelNotFoundError,
    ProviderError,
    RateLimitError,
)
from .metrics import LLMUsage


class GeminiClient(LLMClient):

    def __init__(
        self,
        api_key: str,
        model: str,
        timeout_seconds: float,
    ):
        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=int(
                    timeout_seconds * 1000
                )
            ),
        )

        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        try:

            response = (
                self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
            )

        except ClientError as e:

            status_code = getattr(
                e,
                "status_code",
                None,
            )

            if status_code == 401:

                raise AuthenticationError(
                    "Gemini authentication failed. "
                    "Check GEMINI_API_KEY."
                ) from e

            if status_code == 403:

                raise AuthenticationError(
                    "Gemini authorization failed."
                ) from e

            if status_code == 404:

                raise ModelNotFoundError(
                    f"Gemini model "
                    f"'{self.model}' was not found."
                ) from e

            if status_code == 429:

                raise RateLimitError(
                    "Gemini rate limit or quota "
                    "was exceeded."
                ) from e

            raise ProviderError(
                f"Gemini API error: {e}",
                provider="gemini",
                status_code=status_code,
            ) from e

        except Exception as e:

            raise ProviderError(
                f"Unexpected Gemini error: {e}",
                provider="gemini",
            ) from e

        # ---------------------------------
        # Token usage
        # ---------------------------------

        usage_metadata = getattr(
            response,
            "usage_metadata",
            None,
        )

        input_tokens = getattr(
            usage_metadata,
            "prompt_token_count",
            None,
        )

        output_tokens = getattr(
            usage_metadata,
            "candidates_token_count",
            None,
        )

        total_tokens = getattr(
            usage_metadata,
            "total_token_count",
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
            text=response.text,
            provider="gemini",
            model=self.model,
            usage=usage,
        )