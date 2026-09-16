
from __future__ import annotations

from pathlib import Path

from rag_platform.indexing import IndexManifest
from rag_platform.logging import configure_logging
from rag_platform.retrieval import BM25IndexStore
from rag_platform.vector_store import ChromaVectorStore

PROJECT_ROOT = Path(__file__).resolve().parents[1]

VECTOR_STORE_ROOT = PROJECT_ROOT / "data/processed/vector_store/ZCompanyLLC"
MANIFEST_PATH = VECTOR_STORE_ROOT / "index_manifest.json"
SPARSE_INDEX_PATH = VECTOR_STORE_ROOT / "bm25_index.json"

LOG_PATH = PROJECT_ROOT / "logs/indexing.log"

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "zcompany_hr_chunks"
INDEX_VERSION = "index-v1"

LOGGER = configure_logging(
    logger_name=__name__,
    log_file=str(LOG_PATH),
)


def main() -> None:
    LOGGER.info(
        "index_integrity_check_started",
        extra={
            "manifest_path": str(MANIFEST_PATH),
            "vector_store": str(VECTOR_STORE_ROOT),
            "collection": COLLECTION_NAME,
        },
    )

    try:
        # ---------------------------------------------------------
        # Load manifest
        # ---------------------------------------------------------
        manifest = IndexManifest.load(
            MANIFEST_PATH,
            index_version=INDEX_VERSION,
            embedding_model=EMBEDDING_MODEL_NAME,
        )

        manifest_chunk_ids: set[str] = set()
        duplicate_manifest_chunk_ids: set[str] = set()

        for document_id, state in manifest.documents.items():
            for chunk_id in state.chunk_ids:
                if chunk_id in manifest_chunk_ids:
                    duplicate_manifest_chunk_ids.add(chunk_id)

                manifest_chunk_ids.add(chunk_id)

        # ---------------------------------------------------------
        # Read vector-store IDs
        #
        # We use Chroma directly here because this is a validation
        # utility, not normal application retrieval.
        # ---------------------------------------------------------
        vector_store = ChromaVectorStore(
            path=VECTOR_STORE_ROOT,
            collection_name=COLLECTION_NAME,
            embedding_model=EMBEDDING_MODEL_NAME,
        )

        collection = vector_store._collection
        result = collection.get()

        vector_store_chunk_ids = {
            str(chunk_id)
            for chunk_id in result.get("ids", [])
        }

        # ---------------------------------------------------------
        # Read sparse/BM25 index IDs
        # ---------------------------------------------------------
        sparse_index = BM25IndexStore(SPARSE_INDEX_PATH)
        sparse_index_chunk_ids = {str(chunk.chunk_id) for chunk in sparse_index.chunks}

        # ---------------------------------------------------------
        # Compare
        # ---------------------------------------------------------
        missing_chunks = manifest_chunk_ids - vector_store_chunk_ids
        orphan_chunks = vector_store_chunk_ids - manifest_chunk_ids

        missing_sparse_chunks = manifest_chunk_ids - sparse_index_chunk_ids
        orphan_sparse_chunks = sparse_index_chunk_ids - manifest_chunk_ids

        manifest_documents = len(manifest.documents)
        manifest_chunks = len(manifest_chunk_ids)
        vector_store_chunks = len(vector_store_chunk_ids)
        sparse_index_chunks = len(sparse_index_chunk_ids)

        integrity_errors: list[str] = []

        if duplicate_manifest_chunk_ids:
            integrity_errors.append(
                "Duplicate chunk IDs in manifest: "
                f"{sorted(duplicate_manifest_chunk_ids)}"
            )

        if missing_chunks:
            integrity_errors.append(
                f"Manifest chunks missing from vector store: "
                f"{sorted(missing_chunks)}"
            )

        if orphan_chunks:
            integrity_errors.append(
                f"Vector-store chunks missing from manifest: "
                f"{sorted(orphan_chunks)}"
            )

        if missing_sparse_chunks:
            integrity_errors.append(
                f"Manifest chunks missing from sparse index: "
                f"{sorted(missing_sparse_chunks)}"
            )

        if orphan_sparse_chunks:
            integrity_errors.append(
                f"Sparse-index chunks missing from manifest: "
                f"{sorted(orphan_sparse_chunks)}"
            )

        # ---------------------------------------------------------
        # Result
        # ---------------------------------------------------------
        if integrity_errors:
            LOGGER.error(
                "index_integrity_check_failed",
                extra={
                    "documents": manifest_documents,
                    "manifest_chunks": manifest_chunks,
                    "vector_store_chunks": vector_store_chunks,
                    "sparse_index_chunks": sparse_index_chunks,
                    "missing_chunks": len(missing_chunks),
                    "orphan_chunks": len(orphan_chunks),
                    "missing_sparse_chunks": len(missing_sparse_chunks),
                    "orphan_sparse_chunks": len(orphan_sparse_chunks),
                    "duplicate_manifest_chunks": len(
                        duplicate_manifest_chunk_ids
                    ),
                    "errors": integrity_errors,
                },
            )

            print("Index integrity check FAILED.")
            print()
            print(f"Documents: {manifest_documents}")
            print(f"Manifest chunks: {manifest_chunks}")
            print(f"Vector store chunks: {vector_store_chunks}")
            print(f"Sparse index chunks: {sparse_index_chunks}")
            print(f"Missing: {len(missing_chunks)}")
            print(f"Orphans: {len(orphan_chunks)}")
            print(f"Sparse missing: {len(missing_sparse_chunks)}")
            print(f"Sparse orphans: {len(orphan_sparse_chunks)}")
            print(
                "Duplicate manifest chunks: "
                f"{len(duplicate_manifest_chunk_ids)}"
            )
            print()
            for error in integrity_errors:
                print(f"ERROR: {error}")

            raise SystemExit(1)

        LOGGER.info(
            "index_integrity_check_completed",
            extra={
                "documents": manifest_documents,
                "manifest_chunks": manifest_chunks,
                "vector_store_chunks": vector_store_chunks,
                "sparse_index_chunks": sparse_index_chunks,
                "missing_chunks": 0,
                "orphan_chunks": 0,
                "missing_sparse_chunks": 0,
                "orphan_sparse_chunks": 0,
                "duplicate_manifest_chunks": 0,
            },
        )

        print("Index integrity check passed.")
        print()
        print(f"Documents: {manifest_documents}")
        print(f"Manifest chunks: {manifest_chunks}")
        print(f"Vector store chunks: {vector_store_chunks}")
        print(f"Sparse index chunks: {sparse_index_chunks}")
        print("Missing: 0")
        print("Orphans: 0")
        print("Sparse missing: 0")
        print("Sparse orphans: 0")
        print("Duplicate manifest chunks: 0")

    except SystemExit:
        raise
    except Exception:
        LOGGER.exception("index_integrity_check_failed")
        raise


if __name__ == "__main__":
    main()
