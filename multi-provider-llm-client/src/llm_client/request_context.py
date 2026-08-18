from contextvars import ContextVar
from dataclasses import dataclass


@dataclass
class RequestContext:

    request_id: str

    attempts: int = 0

    retry_count: int = 0

    retry_delay_seconds: float = 0.0


_current_context: ContextVar[
    RequestContext | None
] = ContextVar(
    "llm_request_context",
    default=None,
)


def set_request_context(
    context: RequestContext,
):
    return _current_context.set(
        context
    )


def get_request_context() -> RequestContext | None:
    return _current_context.get()


def reset_request_context(
    token,
) -> None:

    _current_context.reset(token)