"""
Experiment harness: run a pipeline config against the golden set, produce a
metrics table, and sweep configurations.

Run the built-in smoke test (no dependencies required):
    python -m rag_lab.harness --demo

The demo uses the hashing embedder, so the ABSOLUTE numbers are meaningless.
Its job is to prove the plumbing works end to end. Swap in
SentenceTransformerEmbedder and your own corpus, and the same code produces
real, comparable results.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Sequence

from .components import (
    BM25Retriever, Chunk, Chunker, DenseRetriever, Embedder, HashingEmbedder,
    HybridRetriever, ParentChildChunker, RecursiveChunker, Retriever,
    StructuralChunker, WeightedHybridRetriever, FixedChunker,
)
from .metrics import QueryResult, RunReport, compare, evaluate_run


# ==========================================================================
# Golden set
# ==========================================================================

@dataclass
class GoldenItem:
    query_id: str
    query: str
    relevant_chunk_ids: list[str] = field(default_factory=list)
    relevant_doc_ids: list[str] = field(default_factory=list)
    reference_answer: str = ""
    should_answer: bool = True     # False = deliberately unanswerable
    tags: list[str] = field(default_factory=list)  # e.g. ["keyword"], ["multi_hop"]


def load_golden(path: str | Path) -> list[GoldenItem]:
    """JSONL, one GoldenItem per line."""
    items = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            items.append(GoldenItem(**json.loads(line)))
    return items


def save_golden(items: Sequence[GoldenItem], path: str | Path) -> None:
    Path(path).write_text("\n".join(json.dumps(asdict(i)) for i in items))


# ==========================================================================
# Experiment definition
# ==========================================================================

@dataclass
class ExperimentConfig:
    name: str
    chunker: Chunker
    retriever_factory: Callable[[Embedder], Retriever]
    embedder: Embedder
    k: int = 10
    reranker: object | None = None
    rerank_to: int = 5
    notes: str = ""


def run_experiment(cfg: ExperimentConfig,
                   docs: dict[str, str],
                   golden: Sequence[GoldenItem]) -> RunReport:
    """Index the corpus under this config, run every golden query, aggregate.

    Note that indexing time is reported separately from query time. At scale
    they have completely different cost structures and completely different
    people complaining about them.
    """
    t0 = time.perf_counter()
    chunks: list[Chunk] = []
    for doc_id, text in docs.items():
        chunks.extend(cfg.chunker.split(doc_id, text))
    chunk_index = {c.chunk_id: c for c in chunks}

    retriever = cfg.retriever_factory(cfg.embedder)
    retriever.index(chunks)
    index_secs = time.perf_counter() - t0

    # Map doc-level ground truth down to chunk level when chunk ids aren't
    # pinned. Doc-level labels survive re-chunking; chunk-level labels do not.
    doc_to_chunks: dict[str, set[str]] = {}
    for c in chunks:
        doc_to_chunks.setdefault(c.doc_id, set()).add(c.chunk_id)

    results: list[QueryResult] = []
    for item in golden:
        relevant = set(item.relevant_chunk_ids)
        for d in item.relevant_doc_ids:
            relevant |= doc_to_chunks.get(d, set())

        qt = time.perf_counter()
        stage: dict[str, float] = {}

        s = time.perf_counter()
        hits = retriever.search(item.query, k=max(cfg.k, cfg.rerank_to * 10))
        stage["retrieve_ms"] = (time.perf_counter() - s) * 1000

        ranked_ids = [cid for cid, _ in hits]
        if cfg.reranker is not None:
            s = time.perf_counter()
            cands = [chunk_index[cid] for cid in ranked_ids if cid in chunk_index]
            reranked = cfg.reranker.rerank(item.query, cands, k=cfg.k)
            ranked_ids = [c.chunk_id for c, _ in reranked]
            stage["rerank_ms"] = (time.perf_counter() - s) * 1000

        results.append(QueryResult(
            query_id=item.query_id, query=item.query,
            retrieved=ranked_ids, relevant=relevant,
            latency_ms=(time.perf_counter() - qt) * 1000,
            stage_latencies=stage,
            answered=bool(ranked_ids), should_answer=item.should_answer,
        ))

    report = evaluate_run(results, config_name=cfg.name)
    report.metrics["index_seconds"] = index_secs
    report.metrics["n_chunks"] = float(len(chunks))
    report.metrics["avg_chunk_chars"] = (
        sum(len(c.text) for c in chunks) / max(1, len(chunks))
    )
    return report


def sweep(configs: Sequence[ExperimentConfig],
          docs: dict[str, str],
          golden: Sequence[GoldenItem],
          sort_by: str = "recall@10") -> list[RunReport]:
    """Run several configs and print a leaderboard.

    This is the function you will spend the most time in. Every lab in the
    plan is 'define N configs, sweep, read the table, form a hypothesis
    about WHY, then test that'.
    """
    reports = [run_experiment(c, docs, golden) for c in configs]
    reports.sort(key=lambda r: -r.metrics.get(sort_by, 0))

    cols = ["recall@5", "recall@10", "ndcg@10", "mrr",
            "latency_p95_ms", "n_chunks", "index_seconds"]
    name_w = max(len(r.config_name) for r in reports) + 2
    print(f"\n{'config'.ljust(name_w)}" + "".join(c.rjust(16) for c in cols))
    print("-" * (name_w + 16 * len(cols)))
    for r in reports:
        row = "".join(f"{r.metrics.get(c, 0):.4f}".rjust(16) for c in cols)
        print(f"{r.config_name.ljust(name_w)}{row}")
    return reports


def grid(**axes) -> list[dict]:
    """Cartesian product helper for parameter sweeps.

        for p in grid(size=[256, 512], overlap=[0.0, 0.1]):
            ...
    """
    keys = list(axes)
    return [dict(zip(keys, vals)) for vals in itertools.product(*axes.values())]


# ==========================================================================
# Demo
# ==========================================================================

DEMO_DOCS = {
    "refund_policy": """# Refund Policy

