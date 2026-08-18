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

from .base import LLMClient, LLMResponse


class GroqClient(LLMClient):

    def __init__( self, api_key: str, model: str):
        self.client = Groq( api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> LLMResponse:
        start = time.perf_counter()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

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