"""
Retrieval metrics for the RAG lab harness.

These are the numbers every experiment reports. Keep them dependency-free
so they can never be the reason a lab doesn't run.

Convention throughout:
    retrieved : list[str]  -- chunk ids, ranked best-first
    relevant  : set[str]   -- ground-truth chunk ids for the query
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from statistics import mean
from typing import Iterable, Sequence


# --------------------------------------------------------------------------
# Core metrics
# --------------------------------------------------------------------------

def recall_at_k(retrieved: Sequence[str], relevant: Iterable[str], k: int) -> float:
    """Fraction of relevant chunks that appear in the top k.

    THE most important RAG metric. If the answer-bearing chunk is not in the
    candidate set, no reranker, prompt or model can recover it.
    """
    relevant = set(relevant)
    if not relevant:
        return 0.0
    hits = len(relevant & set(retrieved[:k]))
    return hits / len(relevant)


def hit_rate_at_k(retrieved: Sequence[str], relevant: Iterable[str], k: int) -> float:
    """1.0 if ANY relevant chunk is in the top k. Useful when a single chunk
    is sufficient to answer -- often more meaningful than recall for QA."""
    return 1.0 if set(retrieved[:k]) & set(relevant) else 0.0


def precision_at_k(retrieved: Sequence[str], relevant: Iterable[str], k: int) -> float:
    """Fraction of the top k that is relevant. Drives prompt cost and noise."""
    if k == 0:
        return 0.0
    return len(set(retrieved[:k]) & set(relevant)) / k


def mrr(retrieved: Sequence[str], relevant: Iterable[str]) -> float:
    """Reciprocal rank of the first relevant result."""
    relevant = set(relevant)
    for i, cid in enumerate(retrieved, start=1):
        if cid in relevant:
            return 1.0 / i
    return 0.0


def ndcg_at_k(
    retrieved: Sequence[str],
    relevant: Iterable[str],
    k: int,
    gains: dict[str, float] | None = None,
) -> float:
    """Rank-weighted quality. This is the metric that moves when a reranker
    works: recall can stay flat while nDCG jumps, because reranking reorders
    rather than retrieves.

    `gains` allows graded relevance (e.g. {"chunk_1": 3.0}); defaults to binary.
    """
    relevant = set(relevant)
    if not relevant:
        return 0.0
    gains = gains or {}

    def gain(cid: str) -> float:
        return gains.get(cid, 1.0) if cid in relevant else 0.0

    dcg = sum(gain(cid) / math.log2(i + 1) for i, cid in enumerate(retrieved[:k], start=1))
    ideal = sorted((gains.get(c, 1.0) for c in relevant), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 1) for i, g in enumerate(ideal, start=1))
    return dcg / idcg if idcg else 0.0


def ann_recall(approx: Sequence[str], exact: Sequence[str], k: int) -> float:
    """Recall of an ANN index measured against exact (flat) search.

    Run this. An under-tuned efSearch/nprobe is a SILENT quality ceiling:
    the relevant chunk is dropped before reranking and nothing logs an error.
    """
    exact_k = set(exact[:k])
    if not exact_k:
        return 0.0
    return len(set(approx[:k]) & exact_k) / len(exact_k)


# --------------------------------------------------------------------------
# Aggregation
# --------------------------------------------------------------------------

@dataclass
class QueryResult:
    query_id: str
    query: str
    retrieved: list[str]
    relevant: set[str]
    latency_ms: float = 0.0
    stage_latencies: dict[str, float] = field(default_factory=dict)
    answered: bool = True          # False when the system abstained
    should_answer: bool = True     # False for deliberately unanswerable queries


@dataclass
class RunReport:
    config_name: str
    metrics: dict[str, float]
    per_query: list[QueryResult]

    def table(self) -> str:
        width = max(len(k) for k in self.metrics) + 2
        lines = [f"\n=== {self.config_name} ===",
                 f"{'metric'.ljust(width)}value",
                 f"{'-' * width}------"]
        for key, val in self.metrics.items():
            lines.append(f"{key.ljust(width)}{val:.4f}")
        return "\n".join(lines)


def evaluate_run(
    results: list[QueryResult],
    config_name: str = "run",
    ks: tuple[int, ...] = (1, 3, 5, 10, 20, 50),
) -> RunReport:
    """Aggregate per-query results into the metrics table for one config."""
    if not results:
        raise ValueError("no results to evaluate")

    m: dict[str, float] = {}
    for k in ks:
        m[f"recall@{k}"] = mean(recall_at_k(r.retrieved, r.relevant, k) for r in results)
        m[f"hit_rate@{k}"] = mean(hit_rate_at_k(r.retrieved, r.relevant, k) for r in results)
    for k in (5, 10):
        m[f"ndcg@{k}"] = mean(ndcg_at_k(r.retrieved, r.relevant, k) for r in results)
        m[f"precision@{k}"] = mean(precision_at_k(r.retrieved, r.relevant, k) for r in results)
    m["mrr"] = mean(mrr(r.retrieved, r.relevant) for r in results)

    lat = sorted(r.latency_ms for r in results)
    m["latency_p50_ms"] = _pct(lat, 50)
    m["latency_p95_ms"] = _pct(lat, 95)

    # Abstention: are we declining exactly when we should?
    should_not = [r for r in results if not r.should_answer]
    if should_not:
        m["correct_abstention_rate"] = mean(0.0 if r.answered else 1.0 for r in should_not)
    should = [r for r in results if r.should_answer]
    if should:
        m["false_abstention_rate"] = mean(0.0 if r.answered else 1.0 for r in should)

    return RunReport(config_name=config_name, metrics=m, per_query=results)


def _pct(sorted_vals: list[float], pct: float) -> float:
    if not sorted_vals:
        return 0.0
    idx = min(int(len(sorted_vals) * pct / 100), len(sorted_vals) - 1)
    return sorted_vals[idx]


def compare(baseline: RunReport, candidate: RunReport, key: str = "recall@10") -> str:
    """Diff two runs. Aggregate deltas hide the story -- per-query win/loss
    counts tell you whether a change helped broadly or helped a few queries
    a lot while hurting others."""
    base = {r.query_id: r for r in baseline.per_query}
    wins, losses, ties = [], [], 0
    k = int(key.split("@")[1]) if "@" in key else 10

    for r in candidate.per_query:
        b = base.get(r.query_id)
        if b is None:
            continue
        db = recall_at_k(b.retrieved, b.relevant, k)
        dc = recall_at_k(r.retrieved, r.relevant, k)
        if dc > db:
            wins.append((r.query, db, dc))
        elif dc < db:
            losses.append((r.query, db, dc))
        else:
            ties += 1

    delta = candidate.metrics.get(key, 0) - baseline.metrics.get(key, 0)
    out = [
        f"\n{baseline.config_name}  ->  {candidate.config_name}",
        f"{key}: {baseline.metrics.get(key, 0):.4f} -> {candidate.metrics.get(key, 0):.4f} "
        f"({delta:+.4f})",
        f"wins: {len(wins)}   losses: {len(losses)}   ties: {ties}",
    ]
    if losses:
        out.append("\nRegressions worth reading (this is where the insight is):")
        for q, db, dc in losses[:5]:
            out.append(f"  {db:.2f} -> {dc:.2f}  {q[:70]}")
    return "\n".join(out)
