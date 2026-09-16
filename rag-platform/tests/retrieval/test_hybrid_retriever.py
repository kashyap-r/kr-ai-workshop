from collections.abc import Sequence

import pytest

from rag_platform.domain.models import DocumentChunk, RetrievalResult
from rag_platform.domain.types import ChunkID, DocumentID
from rag_platform.retrieval import HybridRetriever


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


class FakeRetriever:
    def __init__(self, results: Sequence[RetrievalResult]) -> None:
        self.results = results
        self.queries: list[tuple[str, int]] = []

    def retrieve(self, query: str, *, top_k: int = 5) -> Sequence[RetrievalResult]:
        self.queries.append((query, top_k))
        return self.results


class FakeFusion:
    def __init__(self) -> None:
        self.calls: list[tuple[Sequence[Sequence[RetrievalResult]], int]] = []

    def fuse(
        self,
        result_sets: Sequence[Sequence[RetrievalResult]],
        *,
        top_k: int = 5,
    ) -> Sequence[RetrievalResult]:
        self.calls.append((result_sets, top_k))
        return result_sets[0]


def test_hybrid_retriever_queries_both_retrievers_and_fuses_results() -> None:
    dense_results = [make_result("dense", 0.9, 1)]
    sparse_results = [make_result("sparse", 10.0, 1)]
    dense = FakeRetriever(dense_results)
    sparse = FakeRetriever(sparse_results)
    fusion = FakeFusion()

    results = HybridRetriever(dense, sparse, fusion).retrieve(
        "work from home",
        top_k=3,
    )

    assert results == dense_results
    assert dense.queries == [("work from home", 12)]
    assert sparse.queries == [("work from home", 12)]
    assert len(fusion.calls) == 1
    assert fusion.calls[0][0] == [dense_results, sparse_results]
    assert fusion.calls[0][1] == 3


def test_hybrid_retriever_rejects_empty_query() -> None:
    hybrid = HybridRetriever(FakeRetriever([]), FakeRetriever([]), FakeFusion())

    with pytest.raises(ValueError, match="query must not be empty"):
        hybrid.retrieve("   ")


def test_hybrid_retriever_rejects_invalid_candidate_multiplier() -> None:
    with pytest.raises(ValueError, match="candidate_multiplier must be positive"):
        HybridRetriever(FakeRetriever([]), FakeRetriever([]), FakeFusion(), candidate_multiplier=0)


def test_hybrid_retriever_rejects_invalid_top_k() -> None:
    hybrid = HybridRetriever(FakeRetriever([]), FakeRetriever([]), FakeFusion())

    with pytest.raises(ValueError, match="top_k must be positive"):
        hybrid.retrieve("policy", top_k=0)


def test_hybrid_falls_back_to_non_empty_retriever() -> None:
    dense_results = [make_result("dense", 0.9, 1)]
    sparse_results: list[RetrievalResult] = []
    dense = FakeRetriever(dense_results)
    sparse = FakeRetriever(sparse_results)
    fusion = FakeFusion()

    results = HybridRetriever(dense, sparse, fusion).retrieve("policy", top_k=1)

    assert results == dense_results
    assert fusion.calls == []
