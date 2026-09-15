from collections.abc import Sequence

from rag_platform.domain.contracts import (
    Chunker,
    Embedder,
    Generator,
    Parser,
    Reranker,
    Retriever,
)
from rag_platform.domain.models import (
    DocumentChunk,
    DocumentFormat,
    ParsedDocument,
    RetrievalResult,
    SourceDocument,
)
from rag_platform.domain.types import (
    ChunkID,
    DocumentID,
    SourceID,
)


class FakeParser:
    def parse(self, document: SourceDocument) -> ParsedDocument:
        return ParsedDocument(
            id=document.id,
            source_document_id=document.id,
            parser_version=1,
            format=document.format,
            text=document.content.decode("utf-8"),
            metadata={},
            parsed_at=document.ingested_at,
        )


class FakeChunker:
    def chunk(self, document: ParsedDocument) -> Sequence[DocumentChunk]:
        return []


class FakeEmbedder:
    def embed(self, texts: Sequence[str]) -> Sequence[Sequence[float]]:
        return [[0.1, 0.2] for _ in texts]


class FakeRetriever:
    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> Sequence[RetrievalResult]:
        return []


class FakeReranker:
    def rerank(
        self,
        query: str,
        results: Sequence[RetrievalResult],
    ) -> Sequence[RetrievalResult]:
        return results


class FakeGenerator:
    def generate(
        self,
        query: str,
        context: Sequence[RetrievalResult],
    ) -> str:
        return "fake answer"

def test_parser_satisfies_contract() -> None:
    parser: Parser = FakeParser()

    assert parser


def test_chunker_satisfies_contract() -> None:
    chunker: Chunker = FakeChunker()

    assert chunker


def test_embedder_satisfies_contract() -> None:
    embedder: Embedder = FakeEmbedder()

    assert embedder.embed(["hello"]) == [[0.1, 0.2]]


def test_retriever_satisfies_contract() -> None:
    retriever: Retriever = FakeRetriever()

    assert retriever.retrieve("policy") == []


def test_reranker_satisfies_contract() -> None:
    reranker: Reranker = FakeReranker()

    assert reranker.rerank("policy", []) == []


def test_generator_satisfies_contract() -> None:
    generator: Generator = FakeGenerator()

    assert generator.generate("policy", []) == "fake answer"