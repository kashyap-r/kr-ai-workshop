from pathlib import Path

from rag_platform.embeddings import SentenceTransformerEmbeddingModel
from rag_platform.retrieval import (
    BM25IndexStore,
    BM25Retriever,
    CrossEncoderReranker,
    DenseRetriever,
    HybridRetriever,
    RRFFusion,
)
from rag_platform.vector_store import ChromaVectorStore


MODEL_NAME = "BAAI/bge-small-en-v1.5"
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

VECTOR_STORE_ROOT = Path(
    "data/processed/vector_store/ZCompanyLLC"
)
COLLECTION_NAME = "zcompany_hr_chunks"
BM25_INDEX_PATH = VECTOR_STORE_ROOT / "bm25_index.json"


def build_hybrid_retriever() -> HybridRetriever:
    """Build the same hybrid retriever used by M8."""

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

    return HybridRetriever(
        dense_retriever=dense_retriever,
        sparse_retriever=sparse_retriever,
        fusion=RRFFusion(),
    )


def run_reranker_validation() -> None:
    """Validate real hybrid retrieval followed by cross-encoder reranking."""

    query = "What is the company's policy for working from home?"
    candidate_k = 20
    top_k = 5

    hybrid_retriever = build_hybrid_retriever()

    reranker = CrossEncoderReranker(
        model_name=RERANKER_MODEL_NAME
    )

    candidates = hybrid_retriever.retrieve(
        query,
        top_k=candidate_k,
    )

    print("=== M9.3 — Real Cross-Encoder Reranking ===")
    print()
    print(f"Query: {query}")
    print(f"Candidates from M8: {len(candidates)}")
    print(f"Final top_k: {top_k}")
    print(f"Reranker: {RERANKER_MODEL_NAME}")
    print()

    if not candidates:
        raise AssertionError(
            "Expected hybrid retrieval to return candidates."
        )

    reranked = reranker.rerank(
        query,
        candidates,
    )

    if len(reranked) != len(candidates):
        raise AssertionError(
            "Reranker must return the same number of candidates."
        )

    candidate_ids = {
        str(result.chunk.chunk_id)
        for result in candidates
    }

    reranked_ids = {
        str(result.chunk.chunk_id)
        for result in reranked
    }

    if candidate_ids != reranked_ids:
        raise AssertionError(
            "Reranker changed the candidate set."
        )

    ranks = [
        result.rank
        for result in reranked
    ]

    if ranks != list(range(1, len(reranked) + 1)):
        raise AssertionError(
            f"Reranked ranks are not sequential: {ranks}"
        )

    scores = [
        result.score
        for result in reranked
    ]

    if scores != sorted(scores, reverse=True):
        raise AssertionError(
            "Reranked results are not ordered by descending score."
        )

    if len(set(scores)) <= 1:
        raise AssertionError(
            "Expected cross-encoder to produce varying relevance scores."
        )

    print("M8 HYBRID CANDIDATES")

    for result in candidates:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"rrf_score={result.score:.6f}"
        )

    print()
    print("M9 RERANKED CANDIDATES")

    for result in reranked:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"rerank_score={result.score:.6f}"
        )

    print()
    print("FINAL TOP-K")

    for result in reranked[:top_k]:
        print(
            f"rank={result.rank} "
            f"chunk_id={result.chunk.chunk_id} "
            f"rerank_score={result.score:.6f}"
        )

    print()
    print("PASS")
    print()
    print(
        "M9.3 real cross-encoder reranking "
        "validation completed successfully."
    )


def main() -> None:
    run_reranker_validation()


if __name__ == "__main__":
    main()