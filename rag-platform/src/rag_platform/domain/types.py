"""Strongly typed identifiers used by the RAG domain."""

from typing import NewType

TenantID = NewType("TenantID", str)
SourceID = NewType("SourceID", str)
DocumentID = NewType("DocumentID", str)
ChunkID = NewType("ChunkID", str)
EmbeddingID = NewType("EmbeddingID", str)
