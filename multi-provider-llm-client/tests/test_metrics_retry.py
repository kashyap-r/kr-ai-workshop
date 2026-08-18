from llm_client.base import LLMClient, LLMResponse
from llm_client.errors import RateLimitError
from llm_client.retry import RetryPolicy
from llm_client.retrying_client import RetryingLLMClient
from llm_client.metrics_client import MetricsLLMClient


class FakeLLMClient(LLMClient):

    def __init__(self):

        self.attempts = 0

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        self.attempts += 1

        if self.attempts < 3:

            raise RateLimitError(
                "Simulated rate limit"
            )

        return LLMResponse(
            text="Success!",
            provider="fake",
            model="fake-model",
        )


base_client = FakeLLMClient()

retry_client = RetryingLLMClient(
    client=base_client,
    policy=RetryPolicy(
        max_attempts=3,
        initial_delay_seconds=0.1,
        max_delay_seconds=1.0,
        jitter=False,
    ),
)

metrics_client = MetricsLLMClient(
    client=retry_client,
)


response = metrics_client.generate(
    "Hello"
)


print("\nResponse:")
print(response.text)

print("\nMetrics:")
print(
    f"Request ID: "
    f"{response.metrics.request_id}"
)

print(
    f"Provider: "
    f"{response.metrics.provider}"
)

print(
    f"Model: "
    f"{response.metrics.model}"
)

print(
    f"Latency: "
    f"{response.metrics.latency_ms:.2f} ms"
)

print(
    f"Attempts: "
    f"{response.metrics.attempts}"
)

print(
    f"Retries: "
    f"{response.metrics.retry_count}"
)

print(
    f"Retry delay: "
    f"{response.metrics.retry_delay_ms:.2f} ms"
)

print(
    f"Success: "
    f"{response.metrics.success}"
)