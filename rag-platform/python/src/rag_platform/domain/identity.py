"""Identity and content-addressing utilities for the RAG domain."""

from hashlib import sha256
from uuid import uuid4

from rag_platform.domain.types import ChunkID, DocumentID, SourceID


def generate_source_id() -> SourceID:
    """Generate a time-sortable identifier for a new source."""
    return SourceID(str(uuid4()))


def derive_document_id(source_id: SourceID, source_document_key: str) -> DocumentID:
    """Derive a deterministic logical document identifier."""
    canonical_key = f"{source_id}:{source_document_key}"
    digest = sha256(canonical_key.encode("utf-8")).hexdigest()
    return DocumentID(digest)


def calculate_checksum(content: bytes) -> str:
    """Calculate the SHA-256 checksum of raw source content."""
    return sha256(content).hexdigest()


def derive_chunk_id(
    document_id: DocumentID,
    document_version: int,
    chunking_version: str,
    sequence_number: int,
    text: str,
) -> ChunkID:
    """Derive a deterministic identifier for a document chunk."""
    canonical_key = (
        f"{document_id}:"
        f"{document_version}:"
        f"{chunking_version}:"
        f"{sequence_number}:"
        f"{text}"
    )

    digest = sha256(canonical_key.encode("utf-8")).hexdigest()
    return ChunkID(digest)
