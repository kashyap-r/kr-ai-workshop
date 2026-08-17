from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt:str) -> str:
        # Generate a response from the configured LLM.
        # Args:
            # prompt: User prompt.
        # 
        # Returns:
            # Generated text.

        # The expectation / contract is that any provider implementation must provide "generate(prompt: str) -> str"
        pass 

