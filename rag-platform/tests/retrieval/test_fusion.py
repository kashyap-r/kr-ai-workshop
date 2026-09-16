import pytest

from rag_platform.domain.models import DocumentChunk, RetrievalResult
from rag_platform.domain.types import ChunkID, DocumentID
from rag_platform.retrieval import RRFFusion


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


def test_rrf_fuses_rankings_without_comparing_raw_scores() -> None:
    dense = [
        make_result("A", 0.99, 1),
        make_result("B", 0.98, 2),
        make_result("C", 0.97, 3),
    ]
    sparse = [
        make_result("B", 18.0, 1),
        make_result("D", 12.0, 2),
        make_result("A", 8.0, 3),
    ]

    results = RRFFusion(k=60).fuse([dense, sparse], top_k=4)

    assert [result.chunk.chunk_id for result in results] == [
        ChunkID("B"),
        ChunkID("A"),
        ChunkID("D"),
        ChunkID("C"),
    ]
    assert [result.rank for result in results] == [1, 2, 3, 4]
    assert results[0].score == pytest.approx(1 / 62 + 1 / 61)
    assert results[1].score == pytest.approx(1 / 61 + 1 / 63)


def test_rrf_respects_top_k() -> None:
    results = RRFFusion().fuse(
        [[make_result("A", 1.0, 1), make_result("B", 0.9, 2)]],
        top_k=1,
    )

    assert len(results) == 1
    assert results[0].chunk.chunk_id == ChunkID("A")
    assert results[0].rank == 1


def test_rrf_handles_empty_result_sets() -> None:
    assert RRFFusion().fuse([[], []], top_k=5) == []


def test_rrf_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError, match="k must be non-negative"):
        RRFFusion(k=-1)

    with pytest.raises(ValueError, match="top_k must be positive"):
        RRFFusion().fuse([], top_k=0)


def test_rrf_deduplicates_duplicate_chunk_within_one_result_set() -> None:
    results = RRFFusion(k=0).fuse(
        [[
            make_result("A", 1.0, 1),
            make_result("A", 0.5, 2),
        ]],
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].score == pytest.approx(1.0)
