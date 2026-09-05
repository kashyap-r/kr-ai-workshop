# RAG Hands-On Lab Plan
### 12 labs, ~10 weeks part-time, each producing a measurable artifact

---

## How to run this program

**The rule:** every lab ends with a **numbers table**, not a working demo. A demo proves it runs. A table proves you understand the trade. In an interview, "I compared four chunking strategies and semantic chunking cost 8× more for a 1.2-point nDCG gain, so I shipped recursive with structural boundaries" is worth ten times "I built a RAG app."

**Corpus choice.** Pick one corpus and stick with it across all labs so results are comparable. Good options:
- Your own company's docs (best — real messiness, real query distribution)
- A public messy corpus: SEC 10-K filings (tables + long docs), arXiv papers (structure + math), or a government policy site (the realistic enterprise analogue)
- Avoid: clean Wikipedia dumps. They make every technique look equally good and teach you nothing about parsing.

**Keep a lab journal.** For each experiment: hypothesis → configuration → result → interpretation → decision. This is what you'll actually talk from in an interview, and it's a strong portfolio artifact on its own.

---

## Lab 0 — The Evaluation Harness (Week 1) ⭐ Do this first

**Why first:** without it, every subsequent lab is vibes. This is the discipline that separates practitioners from tutorial-followers.

**Build:**
1. A golden set of 100+ `(query, relevant_chunk_ids, reference_answer)` triples. Generate 70 synthetically from chunks, hand-write 30 (including 10 unanswerable ones to measure abstention).
2. Metric functions: `recall@k`, `nDCG@k`, `MRR`, `context_precision`.
3. A runner that takes a pipeline config, executes the golden set, and writes results to a CSV/SQLite with the config hash.
4. A comparison script that diffs two runs and shows per-query wins/losses.

**Deliverable:** `python -m rag_lab.eval --config configs/baseline.yaml` prints a metrics table.

**Watch out for:** synthetic questions are lexically too close to their source chunk, which inflates recall. Prompt for paraphrased, user-voice questions and hand-check 20.

---

## Lab 1 — Baseline End-to-End (Week 1–2)

Build the dumbest thing that works: PyMuPDF text extraction → 512-token recursive chunks with 50-token overlap → one embedding model → pgvector or Qdrant → top-5 → LLM with a grounding prompt → Streamlit UI.

**Deliverable:** baseline numbers in the harness. Every future lab is measured against this line.

**Expected finding:** recall@10 somewhere in 0.55–0.75, and a set of failures you can already categorize by hand. Spend an hour reading 20 failures before you touch anything — it will tell you which lab to prioritize.

---

## Lab 2 — Parsing Bake-Off (Week 2)

**Hypothesis:** parser choice matters more on hard documents than any downstream tuning.

**Run:** 20 documents (5 digital PDFs, 5 scanned, 5 multi-column, 5 table-heavy) × {pypdf, PyMuPDF, pdfplumber, unstructured, Docling} + one cloud service.

**Measure:** manual fidelity score (1–5), reading-order correctness, table cell accuracy, seconds/page, cost/1000 pages.

**Then build:** the routing function — text-layer character density per page decides native vs OCR path.

**Expected finding:** a 2–4× spread in table accuracy and a 10–50× spread in speed. The cloud service wins on quality and loses badly on cost. Your router recovers most of the quality at a fraction of the price. **This tradeoff is the deliverable.**

---

## Lab 3 — Chunking Sweep (Week 3)

**Hypothesis:** there's a plateau in chunk size, and structure-aware beats size-tuning.

**Run:** the grid — size {128, 256, 512, 1024} × overlap {0, 10%, 25%}, then structural chunking, then parent–child, then semantic chunking, then contextual retrieval on a 500-chunk subset.

**Measure:** recall@10, nDCG@10, avg chunks needed to cover the answer, index size, ingestion cost/time.

