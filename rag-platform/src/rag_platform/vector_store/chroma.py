from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast

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

    def delete(self, ids: Sequence[str]) -> None:
        """Delete the supplied chunk IDs from the collection."""
        if not ids:
            return
        self._collection.delete(ids=[str(chunk_id) for chunk_id in ids])

    def delete_all(self) -> None:
        """Delete every chunk currently stored in the collection."""
        result = self._collection.get()
        ids = result.get("ids", [])
        if ids:
            self._collection.delete(ids=[str(chunk_id) for chunk_id in ids])

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
        documents_result = results["documents"]
        if documents_result is None:
            raise RuntimeError("Chroma query did not return documents.")
        documents = documents_result[0]
        if documents is None:
            raise RuntimeError("Chroma query did not return documents.")
        distances_result = results["distances"]
        if distances_result is None:
            raise RuntimeError("Chroma query did not return distances.")
        distances = distances_result[0]
        metadatas_result = results["metadatas"]
        if metadatas_result is None:
            raise RuntimeError("Chroma query did not return metadata.")
        metadatas = metadatas_result[0]

        retrieval_results: list[RetrievalResult] = []

        for rank, (chunk_id, text, distance, metadata) in enumerate(
            zip(ids, documents, distances, metadatas),
            start=1,
        ):
            metadata_dict = cast(dict[str, Any], metadata)

            document_id = cast(str, metadata_dict["document_id"])
            document_version = int(metadata_dict["document_version"])
            chunking_version = cast(str, metadata_dict["chunking_version"])
            sequence_number = int(metadata_dict["sequence_number"])

            chunk = DocumentChunk(
                chunk_id=cast(ChunkID, chunk_id),
                document_id=metadata_dict["document_id"],
                document_version=document_version,
                chunking_version=chunking_version,
                text=text,
                metadata={},
                sequence_number=sequence_number,
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
