from collections.abc import Sequence

from rag_platform.domain.models import RetrievalResult
from rag_platform.embeddings import EmbeddingModel
from rag_platform.vector_store import VectorStore


class DenseRetriever:
    """Retrieve chunks using dense vector similarity."""

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
    ) -> None:
        self._embedding_model = embedding_model
        self._vector_store = vector_store

    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> Sequence[RetrievalResult]:
        if not query.strip():
            raise ValueError("query must not be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        embeddings = self._embedding_model.embed([query])

        if len(embeddings) != 1:
            raise RuntimeError(
                "Embedding model must return exactly one embedding for one query."
            )

        return self._vector_store.query(
            embeddings[0],
            top_k=top_k,
        )
