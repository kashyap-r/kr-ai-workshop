"""
Author: Kashyap R
Date: 17th Aug, 2026
Change Description:
    What did we do here?
    We abstracted the Gemni SDK, API Authentication, Gemini request format, Gemini Response Format
"""

from google import genai
from .base import LLMClient

class GeminiClent (LLMClient):
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str)-> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        ) 
        return response.text
    