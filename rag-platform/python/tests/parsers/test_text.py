from datetime import UTC, datetime

from rag_platform.domain.models import (
    DocumentFormat,
    SourceDocument,
)
from rag_platform.domain.types import DocumentID, SourceID
from rag_platform.parsers.text import TextParser


def create_document(content: bytes) -> SourceDocument:
    return SourceDocument(
        id=DocumentID("document-1"),
        source_id=SourceID("source-1"),
        version=1,
        format=DocumentFormat.TXT,
        content=content,
        checksum="checksum",
        ingested_at=datetime.now(UTC),
    )


def test_text_parser_extracts_text() -> None:
    document = create_document(b"Hello RAG")

    parsed = TextParser().parse(document)

    assert parsed.text == "Hello RAG"
    assert parsed.parser_version == 1
    assert parsed.source_document_id == document.id