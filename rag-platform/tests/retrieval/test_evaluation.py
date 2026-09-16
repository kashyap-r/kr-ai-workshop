from rag_platform.domain.models import DocumentChunk, RetrievalResult
from rag_platform.domain.types import ChunkID, DocumentID
from rag_platform.retrieval.evaluation import precision_at_k, recall_at_k, reciprocal_rank


def result(chunk_id: str, rank: int) -> RetrievalResult:
    chunk = DocumentChunk(
        chunk_id=ChunkID(chunk_id),
        document_id=DocumentID("doc"),
        document_version=1,
        chunking_version="v1",
        text=chunk_id,
        metadata={},
        sequence_number=rank,
        start_offset=0,
        end_offset=1,
    )
    return RetrievalResult(chunk=chunk, score=1.0, rank=rank)


def test_retrieval_metrics() -> None:
    results = [result("a", 1), result("b", 2), result("c", 3)]
    assert recall_at_k(results, ["b", "c"], 2) == 0.5
    assert precision_at_k(results, ["b", "c"], 2) == 0.5
    assert reciprocal_rank(results, ["b", "c"]) == 0.5
