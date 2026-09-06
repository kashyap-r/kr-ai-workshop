from datetime import UTC, datetime
from pathlib import Path

from rag_platform.domain.identity import (
    calculate_checksum, 
    derive_document_id, 
    generate_source_id,
)

from rag_platform.domain.models import (
    DocumentFormat, 
    DocumentSource,
    SourceDocument,
    SourceType,
)

from rag_platform.domain.types import TenantID

class FileSourceReader:
    """Read documents from a local filesystem directory."""

    def __init__(self, root: path, tenant_id: TenantID) -> None:
        self.root = root 
        self.tenant_id = tenant_id

        self.source = DocumentSource(
            id=generate_source_id(),
            tenant_id=tenant_id,
            source_type=SourceType.FILE,
            uri=str(root),
        )

    def read(self) -> list[SourceDocument]:
        documents: list[SourceDocument] = []

        for path in sorted(self.root.iterdir()):
            if not path.is_file():
                continue
            document_format = self._detect_format(path)
            if document_format is None:
                continue
            content = path.read_bytes()
            document_id = derive_document_id(
                self.source.id,
                path.name,
            )

            documents.append(
                SourceDocument(
                    id=document_id,
                    source_id=self.source.id,
                    version=1,
                    format=document_format,
                    content=content,
                    checksum=calculate_checksum(content),
                    ingested_at=datetime.now(UTC),
                )
            )

        return documents

    @staticmethod
    def _detect_format(path: Path) -> DocumentFormat | None:
        suffix = path.suffix.lower()

        mapping = {
            ".pdf": DocumentFormat.PDF,
            ".md": DocumentFormat.MARKDOWN,
            ".markdown": DocumentFormat.MARKDOWN,
            ".txt": DocumentFormat.TXT,
        }

        return mapping.get(suffix)
 



    