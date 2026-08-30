# rag_lab — experiment scaffold

A dependency-light harness for running the labs in `RAG_Lab_Plan.md`. The
design principle: **every stage exposes the same interface, so an experiment is
a config change, not a rewrite.** Cheap sweeps are what produce comparison
tables, and comparison tables are the actual deliverable of this program.

```
rag_lab/
  metrics.py      recall@k, nDCG@k, MRR, ANN recall, abstention, run comparison
  components.py   chunkers, embedders, retrievers, fusion, reranker, assembly
  harness.py      experiment runner, sweep, golden-set loader, demo
```

## Run the smoke test right now

```bash
python -m rag_lab.harness --demo
```

No dependencies required. It uses a hashing embedder, so **the absolute numbers
are meaningless** — its only job is to prove the plumbing works end to end.

## Make it real

```bash
pip install sentence-transformers
```

Then swap the embedder:

```python
from rag_lab.components import SentenceTransformerEmbedder, CrossEncoderReranker

emb = SentenceTransformerEmbedder(
    "BAAI/bge-small-en-v1.5",
    query_prefix="Represent this sentence for searching relevant passages: ",
)
```

That prefix matters. Models trained with instruction prefixes lose several
points of recall without them, and nothing errors — it's one of the hardest
bugs in the stack to notice. Lab 4d has you reproduce it deliberately.

## Your golden set (Lab 0)

JSONL, one record per line:

```json
{"query_id": "q1", "query": "refund policy for digital products",
 "relevant_doc_ids": ["refund_policy"], "should_answer": true, "tags": ["conceptual"]}
```

```python
from rag_lab.harness import load_golden
golden = load_golden("data/golden.jsonl")
```

**Use `relevant_doc_ids` rather than `relevant_chunk_ids` wherever you can.**
Chunk IDs change every time you re-chunk, which would invalidate your labels on
exactly the experiments you most want to run. Doc-level labels survive
re-chunking, and the harness maps them down automatically.

**Tag your queries** (`keyword`, `conceptual`, `multi_hop`, `unanswerable`).
Lab 6's whole insight comes from segmenting metrics by tag — the aggregate
number hides the fact that BM25 wins one segment and dense wins the other.

## Running a sweep

```python
from rag_lab.harness import ExperimentConfig, sweep, grid
from rag_lab.components import RecursiveChunker, DenseRetriever, HybridRetriever, BM25Retriever

configs = [
    ExperimentConfig(
        name=f"recursive_{p['size']}_{int(p['ov']*100)}",
        chunker=RecursiveChunker(p["size"], p["ov"]),
        retriever_factory=lambda e: HybridRetriever(DenseRetriever(e), BM25Retriever()),
        embedder=emb,
    )
    for p in grid(size=[128, 256, 512, 1024], overlap=[0.0, 0.1, 0.25])
    for p in [{"size": p["size"], "ov": p["overlap"]}]
]

reports = sweep(configs, docs, golden)
```

`docs` is just `{doc_id: text}`. Plug your parser output straight into it.

## Comparing two runs

```python
from rag_lab.metrics import compare
print(compare(baseline_report, candidate_report, key="recall@10"))
```

This prints per-query wins and losses, not just the aggregate delta. **Read the
regressions.** A change that lifts the mean by two points while breaking six
queries is usually the wrong change, and the aggregate alone will never tell
you that.

## What to add as you progress

| Lab | Add |
|---|---|
| 2 | A `Parser` interface + the text-density OCR router |
| 3 | `ContextualChunker` (LLM-generated chunk context, with prompt caching) |
| 5 | A real vector store behind the `Retriever` interface (Qdrant/pgvector) + `ann_recall` vs `DenseRetriever` as ground truth |
| 7 | `QueryRewriter` and `IntentClassifier` stages before retrieval |
| 9 | Generation + faithfulness/citation-accuracy metrics |
| 10 | FastAPI service, cache with ACL scope in the key, OTel spans |

The `Retriever` ABC is deliberately minimal (`index`, `search`) so a real
vector database drops in behind it without touching the harness.

## A note on `DenseRetriever`

It is exact (flat) brute-force cosine search, which is *correct by
construction*. That makes it the ground truth you measure your ANN index
against in Lab 5. Keep it — measuring ANN recall against exact search is the
step that catches silent recall ceilings, and almost nobody does it.
