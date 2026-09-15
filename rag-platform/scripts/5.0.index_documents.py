from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

from rag_platform.domain.models import DocumentChunk
from rag_platform.embeddings import SentenceTransformerEmbeddingModel
from rag_platform.indexing import IndexManifest, Indexer
from rag_platform.logging import configure_logging
from rag_platform.vector_store import ChromaVectorStore

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHUNKS_ROOT = PROJECT_ROOT / "data/processed/chunks/ZCompanyLLC"
VECTOR_STORE_ROOT = PROJECT_ROOT / "data/processed/vector_store/ZCompanyLLC"
MANIFEST_PATH = VECTOR_STORE_ROOT / "index_manifest.json"
LOG_PATH = PROJECT_ROOT / "logs/indexing.log"
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "zcompany_hr_chunks"
INDEX_VERSION = "index-v1"

LOGGER = configure_logging(
    logger_name=__name__,
    log_file=str(LOG_PATH),
)


def load_chunks() -> dict[str, list[DocumentChunk]]:
    documents: dict[str, list[DocumentChunk]] = {}
    files = sorted(CHUNKS_ROOT.rglob("*.jsonl"))
    LOGGER.info("chunks_loading_started", extra={"files": len(files), "chunks_root": str(CHUNKS_ROOT)})

    for path in files:
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    raw: dict[str, Any] = json.loads(line)
                    chunk = DocumentChunk(**raw)
                    documents.setdefault(str(chunk.document_id), []).append(chunk)
        except Exception:
            LOGGER.exception("chunks_file_load_failed", extra={"path": str(path)})
            raise

    for chunks in documents.values():
        chunks.sort(key=lambda item: item.sequence_number)

    LOGGER.info(
        "chunks_loaded",
        extra={
            "documents": len(documents),
            "chunks": sum(len(chunks) for chunks in documents.values()),
        },
    )
    return documents


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Synchronize document chunks into the persistent vector index."
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Delete the existing vector index and rebuild it from all persisted chunks.",
    )
    args = parser.parse_args()

    LOGGER.info("indexing_started", extra={"rebuild": args.rebuild})
    VECTOR_STORE_ROOT.mkdir(parents=True, exist_ok=True)

    try:
        vector_store = ChromaVectorStore(
            path=VECTOR_STORE_ROOT,
            collection_name=COLLECTION_NAME,
            embedding_model=EMBEDDING_MODEL_NAME,
        )
        embedding_model = SentenceTransformerEmbeddingModel(EMBEDDING_MODEL_NAME)
        indexer = Indexer(
            embedding_model=embedding_model,
            vector_store=vector_store,
            embedding_model_name=EMBEDDING_MODEL_NAME,
        )

        if args.rebuild:
            LOGGER.info(
                "full_index_rebuild_started",
                extra={"manifest_path": str(MANIFEST_PATH)},
            )
            vector_store.delete_all()
            manifest = IndexManifest.empty(
                index_version=INDEX_VERSION,
                embedding_model=EMBEDDING_MODEL_NAME,
            )
        else:
            manifest = IndexManifest.load(
                MANIFEST_PATH,
                index_version=INDEX_VERSION,
                embedding_model=EMBEDDING_MODEL_NAME,
            )

        documents = load_chunks()
        result = indexer.synchronize(documents, manifest)
        manifest.save(MANIFEST_PATH)
        LOGGER.info(
            "indexing_manifest_saved",
            extra={
                "manifest_path": str(MANIFEST_PATH),
                "documents": len(manifest.documents),
            },
        )

        print(
            f"Indexing complete: {result.chunks_indexed} chunks indexed, "
            f"{result.documents_new} new, {result.documents_changed} changed, "
            f"{result.documents_unchanged} unchanged, {result.documents_deleted} deleted."
        )
    except Exception:
        LOGGER.exception("indexing_failed", extra={"rebuild": args.rebuild})
        raise


if __name__ == "__main__":
    main()
