from rag_platform.vector_store import VectorStore

class FakeVectorStore:
    def upsert(self, chunks, embeddings) -> None:
        pass

    def query(self, embedding, *, top_k):
        return []


def test_vector_store_contract() -> None:
    store: VectorStore = FakeVectorStore()

    store.upsert([], [])

    results = store.query([1.0], top_k=5)

    assert results == []