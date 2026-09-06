"""Filesystem connector for local document ingestion."""

from datetime import UTC, datetime
from pathlib import Path

from rag_platform.domain.identity import (
    calculate_checksum,
    derive_document_id,
)
from rag_platform.domain.models import (
    DocumentFormat,
    DocumentSource,
    SourceDocument,
    SourceType,
)


class FilesystemConnector:
    """Read supported documents from a local filesystem directory."""

    SUPPORTED_FORMATS: dict[str, DocumentFormat] = {
        ".pdf": DocumentFormat.PDF,
        ".md": DocumentFormat.MARKDOWN,
        ".markdown": DocumentFormat.MARKDOWN,
        ".txt": DocumentFormat.TXT,
    }

    def __init__(self, source: DocumentSource) -> None:
        if source.source_type is not SourceType.FILE:
            raise ValueError(
                "FilesystemConnector requires a FILE source."
            )

        self.source = source
        self.root = Path(source.uri)

    def read(self) -> list[SourceDocument]:
        """Read supported files from the configured source."""
        if not self.root.exists():
            raise FileNotFoundError(
                f"Source directory does not exist: {self.root}"
            )

        if not self.root.is_dir():
            raise NotADirectoryError(
                f"Source URI is not a directory: {self.root}"
            )

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

    @classmethod
    def _detect_format(
        cls,
        path: Path,
    ) -> DocumentFormat | None:
        return cls.SUPPORTED_FORMATS.get(path.suffix.lower())