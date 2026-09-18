from pathlib import Path

from rag_platform.context import ContextAssembler
from rag_platform.context.assembler import ContextAssemblyConfig
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

CONTEXT_BUDGET = 4000
CANDIDATE_K = 20
FINAL_TOP_K = 5


QUERIES = [
    "What is the company's policy for working from home?",
    "How much maternity leave is available in Germany?",
    (
        "Which maternity leave policy applies to a Sweden-based "
        "employee temporarily working in India?"
    ),
    "Does being on a PIP remove an employee's right to annual leave?",
    (
        "Compare annual leave and maternity leave entitlements "
        "across Sweden, Germany, and India."
    ),
]


def build_hybrid_retriever() -> HybridRetriever:
    embedding_model = SentenceTransformerEmbeddingModel(
        MODEL_NAME,
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

    sparse_index = BM25IndexStore(
        BM25_INDEX_PATH,
    )

    sparse_retriever = BM25Retriever(
        sparse_index,
    )

    return HybridRetriever(
        dense_retriever=dense_retriever,
        sparse_retriever=sparse_retriever,
        fusion=RRFFusion(),
    )


def run_validation() -> None:
    print("=== M10.3 — Real Context Assembly Validation ===")
    print()

    retriever = build_hybrid_retriever()

    reranker = CrossEncoderReranker(
        model_name=RERANKER_MODEL_NAME,
    )

    assembler = ContextAssembler(
        config=ContextAssemblyConfig(
            max_context_tokens=CONTEXT_BUDGET,
        ),
    )

    for query_number, query in enumerate(QUERIES, start=1):
        print("=" * 80)
        print(f"QUERY {query_number}")
        print("=" * 80)
        print()
        print(f"Query: {query}")
        print()

        candidates = retriever.retrieve(
            query,
            top_k=CANDIDATE_K,
        )

        if not candidates:
            raise AssertionError(
                f"No hybrid retrieval candidates for query: {query}"
            )

        reranked = reranker.rerank(
            query,
            candidates,
        )

        final_results = reranked[:FINAL_TOP_K]

        package = assembler.assemble(
            query,
            final_results,
        )

        print(f"M8 candidates:        {len(candidates)}")
        print(f"M9 reranked:          {len(reranked)}")
        print(f"M9 final top-k:       {len(final_results)}")
        print(f"M10 context chunks:   {len(package.chunks)}")
        print(f"M10 context tokens:   {package.token_count}")
        print(
            "M10 budget utilization:"
            f" {package.token_count / CONTEXT_BUDGET:.2%}"
        )
        print()

        print("M10 CONTEXT CHUNKS")
        print("-" * 80)

        for index, context_chunk in enumerate(
            package.chunks,
            start=1,
        ):
            chunk = context_chunk.chunk

            print(
                f"[{index}] "
                f"rank={context_chunk.rank} "
                f"score={context_chunk.score:.6f} "
                f"tokens={context_chunk.token_count}"
            )
            print(
                f"    document_id={chunk.document_id}"
            )
            print(
                f"    chunk_id={chunk.chunk_id}"
            )
            print(
                f"    sequence={chunk.sequence_number}"
            )
            print(
                f"    text={chunk.text[:300]!r}"
            )
            print()

        print("FORMATTED CONTEXT")
        print("-" * 80)
        print(package.context_text)
        print()

        # Basic invariants.
        assert package.query == query
        assert package.token_count <= CONTEXT_BUDGET
        assert len(package.chunks) <= FINAL_TOP_K

        ranks = [
            chunk.rank
            for chunk in package.chunks
        ]

        assert ranks == sorted(ranks)

        chunk_keys = [
            (
                str(chunk.chunk.document_id),
                str(chunk.chunk.chunk_id),
            )
            for chunk in package.chunks
        ]

        assert len(chunk_keys) == len(set(chunk_keys))

    print("=" * 80)
    print("PASS")
    print("=" * 80)


def main() -> None:
    run_validation()


if __name__ == "__main__":
    main()