**Expected findings:**
- Recall plateaus around 256–512 tokens for most prose; larger chunks help nDCG slightly but cost prompt tokens.
- Overlap beyond ~15% buys almost nothing and inflates the index.
- Semantic chunking often fails to beat recursive despite costing far more — a genuinely useful negative result to be able to report.
- Parent–child improves answer quality more than retrieval metrics show (measure faithfulness too, or you'll miss the gain).
- Contextual retrieval gives the biggest single jump. Compute its break-even.

---

## Lab 4 — Embedding Model Bake-Off (Week 3–4)

**Run:** 4 models spanning small-open / large-open / API / domain-specific. Then MRL truncation {1024, 512, 256, 128}. Then quantization {fp32, int8, binary+rescore}.

**Measure:** recall@10, nDCG@10, ms/query, index bytes, $/1M chunks embedded, max seq length utilization.

**Deliberate experiment:** omit the instruction prefix on a model that requires one, and record the damage.

**Expected findings:** the gap between a good open 768d model and a top API model is smaller than leaderboards suggest on a specific domain corpus — frequently 1–3 points — while cost differs by an order of magnitude. MRL truncation to 256d typically costs a couple of points for 4× memory savings. Binary quantization with rescoring retains most quality at 1/32 the memory. **The MRL and quantization curves are the most interview-quotable results in the whole program.**

---

## Lab 5 — Index Structures & the Filter Trap (Week 4–5)

**Run:** Flat (ground truth) vs HNSW at three `(M, efSearch)` settings vs IVF-PQ, on 100k+ vectors.

**Measure:** ANN recall@10 *against Flat*, latency P50/P95, memory, build time.

**Then the important one:** apply a metadata filter matching ~1% of the corpus, using post-filtering. Watch recall collapse. Fix it with native filtered ANN and with partitioning; compare.

**Expected finding:** you can lose 20+ points of recall to post-filtering and never see an error message. This is the most instructive failure in the curriculum and an excellent interview story.

---

## Lab 6 — Hybrid Retrieval & Fusion (Week 5)

**Run:** dense-only, BM25-only, RRF hybrid, weighted-score hybrid. Sweep RRF `k` and weighted `α`.

**Critical step:** **segment your golden set** into keyword-ish queries (contain IDs, codes, proper nouns) and conceptual queries. Report metrics per segment, not just in aggregate.

**Expected finding:** hybrid gains 5–15 points of recall overall — but the segmentation shows *why*: BM25 dominates the keyword segment, dense dominates the conceptual one, and the aggregate number hides both. Producing that segmented analysis is the actual skill this lab teaches.

---

## Lab 7 — Query Understanding (Week 6)

**Run:** three intent classifiers (rules / embedding+logreg / LLM) — measure accuracy, P95 latency, cost per 1M. Then distill the LLM's labels into the small classifier and re-measure. Then implement HyDE, multi-query, and conversational rewriting.

**Build a multi-turn golden set** (10 conversations × 5 turns) — you need this to measure rewriting at all.

**Expected findings:** distillation gets ~95% of LLM routing accuracy at ~1% of the latency. HyDE helps short vague queries and *hurts* precise keyword queries — so route it. Conversational rewriting produces a very large gain on multi-turn queries; without it, follow-up retrieval is close to random.

---

## Lab 8 — Reranking (Week 6–7)

**Run:** no rerank vs cross-encoder vs ColBERT-style vs LLM listwise. Candidate sweep {10, 25, 50, 100, 200}.

**Measure:** nDCG@5, MRR, P95 latency added, cost, and — importantly — **how many chunks you now need in the prompt** to hit the same answer quality.

**Then:** calibrate an abstention threshold on the reranker score using your 10 unanswerable questions.

**Expected findings:** cross-encoder reranking is the largest single quality gain in the online pipeline, and it lets you drop from ~10 chunks to ~5 in the prompt — so it *reduces* generation cost while improving quality. The candidate-count curve knees around 50. Abstention thresholding sharply cuts confident-wrong answers.

---

## Lab 9 — Context Assembly & Generation (Week 7–8)

**Run:** chunk-count sweep {3, 5, 10, 20} against faithfulness and cost. Position experiment (best chunk first vs middle vs last) to measure lost-in-the-middle on your model. Citation format experiment. Model tier comparison. Context compression on/off.

**Measure:** faithfulness, answer relevance, citation accuracy, TTFT, cost/query.

**Expected findings:** quality peaks around 5–8 chunks and then *degrades* with more — the "more context is better" intuition is wrong, and demonstrating that with your own numbers is compelling. Position effects are real but model-dependent. A smaller model with better retrieval usually beats a bigger model with worse retrieval, at a fraction of the cost.

---

## Lab 10 — Production Hardening (Week 8–9)

**Build:** FastAPI + SSE streaming, Next.js or a decent chat UI, the cache hierarchy (with ACL scope in the key), permission-filtered retrieval with a second test user, OpenTelemetry tracing with per-stage spans, a cost dashboard, guardrails (injection detection on ingestion, citation validation on output).

**Then attack it:** plant a document containing an injection payload in your corpus and confirm your defenses catch it. Confirm user B cannot retrieve user A's document via a cached response.

**Deliverable:** a latency waterfall showing where every millisecond goes, and a security test report.

---

## Lab 11 — Scale Simulation (Week 9–10)

You don't need 50M real documents. Simulate:
- Duplicate/perturb your corpus to 5–10M chunks.
- Run ingestion through Ray Data or a queue + worker pool. Measure throughput and find the actual bottleneck.
- Extrapolate to 50M with a spreadsheet: GPU-hours, storage per quantization level, index build time, monthly infra cost.
- Execute a **dual-index migration**: build a second index with a different embedding model, shadow-evaluate on the golden set, cut over via alias, and roll back.

**Deliverable:** a capacity and cost model, plus a written migration runbook. This is a Principal-level artifact — very few candidates have one.

---

## Lab 12 — Failure Analysis & the Improvement Loop (Week 10)

Take 50 failing queries from all your labs. Attribute each to a stage: **not ingested / not chunked well / not retrieved / retrieved but ranked low / ranked well but generation ignored it**. Build the taxonomy, count the buckets, and rank the fixes by expected value.

**Deliverable:** a one-page "where this system loses" analysis. This is the single most valuable interview document you'll produce — it demonstrates diagnostic thinking, which is exactly what Staff/Principal interviews probe for.

---

## Suggested schedule

| Week | Labs | Theme |
|---|---|---|
| 1 | 0, 1 | Harness + baseline |
| 2 | 2 | Parsing |
| 3 | 3, 4 | Chunking + embeddings |
| 4–5 | 5, 6 | Indexing + hybrid retrieval |
| 6 | 7 | Query understanding |
| 6–7 | 8 | Reranking |
| 7–8 | 9 | Assembly + generation |
| 8–9 | 10 | Production hardening |
| 9–10 | 11, 12 | Scale + failure analysis |

**If you only have three weeks:** Labs 0, 1, 3, 6, 8, 12. That sequence covers the eval discipline, the two highest-ROI retrieval upgrades, and diagnostic thinking — which is most of what gets tested.
