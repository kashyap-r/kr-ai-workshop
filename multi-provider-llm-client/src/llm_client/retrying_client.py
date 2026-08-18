from .base import LLMClient, LLMResponse
from .retry import (
    RetryPolicy,
    execute_with_retry,
    RetryEventCallback,
)


class RetryingLLMClient(LLMClient):

    def __init__(
        self,
        client: LLMClient,
        policy: RetryPolicy,
        on_event: RetryEventCallback | None = None,
    ):
        self.client = client
        self.policy = policy
        self.on_event = on_event

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        retry_result = execute_with_retry(
            lambda: self.client.generate(prompt),
            self.policy,
            on_event=self.on_event,
        )

        return retry_result.result