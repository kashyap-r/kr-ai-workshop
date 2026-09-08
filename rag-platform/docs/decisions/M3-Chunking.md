Chunking 

The chunking architecture for this prototype will be small 

Chunking

[1] Define baseline strategy
        ↓
[2] Implement Chunker against existing Chunker protocol
        ↓
[3] Produce DocumentChunk objects
        ↓
[4] Persist chunks locally as JSONL
        ↓
[5] Preserve provenance + offsets
        ↓
[6] Add chunking version
        ↓
[7] Document infrastructure alternatives / ADR
        ↓
[8] Smoke-test on ZCompanyLLC



So... the chunk metadata will inherit from the parser class 

Chunk
│
├── chunk_id
├── document_id
├── document_version
├── chunking_version
├── sequence_number
├── start_offset
├── end_offset
├── text
└── metadata
      ├── path
      ├── filename
      ├── country
      ├── document_type
      └── ...