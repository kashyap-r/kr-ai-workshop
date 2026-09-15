from datetime import datetime, UTC

from rag_platform.domain.models import SourceDocument, DocumentFormat
from rag_platform.domain.types import SourceID, DocumentID
from rag_platform.parsers.markdown import MarkdownParser


def test_markdown_parser_preserves_markdown() -> None:
    document = SourceDocument(
        id=DocumentID("document-1"),
        source_id=SourceID("source-1"),
        version=1,
        format=DocumentFormat.MARKDOWN,
        content=b"# Benefits\n\nEmployees receive benefits.",
        checksum="checksum",
        ingested_at=datetime.now(UTC),
    )

    parsed = MarkdownParser().parse(document)

    assert parsed.text == "# Benefits\n\nEmployees receive benefits."