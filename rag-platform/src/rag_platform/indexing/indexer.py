"""Document chunk indexing orchestration."""
from __future__ import annotations

import hashlib
import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from rag_platform.domain.models import DocumentChunk
from rag_platform.embeddings.base import EmbeddingModel
from rag_platform.indexing.manifest import DocumentIndexState, IndexManifest
from rag_platform.vector_store.base import VectorStore

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class IndexingResult:
    documents_discovered: int
    documents_new: int
    documents_changed: int
    documents_unchanged: int
    documents_deleted: int
    chunks_indexed: int
    chunks_deleted: int
    embeddings_generated: int


class Indexer:
    """Synchronize persisted document chunks with a vector index."""

    INDEX_VERSION = "index-v1"

    def __init__(
        self,
        *,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
        embedding_model_name: str,
    ) -> None:
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.embedding_model_name = embedding_model_name

    @staticmethod
    def document_hash(chunks: Sequence[DocumentChunk]) -> str:
        """Create a deterministic fingerprint of the ordered chunk representation."""
        digest = hashlib.sha256()
        for chunk in sorted(chunks, key=lambda item: item.sequence_number):
            for value in (
                str(chunk.sequence_number),
                str(chunk.document_version),
                chunk.chunking_version,
                chunk.text,
            ):
                encoded = value.encode("utf-8")
                digest.update(len(encoded).to_bytes(8, "big"))
                digest.update(encoded)
        return digest.hexdigest()

    def _index_document(self, document_id: str, chunks: Sequence[DocumentChunk]) -> None:
        if not chunks:
            LOGGER.info(
                "empty_document_indexed",
                extra={"document_id": document_id, "chunk_count": 0},
            )
            return

        texts = [chunk.text for chunk in chunks]
        LOGGER.info(
            "document_embedding_started",
            extra={"document_id": document_id, "chunk_count": len(chunks)},
        )
        embeddings = self.embedding_model.embed(texts)
        if len(embeddings) != len(chunks):
            raise ValueError(
                f"Embedding count mismatch for document {document_id}: "
                f"{len(embeddings)} embeddings for {len(chunks)} chunks"
            )
        LOGGER.info(
            "document_embedding_completed",
            extra={"document_id": document_id, "chunk_count": len(chunks)},
        )
        self.vector_store.upsert(chunks, embeddings)
        LOGGER.info(
            "document_indexed",
            extra={"document_id": document_id, "chunk_count": len(chunks)},
        )

    def synchronize(
        self,
        documents: Mapping[str, Sequence[DocumentChunk]],
        manifest: IndexManifest,
    ) -> IndexingResult:
        """Reconcile current chunks with the persisted index manifest."""
        LOGGER.info(
            "incremental_indexing_started",
            extra={
                "documents_discovered": len(documents),
                "documents_in_manifest": len(manifest.documents),
                "embedding_model": self.embedding_model_name,
            },
        )

        new_count = changed_count = unchanged_count = deleted_count = 0
        chunks_indexed = chunks_deleted = embeddings_generated = 0
        updated_documents: dict[str, DocumentIndexState] = {}

        deleted_ids = sorted(set(manifest.documents) - set(documents))
        for document_id in deleted_ids:
            old_state = manifest.documents[document_id]
            if old_state.chunk_ids:
                self.vector_store.delete(old_state.chunk_ids)
                chunks_deleted += len(old_state.chunk_ids)
            deleted_count += 1
            LOGGER.info(
                "document_deleted_from_index",
                extra={
                    "document_id": document_id,
                    "chunk_count": len(old_state.chunk_ids),
                },
            )

        for document_id in sorted(documents):
            chunks = sorted(documents[document_id], key=lambda item: item.sequence_number)
            current_hash = self.document_hash(chunks)
            old_state = manifest.documents.get(document_id)

            if old_state is not None and old_state.document_hash == current_hash:
                unchanged_count += 1
                updated_documents[document_id] = old_state
                LOGGER.info(
                    "document_unchanged_skipped",
                    extra={
                        "document_id": document_id,
                        "chunk_count": len(chunks),
                        "document_hash": current_hash,
                    },
                )
                continue

            if old_state is None:
                new_count += 1
                LOGGER.info(
                    "document_new_indexing",
                    extra={"document_id": document_id, "chunk_count": len(chunks)},
                )
            else:
                changed_count += 1
                LOGGER.info(
                    "document_changed_reindexing",
                    extra={
                        "document_id": document_id,
                        "old_chunk_count": len(old_state.chunk_ids),
                        "new_chunk_count": len(chunks),
                    },
                )
                if old_state.chunk_ids:
                    self.vector_store.delete(old_state.chunk_ids)
                    chunks_deleted += len(old_state.chunk_ids)

            self._index_document(document_id, chunks)
            chunks_indexed += len(chunks)
            embeddings_generated += len(chunks)
            updated_documents[document_id] = DocumentIndexState(
                document_hash=current_hash,
                chunk_ids=[str(chunk.chunk_id) for chunk in chunks],
            )

        manifest.documents = updated_documents
        result = IndexingResult(
            documents_discovered=len(documents),
            documents_new=new_count,
            documents_changed=changed_count,
            documents_unchanged=unchanged_count,
            documents_deleted=deleted_count,
            chunks_indexed=chunks_indexed,
            chunks_deleted=chunks_deleted,
            embeddings_generated=embeddings_generated,
        )

        LOGGER.info(
            "incremental_indexing_completed",
            extra={
                "documents_discovered": result.documents_discovered,
                "documents_new": result.documents_new,
                "documents_changed": result.documents_changed,
                "documents_unchanged": result.documents_unchanged,
                "documents_deleted": result.documents_deleted,
                "chunks_indexed": result.chunks_indexed,
                "chunks_deleted": result.chunks_deleted,
                "embeddings_generated": result.embeddings_generated,
            },
        )
        return result
