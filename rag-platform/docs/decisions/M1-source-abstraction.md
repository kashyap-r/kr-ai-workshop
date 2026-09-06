# M1 — Source Abstraction
filename: file_source.py

## Context

The RAG platform needs to ingest documents from different source types.

## Initial Scope

The prototype will support local files only:

- PDF
- Markdown
- TXT

Other source types are represented conceptually but not implemented.

## Decision

Use the existing `DocumentSource` domain model to represent source
configuration/identity and a separate source-reader abstraction to
retrieve source content.

## Why Separate Source Configuration from Source Reading?

...

## Why Start With Files?

...

## Alternatives Considered

- Direct filesystem access throughout ingestion
- One class per file format
- Generic connector framework immediately

## Trade-offs

...

## Future Evolution

URL, S3/object storage, databases, SaaS APIs, etc.


Note: The new design for connecting to the source is 
DocumentSource
      ↓
FilesystemConnector
      ↓
SourceDocument[]

I initially considered a FileSourceReader abstraction but consolidated the design into FilesystemConnector to avoid duplicating the source-access responsibility.