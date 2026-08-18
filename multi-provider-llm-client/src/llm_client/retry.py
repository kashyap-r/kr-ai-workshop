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
from typing import Callable
from .request_context import (
    get_request_context,
)

RetryEventCallback = Callable[
    [str, dict],
    None,
]

@dataclass 
class RetryResult:
    result: object
    attempts: int
    retry_count: int
    retry_delay_seconds: float

@dataclass
class RetryExecution:
    attempts: int = 0
    retry_count: int = 0
    retry_delay_seconds: float = 0.0

@dataclass
class RetryPolicy:
    max_attempts: int = 3
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 10.0
    backoff_multiplier: float = 2.0
    jitter: bool = True

def calculate_delay(policy: RetryPolicy, attempt: int,) -> float:
    delay = (policy.initial_delay_seconds * ( policy.backoff_multiplier ** (attempt - 1)))
    delay = min(delay,policy.max_delay_seconds,)

    if policy.jitter:
        delay = random.uniform(0, delay,)
    return delay

def is_retryable(error: Exception) -> bool:
    # These should never be retried.
    if isinstance(error, (AuthenticationError, ModelNotFoundError,),):
        return False
    # These are normally transient.
    if isinstance(error, (RateLimitError, LLMConnectionError,),):
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
    on_event: RetryEventCallback | None = None,
) -> RetryResult:

    attempts = 0
    retry_count = 0
    total_retry_delay = 0.0

    context = get_request_context()

    for attempt in range(
        1,
        policy.max_attempts + 1,
    ):

        attempts = attempt

        if context:

            context.attempts = attempts

        # -----------------------------
        # Attempt started
        # -----------------------------

        if on_event:

            on_event(
                "attempt_started",
                {
                    "attempt": attempt,
                },
            )

        try:

            result = operation()

            # -----------------------------
            # Success
            # -----------------------------

            if on_event:

                on_event(
                    "request_succeeded",
                    {
                        "attempts": attempts,
                        "retry_count": retry_count,
                        "retry_delay_seconds": (
                            total_retry_delay
                        ),
                    },
                )

            return RetryResult(
                result=result,
                attempts=attempts,
                retry_count=retry_count,
                retry_delay_seconds=(
                    total_retry_delay
                ),
            )

        except Exception as error:

            if not is_retryable(error):

                if on_event:

                    on_event(
                        "request_failed",
                        {
                            "attempt": attempt,
                            "retry_count": retry_count,
                            "retry_delay_seconds": (
                                total_retry_delay
                            ),
                            "error_type": (
                                type(error).__name__
                            ),
                            "error_message": str(error),
                        },
                    )

                raise

            if attempt == policy.max_attempts:

                if on_event:

                    on_event(
                        "request_failed",
                        {
                            "attempt": attempt,
                            "retry_count": retry_count,
                            "retry_delay_seconds": (
                                total_retry_delay
                            ),
                            "error_type": (
                                type(error).__name__
                            ),
                            "error_message": str(error),
                        },
                    )

                raise

            delay = calculate_delay(
                policy,
                attempt,
            )

            retry_count += 1

            total_retry_delay += delay

            if context:

                context.retry_count = retry_count

                context.retry_delay_seconds = (
                    total_retry_delay
                )

            # -----------------------------
            # Retry event
            # -----------------------------

            if on_event:

                on_event(
                    "retry",
                    {
                        "attempt": attempt,
                        "retry_count": retry_count,
                        "delay_seconds": delay,
                        "error_type": (
                            type(error).__name__
                        ),
                        "error_message": str(error),
                    },
                )

            print(
                f"Attempt {attempt} failed: "
                f"{type(error).__name__}. "
                f"Retrying in "
                f"{delay:.2f}s..."
            )

            time.sleep(delay)

    raise RuntimeError(
        "Retry execution ended unexpectedly."
    )