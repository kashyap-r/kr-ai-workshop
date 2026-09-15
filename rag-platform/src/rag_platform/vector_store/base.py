from collections.abc import Sequence
from typing import Protocol

from rag_platform.domain.models import DocumentChunk, RetrievalResult


class VectorStore(Protocol):
    """Contract for vector storage and similarity search."""

    def upsert(
        self,
        chunks: Sequence[DocumentChunk],
        embeddings: Sequence[Sequence[float]],
    ) -> None:
        """Store or update chunks and their embeddings."""
        ...

    def delete(self, ids: Sequence[str]) -> None:
        """Delete chunks by their vector-store IDs."""
        ...

    def delete_all(self) -> None:
        """Delete every vector from the current collection."""
        ...

    def query(
        self,
        embedding: Sequence[float],
        *,
        top_k: int,
    ) -> list[RetrievalResult]:
        """Return the most similar chunks."""
        ...