## Digital Products
### Standard Window
Digital products may be refunded within 30 days of purchase, provided the
product has not been downloaded or used. Refunds are issued to the original
payment method within 5 business days.

### Exceptions
Subscription products purchased under promotional pricing are not eligible
for refund after 14 days. Error code E-4471 indicates a refund was blocked
because the licence was already activated.

## Physical Products
### Standard Window
Physical goods may be returned within 60 days of delivery in original
packaging. The customer is responsible for return shipping unless the item
arrived damaged.
""",
    "support_faq": """# Support FAQ

## Getting your money back
If you want your money back on a download you never opened, you generally
have a month from the day you bought it. Contact support with your order id.

## Shipping questions
Standard delivery takes 3 to 5 working days. Express delivery is next day
when ordered before 2pm.
""",
    "engineering_runbook": """# Payments Runbook

## Error codes
E-4471: licence already activated, refund blocked at the gateway.
E-2200: payment method declined by issuer, retry with a different card.

## Escalation
Page the payments on-call if the refund queue exceeds 500 pending items.
""",
}

DEMO_GOLDEN = [
    GoldenItem("q1", "What is the refund policy for digital products?",
               relevant_doc_ids=["refund_policy"], tags=["conceptual"]),
    GoldenItem("q2", "How long do I have to get my money back on a download?",
               relevant_doc_ids=["refund_policy", "support_faq"], tags=["conceptual", "paraphrase"]),
    GoldenItem("q3", "What does error code E-4471 mean?",
               relevant_doc_ids=["engineering_runbook", "refund_policy"], tags=["keyword"]),
    GoldenItem("q4", "Can I return a physical item that arrived damaged?",
               relevant_doc_ids=["refund_policy"], tags=["conceptual"]),
    GoldenItem("q5", "What is the company's parental leave policy?",
               relevant_doc_ids=[], should_answer=False, tags=["unanswerable"]),
]


def _demo() -> None:
    emb = HashingEmbedder(dim=512)
    configs = [
        ExperimentConfig("fixed_512_dense", FixedChunker(512, 0.1),
                         lambda e: DenseRetriever(e), emb),
        ExperimentConfig("recursive_512_dense", RecursiveChunker(512, 0.1),
                         lambda e: DenseRetriever(e), emb),
        ExperimentConfig("recursive_256_dense", RecursiveChunker(256, 0.1),
                         lambda e: DenseRetriever(e), emb),
        ExperimentConfig("structural_dense", StructuralChunker(512),
                         lambda e: DenseRetriever(e), emb),
        ExperimentConfig("structural_bm25", StructuralChunker(512),
                         lambda e: BM25Retriever(), emb),
        ExperimentConfig("structural_hybrid_rrf", StructuralChunker(512),
                         lambda e: HybridRetriever(DenseRetriever(e), BM25Retriever()), emb),
        ExperimentConfig("structural_hybrid_w0.5", StructuralChunker(512),
                         lambda e: WeightedHybridRetriever(DenseRetriever(e),
                                                           BM25Retriever(), alpha=0.5), emb),
        ExperimentConfig("parent_child_hybrid", ParentChildChunker(1500, 250),
                         lambda e: HybridRetriever(DenseRetriever(e), BM25Retriever()), emb),
    ]

    print("\nRAG lab harness -- smoke test")
    print("NOTE: hashing embedder in use. Plumbing check only; the absolute")
    print("numbers mean nothing. Swap in a real embedder before concluding.")
    reports = sweep(configs, DEMO_DOCS, DEMO_GOLDEN)

    base = next(r for r in reports if r.config_name == "recursive_512_dense")
    best = reports[0]
    if best.config_name != base.config_name:
        print(compare(base, best))

    print("\nPer-query detail for the top config (read your failures, always):")
    for qr in best.per_query:
        got = "HIT " if set(qr.retrieved[:5]) & qr.relevant else "MISS"
        if not qr.should_answer:
            got = "N/A "
        print(f"  {got} {qr.query[:60]:<62} p95_stage={qr.stage_latencies}")


def main() -> None:
    ap = argparse.ArgumentParser(description="RAG lab harness")
    ap.add_argument("--demo", action="store_true", help="run the built-in smoke test")
    args = ap.parse_args()
    if args.demo:
        _demo()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
