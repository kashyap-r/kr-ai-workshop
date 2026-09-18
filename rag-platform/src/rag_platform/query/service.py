from collections.abc import Sequence

from rag_platform.domain.contracts import Reranker, Retriever
from rag_platform.domain.models import RetrievalResult
from rag_platform.logging import configure_logging
from rag_platform.query.hybrid import HybridQueryUnderstanding
from rag_platform.query.models import (
    QueryContext,
    QueryUnderstandingMode,
    QueryUnderstandingRequest,
    QueryUnderstandingResult,
)

logger = configure_logging(
    logger_name=__name__,
    log_file="logs/query_service.log",
)


class QueryService:
    """Application service for query understanding and retrieval."""

    def __init__(
        self,
        retriever: Retriever,
        reranker: Reranker | None = None,
        query_understanding: HybridQueryUnderstanding | None = None,
    ) -> None:
        self._retriever = retriever
        self._reranker = reranker
        self._query_understanding = query_understanding or HybridQueryUnderstanding()

    def understand(
        self,
        query: str,
        *,
        context: QueryContext | None = None,
        mode: QueryUnderstandingMode = QueryUnderstandingMode.AUTO,
    ) -> QueryUnderstandingResult:
        if not query.strip():
            raise ValueError("query must not be empty.")

        return self._query_understanding.understand(
            QueryUnderstandingRequest(
                query=query,
                context=context,
                mode=mode,
            )
        )

    def query(
        self,
        query: str,
        *,
        top_k: int = 5,
        context: QueryContext | None = None,
        mode: QueryUnderstandingMode = QueryUnderstandingMode.AUTO,
    ) -> Sequence[RetrievalResult]:
        if not query.strip():
            raise ValueError("query must not be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        understanding = self.understand(
            query,
            context=context,
            mode=mode,
        )

        logger.info(
            "query_understanding_selected",
            extra={
                "strategy": understanding.strategy.value,
                "intent": understanding.intent,
                "entity_count": len(understanding.entities),
                "filter_count": len(understanding.filters),
                "expanded_query_count": len(understanding.expanded_queries),
                "fallback_used": understanding.fallback_used,
            },
        )

        # return self._retriever.retrieve(
        #     understanding.retrieval_query,
        #     top_k=top_k,
        # )

        results = self._retriever.retrieve(
            understanding.retrieval_query,
            top_k=top_k * 4 if self._reranker else top_k,
        )

        if self._reranker:
            results = self._reranker.rerank(
                understanding.retrieval_query,
                results,
            )
            return results[:top_k]

        return results
