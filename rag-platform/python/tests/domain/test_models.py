from datetime import UTC, datetime

from rag_platform.domain.models import (
    DocumentChunk,
    DocumentFormat,
    DocumentSource,
    ParsedDocument,
    SourceDocument,
    SourceType,
)
from rag_platform.domain.types import (
    ChunkID,
    DocumentID,
    SourceID,
    TenantID,
)


def test_document_source_is_tenant_scoped() -> None:
    source_a = DocumentSource(
        id=SourceID("source-1"),
        tenant_id=TenantID("tenant-a"),
        source_type=SourceType.FILE,
        uri="/documents/policy.pdf",
    )

    source_b = DocumentSource(
        id=SourceID("source-2"),
        tenant_id=TenantID("tenant-b"),
        source_type=SourceType.FILE,
        uri="/documents/policy.pdf",
    )

    assert source_a.uri == source_b.uri
    assert source_a.tenant_id != source_b.tenant_id
    assert source_a.id != source_b.id


def test_source_document_supports_versioning() -> None:
    ingested_at = datetime.now(UTC)

    version_1 = SourceDocument(
        id=DocumentID("policy"),
        source_id=SourceID("source-1"),
        version=1,
        format=DocumentFormat.PDF,
        content=b"policy version one",
        checksum="checksum-v1",
        source_created_at=None,
        ingested_at=ingested_at,
    )

    version_2 = SourceDocument(
        id=DocumentID("policy"),
        source_id=SourceID("source-1"),
        version=2,
        format=DocumentFormat.PDF,
        content=b"policy version two",
        checksum="checksum-v2",
        source_created_at=None,
        ingested_at=ingested_at,
    )

    assert version_1.id == version_2.id
    assert version_1.version != version_2.version
    assert version_1.checksum != version_2.checksum


def test_parser_version_is_processing_lineage() -> None:
    parsed_v1 = ParsedDocument(
        id=DocumentID("policy"),
        source_document_id=DocumentID("policy"),
        parser_version=1,
        format=DocumentFormat.PDF,
        text="parsed policy",
        metadata={},
        parsed_at=datetime.now(UTC),
    )

    parsed_v2 = ParsedDocument(
        id=DocumentID("policy"),
        source_document_id=DocumentID("policy"),
        parser_version=2,
        format=DocumentFormat.PDF,
        text="parsed policy differently",
        metadata={},
        parsed_at=datetime.now(UTC),
    )

    assert parsed_v1.source_document_id == parsed_v2.source_document_id
    assert parsed_v1.parser_version != parsed_v2.parser_version


def test_chunking_version_is_processing_lineage() -> None:
    chunk_v1 = DocumentChunk(
        chunk_id=ChunkID("chunk-1"),
        document_id=DocumentID("policy"),
        document_version=1,
        chunking_version="chunker-1",
        text="policy text",
        metadata={},
        sequence_number=0,
        start_offset=0,
        end_offset=11,
    )

    chunk_v2 = DocumentChunk(
        chunk_id=ChunkID("chunk-2"),
        document_id=DocumentID("policy"),
        document_version=1,
        chunking_version="chunker-2",
        text="policy text",
        metadata={},
        sequence_number=0,
        start_offset=0,
        end_offset=11,
    )

    assert chunk_v1.document_id == chunk_v2.document_id
    assert chunk_v1.chunking_version != chunk_v2.chunking_version
    assert chunk_v1.chunk_id != chunk_v2.chunk_id
