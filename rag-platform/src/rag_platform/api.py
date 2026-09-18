from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from starlette.responses import Response

from rag_platform.context import ContextAssembler
from rag_platform.embeddings import SentenceTransformerEmbeddingModel
from rag_platform.logging import configure_logging
from rag_platform.query import QueryService
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
VECTOR_STORE_ROOT = "data/processed/vector_store/ZCompanyLLC"
SPARSE_INDEX_PATH = f"{VECTOR_STORE_ROOT}/bm25_index.json"
COLLECTION_NAME = "zcompany_hr_chunks"

DEFAULT_TOP_K = 5
MAX_TOP_K = 20


# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

logger = configure_logging(
    logger_name=__name__,
    log_file="logs/api.log",
)


# -------------------------------------------------------------------
# API models
# -------------------------------------------------------------------

class QueryRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(
        default=DEFAULT_TOP_K,
        ge=1,
        le=MAX_TOP_K,
    )


class QueryResult(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    score: float
    rank: int
    metadata: dict[str, str]

class ContextChunkResponse(BaseModel):
    chunk_id: str
    document_id: str
    score: float
    rank: int
    token_count: int

class ContextResponse(BaseModel):
    text: str
    chunks: list[ContextChunkResponse]
    chunk_count: int
    token_count: int

class QueryResponse(BaseModel):
    query: str
    results: list[QueryResult]
    result_count: int
    context: ContextResponse
    latency_ms: float


# -------------------------------------------------------------------
# Application services
# -------------------------------------------------------------------

def create_query_service() -> QueryService:
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
    sparse_index = BM25IndexStore(SPARSE_INDEX_PATH)
    sparse_retriever = BM25Retriever(sparse_index)
    retriever = HybridRetriever(
        dense_retriever=dense_retriever,
        sparse_retriever=sparse_retriever,
        fusion=RRFFusion(),
    )
    reranker = CrossEncoderReranker()

    return QueryService(
        retriever,
        reranker=reranker,
        context_assembler=ContextAssembler(),
    )


query_service = create_query_service()


# -------------------------------------------------------------------
# FastAPI application
# -------------------------------------------------------------------

app = FastAPI(
    title="RAG Platform Query API",
    version="0.1.0",
)


# -------------------------------------------------------------------
# Request correlation and API observability
# -------------------------------------------------------------------

@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = request.headers.get("X-Request-ID") or str(uuid4())

    request.state.request_id = request_id

    start = perf_counter()

    logger.info(
        "request_started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    try:
        response = await call_next(request)

    except Exception:
        latency_ms = (perf_counter() - start) * 1000

        logger.exception(
            "request_failed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "latency_ms": round(latency_ms, 2),
            },
        )

        raise

    latency_ms = (perf_counter() - start) * 1000

    response.headers["X-Request-ID"] = request_id

    logger.info(
        "request_completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "latency_ms": round(latency_ms, 2),
        },
    )

    return response


# -------------------------------------------------------------------
# Health
# -------------------------------------------------------------------

@app.get("/health")
def health(request: Request) -> dict[str, str]:
    logger.info(
        "health_check",
        extra={
            "request_id": request.state.request_id,
        },
    )

    return {"status": "ok"}


# -------------------------------------------------------------------
# Query
# -------------------------------------------------------------------

@app.post("/query", response_model=QueryResponse)
def query(
    request: Request,
    payload: QueryRequest,
) -> QueryResponse:

    request_id = request.state.request_id

    logger.info(
        "query_started",
        extra={
            "request_id": request_id,
            "top_k": payload.top_k,
            "query_length": len(payload.query),
        },
    )

    start = perf_counter()

    try:
        # results = query_service.query(
        #     payload.query,
        #     top_k=payload.top_k,
        # )
        results, context_package = query_service.query_with_context(
            payload.query,
            top_k=payload.top_k,
        )

    except ValueError as exc:
        latency_ms = (perf_counter() - start) * 1000

        logger.warning(
            "query_validation_failed",
            extra={
                "request_id": request_id,
                "top_k": payload.top_k,
                "query_length": len(payload.query),
                "latency_ms": round(latency_ms, 2),
                "error_type": type(exc).__name__,
            },
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        latency_ms = (perf_counter() - start) * 1000

        logger.exception(
            "query_failed",
            extra={
                "request_id": request_id,
                "top_k": payload.top_k,
                "query_length": len(payload.query),
                "latency_ms": round(latency_ms, 2),
                "error_type": type(exc).__name__,
            },
        )

        raise HTTPException(
            status_code=503,
            detail="Query service unavailable.",
        ) from exc

    latency_ms = (perf_counter() - start) * 1000

    # logger.info(
    #     "query_completed",
    #     extra={
    #         "request_id": request_id,
    #         "top_k": payload.top_k,
    #         "result_count": len(results),
    #         "latency_ms": round(latency_ms, 2),
    #     },
    # )
    logger.info(
        "query_completed",
        extra={
            "request_id": request_id,
            "top_k": payload.top_k,
            "result_count": len(results),
            "context_chunk_count": len(context_package.chunks),
            "context_token_count": context_package.token_count,
            "latency_ms": round(latency_ms, 2),
        },
    )

    # return QueryResponse(
    #     query=payload.query,
    #     results=[
    #         QueryResult(
    #             chunk_id=str(result.chunk.chunk_id),
    #             document_id=str(result.chunk.document_id),
    #             text=result.chunk.text,
    #             score=result.score,
    #             rank=result.rank,
    #             metadata=dict(result.chunk.metadata),
    #         )
    #         for result in results
    #     ],
    #     result_count=len(results),
    #     latency_ms=round(latency_ms, 2),
    # )
    return QueryResponse(
    query=payload.query,
    results=[
        QueryResult(
            chunk_id=str(result.chunk.chunk_id),
            document_id=str(result.chunk.document_id),
            text=result.chunk.text,
            score=result.score,
            rank=result.rank,
            metadata=dict(result.chunk.metadata),
        )
        for result in results
    ],
    result_count=len(results),
    context=ContextResponse(
        text=context_package.context_text,
        chunks=[
            ContextChunkResponse(
                chunk_id=str(context_chunk.chunk.chunk_id),
                document_id=str(context_chunk.chunk.document_id),
                score=context_chunk.score,
                rank=context_chunk.rank,
                token_count=context_chunk.token_count,
            )
            for context_chunk in context_package.chunks
        ],
        chunk_count=len(context_package.chunks),
        token_count=context_package.token_count,
    ),
    latency_ms=round(latency_ms, 2),
)
