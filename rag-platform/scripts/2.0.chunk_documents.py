import json
import logging
from pathlib import Path

from rag_platform.chunking.recursive import RecursiveChunker
from rag_platform.domain.models import DocumentFormat, ParsedDocument
from rag_platform.logging import configure_logging

logger = configure_logging(
    logger_name=__name__,
    log_file="logs/chunking.log",
)

PARSED_ROOT = Path("data/processed/parsed/ZCompanyLLC")
METADATA_FILE = Path("data/processed/metadata/parsed_documents.jsonl")
CHUNKS_ROOT = Path("data/processed/chunks/ZCompanyLLC")

CHUNKER = RecursiveChunker(
    chunk_size=1000,
    chunk_overlap=150,
)

def load_metadata() -> dict[str, dict]:
    metadata_by_path = {}

    with METADATA_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            record = json.loads(line)

            source_path = Path(record["path"])

            parsed_path = source_path.with_suffix(".txt")

            metadata_by_path[str(parsed_path)] = record

    return metadata_by_path

def main() -> None:
    logger.info(
        "chunking_started",
        extra={
            "source": str(PARSED_ROOT),
            "chunk_size": CHUNKER.chunk_size,
            "chunk_overlap": CHUNKER.chunk_overlap,
            "chunking_version": CHUNKER.VERSION,
        },
    )

    CHUNKS_ROOT.mkdir(parents=True, exist_ok=True)

    metadata_by_path = load_metadata()

    parsed_files = sorted(PARSED_ROOT.rglob("*.txt"))

    total_chunks = 0
    failed = 0

    for parsed_file in parsed_files:
        try:
            # 1. Find metadata for this parsed document
            relative_path = parsed_file.relative_to(PARSED_ROOT)

            metadata = metadata_by_path.get(str(relative_path))

            if metadata is None:
                raise ValueError(
                    f"No metadata found for {relative_path}"
                )

            # 2. Reconstruct ParsedDocument
            text = parsed_file.read_text(encoding="utf-8")

            document_metadata = {
                key: value
                for key, value in metadata.items()
                if key not in {
                    "document_id",
                    "source_document_id",
                    "format",
                    "parser_version",
                    "parsed_at",
                }
            }

            document = ParsedDocument(
                id=metadata["document_id"],
                source_document_id=metadata["source_document_id"],
                parser_version=metadata["parser_version"],
                format=DocumentFormat(metadata["format"]),
                text=text,
                metadata=document_metadata,
                parsed_at=metadata["parsed_at"],
            )

            # 3. Chunk the document
            chunks = CHUNKER.chunk(document)

            # 4. Write chunks to JSONL
            chunk_file = (
                CHUNKS_ROOT
                / relative_path.parent
                / f"{relative_path.stem}.jsonl"
            )

            chunk_file.parent.mkdir(parents=True, exist_ok=True)

            with chunk_file.open("w", encoding="utf-8") as file:
                for chunk in chunks:
                    record = {
                        "chunk_id": str(chunk.chunk_id),
                        "document_id": str(chunk.document_id),
                        "document_version": chunk.document_version,
                        "chunking_version": chunk.chunking_version,
                        "text": chunk.text,
                        "metadata": dict(chunk.metadata),
                        "sequence_number": chunk.sequence_number,
                        "start_offset": chunk.start_offset,
                        "end_offset": chunk.end_offset,
                    }

                    file.write(json.dumps(record) + "\n")

            total_chunks += len(chunks)

            logger.info(
                "document_chunked",
                extra={
                    "document_id": str(document.id),
                    "path": str(relative_path),
                    "chunks": len(chunks),
                    "artifact_path": str(chunk_file),
                },
            )

        except Exception:
            failed += 1

            logger.exception(
                "document_chunking_failed",
                extra={
                    "parsed_file": str(parsed_file),
                },
            )

    # 5. Log final summary
    logger.info(
        "chunking_completed",
        extra={
            "documents_discovered": len(parsed_files),
            "total_chunks": total_chunks,
            "failed": failed,
        },
    )

if __name__ == "__main__":
    main()