from rag_platform.embeddings import SentenceTransformerEmbeddingModel
from rag_platform.vector_store import ChromaVectorStore

MODEL_NAME = "BAAI/bge-small-en-v1.5"
VECTOR_STORE_ROOT = "data/processed/vector_store/ZCompanyLLC"
COLLECTION_NAME = "zcompany_hr_chunks"

QUERY = "How many days can an employee based in India work remotely each week?"
TOP_K = 5


def main() -> None:
    model = SentenceTransformerEmbeddingModel(MODEL_NAME)

    query_embedding = model.embed([QUERY])[0]

    vector_store = ChromaVectorStore(
        path=VECTOR_STORE_ROOT,
        collection_name=COLLECTION_NAME,
        embedding_model=MODEL_NAME,
    )

    results = vector_store.query(
        query_embedding,
        top_k=TOP_K,
    )

    print(f"\nQuery: {QUERY}\n")

    for result in results:
        print(
            f"Rank {result.rank} | "
            f"Score {result.score:.4f} | "
            f"Document {result.chunk.document_id}"
        )
        print(f"  {result.chunk.text[:200]}")
        print()


if __name__ == "__main__":
    main()
