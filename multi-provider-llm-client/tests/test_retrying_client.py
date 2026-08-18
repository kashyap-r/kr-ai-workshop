from llm_client.base import LLMClient, LLMResponse
from llm_client.errors import RateLimitError
from llm_client.retry import RetryPolicy
from llm_client.retrying_client import RetryingLLMClient
from llm_client.errors import AuthenticationError

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
            latency_ms=10.0,
        )


client = FakeLLMClient()

policy = RetryPolicy(
    max_attempts=3,
    initial_delay_seconds=0.1,
    max_delay_seconds=1.0,
    jitter=False,
)

retrying_client = RetryingLLMClient(
    client=client,
    policy=policy,
)


response = retrying_client.generate(
    "Hello"
)


print("Response:", response.text)
print("Attempts:", client.attempts)





class AuthFailureClient(LLMClient):

    def __init__(self):

        self.attempts = 0

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        self.attempts += 1

        raise AuthenticationError(
            "Invalid credentials"
        )

auth_client = AuthFailureClient()

retrying_auth_client = RetryingLLMClient(
    client=auth_client,
    policy=policy,
)


try:

    retrying_auth_client.generate(
        "Hello"
    )

except AuthenticationError as e:

    print("\nAuthentication test:")
    print(f"Error: {e}")
    print(
        f"Attempts: "
        f"{auth_client.attempts}"
    )