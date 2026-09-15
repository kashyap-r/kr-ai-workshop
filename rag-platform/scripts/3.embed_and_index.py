import json
from pathlib import Path
from time import perf_counter

from rag_platform.domain.models import DocumentChunk
from rag_platform.embeddings import SentenceTransformerEmbeddingModel
from rag_platform.logging import configure_logging
from rag_platform.vector_store import ChromaVectorStore

logger = configure_logging(
    logger_name=__name__,
    log_file="logs/embedding.log",
)

CHUNKS_ROOT = Path("data/processed/chunks/ZCompanyLLC")
VECTOR_STORE_ROOT = Path("data/processed/vector_store/ZCompanyLLC")

MODEL_NAME = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "zcompany_hr_chunks"

EMBEDDING_MODEL = SentenceTransformerEmbeddingModel(MODEL_NAME)

VECTOR_STORE = ChromaVectorStore(
    path=VECTOR_STORE_ROOT,
    collection_name=COLLECTION_NAME,
    embedding_model=MODEL_NAME,
)


def load_chunks() -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []

    for chunk_file in sorted(CHUNKS_ROOT.rglob("*.jsonl")):
        with chunk_file.open("r", encoding="utf-8") as file:
            for line in file:
                record = json.loads(line)

                chunks.append(
                    DocumentChunk(
                        chunk_id=record["chunk_id"],
                        document_id=record["document_id"],
                        document_version=record["document_version"],
                        chunking_version=record["chunking_version"],
                        text=record["text"],
                        metadata=record["metadata"],
                        sequence_number=record["sequence_number"],
                        start_offset=record["start_offset"],
                        end_offset=record["end_offset"],
                    )
                )

    return chunks


def main() -> None:
    logger.info(
        "embedding_started",
        extra={
            "chunks_root": str(CHUNKS_ROOT),
            "embedding_model": MODEL_NAME,
        },
    )

    chunks = load_chunks()

    logger.info(
        "chunks_loaded",
        extra={
            "chunks": len(chunks),
        },
    )

    if not chunks:
        logger.warning("no_chunks_found")
        return

    start = perf_counter()

    embeddings = EMBEDDING_MODEL.embed(
        [chunk.text for chunk in chunks]
    )

    embedding_duration = perf_counter() - start

    logger.info(
        "embedding_completed",
        extra={
            "chunks": len(chunks),
            "embedding_dimension": len(embeddings[0]),
            "duration_seconds": round(embedding_duration, 4),
            "chunks_per_second": round(
                len(chunks) / embedding_duration,
                2,
            ),
        },
    )

    start = perf_counter()

    VECTOR_STORE.upsert(
        chunks,
        embeddings,
    )

    indexing_duration = perf_counter() - start

    logger.info(
        "vector_indexing_completed",
        extra={
            "chunks": len(chunks),
            "duration_seconds": round(indexing_duration, 4),
            "vector_store": "chroma",
            "collection": COLLECTION_NAME,
        },
    )

    logger.info(
        "embedding_and_indexing_completed",
        extra={
            "chunks": len(chunks),
            "embedding_model": MODEL_NAME,
            "vector_store": "chroma",
        },
    )


if __name__ == "__main__":
    main()
