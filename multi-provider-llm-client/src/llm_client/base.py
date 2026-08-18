from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    latency_ms: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    # metadata: dict | None = None

class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt:str) -> LLMResponse:
        # Generate a response from the configured LLM.
        # The contract now is to generate the LLMResponse object with all the required fields.
        pass 

