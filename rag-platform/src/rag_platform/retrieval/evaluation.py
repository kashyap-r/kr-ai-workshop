"""Small, dependency-free retrieval evaluation helpers."""

from collections.abc import Iterable, Sequence

from rag_platform.domain.models import RetrievalResult


def recall_at_k(
        results: Sequence[RetrievalResult],
        relevant_ids: Iterable[str], k: int) -> float:
    relevant = {str(item) for item in relevant_ids}
    if not relevant:
        raise ValueError("relevant_ids must not be empty.")
    if k <= 0:
        raise ValueError("k must be positive.")
    retrieved = {str(result.chunk.chunk_id) for result in results[:k]}
    return len(retrieved & relevant) / len(relevant)


def precision_at_k(
        results: Sequence[RetrievalResult],
        relevant_ids: Iterable[str], k: int) -> float:
    relevant = {str(item) for item in relevant_ids}
    if not relevant:
        raise ValueError("relevant_ids must not be empty.")
    if k <= 0:
        raise ValueError("k must be positive.")
    retrieved = results[:k]
    if not retrieved:
        return 0.0
    return sum(
        str(result.chunk.chunk_id) in relevant
        for result in retrieved) / len(retrieved)


def reciprocal_rank(
        results: Sequence[RetrievalResult],
        relevant_ids: Iterable[str]) -> float:
    relevant = {str(item) for item in relevant_ids}
    if not relevant:
        raise ValueError("relevant_ids must not be empty.")
    for rank, result in enumerate(results, start=1):
        if str(result.chunk.chunk_id) in relevant:
            return 1.0 / rank
    return 0.0
