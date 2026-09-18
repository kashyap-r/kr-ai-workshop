from collections.abc import Sequence

import pytest

from rag_platform.domain.models import DocumentChunk, RetrievalResult
from rag_platform.domain.types import ChunkID, DocumentID
from rag_platform.retrieval.reranker import CrossEncoderReranker


def make_result(chunk_id: str, score: float, rank: int) -> RetrievalResult:
    chunk = DocumentChunk(
        chunk_id=ChunkID(chunk_id),
        document_id=DocumentID("document-1"),
        document_version=1,
        chunking_version="test-1",
        text=f"text for {chunk_id}",
        metadata={},
        sequence_number=rank - 1,
        start_offset=0,
        end_offset=10,
    )
    return RetrievalResult(chunk=chunk, score=score, rank=rank)


class FakeCrossEncoder:
    def __init__(self, scores: Sequence[float]) -> None:
        self.scores = list(scores)
        self.pairs: list[tuple[str, str]] = []

    def predict(self, pairs: Sequence[tuple[str, str]]) -> Sequence[float]:
        self.pairs = list(pairs)
        return self.scores


def test_reranker_scores_and_reorders_candidates() -> None:
    results = [
        make_result("chunk-a", 0.8, 1),
        make_result("chunk-b", 0.7, 2),
        make_result("chunk-c", 0.6, 3),
    ]

    reranker = object.__new__(CrossEncoderReranker)
    fake_model = FakeCrossEncoder([0.20, 0.95, 0.60])
    reranker._model = fake_model

    reranked = reranker.rerank("work from home", results)

    assert [result.chunk.chunk_id for result in reranked] == [
        "chunk-b",
        "chunk-c",
        "chunk-a",
    ]

    assert [result.score for result in reranked] == [
        0.95,
        0.60,
        0.20,
    ]

    assert [result.rank for result in reranked] == [1, 2, 3]

    assert fake_model.pairs == [
        ("work from home", "text for chunk-a"),
        ("work from home", "text for chunk-b"),
        ("work from home", "text for chunk-c"),
    ]


def test_reranker_returns_empty_for_empty_context() -> None:
    reranker = object.__new__(CrossEncoderReranker)
    reranker._model = FakeCrossEncoder([])

    assert reranker.rerank("policy", []) == []


def test_reranker_rejects_empty_query() -> None:
    reranker = object.__new__(CrossEncoderReranker)
    reranker._model = FakeCrossEncoder([])

    with pytest.raises(ValueError, match="query must not be empty"):
        reranker.rerank("   ", [])


def test_reranker_uses_deterministic_tie_breaking() -> None:
    results = [
        make_result("chunk-b", 0.8, 1),
        make_result("chunk-a", 0.7, 2),
    ]

    reranker = object.__new__(CrossEncoderReranker)
    reranker._model = FakeCrossEncoder([0.5, 0.5])

    reranked = reranker.rerank("policy", results)

    assert [result.chunk.chunk_id for result in reranked] == [
        "chunk-a",
        "chunk-b",
    ]
