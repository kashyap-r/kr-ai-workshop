from fastapi.testclient import TestClient

import rag_platform.api as api
from rag_platform.api import app
from rag_platform.domain.models import (
    ChunkID,
    ContextChunk,
    ContextPackage,
    DocumentChunk,
    DocumentID,
    RetrievalResult,
)


def make_result(
    chunk_id: str = "chunk-1",
    document_id: str = "doc-1",
) -> RetrievalResult:
    chunk = DocumentChunk(
        chunk_id=ChunkID(chunk_id),
        document_id=DocumentID(document_id),
        document_version=1,
        chunking_version="v1",
        text="Employees may work remotely two days per week.",
        metadata={"source": "test"},
        sequence_number=0,
        start_offset=0,
        end_offset=46,
    )

    return RetrievalResult(
        chunk=chunk,
        score=0.95,
        rank=1,
    )


class FakeQueryService:
    def query(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        if query == "work from home":
            return []

        return [make_result()]

    def query_with_context(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> tuple[list[RetrievalResult], ContextPackage]:
        results = self.query(
            query,
            top_k=top_k,
        )

        if not results:
            return (
                results,
                ContextPackage(
                    query=query,
                    chunks=(),
                    context_text="",
                    token_count=0,
                ),
            )

        result = results[0]

        context_chunk = ContextChunk(
            chunk=result.chunk,
            score=result.score,
            rank=result.rank,
            token_count=12,
        )

        context_package = ContextPackage(
            query=query,
            chunks=(context_chunk,),
            context_text=(
                "[Context 1]\n"
                "Document ID: doc-1\n"
                "Chunk ID: chunk-1\n"
                "Content:\n"
                "Employees may work remotely two days per week."
            ),
            token_count=12,
        )

        return results, context_package


api.query_service = FakeQueryService()

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query() -> None:
    response = client.post(
        "/query",
        json={
            "query": "work from home",
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["query"] == "work from home"
    assert body["results"] == []
    assert body["result_count"] == 0

    assert body["context"]["text"] == ""
    assert body["context"]["chunks"] == []
    assert body["context"]["chunk_count"] == 0
    assert body["context"]["token_count"] == 0

    assert "latency_ms" in body


def test_query_rejects_empty_query() -> None:
    response = client.post(
        "/query",
        json={
            "query": "",
            "top_k": 5,
        },
    )

    assert response.status_code == 422


def test_query_rejects_invalid_top_k() -> None:
    response = client.post(
        "/query",
        json={
            "query": "work from home",
            "top_k": 0,
        },
    )

    assert response.status_code == 422


def test_query_api_returns_context() -> None:
    response = client.post(
        "/query",
        json={
            "query": "What is the remote work policy?",
            "top_k": 1,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["query"] == "What is the remote work policy?"
    assert body["result_count"] == 1

    assert len(body["results"]) == 1

    result = body["results"][0]

    assert result["chunk_id"] == "chunk-1"
    assert result["document_id"] == "doc-1"
    assert result["rank"] == 1
    assert result["score"] == 0.95

    assert "context" in body

    context = body["context"]

    assert context["chunk_count"] == 1
    assert context["token_count"] == 12

    assert context["text"].startswith("[Context 1]")

    assert len(context["chunks"]) == 1

    context_chunk = context["chunks"][0]

    assert context_chunk["chunk_id"] == "chunk-1"
    assert context_chunk["document_id"] == "doc-1"
    assert context_chunk["rank"] == 1
    assert context_chunk["score"] == 0.95
    assert context_chunk["token_count"] == 12
