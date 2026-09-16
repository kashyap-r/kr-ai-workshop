"""Hybrid retrieval orchestration."""

from collections.abc import Sequence

from rag_platform.domain.contracts import ResultFusion, Retriever
from rag_platform.domain.models import RetrievalResult


class HybridRetriever:
    """Retrieve candidates from dense and sparse retrievers and fuse them."""

    def __init__(
        self,
        dense_retriever: Retriever,
        sparse_retriever: Retriever,
        fusion: ResultFusion,
        candidate_multiplier: int = 4,
    ) -> None:
        if candidate_multiplier <= 0:
            raise ValueError("candidate_multiplier must be positive.")
        self._dense_retriever = dense_retriever
        self._sparse_retriever = sparse_retriever
        self._fusion = fusion
        self._candidate_multiplier = candidate_multiplier

    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> Sequence[RetrievalResult]:
        if not query.strip():
            raise ValueError("query must not be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        candidate_k = max(top_k, top_k * self._candidate_multiplier)
        dense_results = self._dense_retriever.retrieve(query, top_k=candidate_k)
        sparse_results = self._sparse_retriever.retrieve(query, top_k=candidate_k)

        if not dense_results:
            return list(sparse_results[:top_k])
        if not sparse_results:
            return list(dense_results[:top_k])

        return self._fusion.fuse(
            [dense_results, sparse_results],
            top_k=top_k,
        )
