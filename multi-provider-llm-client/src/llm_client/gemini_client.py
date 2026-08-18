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

import time

from google import genai
from google.genai import errors

from .base import LLMClient, LLMResponse
from .errors import (
    AuthenticationError,
    ModelNotFoundError,
    RateLimitError,
    LLMConnectionError,
    ProviderError,
)


class GeminiClient(LLMClient):

    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        self.client = genai.Client(
            api_key=api_key
        )
        self.model = model

    def generate(self, prompt: str) -> LLMResponse:

        start = time.perf_counter()

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

        except errors.ClientError as e:

            status_code = getattr(
                e,
                "code",
                None,
            )

            if status_code == 401:

                raise AuthenticationError(
                    "Gemini authentication failed."
                ) from e

            if status_code == 404:

                raise ModelNotFoundError(
                    f"Gemini model '{self.model}' was not found."
                ) from e

            if status_code == 429:

                raise RateLimitError(
                    "Gemini rate limit or quota exceeded."
                ) from e

            raise ProviderError(
                f"Gemini API error: {e}"
            ) from e

        except errors.ServerError as e:

            raise ProviderError(
                f"Gemini server error: {e}"
            ) from e

        except Exception as e:

            raise ProviderError(
                f"Unexpected Gemini error: {e}"
            ) from e

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        usage = getattr(
            response,
            "usage_metadata",
            None,
        )

        return LLMResponse(
            text=response.text,
            provider="gemini",
            model=self.model,
            latency_ms=latency_ms,
            input_tokens=getattr(
                usage,
                "prompt_token_count",
                None,
            ),
            output_tokens=getattr(
                usage,
                "candidates_token_count",
                None,
            ),
            total_tokens=getattr(
                usage,
                "total_token_count",
                None,
            ),
        )