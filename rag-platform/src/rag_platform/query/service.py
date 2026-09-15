from collections.abc import Sequence

from rag_platform.domain.contracts import Retriever
from rag_platform.domain.models import RetrievalResult


class QueryService:
    """Application service for executing retrieval queries."""

    def __init__(self, retriever: Retriever) -> None:
        self._retriever = retriever

    def query(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> Sequence[RetrievalResult]:
        if not query.strip():
            raise ValueError("query must not be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        return self._retriever.retrieve(
            query,
            top_k=top_k,
        )