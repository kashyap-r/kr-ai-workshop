"""Rank-based result fusion strategies for retrieval."""

from collections.abc import Sequence

from rag_platform.domain.models import RetrievalResult


class RRFFusion:
    """Fuse ranked result sets using Reciprocal Rank Fusion (RRF).

    RRF combines rankings rather than raw retrieval scores, which avoids
    assuming that scores from different retrieval strategies are comparable.
    """

    def __init__(self, *, k: int = 60) -> None:
        if k < 0:
            raise ValueError("k must be non-negative.")
        self._k = k

    def fuse(
        self,
        result_sets: Sequence[Sequence[RetrievalResult]],
        *,
        top_k: int = 5,
    ) -> Sequence[RetrievalResult]:
        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        if not result_sets:
            return []

        fused: dict[str, tuple[RetrievalResult, float]] = {}

        for result_set in result_sets:
            seen_chunk_ids: set[str] = set()
            for position, result in enumerate(result_set, start=1):
                chunk_id = str(result.chunk.chunk_id)
                if chunk_id in seen_chunk_ids:
                    continue
                seen_chunk_ids.add(chunk_id)

                rrf_score = 1.0 / (self._k + position)
                existing = fused.get(chunk_id)
                if existing is None:
                    fused[chunk_id] = (result, rrf_score)
                else:
                    fused[chunk_id] = (existing[0], existing[1] + rrf_score)

        ranked = sorted(
            fused.values(),
            key=lambda item: (-item[1], str(item[0].chunk.chunk_id)),
        )[:top_k]

        return [
            RetrievalResult(chunk=result.chunk, score=score, rank=rank)
            for rank, (result, score) in enumerate(ranked, start=1)
        ]
