from rag_platform.embeddings.base import EmbeddingModel

from rag_platform.embeddings import (
    SentenceTransformerEmbeddingModel,
)

class FakeEmbeddingModel:
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(text))] for text in texts]

def test_embedding_model_contract() -> None:
    model: EmbeddingModel = FakeEmbeddingModel()
    vectors = model.embed(["hello", "hello world"])
    assert vectors ==[[5.0], [11.0]]

def test_sentence_transformer_embedding_model() -> None:
    model = SentenceTransformerEmbeddingModel(
        "BAAI/bge-small-en-v1.5"
    )

    vectors = model.embed(
        ["What is the leave policy?"]
    )

    assert len(vectors) == 1
    assert len(vectors[0]) == 384