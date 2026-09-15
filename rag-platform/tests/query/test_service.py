from rag_platform.domain.models import RetrievalResult
from rag_platform.query import QueryService


class FakeRetriever:
    def retrieve(self, query: str, *, top_k: int = 5):
        assert query == "work from home"
        assert top_k == 3
        return []


def test_query_service_delegates_to_retriever() -> None:
    service = QueryService(FakeRetriever())

    results = service.query(
        "work from home",
        top_k=3,
    )

    assert results == []


def test_query_service_rejects_empty_query() -> None:
    service = QueryService(FakeRetriever())

    try:
        service.query("   ")
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "query must not be empty."


def test_query_service_rejects_invalid_top_k() -> None:
    service = QueryService(FakeRetriever())

    try:
        service.query("policy", top_k=0)
        raise AssertionError("Expected ValueError")
    except ValueError as exc:
        assert str(exc) == "top_k must be positive."