"""PDF document parser."""

from datetime import UTC, datetime
from io import BytesIO

from pypdf import PdfReader

from rag_platform.domain.models import ParsedDocument, SourceDocument


class PDFParser:
    """Extract textual content from PDF documents."""
    VERSION = 1
    def parse(self, document: SourceDocument) -> ParsedDocument:
        reader = PdfReader(BytesIO(document.content))
        pages: list[str] = []

        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages.append(text)
        extracted_text = "\n\n".join(pages)
        metadata = {
            **document.metadata,
            "page_count": str(len(reader.pages)),
        }

        return ParsedDocument(
            id=document.id,
            source_document_id=document.id,
            parser_version=self.VERSION,
            format=document.format,
            text=extracted_text,
            metadata=metadata,
            parsed_at=datetime.now(UTC),
        )
