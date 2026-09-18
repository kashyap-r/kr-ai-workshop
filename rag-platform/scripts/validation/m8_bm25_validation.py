
"""Functional validation for M8.2 BM25 sparse retrieval."""

from rag_platform.domain.models import ChunkID, DocumentChunk, DocumentID
from rag_platform.retrieval import BM25IndexStore, BM25Retriever


def build_test_chunks() -> list[DocumentChunk]:
    """Build a small deterministic corpus for BM25 validation."""
    return [
        DocumentChunk(
            chunk_id=ChunkID("chunk-1"),
            document_id=DocumentID("doc-1"),
            document_version=1,
            chunking_version="v1",
            text=(
                "Employee EMP-1042 works as a Principal Engineer "
                "in Germany."
            ),
            metadata={},
            sequence_number=0,
            start_offset=0,
            end_offset=60,
        ),
        DocumentChunk(
            chunk_id=ChunkID("chunk-2"),
            document_id=DocumentID("doc-2"),
            document_version=1,
            chunking_version="v1",
            text=(
                "Employees in Germany are eligible for maternity "
                "leave according to company policy."
            ),
            metadata={},
            sequence_number=0,
            start_offset=0,
            end_offset=80,
        ),
        DocumentChunk(
            chunk_id=ChunkID("chunk-3"),
            document_id=DocumentID("doc-3"),
            document_version=1,
            chunking_version="v1",
            text=(
                "Employees can work from home under the global "
                "WFH policy."
            ),
            metadata={},
            sequence_number=0,
            start_offset=0,
            end_offset=65,
        ),
    ]


def run_identifier_test(retriever: BM25Retriever) -> None:
    """Validate exact identifier retrieval."""
    query = "EMP-1042"
    results = retriever.retrieve(query, top_k=3)

    print("\n=== M8.2 BM25 — Exact Identifier Retrieval ===")
    print(f"Query: {query}")

    if not results:
        raise AssertionError("Expected at least one result.")

    for result in results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"score={result.score:.4f}"
        )

    assert results[0].chunk.chunk_id == "chunk-1"
    assert results[0].score > 0.0

    print("PASS")

def run_multi_term_test(retriever: BM25Retriever) -> None:
    """Validate multi-term keyword retrieval."""
    query = "working from home"

    results = retriever.retrieve(query, top_k=3)

    print("=== M8.2 BM25 — Multi-Term Keyword Retrieval ===")
    print()
    print(f"Query: {query}")
    print()

    if not results:
        raise AssertionError("Expected BM25 results for multi-term query.")

    for result in results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"score={result.score:.4f}"
        )

    # At least one result must contain evidence of the query terms.
    top_result_text = results[0].chunk.text.casefold()

    if not any(
        term in top_result_text
        for term in ("working", "home")
    ):
        raise AssertionError(
            "Top BM25 result does not contain expected query terms."
        )

    print()
    print("PASS")
    print()

"""negative retrieval to prove that BM25 doesn't manufacture a result when none of the query terms exist in the corpus."""
def run_no_match_test(retriever: BM25Retriever) -> None:
    """Validate that BM25 returns no results for an unknown query."""
    query = "quantum blockchain spaceship"

    results = retriever.retrieve(query, top_k=3)

    print("=== M8.2 BM25 — No-Match Query ===")
    print()
    print(f"Query: {query}")
    print()

    if results:
        raise AssertionError(
            f"Expected no BM25 results, got {len(results)}."
        )

    print("No results returned.")
    print()
    print("PASS")
    print()


def main() -> None:
    """Run M8.2 BM25 functional validation."""
    chunks = build_test_chunks()

    index = BM25IndexStore()
    index.upsert(chunks)

    retriever = BM25Retriever(index)

    run_identifier_test(retriever)
    run_multi_term_test(retriever)
    run_no_match_test(retriever)

    print("\nM8.2 BM25 validation completed successfully.")

if __name__ == "__main__":
    main()