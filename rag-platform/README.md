Kashyap's Enterprise RAG Protoype Project — Master To-Do

| Milestone  | Area                         | Major Work                                                       | Status         |
| ---------- | ---------------------------- | ---------------------------------------------------------------- | -------------- |
| **M0**     | Engineering Foundation       | Repo, environments, config, tooling, contracts, tests            | 🟡 In progress |
| **M0.1**   | Project Scaffold             | Python/TS structure, uv, tooling, CI basics                      | ✅ Done         |
| **M0.2-A** | Domain Models                | Core entities, enums, value objects, validation                  | ✅ Done         |
| **M0.2-B** | Identity & Logical Documents | IDs, versions, checksums, lineage, logical documents             | ✅ Done  |
| **M1**     | Data Sources                 | Source abstraction, metadata, source registry                    | ✅ Done               |
|      | Connectors                   | Files, web, DB, APIs, cloud sources                              | ✅ Done               |
| **M2**     | Parsing & Extraction         | PDF, HTML, DOCX, TXT, tables, metadata                           | ✅ Done               |
| **M3**     | Chunking                     | Chunking strategies, boundaries, overlap, semantic structure     | 🔵 **Current**              |
| **M4**     | Embeddings                   | Embedding abstraction, batching, caching, model management       | ⬜              |
| **M5**     | Indexing                     | Vector index, inverted index, metadata index                     | ⬜              |
| **M6**     | User Query                   | Query API, validation, request lifecycle                         | ⬜              |
| **M7**     | Query Understanding          | Normalization, rewriting, decomposition, intent                  | ⬜              |
| **M8**     | Hybrid Retrieval             | BM25/lexical + vector + fusion                                   | ⬜              |
| **M9**    | Reranking                    | Cross-encoder/reranker abstraction and ranking pipeline          | ⬜              |
| **M10**    | Context Assembly             | Deduplication, diversity, ordering, token budgeting              | ⬜              |
| **M112**    | Generation                   | LLM abstraction, prompts, streaming, answer generation           | ⬜              |
| **M12**    | Citations                    | Provenance, source attribution, citation rendering               | ⬜              |
| **M13**    | Feedback                     | User feedback, signals, feedback storage                         | ⬜              |
| **M14**    | Evaluation                   | Retrieval + generation evaluation, datasets, metrics             | ⬜              |
| **M15**    | Failure Analysis             | Retrieval failures, hallucination, attribution, debugging        | ⬜              |
| **M16**    | Optimization                 | Caching, batching, indexing/retrieval optimization               | ⬜              |
| **M17**    | Security & Guardrails        | Prompt injection, data access, content safety, isolation         | ⬜              |
| **M18**    | Observability                | Logs, metrics, traces, RAG-specific telemetry                    | ⬜              |
| **M19**    | Reliability                  | Retries, timeouts, fallbacks, circuit breakers, idempotency      | ⬜              |
| **M20**    | Performance & Cost           | Latency, throughput, token cost, capacity modeling               | ⬜              |
| **M21**    | Deployment & Scaling         | Containers, services, workers, scaling, HA                       | ⬜              |
| **M22**    | Multi-tenancy & Governance   | Tenant isolation, RBAC, policies, audit, lifecycle               | ⬜              |
| **M23**    | Production RAG               | Complete production architecture and operating model             | ⬜              |
| **M24**    | Advanced RAG                 | Agentic retrieval, corrective RAG, adaptive RAG, graph RAG, etc. | ⬜              |
| **M25**    | RAG + Agents                 | Agents, MCP, A2A, tool use, multi-agent RAG systems              | ⬜              |
