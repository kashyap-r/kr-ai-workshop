# M2 — Document Parsing

## Context

Source connectors provide raw document bytes.
The RAG pipeline requires normalized textual content.

## Goal

Convert SourceDocument into ParsedDocument.

## M2.1 — Parsing architecture

The boundary is:

SourceDocument
      │
      ▼
    Parser
      │
      ▼
ParsedDocument

## Initial Formats

- PDF
- Markdown
- TXT

## Decision

Parsing is separated from source acquisition.

Connector responsibility:
- locate source
- read bytes
- identify basic format
- create SourceDocument

Parser responsibility:
- interpret document bytes
- extract textual content
- produce ParsedDocument
- attach parser metadata

## Parser Selection

Parser
 ├── PDFParser
 ├── MarkdownParser
 └── TextParser

 It means adding DOCX later doesn't require modifying existing parser implementations:

AND WHEN WE HAVE MULTIPLE document formats, we can implement a PArser factory when the ingestion pipeline actually needs parser selection.


...

## PDF Parsing

Using pypdf

## Markdown Parsing

...

## TXT Parsing

...

## Alternatives Considered

...

## Trade-offs

...

## Future Evolution

...

## Testing

...


# Questions on Parser

What format is the output of the parser ?
Where are they stored 

