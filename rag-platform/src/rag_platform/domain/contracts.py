""" Behavioral contracts for RAG processing commponents."""

from collections.abc import Sequence
from typing import Protocol

from rag_platform.domain.models import (
    DocumentChunk,
    ParsedDocument,
    RetrievalResult,
    SourceDocument,
)


class Parser(Protocol):
    """ Parse a source document into normalized text and metadata."""

    def parse(self, document: SourceDocument) -> ParsedDocument:
        ...

class Chunker(Protocol):
    """Split a parsed document into retrieval-ready chunks."""
    def chunk(self, document: ParsedDocument) -> Sequence[DocumentChunk]:
        ...

class Embedder(Protocol):
    """Generate vector embeddings for text."""
    def embed(self, texts: Sequence[str]) -> Sequence[Sequence[float]]:
        ...

class Retriever(Protocol):
    """Retrieve candidate chunks for a user query."""
    def retrieve(self, query:str, *, top_k: int = 5,) -> Sequence[RetrievalResult]:
        ...

class Reranker(Protocol):
    """Rerank retrieved candidates against the query."""
    def rerank(self, query: str, context: Sequence[RetrievalResult],) -> str:
        ...

class Generator(Protocol):
    """Generate an answer from a query and retrieved context."""

    def generate(self, query: str, context: Sequence[RetrievalResult],) -> str:
        ...

class SourceReader(Protocol):
    """Read raw documents from a configured source."""
    def read(self) -> Sequence[SourceDocument]:
        ...




