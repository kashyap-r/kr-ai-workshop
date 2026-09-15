from fastapi.testclient import TestClient

import rag_platform.api as api


class FakeQueryService:
    def query(self, query: str, *, top_k: int = 5):
        assert query == "work from home"
        assert top_k == 5
        return []


api.query_service = FakeQueryService()

client = TestClient(api.app)


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