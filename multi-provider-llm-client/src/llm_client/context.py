from dataclasses import dataclass

from .retry import RetryExecution


@dataclass
class LLMExecutionContext:

    retry: RetryExecution | None = None