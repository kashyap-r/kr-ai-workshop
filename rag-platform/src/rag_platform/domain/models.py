from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from rag_platform.domain.types import ChunkID, DocumentID, SourceID, TenantID


class SourceType(StrEnum):
    FILE = "file"
    URL = "url"
    DATABASE = "database"
    API = "api"

class DocumentFormat(StrEnum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"

@dataclass(frozen=True, slots=True)
class DocumentSource:
    id: SourceID
    tenant_id: TenantID
    source_type: SourceType
    uri: str

@dataclass(frozen=True, slots=True)
class SourceDocument:
    id: DocumentID
    source_id: SourceID
    version: int
    format: DocumentFormat
    content: bytes
    checksum: str
    ingested_at: datetime
    source_created_at: datetime | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class ParsedDocument:
    id: DocumentID
    source_document_id: DocumentID
    parser_version: int
    format: DocumentFormat
    text: str
    metadata: Mapping[str, str]
    parsed_at: datetime

@dataclass(frozen=True, slots=True)
class DocumentChunk:
    chunk_id: ChunkID
    document_id: DocumentID
    document_version: int
    chunking_version: str
    text: str
    metadata: Mapping[str, str]
    sequence_number: int
    start_offset: int
    end_offset: int

@dataclass(frozen=True, slots=True)
class Chunk:
    id: str
    document_id: str
    text: str
    sequence: int
    metadata: Mapping[str, Any]


"""
This class becomes important when we implement retrieval and ranking. 
It will be used to represent the results of a retrieval operation, 
including the chunk that was retrieved, the score assigned to that chunk 
by the retrieval model, and the rank of that chunk in the list of retrieved chunks.
BM25
dense retrieval
hybrid fusion
reranking
"""
@dataclass(frozen=True, slots=True)
class RetrievalResult:
    chunk: DocumentChunk
    score: float
    rank: int

