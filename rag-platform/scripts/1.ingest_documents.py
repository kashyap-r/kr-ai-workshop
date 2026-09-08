from pathlib import Path
import json
import logging
from rag_platform.logging import configure_logging
from rag_platform.connectors.filesystem import FilesystemConnector
from rag_platform.domain.models import DocumentFormat, DocumentSource, SourceType
from rag_platform.domain.types import TenantID
from rag_platform.domain.identity import generate_source_id
from rag_platform.parsers.markdown import MarkdownParser
from rag_platform.parsers.pdf import PDFParser
from rag_platform.parsers.text import TextParser

logger = configure_logging(logger_name=__name__, log_file="logs/ingestion.log")

# this path holds the parsed documents 
PARSED_ROOT = Path("data/processed/parsed/ZCompanyLLC")
# this path and file will hold the metadata of all the successfully parsed documents
METADATA_FILE = Path("data/processed/metadata/parsed_documents.jsonl")

# logger = logging.getLogger(__name__)
PARSERS = {
    DocumentFormat.MARKDOWN: MarkdownParser(),
    DocumentFormat.TXT: TextParser(),
    DocumentFormat.PDF: PDFParser(),
}
    
def main() -> None:
    
    root = Path("data/raw/ZCompanyLLC")
    
    logger.info("ingestion_started", 
                extra={"tenant_id": "ZCompanyLLC","source_path": str(root),
                       },
                       )

    PARSED_ROOT.mkdir(parents=True, exist_ok=True)
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    source = DocumentSource(
        id=generate_source_id(),
        tenant_id=TenantID("ZCompanyLLC"),
        source_type=SourceType.FILE,
        uri=str(root) )
    
    connector = FilesystemConnector(source)
    documents = connector.read()

    parsed_count = 0
    failed_count = 0

    for document in documents:
        try:
            parser = PARSERS[document.format]
            parsed = parser.parse(document)

            relative_path = document.metadata.get("path", str(document.id))
            source_relative_path = Path(relative_path)
            parsed_path = (
                PARSED_ROOT
                / source_relative_path.parent
                / f"{source_relative_path.stem}.txt"
            )

            parsed_path.parent.mkdir(parents=True, exist_ok=True)
            parsed_path.write_text(parsed.text, encoding="utf-8")

            logger.info(
                "document_parsed",
                extra={
                    "document_id": str(parsed.id),
                    "path": relative_path,
                    "format": parsed.format.value,
                    "characters": len(parsed.text),
                    "parser_version": parsed.parser_version,
                },
            )

            logger.info(
                "parsed_artifact_written",
                extra={
                    "document_id": str(parsed.id),
                    "artifact_path": str(parsed_path),
                },
            )

            # create the registry record
            metadata_record = {
                "document_id": str(parsed.id),
                "source_document_id": str(parsed.source_document_id),
                "path": relative_path,
                "filename": document.metadata.get("filename", source_relative_path.name),
                "format": parsed.format.value,
                "parser_version": parsed.parser_version,
                "parsed_at": parsed.parsed_at.isoformat(),
                **parsed.metadata,
            }

            # append it to the JSONL
            with METADATA_FILE.open("a", encoding="utf-8") as f:
                f.write(json.dumps(metadata_record) + "\n")

            logger.info(
                "metadata_written",
                extra={
                    "document_id": str(parsed.id),
                    "registry": str(METADATA_FILE),
                },
            )
            parsed_count += 1

        except Exception as exc:
            logger.exception(
                "document_processing_failed",
                extra={
                    "document_id": str(document.id),
                },
            )  
            failed_count += 1
    logger.info(
        "ingestion_completed",
        extra={
            "documents_discovered": len(documents),
            "successfully_parsed": parsed_count,
            "failed": failed_count,
        },
    )

if __name__ == "__main__":
    main()