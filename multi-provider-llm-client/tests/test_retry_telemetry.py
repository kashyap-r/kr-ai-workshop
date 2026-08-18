from llm_client.base import (
    LLMClient,
    LLMResponse,
)
from llm_client.errors import (
    RateLimitError,
)
from llm_client.retry import RetryPolicy
from llm_client.retrying_client import (
    RetryingLLMClient,
)
from llm_client.metrics_client import (
    MetricsLLMClient,
)
from llm_client.metrics_collector import (
    MetricsCollector,
)
from llm_client.logging_config import (
    configure_logging,
)


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


def main():

    configure_logging()

    provider = FakeLLMClient()

    collector = MetricsCollector()

    retry_client = RetryingLLMClient(
        client=provider,
        policy=RetryPolicy(
            max_attempts=3,
            initial_delay_seconds=0.1,
            max_delay_seconds=1.0,
            jitter=False,
        ),
        on_event=(
            collector.record_retry_event
        ),
    )

    client = MetricsLLMClient(
        client=retry_client,
        collector=collector,
    )

    response = client.generate(
        "Hello"
    )

    print("\nResponse:")
    print(response.text)

    print("\nFinal metrics:")

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


if __name__ == "__main__":
    main()