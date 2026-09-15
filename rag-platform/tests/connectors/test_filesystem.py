from pathlib import Path

import pytest

from rag_platform.connectors.filesystem import FilesystemConnector
from rag_platform.domain.identity import calculate_checksum
from rag_platform.domain.models import (
    DocumentFormat,
    DocumentSource,
    SourceType,
)
from rag_platform.domain.types import SourceID, TenantID


def create_source(path: Path) -> DocumentSource:
    return DocumentSource(
        id=SourceID("source-1"),
        tenant_id=TenantID("tenant-1"),
        source_type=SourceType.FILE,
        uri=str(path),
    )

def test_filesystem_connector_reads_supported_files(
    tmp_path: Path,
) -> None:
    (tmp_path / "policy.md").write_text("# Leave Policy")
    (tmp_path / "benefits.txt").write_text("Employee benefits")
    (tmp_path / "ignored.csv").write_text("name,value")

    connector = FilesystemConnector(create_source(tmp_path))

    documents = connector.read()

    assert len(documents) == 2
    assert {document.format for document in documents} == {
        DocumentFormat.MARKDOWN,
        DocumentFormat.TXT,
    }

def test_filesystem_connector_preserves_content(
    tmp_path: Path,
) -> None:
    content = b"parental leave policy"

    (tmp_path / "leave.txt").write_bytes(content)

    connector = FilesystemConnector(create_source(tmp_path))

    documents = connector.read()

    assert len(documents) == 1
    assert documents[0].content == content

def test_filesystem_connector_calculates_checksum(
    tmp_path: Path,
) -> None:
    content = b"parental leave policy"

    (tmp_path / "leave.txt").write_bytes(content)

    connector = FilesystemConnector(create_source(tmp_path))

    documents = connector.read()

    assert documents[0].checksum == calculate_checksum(content)

def test_filesystem_connector_requires_file_source(
    tmp_path: Path,
) -> None:
    source = DocumentSource(
        id=SourceID("source-1"),
        tenant_id=TenantID("tenant-1"),
        source_type=SourceType.URL,
        uri=str(tmp_path),
    )

    with pytest.raises(ValueError, match="FILE source"):
        FilesystemConnector(source)

def test_filesystem_connector_rejects_missing_directory(
    tmp_path: Path,
) -> None:
    source = create_source(tmp_path / "does-not-exist")

    connector = FilesystemConnector(source)

    with pytest.raises(FileNotFoundError):
        connector.read()

def test_filesystem_connector_rejects_file_as_directory(
    tmp_path: Path,
) -> None:
    path = tmp_path / "document.txt"
    path.write_text("hello")

    connector = FilesystemConnector(create_source(path))

    with pytest.raises(NotADirectoryError):
        connector.read()

def test_filesystem_connector_generates_stable_document_identity(
    tmp_path: Path,
) -> None:
    (tmp_path / "policy.txt").write_text("policy")

    source = create_source(tmp_path)

    first = FilesystemConnector(source).read()
    second = FilesystemConnector(source).read()

    assert first[0].id == second[0].id
