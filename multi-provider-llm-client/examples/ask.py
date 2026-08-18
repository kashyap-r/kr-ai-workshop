from llm_client.config import load_config
from llm_client.errors import LLMError
from llm_client.factory import LLMFactory
from llm_client.retrying_client import RetryingLLMClient
from llm_client.metrics_client import MetricsLLMClient
from llm_client.metrics_collector import MetricsCollector
from llm_client.logging_config import (
    configure_logging,
)

def main():

    configure_logging()

    # ---------------------------------
    # Load configuration
    # ---------------------------------

    config = load_config()

    # ---------------------------------
    # Provider
    # ---------------------------------

    client = LLMFactory.create(
        config.provider,
        config,
    )

    # ---------------------------------
    # Metrics collector
    # ---------------------------------

    collector = MetricsCollector()

    # ---------------------------------
    # Retry / resilience
    # ---------------------------------

    client = RetryingLLMClient(
        client=client,
        policy=config.retry_policy,
        on_event=collector.record_retry_event,
    )

    # ---------------------------------
    # Observability
    # ---------------------------------

    client = MetricsLLMClient(
        client=client,
        collector=collector,
    )

    # ---------------------------------
    # Execute request
    # ---------------------------------

    prompt = "Tell me something fun today"

    try:

        response = client.generate(
            prompt
        )

        # ---------------------------------
        # Response
        # ---------------------------------

        print("\nResponse:")
        print(response.text)

        # ---------------------------------
        # Metrics
        # ---------------------------------

        if response.metrics:

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
                f"Success: "
                f"{response.metrics.success}"
            )

        # ---------------------------------
        # Token usage
        # ---------------------------------

        print("\nUsage:")

        if response.usage:

            print(
                f"Input tokens: "
                f"{response.usage.input_tokens}"
            )

            print(
                f"Output tokens: "
                f"{response.usage.output_tokens}"
            )

            print(
                f"Total tokens: "
                f"{response.usage.total_tokens}"
            )

        else:

            print(
                "Token usage unavailable."
            )

    except LLMError as e:

        print(
            f"\nLLM request failed: {e}"
        )


if __name__ == "__main__":
    main()