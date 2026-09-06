# M2 — Document Parsing

python/src/rag_platform/parsers/
├── __init__.py
├── pdf.py
├── markdown.py
└── text.py

Add a small utility:
python/src/rag_platform/parsers/registry.py

## Context

Source connectors provide raw document bytes.
The RAG pipeline requires normalized textual content.

## Goal

Convert SourceDocument into ParsedDocument.

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

...

## PDF Parsing

choose pypdf for pdf parsing. 
Why pypdf rather than a heavyweight document processing framework?

What if I want only part of the PDF or first 10 pages or last 15 pages or a particular chaper or page X to page Y from the PDF ? 
When is it worth implementing this?

...

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

Note: Need to document the below 
Capture:
    Connector vs Parser separation
    PDF / Markdown / TXT support
    Why pypdf
    Why Markdown is preserved as Markdown
    UTF-8 decoding
    parser_version
    Why we did not create ParserFactory yet
    Parser limitations, especially scanned/OCR PDFs
    Testing strategy
    Deferred improvements