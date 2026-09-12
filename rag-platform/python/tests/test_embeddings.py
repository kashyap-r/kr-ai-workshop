from rag_platform.embeddings.base import EmbeddingModel

class FakeEmbeddingModel:
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(text))] for text in texts]

def test_embedding_model_contract() -> None:
    model: EmbeddingModel = FakeEmbeddingModel()
    vectors = model.embed(["heelo", "hello world"])
    assert vectors ==[[5.0], [11.0]]
