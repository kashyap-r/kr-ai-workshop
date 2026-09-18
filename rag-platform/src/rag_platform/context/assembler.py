"""Context assembly for downstream RAG generation."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from rag_platform.context.token_counter import ApproximateTokenCounter
from rag_platform.domain.models import (
    ContextChunk,
    ContextPackage,
    RetrievalResult,
)
from rag_platform.domain.types import ChunkID, DocumentID


@dataclass(frozen=True, slots=True)
class ContextAssemblyConfig:
    """Configuration controlling context assembly."""

    max_context_tokens: int = 4000


class ContextAssembler:
    """Assemble ranked retrieval results into bounded LLM context."""

    def __init__(
        self,
        config: ContextAssemblyConfig | None = None,
        token_counter: ApproximateTokenCounter | None = None,
    ) -> None:
        self._config = config or ContextAssemblyConfig()
        self._token_counter = token_counter or ApproximateTokenCounter()

        if self._config.max_context_tokens <= 0:
            raise ValueError("max_context_tokens must be positive.")

    def assemble(
        self,
        query: str,
        results: Sequence[RetrievalResult],
    ) -> ContextPackage:
        """Assemble ranked retrieval results into a context package."""

        if not query.strip():
            raise ValueError("query must not be empty.")

        selected = self._select_chunks(results)

        context_chunks = tuple(
            ContextChunk(
                chunk=result.chunk,
                score=result.score,
                rank=result.rank,
                token_count=self._token_counter.count(result.chunk.text),
            )
            for result in selected
        )

        context_text = self._format_context(context_chunks)

        return ContextPackage(
            query=query,
            chunks=context_chunks,
            context_text=context_text,
            token_count=sum(
                chunk.token_count
                for chunk in context_chunks
            ),
        )

    def _select_chunks(
        self,
        results: Sequence[RetrievalResult],
    ) -> list[RetrievalResult]:
        """Deduplicate and select ranked results within the token budget."""

        selected: list[RetrievalResult] = []
        seen: set[tuple[DocumentID, ChunkID]] = set()
        total_tokens = 0

        for result in results:
            key = (
                result.chunk.document_id,
                result.chunk.chunk_id,
            )

            if key in seen:
                continue

            seen.add(key)

            token_count = self._token_counter.count(result.chunk.text)

            if total_tokens + token_count > self._config.max_context_tokens:
                continue

            selected.append(result)
            total_tokens += token_count

        return selected

    @staticmethod
    def _format_context(
        chunks: Sequence[ContextChunk],
    ) -> str:
        """Format selected chunks into deterministic LLM context text."""

        sections: list[str] = []

        for index, context_chunk in enumerate(chunks, start=1):
            chunk = context_chunk.chunk

            sections.append(
                "\n".join(
                    [
                        f"[Context {index}]",
                        f"Document ID: {chunk.document_id}",
                        f"Chunk ID: {chunk.chunk_id}",
                        "Content:",
                        chunk.text,
                    ]
                )
            )

        return "\n\n".join(sections)
