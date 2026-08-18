from abc import ABC, abstractmethod
from dataclasses import dataclass
from .metrics import LLMMetrics, LLMUsage


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    usage: LLMUsage | None = None
    metrics: LLMMetrics | None = None

class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt:str) -> LLMResponse:
        # Generate a response from the configured LLM.
        # The contract now is to generate the LLMResponse object with all the required fields.
        pass 

