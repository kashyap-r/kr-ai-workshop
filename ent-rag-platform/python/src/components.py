"""
Swappable RAG components.

The whole point of this module is that every stage exposes the SAME interface,
so an experiment is a config change rather than a rewrite. That is what makes
sweeps cheap -- and cheap sweeps are what produce the comparison tables.

Optional deps degrade gracefully:
    sentence-transformers  -> real embeddings (else: hashing fallback, runs anywhere)
    rank_bm25              -> BM25 (else: a small pure-python BM25 is used)
"""

from __future__ import annotations

import hashlib
import math
import re
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Sequence


# ==========================================================================
# Data model
# ==========================================================================

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    chunk_index: int = 0
    section_path: str = ""        # "Refund Policy > Digital > Window" -- free retrieval signal
    page: int | None = None
    parent_id: str | None = None  # for small-to-big retrieval
    metadata: dict = field(default_factory=dict)

    @property
    def embed_text(self) -> str:
        """What actually gets embedded. Prepending the section path is one of
        the cheapest recall wins available -- it restores the context that
        chunking destroyed."""
        return f"{self.section_path}\n{self.text}".strip() if self.section_path else self.text


def make_chunk_id(doc_id: str, index: int, text: str) -> str:
    """Content-hash IDs make re-ingestion idempotent. Do this from day one or
    you will eventually ship duplicate chunks to production."""
    h = hashlib.sha256(f"{doc_id}|{index}|{text}".encode()).hexdigest()[:16]
    return f"{doc_id}_{index}_{h}"


# ==========================================================================
# Stage 3: Chunking
# ==========================================================================

class Chunker(ABC):
    @abstractmethod
    def split(self, doc_id: str, text: str, **kw) -> list[Chunk]: ...


