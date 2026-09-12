
from collections.abc import Sequence
from pathlib import Path

import chromadb

from rag_platform.domain.models import ChunkID, DocumentChunk, RetrievalResult


class ChromaVectorStore:
    """Vector store implementation backed by ChromaDB."""

    def __init__(
        self,
        *,
        path: str | Path,
        collection_name: str,
        embedding_model: str,
    ) -> None:
        self._client = chromadb.PersistentClient(path=str(path))
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"embedding_model": embedding_model},
        )

    def upsert(
        self,
        chunks: Sequence[DocumentChunk],
        embeddings: Sequence[Sequence[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("chunks and embeddings must have the same length.")

        if not chunks:
            return

        self._collection.upsert(
            ids=[str(chunk.chunk_id) for chunk in chunks],
            embeddings=[list(embedding) for embedding in embeddings],
            documents=[chunk.text for chunk in chunks],
            metadatas=[
                {
                    "document_id": str(chunk.document_id),
                    "document_version": str(chunk.document_version),
                    "sequence_number": str(chunk.sequence_number),
                    "chunking_version": chunk.chunking_version,
                }
                for chunk in chunks
            ],
        )

    def query(
        self,
        embedding: Sequence[float],
        *,
        top_k: int,
    ) -> list[RetrievalResult]:
        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        results = self._collection.query(
            query_embeddings=[list(embedding)],
            n_results=top_k,
        )

        ids = results["ids"][0]
        documents = results["documents"][0]
        distances = results["distances"][0]
        metadatas = results["metadatas"][0]

        retrieval_results: list[RetrievalResult] = []

        for rank, (chunk_id, text, distance, metadata) in enumerate(
            zip(ids, documents, distances, metadatas),
            start=1,
        ):
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                document_id=metadata["document_id"],
                document_version=int(metadata["document_version"]),
                chunking_version=metadata["chunking_version"],
                text=text,
                metadata={},
                sequence_number=int(metadata["sequence_number"]),
                start_offset=0,
                end_offset=len(text),
            )

            # Chroma's squared L2 distance for normalized vectors:
            # distance = 2 * (1 - cosine_similarity)
            score = 1.0 - (distance / 2.0)

            retrieval_results.append(
                RetrievalResult(
                    chunk=chunk,
                    score=score,
                    rank=rank,
                )
            )

        return retrieval_results