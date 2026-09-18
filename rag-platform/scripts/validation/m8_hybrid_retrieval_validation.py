from pathlib import Path

from rag_platform.embeddings import SentenceTransformerEmbeddingModel
from rag_platform.retrieval import (
    BM25IndexStore,
    BM25Retriever,
    DenseRetriever,
    HybridRetriever,
    RRFFusion,
)
from rag_platform.vector_store import ChromaVectorStore


MODEL_NAME = "BAAI/bge-small-en-v1.5"
VECTOR_STORE_ROOT = Path(
    "data/processed/vector_store/ZCompanyLLC"
)
COLLECTION_NAME = "zcompany_hr_chunks"
BM25_INDEX_PATH = VECTOR_STORE_ROOT / "bm25_index.json"


def run_hybrid_retrieval_test() -> None:
    """Validate the complete dense + BM25 + RRF retrieval pipeline."""

    query = "What is the company's policy for working from home?"
    top_k = 5

    embedding_model = SentenceTransformerEmbeddingModel(
        MODEL_NAME
    )

    vector_store = ChromaVectorStore(
        path=VECTOR_STORE_ROOT,
        collection_name=COLLECTION_NAME,
        embedding_model=MODEL_NAME,
    )

    dense_retriever = DenseRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    sparse_index = BM25IndexStore(BM25_INDEX_PATH)

    sparse_retriever = BM25Retriever(
        sparse_index
    )

    hybrid_retriever = HybridRetriever(
        dense_retriever=dense_retriever,
        sparse_retriever=sparse_retriever,
        fusion=RRFFusion(),
    )

    results = hybrid_retriever.retrieve(
        query,
        top_k=top_k,
    )

    print("=== M8.3 — Real Hybrid Retrieval ===")
    print()
    print(f"Query: {query}")
    print()

    if not results:
        raise AssertionError(
            "Expected hybrid retrieval to return results."
        )

    if len(results) > top_k:
        raise AssertionError(
            f"Expected at most {top_k} results, "
            f"got {len(results)}."
        )

    for result in results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"rrf_score={result.score:.6f}"
        )

    ranks = [result.rank for result in results]

    if ranks != list(range(1, len(results) + 1)):
        raise AssertionError(
            f"Ranks are not sequential: {ranks}"
        )

    scores = [result.score for result in results]

    if scores != sorted(scores, reverse=True):
        raise AssertionError(
            "Hybrid results are not ordered by descending RRF score."
        )

    print()
    print("PASS")
    print()
    print("M8.3 real hybrid retrieval validation completed successfully.")

def run_retrieval_comparison_test() -> None:
    """Compare dense, sparse, and hybrid retrieval for the same query."""

    query = "What is the company's policy for working from home?"
    top_k = 5

    embedding_model = SentenceTransformerEmbeddingModel(
        MODEL_NAME
    )

    vector_store = ChromaVectorStore(
        path=VECTOR_STORE_ROOT,
        collection_name=COLLECTION_NAME,
        embedding_model=MODEL_NAME,
    )

    dense_retriever = DenseRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    sparse_index = BM25IndexStore(BM25_INDEX_PATH)

    sparse_retriever = BM25Retriever(
        sparse_index
    )

    hybrid_retriever = HybridRetriever(
        dense_retriever=dense_retriever,
        sparse_retriever=sparse_retriever,
        fusion=RRFFusion(),
    )

    dense_results = dense_retriever.retrieve(
        query,
        top_k=top_k,
    )

    sparse_results = sparse_retriever.retrieve(
        query,
        top_k=top_k,
    )

    hybrid_results = hybrid_retriever.retrieve(
        query,
        top_k=top_k,
    )

    print("=== M8.3 — Dense vs BM25 vs Hybrid ===")
    print()
    print(f"Query: {query}")
    print()

    print("DENSE")
    for result in dense_results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"score={result.score:.6f}"
        )

    print()

    print("BM25")
    for result in sparse_results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"score={result.score:.6f}"
        )

    print()

    print("HYBRID")
    for result in hybrid_results:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"rrf_score={result.score:.6f}"
        )

    dense_ids = {
        str(result.chunk.chunk_id)
        for result in dense_results
    }

    sparse_ids = {
        str(result.chunk.chunk_id)
        for result in sparse_results
    }

    hybrid_ids = {
        str(result.chunk.chunk_id)
        for result in hybrid_results
    }

    overlap_ids = dense_ids & sparse_ids

    print()
    print(
        "Dense/BM25 overlap: "
        f"{len(overlap_ids)} chunk(s)"
    )

    if overlap_ids:
        for chunk_id in sorted(overlap_ids):
            print(f"  {chunk_id}")

    print()

    if not hybrid_ids:
        raise AssertionError(
            "Hybrid retrieval returned no results."
        )

    if not overlap_ids:
        raise AssertionError(
            "Expected at least one chunk to be shared by "
            "dense and BM25 retrieval."
        )

    shared_hybrid_ids = overlap_ids & hybrid_ids

    if not shared_hybrid_ids:
        raise AssertionError(
            "Hybrid retrieval did not return any chunk that was "
            "present in both dense and BM25 candidate sets."
        )

    if len(hybrid_ids) > top_k:
        raise AssertionError(
            f"Hybrid returned more than {top_k} results."
        )

    print("PASS")
    print()
    print(
        "M8.3 dense vs BM25 vs hybrid "
        "validation completed successfully."
    )


def main() -> None:
    run_hybrid_retrieval_test()
    run_retrieval_comparison_test()


if __name__ == "__main__":
    main()