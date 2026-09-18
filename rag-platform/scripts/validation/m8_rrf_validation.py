from collections.abc import Sequence

from rag_platform.domain.models import DocumentChunk, RetrievalResult
from rag_platform.domain.types import ChunkID, DocumentID
from rag_platform.retrieval import RRFFusion


def make_result(
    chunk_id: str,
    score: float,
    rank: int,
) -> RetrievalResult:
    chunk = DocumentChunk(
        chunk_id=ChunkID(chunk_id),
        document_id=DocumentID("document-1"),
        document_version=1,
        chunking_version="validation-1",
        text=f"text for {chunk_id}",
        metadata={},
        sequence_number=rank - 1,
        start_offset=0,
        end_offset=10,
    )

    return RetrievalResult(
        chunk=chunk,
        score=score,
        rank=rank,
    )


def run_rrf_rank_fusion_test() -> None:
    """Validate that RRF combines ranked lists correctly."""

    dense_results: Sequence[RetrievalResult] = [
        make_result("chunk-a", 0.95, 1),
        make_result("chunk-b", 0.90, 2),
        make_result("chunk-c", 0.85, 3),
    ]

    sparse_results: Sequence[RetrievalResult] = [
        make_result("chunk-b", 12.0, 1),
        make_result("chunk-a", 10.0, 2),
        make_result("chunk-d", 8.0, 3),
    ]

    fusion = RRFFusion(k=60)

    results = fusion.fuse(
        [dense_results, sparse_results],
        top_k=4,
    )

    print("=== M8.3 — RRF Rank Fusion ===")
    print()

    print("Dense ranking:")
    for result in dense_results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"score={result.score:.4f}"
        )

    print()

    print("Sparse ranking:")
    for result in sparse_results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"score={result.score:.4f}"
        )

    print()

    print("Fused ranking:")
    for result in results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"rrf_score={result.score:.6f}"
        )

    print()

    expected_scores = {
        "chunk-a": (1.0 / 61) + (1.0 / 62),
        "chunk-b": (1.0 / 62) + (1.0 / 61),
        "chunk-c": 1.0 / 63,
        "chunk-d": 1.0 / 63,
    }

    actual_scores = {
        str(result.chunk.chunk_id): result.score
        for result in results
    }

    for chunk_id, expected_score in expected_scores.items():
        actual_score = actual_scores.get(chunk_id)

        if actual_score is None:
            raise AssertionError(
                f"Expected {chunk_id} in fused results."
            )

        if abs(actual_score - expected_score) > 1e-12:
            raise AssertionError(
                f"Unexpected RRF score for {chunk_id}: "
                f"expected={expected_score}, actual={actual_score}"
            )

    # chunk-a and chunk-b have identical RRF scores.
    # The implementation uses chunk_id as the deterministic tie-breaker.
    expected_order = [
        "chunk-a",
        "chunk-b",
        "chunk-c",
        "chunk-d",
    ]

    actual_order = [
        str(result.chunk.chunk_id)
        for result in results
    ]

    if actual_order != expected_order:
        raise AssertionError(
            f"Unexpected fused ranking: "
            f"expected={expected_order}, actual={actual_order}"
        )

    print("PASS")
    print()
    print("M8.3 RRF validation completed successfully.")

def run_cross_retriever_agreement_test() -> None:
    """Validate that results appearing in both rankings accumulate RRF score."""

    dense_results = [
        make_result("shared", 0.90, 1),
        make_result("dense-only", 0.80, 2),
    ]

    sparse_results = [
        make_result("sparse-only", 10.0, 1),
        make_result("shared", 9.0, 2),
    ]

    fusion = RRFFusion(k=60)

    results = fusion.fuse(
        [dense_results, sparse_results],
        top_k=3,
    )

    print("=== M8.3 — RRF Cross-Retriever Agreement ===")
    print()

    for result in results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"rrf_score={result.score:.6f}"
        )

    expected_shared_score = (1.0 / 61) + (1.0 / 62)

    shared_result = next(
        result
        for result in results
        if str(result.chunk.chunk_id) == "shared"
    )

    if abs(shared_result.score - expected_shared_score) > 1e-12:
        raise AssertionError(
            "Shared result did not accumulate contributions "
            "from both retrievers."
        )

    if str(results[0].chunk.chunk_id) != "shared":
        raise AssertionError(
            "Cross-retriever agreement should produce the highest "
            "RRF score in this scenario."
        )

    print()
    print("PASS")
    print()

def main() -> None:
    run_rrf_rank_fusion_test()
    run_cross_retriever_agreement_test()


if __name__ == "__main__":
    main()