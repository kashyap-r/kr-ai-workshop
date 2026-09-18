from collections.abc import Sequence

from rag_platform.context import ContextAssembler
from rag_platform.domain.contracts import Reranker, Retriever
from rag_platform.domain.models import ContextPackage, RetrievalResult
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
    """Application service for query understanding, retrieval, reranking, and context assembly."""

    def __init__(
        self,
        retriever: Retriever,
        reranker: Reranker,
        query_understanding: HybridQueryUnderstanding | None = None,
        context_assembler: ContextAssembler | None = None,
    ) -> None:
        self._retriever = retriever
        self._reranker = reranker
        self._query_understanding = (
            query_understanding or HybridQueryUnderstanding()
        )
        self._context_assembler = (
            context_assembler or ContextAssembler()
        )

    def understand(
        self,
        query: str,
        *,
        context: QueryContext | None = None,
        mode: QueryUnderstandingMode = QueryUnderstandingMode.AUTO,
    ) -> QueryUnderstandingResult:
        """Understand the query before retrieval."""

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
        """Execute query understanding, retrieval, and reranking."""

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
                "expanded_query_count": len(
                    understanding.expanded_queries
                ),
                "fallback_used": understanding.fallback_used,
            },
        )

        candidates = self._retriever.retrieve(
            understanding.retrieval_query,
            top_k=top_k * 4,
        )

        logger.info(
            "retrieval_completed",
            extra={
                "candidate_count": len(candidates),
                "requested_top_k": top_k,
            },
        )

        reranked = self._reranker.rerank(
            query,
            candidates,
        )

        results = list(reranked[:top_k])

        logger.info(
            "reranking_completed",
            extra={
                "candidate_count": len(candidates),
                "reranked_count": len(reranked),
                "returned_count": len(results),
            },
        )

        return results

    def query_with_context(
        self,
        query: str,
        *,
        top_k: int = 5,
        context: QueryContext | None = None,
        mode: QueryUnderstandingMode = QueryUnderstandingMode.AUTO,
    ) -> tuple[Sequence[RetrievalResult], ContextPackage]:
        """Execute the M9 query pipeline and assemble M10 context."""

        results = self.query(
            query,
            top_k=top_k,
            context=context,
            mode=mode,
        )

        context_package = self._context_assembler.assemble(
            query=query,
            results=results,
        )

        logger.info(
            "context_assembled",
            extra={
                "result_count": len(results),
                "context_chunk_count": len(
                    context_package.chunks
                ),
                "context_token_count": (
                    context_package.token_count
                ),
            },
        )

        return results, context_package
