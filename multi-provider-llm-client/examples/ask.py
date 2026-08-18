from llm_client.config import load_config
from llm_client.errors import LLMError
from llm_client.factory import LLMFactory
from llm_client.retry import RetryPolicy
from llm_client.retrying_client import RetryingLLMClient


def main():

    config = load_config()

    client = LLMFactory.create(
        config.provider,
        config,
    )

    retry_policy = RetryPolicy(
        max_attempts=3,
        initial_delay_seconds=1.0,
        max_delay_seconds=10.0,
        backoff_multiplier=2.0,
        jitter=True,
    )

    client = RetryingLLMClient(
        client=client,
        policy=retry_policy,
    )

    try:

        response = client.generate(
            "Tell me something fun today"
        )

        print("\nResponse:")
        print(response.text)

        print("\nMetadata:")
        print(f"Provider: {response.provider}")
        print(f"Model: {response.model}")
        print(
            f"Latency: "
            f"{response.latency_ms:.2f} ms"
        )

    except LLMError as e:

        print(
            f"\nLLM request failed: {e}"
        )


if __name__ == "__main__":
    main()