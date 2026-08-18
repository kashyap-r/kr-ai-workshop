from llm_client.errors import (
    AuthenticationError,
    RateLimitError,
)
from llm_client.retry import (
    RetryPolicy,
    execute_with_retry,
)


# -----------------------------
# Test 1: transient failure
# -----------------------------

attempts = 0


def flaky_operation():

    global attempts

    attempts += 1

    if attempts < 3:
        raise RateLimitError(
            "Simulated rate limit"
        )

    return "SUCCESS"


policy = RetryPolicy(
    max_attempts=3,
    initial_delay_seconds=0.1,
    max_delay_seconds=1.0,
    jitter=False,
)


result = execute_with_retry(
    flaky_operation,
    policy,
)

print("\nTest 1:")
print(f"Result: {result}")
print(f"Attempts: {attempts}")


# -----------------------------
# Test 2: non-retryable error
# -----------------------------

attempts = 0


def authentication_failure():

    global attempts

    attempts += 1

    raise AuthenticationError(
        "Simulated authentication failure"
    )


try:

    execute_with_retry(
        authentication_failure,
        policy,
    )

except AuthenticationError:

    print("\nTest 2:")
    print(
        f"Authentication failure "
        f"attempts: {attempts}"
    )