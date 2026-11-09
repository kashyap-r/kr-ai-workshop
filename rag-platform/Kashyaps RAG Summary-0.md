# Enterprise Product & Policy Knowledge Assistant

#### What am I trying to do ?

How do I architect, implement, optimize, evaluate, observe and productionize an enterprise RAG platform?

#### The Journey 

    Raw documents → ingestion → chunking → embeddings → indexing → hybrid retrieval → reranking → generation → evaluation → feedback → production architecture

| Dimension | Python | TypeScript |
|---|---|---|
| RAG ecosystem | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Document processing | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| ML/embeddings experimentation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Vector DB integration | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| LLM APIs | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| LangChain | Excellent | Excellent |
| LlamaIndex | Excellent | Good |
| Reranking / NLP | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Evaluation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| FastAPI / API services | ⭐⭐⭐⭐⭐ | — |
| Node.js APIs / backend | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Streaming | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Enterprise application integration | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Agentic AI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| ML experimentation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Production microservices | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Learning RAG internals | **Best** | Very good |
| Full-stack AI application | Very good | **Excellent** |

#### It involves aspects like ... 

Documents
   ↓
Parsing
   ↓
Cleaning
   ↓
Chunking
   ↓
Metadata
   ↓
Embeddings
   ↓
Vector Index
   ↓
BM25 / Keyword Index
   ↓
Hybrid Retrieval
   ↓
Reranking
   ↓
Context Assembly
   ↓
LLM
   ↓
Citations
   ↓
Evaluation
   ↓
Feedback
   ↓
Observability
   ↓
Optimization
   ↓
Production RAG

#### Documents Processing 
    Document types 
        PDF
        DOCX
        PPTX
        HTML
        OCR
        tables
        scientific documents
        structured extraction
        metadata extraction


### Stage 1 — Ingestion & Indexing

#### 1. Data Sources
At least two implementations:
    PDF, DOCX, TXT, CSV, Web, API, Database

#### 2. Connectors
We'll implement multiple connector patterns:
    File Connector
    Web Connector
    Database Connector
    API Connector

#### 3. Parsing & Extraction
At least two approaches:
    PDF → text
    HTML → clean text
    OCR
    Tables
    Metadata
    Language detection

#### 4. Chunking
We'll deliberately compare:
    Implementation A
    Fixed / recursive chunking

    Implementation B
    Semantic chunking

Then experiment with:
    chunk size
    overlap
    document structure
    metadata
    parent-child chunks

This is important because chunking is one of the biggest sources of RAG quality differences.

Questions here: 

#### 5. Embedding Generation
We'll implement at least two embedding approaches:
    Embedding Model A
    Cloud embedding API

    Embedding Model B
    Local embedding model

Then Benchmark:
    quality
    latency
    cost
    dimension
    storage
    recall

#### 6. Indexing
We'll implement both sides of retrieval:
Vector Index
      +
Keyword / BM25 Index

leading to:
              ┌── Vector Search
Query ────────┤
              └── Keyword Search
                      ↓
                 Hybrid Results

### Stage 2 — Retrieval & Generation

Then we'll implement all 7 stages.
1. User Query
       ↓
2. Query Understanding
       ↓
3. Hybrid Retrieval
       ↓
4. Reranking
       ↓
5. Context Assembly
       ↓
6. Generation
       ↓
7. Response + Citations

### Stage 3 — Feedback & Continuous Improvement
We'll then add the third major component from your architecture:

                  ┌──────────────────┐
                  │ User Feedback    │
                  └────────┬─────────┘
                           ↓
                  ┌──────────────────┐
                  │ Usage Analytics  │
                  └────────┬─────────┘
                           ↓
                  ┌──────────────────┐
                  │ Failure Analysis │
                  └────────┬─────────┘
                           ↓
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
        Re-indexing   Prompt tuning   Model tuning
             ↓             ↓             ↓
             └─────────────┼─────────────┘
                           ↓
                       Evaluation

We'll introduce:
- retrieval evaluation
- answer evaluation
- faithfulness
- relevance
- groundedness
- citation correctness
- user feedback
- failed queries
- retrieval failures
- hallucination detection
- regression testing
- evaluation datasets

