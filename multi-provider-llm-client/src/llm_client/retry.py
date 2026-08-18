from dataclasses import dataclass
import random
import time
from .errors import (
    AuthenticationError,
    ModelNotFoundError,
    RateLimitError,
    LLMConnectionError,
    ProviderError,
)


@dataclass
class RetryPolicy:

    max_attempts: int = 3

    initial_delay_seconds: float = 1.0

    max_delay_seconds: float = 10.0

    backoff_multiplier: float = 2.0

    jitter: bool = True




def calculate_delay(
    policy: RetryPolicy,
    attempt: int,
) -> float:

    delay = (
        policy.initial_delay_seconds
        * (
            policy.backoff_multiplier
            ** (attempt - 1)
        )
    )

    delay = min(
        delay,
        policy.max_delay_seconds,
    )

    if policy.jitter:

        delay = random.uniform(
            0,
            delay,
        )

    return delay



def is_retryable(error: Exception) -> bool:

    # These should never be retried.
    if isinstance(
        error,
        (
            AuthenticationError,
            ModelNotFoundError,
        ),
    ):
        return False

    # These are normally transient.
    if isinstance(
        error,
        (
            RateLimitError,
            LLMConnectionError,
        ),
    ):
        return True

    # Provider errors depend on HTTP status.
    if isinstance(error, ProviderError):

        status_code = error.status_code

        if status_code is None:
            return False

        # Explicitly rate limited.
        if status_code == 429:
            return True

        # Request timeout.
        if status_code == 408:
            return True

        # Server-side failures.
        if 500 <= status_code <= 599:
            return True

        # Other 4xx errors are normally permanent.
        return False

    return False




def execute_with_retry(
    operation,
    policy: RetryPolicy,
):
    
    for attempt in range(
        1,
        policy.max_attempts + 1,
    ):

        try:

            return operation()

        except Exception as error:

            if not is_retryable(error):

                raise

            if attempt == policy.max_attempts:

                raise

            delay = calculate_delay(
                policy,
                attempt,
            )

            print(
                f"Attempt {attempt} failed: "
                f"{type(error).__name__}. "
                f"Retrying in "
                f"{delay:.2f}s..."
            )

            time.sleep(delay)