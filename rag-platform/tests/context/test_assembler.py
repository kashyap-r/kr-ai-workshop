import pytest

from rag_platform.context.assembler import (
    ContextAssembler,
    ContextAssemblyConfig,
)
from rag_platform.domain.models import (
    ChunkID,
    DocumentChunk,
    DocumentID,
    RetrievalResult,
)


def make_result(
    chunk_id: str,
    text: str,
    *,
    document_id: str = "doc-1",
    score: float = 0.9,
    rank: int = 1,
) -> RetrievalResult:
    chunk = DocumentChunk(
        chunk_id=ChunkID(chunk_id),
        document_id=DocumentID(document_id),
        document_version=1,
        chunking_version="v1",
        text=text,
        metadata={},
        sequence_number=rank,
        start_offset=0,
        end_offset=len(text),
    )

    return RetrievalResult(
        chunk=chunk,
        score=score,
        rank=rank,
    )

def test_assemble_preserves_rank_order() -> None:
    assembler = ContextAssembler()

    results = [
        make_result("chunk-1", "First", rank=1),
        make_result("chunk-2", "Second", rank=2),
    ]

    package = assembler.assemble(
        "test query",
        results,
    )

    assert [chunk.rank for chunk in package.chunks] == [1, 2]
    assert "[Context 1]" in package.context_text
    assert "[Context 2]" in package.context_text

""" Deduplication test """
def test_duplicate_chunks_are_removed() -> None:
    assembler = ContextAssembler()

    results = [
        make_result("chunk-1", "Same content", rank=1),
        make_result("chunk-1", "Same content", rank=2),
        make_result("chunk-2", "Different content", rank=3),
    ]

    package = assembler.assemble(
        "test query",
        results,
    )

    assert len(package.chunks) == 2
    assert [
        chunk.chunk.chunk_id
        for chunk in package.chunks
    ] == ["chunk-1", "chunk-2"]

""" Testing Same document, different chunks """
def test_different_chunks_from_same_document_are_retained() -> None:
    assembler = ContextAssembler()

    results = [
        make_result("chunk-1", "First", rank=1),
        make_result("chunk-2", "Second", rank=2),
    ]

    package = assembler.assemble(
        "test query",
        results,
    )

    assert len(package.chunks) == 2

""" TEsting Context Budget """
class FixedTokenCounter:
    def __init__(self, counts: dict[str, int]) -> None:
        self._counts = counts

    def count(self, text: str) -> int:
        return self._counts[text]

def test_context_budget_excludes_chunks_that_do_not_fit() -> None:
    counter = FixedTokenCounter(
        {
            "one": 600,
            "two": 700,
            "three": 900,
        }
    )

    assembler = ContextAssembler(
        config=ContextAssemblyConfig(
            max_context_tokens=1500,
        ),
        token_counter=counter,
    )

    results = [
        make_result("chunk-1", "one", rank=1),
        make_result("chunk-2", "two", rank=2),
        make_result("chunk-3", "three", rank=3),
    ]

    package = assembler.assemble(
        "test query",
        results,
    )

    assert [
        chunk.chunk.chunk_id
        for chunk in package.chunks
    ] == ["chunk-1", "chunk-2"]

    assert package.token_count == 1300

""" Testing oversized first chunk """
def test_oversized_chunk_does_not_block_later_chunks() -> None:
    counter = FixedTokenCounter(
        {
            "large": 2000,
            "small": 500,
        }
    )

    assembler = ContextAssembler(
        config=ContextAssemblyConfig(
            max_context_tokens=1000,
        ),
        token_counter=counter,
    )

    results = [
        make_result("chunk-1", "large", rank=1),
        make_result("chunk-2", "small", rank=2),
    ]

    package = assembler.assemble(
        "test query",
        results,
    )

    assert [
        chunk.chunk.chunk_id
        for chunk in package.chunks
    ] == ["chunk-2"]

    assert package.token_count == 500

""" Testing Empty Retrieval Results """
def test_empty_results_produce_empty_context() -> None:
    assembler = ContextAssembler()

    package = assembler.assemble(
        "test query",
        [],
    )

    assert package.chunks == ()
    assert package.context_text == ""
    assert package.token_count == 0



"""Testing Invalid input """
def test_empty_query_is_rejected() -> None:
    assembler = ContextAssembler()

    with pytest.raises(ValueError, match="query must not be empty"):
        assembler.assemble("   ", [])

def test_invalid_context_budget_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="max_context_tokens must be positive",
    ):
        ContextAssembler(
            config=ContextAssemblyConfig(
                max_context_tokens=0,
            )
        )

""" Test Metadata Preservation """
def test_chunk_metadata_is_preserved() -> None:
    chunk = DocumentChunk(
        chunk_id=ChunkID("chunk-1"),
        document_id=DocumentID("doc-1"),
        document_version=1,
        chunking_version="v1",
        text="Some content",
        metadata={
            "country": "Sweden",
            "policy": "parental_leave",
        },
        sequence_number=1,
        start_offset=0,
        end_offset=12,
    )

    result = RetrievalResult(
        chunk=chunk,
        score=0.95,
        rank=1,
    )

    package = ContextAssembler().assemble(
        "test query",
        [result],
    )

    selected = package.chunks[0]

    assert selected.chunk.metadata["country"] == "Sweden"
    assert selected.score == 0.95
    assert selected.rank == 1
