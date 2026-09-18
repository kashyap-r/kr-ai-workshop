from collections.abc import Sequence

from rag_platform.domain.models import (
    ContextPackage,
    DocumentChunk,
    RetrievalResult,
)
from rag_platform.domain.types import ChunkID, DocumentID
from rag_platform.query import QueryService


class FakeRetriever:
    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> Sequence[RetrievalResult]:
        assert query == "work from home"
        assert top_k == 12
        return []


class FakeReranker:
    def __init__(self, results: Sequence[RetrievalResult]) -> None:
        self.results = results
        self.calls: list[
            tuple[str, Sequence[RetrievalResult]]
        ] = []

    def rerank(
        self,
        query: str,
        context: Sequence[RetrievalResult],
    ) -> Sequence[RetrievalResult]:
        self.calls.append((query, context))
        return self.results


class EmptyRetriever:
    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> Sequence[RetrievalResult]:
        return []


class FakeContextAssembler:
    def __init__(self, package: ContextPackage) -> None:
        self.package = package
        self.calls: list[
            tuple[str, Sequence[RetrievalResult]]
        ] = []

    def assemble(
        self,
        query: str,
        results: Sequence[RetrievalResult],
    ) -> ContextPackage:
        self.calls.append((query, results))
        return self.package


def make_result(
    chunk_id: str,
    score: float,
    rank: int,
) -> RetrievalResult:
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

    return RetrievalResult(
        chunk=chunk,
        score=score,
        rank=rank,
    )


def make_context_package(
    query: str,
    context_text: str = "assembled context",
    token_count: int = 100,
) -> ContextPackage:
    return ContextPackage(
        query=query,
        chunks=(),
        context_text=context_text,
        token_count=token_count,
    )


def test_query_service_delegates_to_retriever() -> None:
    service = QueryService(
        FakeRetriever(),
        reranker=FakeReranker([]),
    )

    results = service.query(
        "work from home",
        top_k=3,
    )

    assert results == []


def test_query_service_rejects_empty_query() -> None:
    service = QueryService(
        FakeRetriever(),
        reranker=FakeReranker([]),
    )

    try:
        service.query("   ")
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "query must not be empty."


def test_query_service_rejects_invalid_top_k() -> None:
    service = QueryService(
        FakeRetriever(),
        reranker=FakeReranker([]),
    )

    try:
        service.query("policy", top_k=0)
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "top_k must be positive."


def test_query_service_retrieves_candidates_reranks_and_returns_top_k() -> None:
    candidates = [
        make_result("chunk-1", 0.9, 1),
        make_result("chunk-2", 0.8, 2),
        make_result("chunk-3", 0.7, 3),
        make_result("chunk-4", 0.6, 4),
        make_result("chunk-5", 0.5, 5),
        make_result("chunk-6", 0.4, 6),
        make_result("chunk-7", 0.3, 7),
        make_result("chunk-8", 0.2, 8),
    ]

    reranked = [
        candidates[7],
        candidates[2],
        candidates[0],
        candidates[4],
        candidates[1],
        candidates[3],
        candidates[5],
        candidates[6],
    ]

    class CandidateRetriever:
        def __init__(self) -> None:
            self.calls: list[tuple[str, int]] = []

        def retrieve(
            self,
            query: str,
            *,
            top_k: int = 5,
        ) -> Sequence[RetrievalResult]:
            self.calls.append((query, top_k))
            return candidates

    retriever = CandidateRetriever()
    reranker = FakeReranker(reranked)

    service = QueryService(
        retriever,
        reranker=reranker,
    )

    results = service.query(
        "work from home",
        top_k=2,
    )

    assert retriever.calls == [("work from home", 8)]

    assert len(reranker.calls) == 1
    assert reranker.calls[0][0] == "work from home"
    assert reranker.calls[0][1] == candidates

    assert [str(result.chunk.chunk_id) for result in results] == [
        "chunk-8",
        "chunk-3",
    ]


def test_query_with_context_assembles_retrieved_results() -> None:
    result = make_result(
        chunk_id="chunk-1",
        score=0.95,
        rank=1,
    )

    class Retriever:
        def retrieve(
            self,
            query: str,
            *,
            top_k: int = 5,
        ) -> Sequence[RetrievalResult]:
            assert query == "work from home"
            assert top_k == 4
            return [result]

    package = make_context_package(
        query="work from home",
    )

    assembler = FakeContextAssembler(package)

    service = QueryService(
        Retriever(),
        reranker=FakeReranker([result]),
        context_assembler=assembler,  # type: ignore[arg-type]
    )

    results, context = service.query_with_context(
        "work from home",
        top_k=1,
    )

    assert results == [result]
    assert context == package

    assert len(assembler.calls) == 1
    assert assembler.calls[0][0] == "work from home"
    assert list(assembler.calls[0][1]) == [result]


def test_query_with_context_uses_reranked_results() -> None:
    candidate = make_result(
        chunk_id="candidate",
        score=0.5,
        rank=1,
    )

    reranked = make_result(
        chunk_id="reranked",
        score=0.95,
        rank=1,
    )

    class Retriever:
        def retrieve(
            self,
            query: str,
            *,
            top_k: int = 5,
        ) -> Sequence[RetrievalResult]:
            return [candidate]

    reranker = FakeReranker([reranked])

    package = make_context_package(
        query="work from home",
    )

    assembler = FakeContextAssembler(package)

    service = QueryService(
        Retriever(),
        reranker=reranker,
        context_assembler=assembler,  # type: ignore[arg-type]
    )

    results, context = service.query_with_context(
        "work from home",
        top_k=1,
    )

    assert results == [reranked]
    assert context == package

    assert len(assembler.calls) == 1
    assert list(assembler.calls[0][1]) == [reranked]


def test_query_with_context_returns_empty_context_for_empty_results() -> None:
    package = make_context_package(
        query="unknown policy",
        context_text="",
        token_count=0,
    )

    assembler = FakeContextAssembler(package)

    service = QueryService(
        EmptyRetriever(),
        reranker=FakeReranker([]),
        context_assembler=assembler,  # type: ignore[arg-type]
    )

    results, context = service.query_with_context(
        "unknown policy",
        top_k=3,
    )

    assert results == []
    assert context == package

    assert len(assembler.calls) == 1
    assert assembler.calls[0][0] == "unknown policy"
    assert list(assembler.calls[0][1]) == []
