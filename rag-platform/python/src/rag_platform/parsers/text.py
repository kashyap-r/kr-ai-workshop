"""Plain text document parser."""

from datetime import UTC, datetime
from rag_platform.domain.models import ParsedDocument, SourceDocument

class TextParser:
    """Parse UTF-8 plain text documents."""
    VERSION = 1
    def parse(self, document: SourceDocument) -> ParsedDocument:
        text = document.content.decode("utf-8")

        return ParsedDocument(
            id=document.id,
            source_document_id=document.id,
            parser_version=self.VERSION,
            format=document.format,
            text=text,
            metadata={},
            parsed_at=datetime.now(UTC),
        )