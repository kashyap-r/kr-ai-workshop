from typing import Protocol

from rag_platform.query.models import (
    QueryUnderstandingRequest,
    QueryUnderstandingResult,
)


class QueryUnderstanding(Protocol):
    """Understand a user query without performing retrieval."""

    def understand(
        self,
        request: QueryUnderstandingRequest,
    ) -> QueryUnderstandingResult:
        ...
