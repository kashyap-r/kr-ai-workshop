
Creating the directory Structure 

ent-rag-platform/
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

Python becomes our AI/RAG laboratory - What it does?
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

Testing Strategy - Every milestone will have tests 
So we'll eventually have:
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

and what tests we perform ? and how will we distigusih them.. 

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



