"""Sparse BM25 retrieval and its persistent index."""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, cast

from rag_platform.domain.models import DocumentChunk, RetrievalResult

_TOKEN_PATTERN = re.compile(r"[\w]+(?:[-_][\w]+)*|[^\W_]+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    """Tokenize text while preserving useful identifiers such as EMP-1042."""
    return [token.casefold() for token in _TOKEN_PATTERN.findall(text)]


class BM25IndexStore:
    """In-memory BM25 corpus with optional atomic JSON persistence.

    The store keeps canonical DocumentChunk objects keyed by chunk_id.  The
    inverted statistics are rebuilt lazily after mutations, which keeps the
    incremental lifecycle simple and deterministic for the prototype.
    """

    VERSION = "bm25-index-v1"

    def __init__(self, path: str | Path | None = None) -> None:
        self._path = Path(path) if path is not None else None
        self._chunks: dict[str, DocumentChunk] = {}
        self._dirty = False
        self._revision = 0
        if self._path is not None and self._path.exists():
            self._load()

    @property
    def path(self) -> Path | None:
        return self._path

    @property
    def revision(self) -> int:
        return self._revision

    @property
    def chunks(self) -> tuple[DocumentChunk, ...]:
        return tuple(self._chunks[key] for key in sorted(self._chunks))

    def upsert(self, chunks: Sequence[DocumentChunk]) -> None:
        seen: set[str] = set()
        for chunk in chunks:
            chunk_id = str(chunk.chunk_id)
            if chunk_id in seen:
                raise ValueError(f"Duplicate chunk ID in upsert: {chunk_id!r}")
            seen.add(chunk_id)
            self._chunks[chunk_id] = chunk
        if chunks:
            self._dirty = True
            self._revision += 1

    def delete(self, ids: Sequence[str]) -> None:
        changed = False
        for chunk_id in ids:
            changed = self._chunks.pop(str(chunk_id), None) is not None or changed
        if changed:
            self._dirty = True
            self._revision += 1

    def delete_all(self) -> None:
        if self._chunks:
            self._chunks.clear()
            self._dirty = True
            self._revision += 1

    def save(self) -> None:
        if self._path is None:
            self._dirty = False
            return
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": self.VERSION,
            "chunks": [asdict(chunk) for chunk in self.chunks],
        }
        encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self._path.parent,
            prefix=f".{self._path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            try:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            except Exception:
                temp_path.unlink(missing_ok=True)
                raise
        temp_path.replace(self._path)
        self._dirty = False

    def _load(self) -> None:
        if self._path is None:
            return
        with self._path.open("r", encoding="utf-8") as handle:
            raw: Any = json.load(handle)
        if not isinstance(raw, dict) or raw.get("version") != self.VERSION:
            raise ValueError("Unsupported BM25 index format.")
        raw_chunks = raw.get("chunks")
        if not isinstance(raw_chunks, list):
            raise ValueError("BM25 index 'chunks' must be an array.")
        chunks: dict[str, DocumentChunk] = {}
        for raw_chunk in raw_chunks:
            if not isinstance(raw_chunk, dict):
                raise ValueError("Invalid BM25 chunk record.")
            chunk = DocumentChunk(**cast(dict[str, Any], raw_chunk))
            chunk_id = str(chunk.chunk_id)
            if chunk_id in chunks:
                raise ValueError(f"Duplicate chunk ID in BM25 index: {chunk_id!r}")
            chunks[chunk_id] = chunk
        self._chunks = chunks
        self._dirty = False
        self._revision += 1


class BM25Retriever:
    """Retrieve chunks using Okapi BM25 over a sparse chunk index."""

    def __init__(
        self,
        index: BM25IndexStore,
        *,
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        if k1 < 0:
            raise ValueError("k1 must be non-negative.")
        if not 0 <= b <= 1:
            raise ValueError("b must be between 0 and 1.")
        self._index = index
        self._k1 = k1
        self._b = b
        self._statistics_revision = -1
        self._postings: dict[str, set[str]] = {}
        self._document_frequencies: Counter[str] = Counter()
        self._document_lengths: dict[str, int] = {}
        self._average_length = 0.0

    def _ensure_statistics(self) -> None:
        if self._statistics_revision == self._index.revision:
            return

        postings: defaultdict[str, set[str]] = defaultdict(set)
        document_frequencies: Counter[str] = Counter()
        document_lengths: dict[str, int] = {}
        total_length = 0

        for chunk in self._index.chunks:
            chunk_id = str(chunk.chunk_id)
            terms = tokenize(chunk.text)
            document_lengths[chunk_id] = len(terms)
            total_length += len(terms)
            for term in set(terms):
                postings[term].add(chunk_id)
                document_frequencies[term] += 1

        self._postings = dict(postings)
        self._document_frequencies = document_frequencies
        self._document_lengths = document_lengths
        self._average_length = (total_length / len(document_lengths)) if document_lengths else 0.0
        self._statistics_revision = self._index.revision

    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> Sequence[RetrievalResult]:
        if not query.strip():
            raise ValueError("query must not be empty.")
        if top_k <= 0:
            raise ValueError("top_k must be positive.")

        chunks = self._index.chunks
        if not chunks:
            return []

        query_terms = tokenize(query)
        if not query_terms:
            return []

        self._ensure_statistics()
        document_count = len(chunks)
        if self._average_length == 0.0:
            return []

        chunks_by_id = {str(chunk.chunk_id): chunk for chunk in chunks}
        candidate_ids: set[str] = set()
        for term in set(query_terms):
            candidate_ids.update(self._postings.get(term, set()))

        scores: list[tuple[float, DocumentChunk]] = []
        for chunk_id in candidate_ids:
            chunk = chunks_by_id[chunk_id]
            terms = tokenize(chunk.text)
            term_frequency = Counter(terms)
            document_length = self._document_lengths[chunk_id]
            score = 0.0
            for term in query_terms:
                frequency = term_frequency.get(term, 0)
                if frequency == 0:
                    continue
                df = self._document_frequencies[term]
                idf = math.log(1.0 + (document_count - df + 0.5) / (df + 0.5))
                denominator = frequency + self._k1 * (
                    1.0 - self._b + self._b * document_length / self._average_length
                )
                score += idf * (frequency * (self._k1 + 1.0)) / denominator
            if score > 0.0:
                scores.append((score, chunk))

        ranked = sorted(scores, key=lambda item: (-item[0], str(item[1].chunk_id)))[:top_k]
        return [
            RetrievalResult(chunk=chunk, score=score, rank=rank)
            for rank, (score, chunk) in enumerate(ranked, start=1)
        ]