And then we turn it into Production RAG
This is where the project becomes much more valuable.

The final evolution will look approximately like:
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │ API Gateway │
                    └──────┬──────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Query Router    │
                  └────────┬────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
       Simple Query      RAG Query     Agentic RAG
                              │
                              ▼
                       Query Rewrite
                              │
                              ▼
                     Hybrid Retrieval
                       /          \
                      /            \
                Vector Search    BM25
                      \            /
                       \          /
                        ▼        ▼
                         Reranker
                            │
                            ▼
                     Context Assembly
                            │
                            ▼
                         LLM
                            │
                    ┌───────┴────────┐
                    ▼                ▼
               Citations        Guardrails
                    │                │
                    └───────┬────────┘
                            ▼
                         Response

And Arounf the whole thing:
        ┌───────────────────────────────────────┐
        │          OBSERVABILITY                │
        │ tracing / latency / tokens / cost     │
        └───────────────────────────────────────┘

        ┌───────────────────────────────────────┐
        │          EVALUATION                   │
        │ quality / relevance / faithfulness    │
        └───────────────────────────────────────┘

        ┌───────────────────────────────────────┐
        │       SECURITY & GUARDRAILS           │
        │ PII / injection / access control      │
        └───────────────────────────────────────┘

        ┌───────────────────────────────────────┐
        │       FEEDBACK LOOP                   │
        │ analytics → failures → improvement    │
        └───────────────────────────────────────┘

Python vs TypeScript for our project
Version 1 — Python
Build the complete system:
Python
├── ingestion
├── parsing
├── chunking
├── embeddings
├── indexing
├── retrieval
├── reranking
├── generation
├── evaluation
├── feedback
└── API

Version 2 — TypeScript
Reimplement the application-facing portions:
TypeScript
├── API
├── streaming
├── RAG orchestration
├── retrieval
├── LLM integration
├── tool integration
├── authentication
├── RBAC
└── production service


#### The Overall Journey 

                         RAG ENGINEERING PROJECT
                                  │
                                  ▼
                    M0 — Engineering Foundation
                                  │
                                  ▼
              ┌────────────────────────────────────┐
              │  PHASE 1 — OFFLINE RAG             │
              │                                    │
              │  M1 Data Sources                   │
              │  M2 Connectors                     │
              │  M3 Parsing & Extraction           │
              │  M4 Chunking                       │
              │  M5 Embeddings                     │
              │  M6 Indexing                       │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │  PHASE 2 — ONLINE RAG              │
              │                                    │
              │  M7  User Query                    │
              │  M8  Query Understanding           │
              │  M9  Hybrid Retrieval              │
              │  M10 Reranking                     │
              │  M11 Context Assembly              │
              │  M12 Generation                    │
              │  M13 Citations                     │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │  PHASE 3 — CONTINUOUS IMPROVEMENT  │
              │                                    │
              │  M14 Feedback                      │
              │  M15 Evaluation                    │
              │  M16 Failure Analysis              │
              │  M17 Optimization                  │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │  PHASE 4 — PRODUCTION ENGINEERING  │
              │                                    │
              │  M18 Security & Guardrails         │
              │  M19 Observability                 │
              │  M20 Reliability                   │
              │  M21 Performance & Cost            │
              │  M22 Deployment & Scaling          │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │  PHASE 5 — ENTERPRISE RAG          │
              │                                    │
              │  M23 Multi-tenancy & Governance    │
              │  M24 Production RAG                │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │  PHASE 6 — ADVANCED / AGENTIC RAG  │
              │                                    │
              │  M25 Advanced RAG Patterns         │
              │  M26 RAG + Agents / MCP / A2A     │
              └────────────────────────────────────┘

THe Happy path baseline is.. 

Employee
   │
   ▼
TypeScript API
   │
   ▼
Agent Runtime
   │
   ▼
Understand request
   │
   ├─────────────────────────────┐
   │                             │
   ▼                             ▼
Knowledge task                 Action task
   │                             │
   ▼                             ▼
RAG Search Tool            Leave Request Tool
   │                             │
   ▼                             ▼
Python RAG Service        HR/business system
   │
   ▼
Hybrid Retrieval
   │
   ▼
Reranking
   │
   ▼
