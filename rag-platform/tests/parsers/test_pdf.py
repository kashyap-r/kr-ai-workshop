from io import BytesIO
from pypdf import PdfWriter
from datetime import datetime, UTC 

from rag_platform.domain.models import ParsedDocument, SourceDocument, DocumentFormat
from rag_platform.domain.types import DocumentID, SourceID
from rag_platform.parsers.pdf import PDFParser

def create_pdf() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)

    buffer = BytesIO()
    writer.write(buffer)

    return buffer.getvalue()

def test_pdf_parser_reads_pdf() -> None:
    content = create_pdf()

    document = SourceDocument(
        id=DocumentID("document-1"),
        source_id=SourceID("source-1"),
        version=1,
        format=DocumentFormat.PDF,
        content=content,
        checksum="checksum",
        ingested_at=datetime.now(UTC),
    )

    parsed = PDFParser().parse(document)

    assert parsed.parser_version == 1
    assert parsed.metadata["page_count"] == "1"