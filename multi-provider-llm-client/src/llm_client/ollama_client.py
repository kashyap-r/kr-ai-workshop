"""
Author: Kashyap R
Date: 17th Aug, 2026
Description: This file contains the OllamaClient class, which is a client for interacting with the Ollama LLM API. 
            It provides a method to generate responses from the model based on a given prompt. 
            The implementation abstracts away the details of the Ollama SDK, request and response formats, and model handling, 
            allowing users to interact with the LLM without needing to know these specifics.

            What did we do here"
                We've hidden the below 
                Ollama SDK
                Ollama request format
                Ollama response format
                model handling
            and the caller doesn't need to know any of that

Date: 18th Aug, 2026
Update: Added latency measurement to the generate method. The time taken for the Ollama API call is now calculated and included in the LLMResponse object. 
        This allows users to see how long it took to generate a response from the model, which can be useful for performance monitoring and optimization.
"""

from ollama import Client, ResponseError

from .base import LLMClient, LLMResponse
from .errors import (
    LLMConnectionError,
    ModelNotFoundError,
    ProviderError,
)
from .metrics import LLMUsage


class OllamaClient(LLMClient):

    def __init__(
        self,
        model: str,
        timeout_seconds: float,
    ):
        self.client = Client(
            host="http://localhost:11434",
            timeout=timeout_seconds,
        )

        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        try:

            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

        except ResponseError as e:

            status_code = getattr(
                e,
                "status_code",
                None,
            )

            if status_code == 404:

                raise ModelNotFoundError(
                    f"Ollama model "
                    f"'{self.model}' was not found."
                ) from e

            raise ProviderError(
                f"Ollama error: {e}",
                provider="ollama",
                status_code=status_code,
            ) from e

        except Exception as e:

            raise LLMConnectionError(
                "Unable to connect to Ollama. "
                "Is Ollama running?"
            ) from e

        # ---------------------------------
        # Token usage
        # ---------------------------------

        input_tokens = getattr(
            response,
            "prompt_eval_count",
            None,
        )

        output_tokens = getattr(
            response,
            "eval_count",
            None,
        )

        total_tokens = None

        if (
            input_tokens is not None
            and output_tokens is not None
        ):
            total_tokens = (
                input_tokens
                + output_tokens
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
            text=response.message.content,
            provider="ollama",
            model=self.model,
            usage=usage,
        )