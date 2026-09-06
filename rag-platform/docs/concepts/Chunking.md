### 1. What is Chunking?

Chunking is the process of splitting a larger document into smaller, semantically useful units that can be independently indexed, embedded, retrieved, and passed to an LLM.

Suppose, we have a 50-page document (PDF):
Document
│
├── Introduction
├── Architecture
│   ├── Components
│   ├── Data Flow
│   └── Security
├── Deployment
│   ├── Kubernetes
│   └── AWS
└── Troubleshooting

Instead of embedding the entire docuement as one vector, we create chunks. 
The vector database then operates primarily at chunk level. 

                        Documents
                            │
                            ▼
                        Parsing
                            │
                            ▼
                        Structural representation
                            │
                            ▼
                        CHUNKING
                            │
                            ├── Chunk 1
                            ├── Chunk 2
                            ├── Chunk 3
                            └── ...
                            │
                            ▼
                        Embedding
                            │
                            ▼
                        Vector Index
                            │
                            ▼
                        Retrieval
                            │
                            ▼
                        Relevant Chunks
                            │
                            ▼
                        LLM

### 1.1 Why do we need Chunking?

There are four fundamental reasons. 

1.1.1 Retrieval Granularity
1.1.2 LLM Context Limitations 
1.1.3 Embedding Quality 
1.1.4 Retrieval Precision 


### 1.2 Chunking Techniques 