Context Assembly
   │
   ▼
Grounded Answer
   │
   └───────────────┐
                   ▼
            Agent decides:
            "Need approval?"
                   │
                   ▼
             Action execution
                   │
                   ▼
             Confirmation

### M0 — Project Foundation & Engineering Standards

Type safety
Interfaces
Dependency boundaries
Configuration
Secrets
Logging
Exceptions
Validation
Testing
Observability hooks
Idempotency
Documentation
Versioning
Clean architecture

#### Task M0.1 — Define the project

Create an initial Corpus that contains...
documents/
│
├── policies/
│   ├── refund_policy.pdf
│   ├── cancellation_policy.pdf
│   └── warranty_policy.pdf
│
├── product/
│   ├── product_manual.pdf
│   └── product_faq.docx
│
└── web/
    ├── terms.html
    └── support.html

That answers queries such as..
"What is our refund policy for a digital product purchased 20 days ago?"
OR 
"Does the warranty cover accidental damage?"

This is deliberately simple enough to understand, but rich enough to eventually demonstrate:
   - metadata filtering
   - citations
   - hybrid search
   - reranking
   - authorization
   - feedback
   - evaluation
   - production observability

### M0.2 — Repository architecture
rag-platform/
│
├── python/
│   ├── src/
│   ├── tests/
│   ├── pyproject.toml
│   └── README.md
│
├── typescript/
│   ├── src/
│   ├── tests/
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── evaluation/
│
├── configs/
│
├── docker/
│
├── docs/
│   ├── architecture/
│   ├── decisions/
│   └── experiments/
│
├── scripts/
│
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
└── README.md

We're separating:
Source code
Data
Configuration
Infrastructure
Documentation
Experiments
Tests

### M0.3 — Define our core domain objects
Before implementing ingestion, we'll define the contracts.
SourceDocument
       │
       ▼
ParsedDocument
       │
       ▼
DocumentChunk
       │
       ▼
EmbeddedChunk
       │
       ▼
IndexedDocument
and THhen..
UserQuery
       │
       ▼
RetrievalResult
       │
       ▼
RerankedResult
       │
       ▼
Context
       │
       ▼
GenerationResult
       │
       ▼
RAGResponse

We're going to design these as domain objects. Why?
Because, our application should not care whether embeddings come from OpenAI, Cohere, Hugging Face or a local model.

### M0.4 — Python and TypeScript roles

Python becomes our AI/RAG laboratory
Python
│
├── document processing
├── chunking
├── embeddings
├── retrieval experiments
├── reranking
├── evaluation
├── benchmarking
└── RAG reference implementation

TypeScript becomes our production application layer
TypeScript
│
├── API
├── request/response contracts
├── streaming
├── application orchestration
├── authentication
├── authorization
├── integrations
└── agent/MCP/A2A evolution

### M0.5 — Our first production-quality rule

We'll progressively build toward:
Application
     │
     ▼
RAGService
     │
     ├── QueryProcessor
     ├── Retriever
     ├── Reranker
     ├── ContextBuilder
     └── Generator

with explicit contracts between each component.

### M0.6 — Testing strategy

Every milestone will have tests.

We'll eventually have:
tests/
│
├── unit/
│
├── integration/
│
├── contract/
│
├── retrieval/
│
├── evaluation/
│
├── security/
│
├── performance/
│
└── regression/

We will distinguish 
Unit test
    ↓
Component works

Integration test
    ↓
Components work together

Evaluation test
    ↓
RAG quality is acceptable

Regression test
    ↓
New change didn't degrade quality

Security test
    ↓
System doesn't expose/execute unsafe behavior

Performance test
    ↓
System meets latency/throughput targets

Shared engineering conventions
.gitignore
.env.example
README
logging conventions
error conventions
configuration conventions





### 
### 
### 




Questions

Why use pyproject.toml 
uv package manger
pytest
ruff provides for 
   linting + import sorting + basic correctness rules
mypy 
   - Since we're going to create lots of domain contracts, we want the type checker to tell us if we accidentally 
   implment an existing functionality 
   Ex. If we have a DocumentLoader class defined to load a document, we have to have an architectural guardrail to 
   stop us from writing a separate method to load documents.




what are the features and advantages?

