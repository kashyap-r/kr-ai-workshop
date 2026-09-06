
# M2 — Connector Boundary
filename: filesystem.py

## Context

Sources may be backed by different external systems.

## Decision

Separate source configuration/identity from connector implementation.

## Initial Implementation

Local filesystem only.

## Source vs Connector

Source = what/where

Connector = how

## Why?

...

## Alternatives Considered

...

## Trade-offs

...

## Future Connectors

- S3
- HTTP
- Google Drive
- SharePoint
- Database
- SaaS APIs


"Why did you introduce a connector abstraction instead of just reading files directly?"

"I wanted source acquisition to be decoupled from the downstream RAG pipeline. 
The domain model represents the source and its identity, while the connector 
encapsulates how we acquire documents from that source. For the prototype I only 
implemented a filesystem connector, but the same boundary allows us to add object 
storage, SharePoint, Google Drive or API-backed sources without changing parsing, 
chunking or retrieval."

"Why didn't you implement all those connectors?"
"Because this was a production-oriented prototype. I optimized for demonstrating the complete ingestion-to-retrieval path rather than breadth of integrations. The abstraction is there, but I implemented only the connector needed for the demo."