def _approx_tokens(text: str) -> int:
    """Rough proxy. In a real lab, use the embedding model's ACTUAL tokenizer --
    silent truncation at the model's max length is invisible in your logs."""
    return max(1, len(text) // 4)


class FixedChunker(Chunker):
    """Baseline. Cuts mid-sentence. Exists to be beaten."""

    def __init__(self, size_tokens: int = 512, overlap_pct: float = 0.1):
        self.size = size_tokens * 4          # chars
        self.overlap = int(self.size * overlap_pct)

    def split(self, doc_id: str, text: str, **kw) -> list[Chunk]:
        chunks, start, idx = [], 0, 0
        step = max(1, self.size - self.overlap)
        while start < len(text):
            body = text[start:start + self.size]
            if body.strip():
                chunks.append(Chunk(make_chunk_id(doc_id, idx, body), doc_id, body, idx))
                idx += 1
            start += step
        return chunks


class RecursiveChunker(Chunker):
    """The sensible default: split on the largest natural boundary that fits."""

    SEPARATORS = ["\n\n\n", "\n\n", "\n", ". ", "? ", "! ", "; ", " "]

    def __init__(self, size_tokens: int = 512, overlap_pct: float = 0.1):
        self.size = size_tokens * 4
        self.overlap = int(self.size * overlap_pct)

    def split(self, doc_id: str, text: str, **kw) -> list[Chunk]:
        pieces = self._recurse(text, 0)
        merged, buf = [], ""
        for p in pieces:
            if len(buf) + len(p) <= self.size:
                buf += p
            else:
                if buf.strip():
                    merged.append(buf)
                tail = buf[-self.overlap:] if self.overlap and buf else ""
                buf = tail + p
        if buf.strip():
            merged.append(buf)
        return [Chunk(make_chunk_id(doc_id, i, c), doc_id, c, i) for i, c in enumerate(merged)]

    def _recurse(self, text: str, depth: int) -> list[str]:
        if len(text) <= self.size or depth >= len(self.SEPARATORS):
            return [text]
        sep = self.SEPARATORS[depth]
        parts = text.split(sep)
        out: list[str] = []
        for i, part in enumerate(parts):
            piece = part + (sep if i < len(parts) - 1 else "")
            out.extend(self._recurse(piece, depth + 1) if len(piece) > self.size else [piece])
        return out


class StructuralChunker(Chunker):
    """Splits on markdown headings and carries the heading hierarchy into
    section_path. On real enterprise docs this usually beats size tuning,
    because it chunks on meaning boundaries the author already provided."""

    HEADING = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

    def __init__(self, max_tokens: int = 512, fallback: Chunker | None = None):
        self.max_chars = max_tokens * 4
        self.fallback = fallback or RecursiveChunker(max_tokens)

    def split(self, doc_id: str, text: str, **kw) -> list[Chunk]:
        matches = list(self.HEADING.finditer(text))
        if not matches:
            return self.fallback.split(doc_id, text)

        chunks: list[Chunk] = []
        stack: list[tuple[int, str]] = []
        idx = 0
        for i, m in enumerate(matches):
            level, title = len(m.group(1)), m.group(2).strip()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[m.end():end].strip()

            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            path = " > ".join(t for _, t in stack)

            if not body:
                continue
            if len(body) <= self.max_chars:
                chunks.append(Chunk(make_chunk_id(doc_id, idx, body), doc_id, body, idx,
                                    section_path=path))
                idx += 1
            else:  # oversized section -> recurse inside it, keep the path
                for sub in self.fallback.split(doc_id, body):
                    chunks.append(Chunk(make_chunk_id(doc_id, idx, sub.text), doc_id,
                                        sub.text, idx, section_path=path))
                    idx += 1
        return chunks


class ParentChildChunker(Chunker):
    """Small-to-big. Embed precise children, hand the LLM the coherent parent.

    The best general-purpose upgrade in the chunking stage: it decouples
    'what embeds well' from 'what reads well', which are genuinely different
    optimisation targets.
    """

    def __init__(self, parent_tokens: int = 1500, child_tokens: int = 250):
        self.parent = RecursiveChunker(parent_tokens, 0.0)
        self.child = RecursiveChunker(child_tokens, 0.1)
        self.parents: dict[str, Chunk] = {}

    def split(self, doc_id: str, text: str, **kw) -> list[Chunk]:
        out: list[Chunk] = []
        idx = 0
        for p in self.parent.split(doc_id, text):
            self.parents[p.chunk_id] = p
            for c in self.child.split(doc_id, p.text):
                out.append(Chunk(make_chunk_id(doc_id, idx, c.text), doc_id, c.text,
                                 idx, parent_id=p.chunk_id))
                idx += 1
        return out

    def expand(self, chunk_ids: Sequence[str], index: dict[str, Chunk]) -> list[Chunk]:
        """Retrieval returns children; generation gets deduped parents."""
        seen, out = set(), []
        for cid in chunk_ids:
            ch = index.get(cid)
            if ch is None:
                continue
            target = self.parents.get(ch.parent_id or "", ch)
            if target.chunk_id not in seen:
                seen.add(target.chunk_id)
                out.append(target)
        return out


# ==========================================================================
# Stage 4: Embedding
# ==========================================================================

class Embedder(ABC):
    dim: int

    @abstractmethod
    def encode(self, texts: Sequence[str], is_query: bool = False) -> list[list[float]]: ...


class HashingEmbedder(Embedder):
    """Zero-dependency fallback so the harness always runs. NOT semantic --
    it is a deterministic bag-of-words projection. Use it to validate plumbing,
    never to draw conclusions about retrieval quality."""

    def __init__(self, dim: int = 256):
        self.dim = dim

    def encode(self, texts: Sequence[str], is_query: bool = False) -> list[list[float]]:
        vecs = []
        for t in texts:
            v = [0.0] * self.dim
            for tok in _tokenize(t):
                v[int(hashlib.md5(tok.encode()).hexdigest(), 16) % self.dim] += 1.0
            n = math.sqrt(sum(x * x for x in v)) or 1.0
            vecs.append([x / n for x in v])
        return vecs


class SentenceTransformerEmbedder(Embedder):
    """Real embeddings. Note the query/passage prefixes -- forgetting them on a
    model that was trained with them silently costs several points of recall,
    and it is one of the hardest bugs to spot because nothing errors."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5",
                 query_prefix: str = "", passage_prefix: str = "",
                 truncate_dim: int | None = None):
        from sentence_transformers import SentenceTransformer  # lazy import
        self.model = SentenceTransformer(model_name)
        self.query_prefix = query_prefix
        self.passage_prefix = passage_prefix
        self.truncate_dim = truncate_dim
        self.dim = truncate_dim or self.model.get_sentence_embedding_dimension()

    def encode(self, texts: Sequence[str], is_query: bool = False) -> list[list[float]]:
        prefix = self.query_prefix if is_query else self.passage_prefix
        payload = [prefix + t for t in texts] if prefix else list(texts)
        # sort-by-length batching would go here at scale: padding waste is
        # commonly a 2-3x throughput loss on GPU
        vecs = self.model.encode(payload, normalize_embeddings=True,
                                 batch_size=64, show_progress_bar=False)
        out = [v.tolist() for v in vecs]
        if self.truncate_dim:  # Matryoshka truncation -- renormalise after slicing
            out = [_renorm(v[:self.truncate_dim]) for v in out]
        return out


def _renorm(v: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


# ==========================================================================
# Stages 5 & 8: Retrieval
# ==========================================================================

class Retriever(ABC):
    @abstractmethod
    def index(self, chunks: Sequence[Chunk]) -> None: ...

    @abstractmethod
    def search(self, query: str, k: int = 50) -> list[tuple[str, float]]: ...


class DenseRetriever(Retriever):
    """Exact (flat) cosine search. Correct by construction -- which makes it
    the ground truth you measure ANN recall against in Lab 5."""

    def __init__(self, embedder: Embedder):
        self.embedder = embedder
        self.ids: list[str] = []
        self.vecs: list[list[float]] = []

    def index(self, chunks: Sequence[Chunk]) -> None:
        self.ids = [c.chunk_id for c in chunks]
        self.vecs = self.embedder.encode([c.embed_text for c in chunks], is_query=False)

    def search(self, query: str, k: int = 50) -> list[tuple[str, float]]:
        q = self.embedder.encode([query], is_query=True)[0]
        scored = [(cid, sum(a * b for a, b in zip(q, v)))
                  for cid, v in zip(self.ids, self.vecs)]
        scored.sort(key=lambda x: -x[1])
        return scored[:k]


class BM25Retriever(Retriever):
    """Lexical. Wins on identifiers, error codes, part numbers, proper nouns --
    exactly where dense retrieval quietly fails."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.ids: list[str] = []
        self.docs: list[list[str]] = []
        self.df: Counter = Counter()
        self.avgdl = 0.0
        self.postings: dict[str, list[int]] = defaultdict(list)

    def index(self, chunks: Sequence[Chunk]) -> None:
        self.ids = [c.chunk_id for c in chunks]
        self.docs = [_tokenize(c.embed_text) for c in chunks]
        self.avgdl = sum(len(d) for d in self.docs) / max(1, len(self.docs))
        self.df.clear()
        self.postings.clear()
        for i, d in enumerate(self.docs):
            for term in set(d):
                self.df[term] += 1
                self.postings[term].append(i)

    def search(self, query: str, k: int = 50) -> list[tuple[str, float]]:
        n = len(self.docs)
        scores: dict[int, float] = defaultdict(float)
        for term in _tokenize(query):
            if term not in self.postings:
                continue
            idf = math.log(1 + (n - self.df[term] + 0.5) / (self.df[term] + 0.5))
            for i in self.postings[term]:
                doc = self.docs[i]
                tf = doc.count(term)
                denom = tf + self.k1 * (1 - self.b + self.b * len(doc) / self.avgdl)
                scores[i] += idf * (tf * (self.k1 + 1)) / denom
        ranked = sorted(scores.items(), key=lambda x: -x[1])[:k]
        return [(self.ids[i], s) for i, s in ranked]


class HybridRetriever(Retriever):
    """Dense + sparse with Reciprocal Rank Fusion.

    RRF fuses on RANKS, not scores, which is the entire point: cosine
    similarity and BM25 live on incomparable scales, and score normalisation
    needs per-corpus calibration that drifts. RRF needs none.

    In production, run the two searches CONCURRENTLY (asyncio.gather) --
    sequential execution makes your latency the sum instead of the max.
    """

    def __init__(self, dense: DenseRetriever, sparse: BM25Retriever,
                 rrf_k: int = 60, candidates: int = 100):
        self.dense, self.sparse = dense, sparse
        self.rrf_k, self.candidates = rrf_k, candidates

    def index(self, chunks: Sequence[Chunk]) -> None:
        self.dense.index(chunks)
        self.sparse.index(chunks)

    def search(self, query: str, k: int = 50) -> list[tuple[str, float]]:
        fused: dict[str, float] = defaultdict(float)
        for results in (self.dense.search(query, self.candidates),
                        self.sparse.search(query, self.candidates)):
            for rank, (cid, _) in enumerate(results, start=1):
                fused[cid] += 1.0 / (self.rrf_k + rank)
        return sorted(fused.items(), key=lambda x: -x[1])[:k]


class WeightedHybridRetriever(HybridRetriever):
    """Score fusion with min-max normalisation. Can beat RRF IF you tune alpha
    per corpus -- and re-tune it when the corpus shifts. More ceiling, more
    maintenance. Sweep alpha in Lab 6 and look at how sharp the peak is."""

    def __init__(self, dense, sparse, alpha: float = 0.5, candidates: int = 100):
        super().__init__(dense, sparse, candidates=candidates)
        self.alpha = alpha

    def search(self, query: str, k: int = 50) -> list[tuple[str, float]]:
        d = _minmax(self.dense.search(query, self.candidates))
        s = _minmax(self.sparse.search(query, self.candidates))
        merged: dict[str, float] = defaultdict(float)
        for cid, sc in d.items():
            merged[cid] += self.alpha * sc
        for cid, sc in s.items():
            merged[cid] += (1 - self.alpha) * sc
        return sorted(merged.items(), key=lambda x: -x[1])[:k]


def _minmax(results: list[tuple[str, float]]) -> dict[str, float]:
    if not results:
        return {}
    vals = [s for _, s in results]
    lo, hi = min(vals), max(vals)
    rng = (hi - lo) or 1.0
    return {cid: (s - lo) / rng for cid, s in results}


# ==========================================================================
# Stage 9: Reranking
# ==========================================================================

class CrossEncoderReranker:
    """A cross-encoder sees (query, doc) JOINTLY, so it models term interaction
    and negation that a bi-encoder cannot. Far more accurate, far too slow for
    the full corpus -- hence retrieve-wide-then-rerank-narrow.

    Tune `top_n` in Lab 8: latency grows linearly, quality knees around 50.
    Use the top score as an ABSTENTION signal -- below threshold, say
    'I don't know'. Cheapest hallucination control there is.
    """

    def __init__(self, model_name: str = "BAAI/bge-reranker-base", top_n: int = 50):
        from sentence_transformers import CrossEncoder  # lazy import
        self.model = CrossEncoder(model_name)
        self.top_n = top_n

    def rerank(self, query: str, chunks: Sequence[Chunk], k: int = 5
               ) -> list[tuple[Chunk, float]]:
        cands = list(chunks)[:self.top_n]
        if not cands:
            return []
        scores = self.model.predict([(query, c.text) for c in cands])  # batched
        ranked = sorted(zip(cands, scores), key=lambda x: -x[1])
        return ranked[:k]


# ==========================================================================
# Stage 10: Context assembly
# ==========================================================================

def assemble_context(chunks: Sequence[Chunk], max_tokens: int = 4000,
                     edge_ordering: bool = True) -> tuple[str, list[dict]]:
    """Build the prompt context block and the citation manifest.

    Two things here that tutorials skip:
      1. edge_ordering -- models attend most reliably to the START and END of
         long contexts ('lost in the middle'), so the best chunks go on the
         edges, not buried in the centre.
      2. every block carries a STABLE ID, so you can deterministically verify
         after generation that each cited [n] actually exists. A free,
         zero-latency hallucination check.
    """
    ordered = list(chunks)
    if edge_ordering and len(ordered) > 2:
        front, back = [], []
        for i, c in enumerate(ordered):
            (front if i % 2 == 0 else back).append(c)
        ordered = front + back[::-1]

    parts, citations, used = [], [], 0
    for i, c in enumerate(ordered, start=1):
        header = f"[{i}] Source: {c.doc_id}"
        if c.section_path:
            header += f" | Section: {c.section_path}"
        if c.page is not None:
            header += f" | Page: {c.page}"
        block = f"{header}\n{c.text}"
        cost = _approx_tokens(block)
        if used + cost > max_tokens:
            break  # truncate on a CHUNK boundary, never mid-chunk
        parts.append(block)
        citations.append({"n": i, "chunk_id": c.chunk_id, "doc_id": c.doc_id,
                          "section": c.section_path, "page": c.page})
        used += cost
    return "\n\n".join(parts), citations


def validate_citations(answer: str, citations: list[dict]) -> dict:
    """Deterministic post-check: did the model cite a source that exists?
    Costs ~0ms and catches a real class of hallucination."""
    cited = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
    valid = {c["n"] for c in citations}
    invalid = sorted(cited - valid)
    return {"cited": sorted(cited), "invalid": invalid,
            "uncited_answer": len(cited) == 0, "ok": not invalid}


# --------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"[a-z0-9]+")

def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())
