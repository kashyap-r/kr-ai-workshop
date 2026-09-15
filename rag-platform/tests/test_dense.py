from rag_platform.retrieval import DenseRetriever


class FakeEmbeddingModel:
    def embed(self, texts):
        assert texts == ["work from home"]
        return [[0.1, 0.2, 0.3]]


class FakeVectorStore:
    def query(self, embedding, *, top_k):
        assert embedding == [0.1, 0.2, 0.3]
        assert top_k == 3
        return []

    def upsert(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def delete_all(self, *args, **kwargs):
        pass


def test_dense_retriever_embeds_query_and_searches_vector_store() -> None:
    retriever = DenseRetriever(
        embedding_model=FakeEmbeddingModel(),
        vector_store=FakeVectorStore(),
    )

    results = retriever.retrieve("work from home", top_k=3)

    assert results == []


# def test_dense_retriever_rejects_empty_query() -> None:
#     retriever = DenseRetriever(
#         embedding_model=FakeEmbeddingModel(),
#         vector_store=FakeVectorStore(),
#     )

#     try:
#         retriever.retrieve("   ")
#         assert False
#     except ValueError as exc:
#         assert str(exc) == "query must not be empty."


# def test_dense_retriever_rejects_invalid_top_k() -> None:
#     retriever = DenseRetriever(
#         embedding_model=FakeEmbeddingModel(),
#         vector_store=FakeVectorStore(),
#     )

#     try:
#         retriever.retrieve("policy", top_k=0)
#         assert False
#     except ValueError as exc:
#         assert str(exc) == "top_k must be positive."

def test_dense_retriever_rejects_empty_query() -> None:
    retriever = DenseRetriever(
        embedding_model=FakeEmbeddingModel(),
        vector_store=FakeVectorStore(),
    )

    with pytest.raises(ValueError, match="query must not be empty"):
        retriever.retrieve("   ")


def test_dense_retriever_rejects_invalid_top_k() -> None:
    retriever = DenseRetriever(
        embedding_model=FakeEmbeddingModel(),
        vector_store=FakeVectorStore(),
    )

    with pytest.raises(ValueError, match="top_k must be positive"):
        retriever.retrieve("policy", top_k=0)