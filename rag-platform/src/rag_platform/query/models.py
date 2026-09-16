from dataclasses import dataclass, field
from enum import StrEnum


class QueryUnderstandingMode(StrEnum):
    AUTO = "auto"
    RULE = "rule"
    LLM = "llm"


@dataclass(frozen=True, slots=True)
class QueryContext:
    """Optional conversational context; session/state is owned by a later milestone."""

    conversation: tuple[dict[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class QueryUnderstandingRequest:
    query: str
    context: QueryContext | None = None
    mode: QueryUnderstandingMode = QueryUnderstandingMode.AUTO


@dataclass(frozen=True, slots=True)
class QueryUnderstandingResult:
    original_query: str
    normalized_query: str
    rewritten_query: str | None = None
    intent: str | None = None
    entities: dict[str, str] = field(default_factory=dict)
    filters: dict[str, str] = field(default_factory=dict)
    expanded_queries: tuple[str, ...] = ()
    strategy: QueryUnderstandingMode = QueryUnderstandingMode.RULE
    fallback_used: bool = False

    @property
    def retrieval_query(self) -> str:
        return self.rewritten_query or self.normalized_query
