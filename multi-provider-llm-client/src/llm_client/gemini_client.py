"""
Author: Kashyap R
Date: 17th Aug, 2026
Change Description:
    What did we do here?
    We abstracted the Gemni SDK, API Authentication, Gemini request format, Gemini Response Format

Date: 18th Aug, 2026
Update: Added latency measurement to the generate method. The time taken for the Gemini API call is now calculated and included in the LLMResponse object. 
        This allows users to see how long it took to generate a response from the model, which can be useful for performance monitoring and optimization.
"""

import time
from google import genai
from .base import LLMClient, LLMResponse


class GeminiClient(LLMClient):

    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> LLMResponse:
        start = time.perf_counter()
        response = self.client.models.generate_content(model=self.model, contents=prompt)   
        latency_ms = (time.perf_counter() - start) * 1000

        usage = getattr(response, "usage_metadata", None)

        return LLMResponse(
            text=response.text,
            provider="gemini",
            model=self.model,
            latency_ms=latency_ms,
            input_tokens=getattr(
                usage,
                "prompt_token_count",
                None
            ),
            output_tokens=getattr(usage, "candidates_token_count", None),
            total_tokens=getattr(usage, "total_token_count", None),
        )
    