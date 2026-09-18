from collections.abc import Sequence

from sentence_transformers import CrossEncoder

from rag_platform.domain.models import RetrievalResult


class CrossEncoderReranker:
    """Rerank retrieved candidates using a cross-encoder relevance model."""

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ) -> None:
        self._model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        context: Sequence[RetrievalResult],
    ) -> Sequence[RetrievalResult]:
        if not query.strip():
            raise ValueError("query must not be empty.")

        if not context:
            return []

        pairs = [
            (query, result.chunk.text)
            for result in context
        ]

        scores = self._model.predict(pairs)

        ranked = sorted(
            zip(context, scores, strict=True),
            key=lambda item: (-float(item[1]), str(item[0].chunk.chunk_id)),
        )

        return [
            RetrievalResult(
                chunk=result.chunk,
                score=float(score),
                rank=rank,
            )
            for rank, (result, score) in enumerate(ranked, start=1)
        ]
