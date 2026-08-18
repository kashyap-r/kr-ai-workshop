from .base import LLMClient, LLMResponse
from .retry import (
    RetryPolicy,
    execute_with_retry,
)


class RetryingLLMClient(LLMClient):

    def __init__(
        self,
        client: LLMClient,
        policy: RetryPolicy,
    ):
        self.client = client
        self.policy = policy

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        return execute_with_retry(
            lambda: self.client.generate(prompt),
            self.policy,
        )