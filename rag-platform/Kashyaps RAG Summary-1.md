
### M0.2 — RAG Domain Contracts

1. What we're building
Our initial domain model will eventually look like:

                        ┌─────────────────┐
                        │ DocumentSource  │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ SourceDocument  │
                        └────────┬────────┘
                                 │
                              parsing
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ ParsedDocument  │
                        └────────┬────────┘
                                 │
                              chunking
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ DocumentChunk   │
                        └────────┬────────┘
                                 │
                            embedding
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Embedding     │
                        └────────┬────────┘
                                 │
                             indexing
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  IndexedChunk   │
                        └─────────────────┘

On the online side 
UserQuery
    │
    ▼
QueryUnderstanding
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

And eventually these will connect to:
DocumentLoader
Parser
Chunker
EmbeddingProvider
VectorStore
KeywordStore
Retriever
Reranker
LLMProvider
Evaluator
FeedbackStore

#### M0.2-A — Domain Model

Domain objects should NOT know about infrastructure.

Domain
  │
  ├── Document
  ├── Chunk
  ├── Embedding
  └── Query
       │
       │ contracts
       ▼
Application
       │
       ▼
Infrastructure
  ├── filesystem
  ├── PDF parser
  ├── embedding API
  ├── vector DB
  └── LLM API

Domain Types 

Document Srouce Types 
class SourceType(StrEnum):
    FILE = "file"
    WEB_PAGE = "web_page"
    API = "api"
    DATABASE = "database"


class DocumentFormat(StrEnum):
    PDF = "pdf"
    HTML = "html"
    MARKDOWN = "markdown"
    TEXT = "text"
    JSON = "json"

Document Source

@dataclass(frozen=True, slots=True)
class DocumentSource:
    id: SourceId
    tenant_id
    source_type: SourceType
    uri: str

class SourceDocument:
    document_id / logical document identity
    version
    source_id
    format
    content
    checksum
    source_created_at
    ingested_at

class ParsedDocument:
    id: DocumentId
    source_document_id: DocumentId
    document version
    parser_version
    format
    text
    metadata
    parsed_at

@dataclass(frozen=True, slots=True)
class DocumentChunk:
    chunk_id=ChunkID("chunk-1"),
    document_id=DocumentID("policy"),
    document_version=1,
    chunking_version="chunker-1",
    text="policy text",
    metadata={},
    sequence_number=0,
    start_offset=0,
    end_offset=11,


Note: We are intentionally making the domain objects immutable using the decorator. Because a document flowing through a pipeline should behave more like a value/message than a mutable global object.

What is provenance ?

The ability to trace .."where this data / answer came from ?"

Answer
 ↓
Generation
 ↓
Context
 ↓
Retrieved chunks
 ↓
Chunk version
 ↓
Chunking strategy
 ↓
Parsed document
 ↓
Parser version
 ↓
Source document version
 ↓
Checksum
 ↓
Original source
 ↓
Tenant


#### How to generate the IDs?
Option A — Random UUID
Option B — Time-sortable UUID
Option C — Deterministic hash
Option D — Composite identity
Option E — Hybrid


ChunkID =
    hash(document identity + document version + chunking version + sequence number + chunk content )

| Entity | Identity strategy | Why |
|---|---|---|
| `TenantID` | Platform-defined identifier | Security/isolation boundary |
| `SourceID` | UUIDv7 | Entity identity + useful temporal locality |
| `DocumentID` | Deterministic logical identity | Idempotent document discovery |
| `DocumentVersion` | Monotonic integer | Content revision |
| `Checksum` | SHA-256 | Exact artifact identity |
| `ChunkID` | Deterministic identity | Idempotent chunk generation |
| `sequence_number` | Integer | **Document ordering** |


The resulting model becomes:

                         Tenant
                           │
                           ▼
                     ┌───────────┐
                     │  Source   │
                     │ UUIDv7    │
                     └─────┬─────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │ Logical Document │
                 │ deterministic ID │
                 └────────┬─────────┘
                          │
                  ┌───────┴────────┐
                  ▼                ▼
              Version 1         Version 2
              checksum A        checksum B
                  │                │
                  └───────┬────────┘
                          ▼
                       Chunks
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
           ChunkID     ChunkID     ChunkID
           hash        hash        hash
              │           │           │
           seq=0       seq=1       seq=2

That is 
TenantID → tenant-scoped identifier
SourceID → UUIDv7
DocumentVersion → integer
Checksum → SHA-256
Chunk ordering → sequence_number
Chunk identity → deterministic, not temporal

#### Identity primitives
The BIG Question: What to use / How to generat the IDs ?? 
Create strongly typed identifiers for:
TenantID
SourceID
DocumentID
ChunkID

The ID decides: representation, validation, serialization, equality, hashing, generation strategy. 

So, UUIDv7 for generated entity identifiers where appropriate.
UUIDv7 contains a time-ordered component, which is useful for:
- database locality
- index behavior
- chronological sorting
- operational debugging

Document Version: A version should capture things such as:
- version identifier
- logical document ID
- version number
- source
- checksum
- ingestion timestamp
- parser version
- chunking version
- metadata
This gives us lineage.

Chunk identity: A chunk needs an identity and relationship to its parent version.
So, 
Chunk
 ├── chunk_id
 ├── document_id
 ├── document_version
 ├── sequence_number
 ├── content
 └── metadata

 Note: The Key field is sequence_number, because retrieval should not destroy the original document order. 

 Finally, the identity hierarchy looks like 

 TenantID
   │
   └── SourceID
          │
          └── DocumentID
                 │
                 └── DocumentVersion
                        │
                        └── ChunkID

                    