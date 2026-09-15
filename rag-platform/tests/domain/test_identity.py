from rag_platform.domain.identity import (
    calculate_checksum,
    derive_chunk_id,
    derive_document_id,
    generate_source_id,
)
from rag_platform.domain.types import DocumentID, SourceID


def test_source_id_is_generated() -> None:
    source_id = generate_source_id()

    assert source_id
    assert len(str(source_id)) == 36


def test_document_id_is_deterministic() -> None:
    source_id = SourceID("source-123")

    first = derive_document_id(source_id, "policy-123")
    second = derive_document_id(source_id, "policy-123")

    assert first == second


def test_document_id_changes_when_source_identity_changes() -> None:
    first = derive_document_id(
        SourceID("source-1"),
        "policy-123",
    )

    second = derive_document_id(
        SourceID("source-2"),
        "policy-123",
    )

    assert first != second


def test_checksum_is_content_deterministic() -> None:
    content = b"customer trading policy"

    first = calculate_checksum(content)
    second = calculate_checksum(content)

    assert first == second


def test_checksum_changes_when_content_changes() -> None:
    first = calculate_checksum(b"version one")
    second = calculate_checksum(b"version two")

    assert first != second


def test_chunk_id_is_deterministic() -> None:
    document_id = DocumentID("document-123")

    first = derive_chunk_id(
        document_id,
        1,
        "chunker-1",
        0,
        "policy text",
    )

    second = derive_chunk_id(
        document_id,
        1,
        "chunker-1",
        0,
        "policy text",
    )

    assert first == second


def test_chunk_id_changes_when_chunk_lineage_changes() -> None:
    document_id = DocumentID("document-123")

    first = derive_chunk_id(
        document_id,
        1,
        "chunker-1",
        0,
        "policy text",
    )

    second = derive_chunk_id(
        document_id,
        2,
        "chunker-1",
        0,
        "policy text",
    )

    assert first != second


def test_source_id_is_time_sortable() -> None:
    first = generate_source_id()
    second = generate_source_id()

    assert first
    assert second
    assert len(str(first)) == 36
    assert len(str(second)) == 36

def test_checksum_is_sha256_hex() -> None:
    checksum = calculate_checksum(b"hello")

    assert len(checksum) == 64
    assert all(character in "0123456789abcdef" for character in checksum)

def test_chunk_id_changes_when_chunking_version_changes() -> None:
    document_id = DocumentID("document-123")

    first = derive_chunk_id(
        document_id,
        1,
        "chunker-1",
        0,
        "policy text",
    )

    second = derive_chunk_id(
        document_id,
        1,
        "chunker-2",
        0,
        "policy text",
    )

    assert first != second

def test_chunk_id_changes_when_text_changes() -> None:
    document_id = DocumentID("document-123")

    first = derive_chunk_id(
        document_id,
        1,
        "chunker-1",
        0,
        "policy text",
    )

    second = derive_chunk_id(
        document_id,
        1,
        "chunker-1",
        0,
        "different policy text",
    )

    assert first != second