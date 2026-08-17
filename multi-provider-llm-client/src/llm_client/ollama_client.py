"""
What did we do here"
We've hidden the below 
    Ollama SDK
    Ollama request format
    Ollama response format
    model handling

and the called doesn't need to know any of that
"""

from ollama import chat 
from .base import LLMClient

class OllamaClient(LLMClient):
    def __init__(self, model:str):
        self.model = model 

    def generate(self, prompt: str) -> str:
        response = chat(
            model=self.model, 
            messages=[
                {
                    "role": "user",
                    "content": "prompt"
                }
            ]
        )

        return response.message.content